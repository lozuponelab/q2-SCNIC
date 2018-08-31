from biom.table import Table
import pandas as pd
from scipy.stats import spearmanr, pearsonr, kendalltau
import networkx as nx

from SCNIC.general import sparcc_paper_filter, correls_to_net, get_metadata_from_table, filter_correls
from SCNIC import correlation_analysis as ca
from SCNIC import module_analysis as ma


def sparcc_filter(table: Table) -> Table:
    return sparcc_paper_filter(table)


correl_methods = {'spearman': spearmanr, 'pearson': pearsonr, 'kendall': kendalltau, 'sparcc': 'sparcc'}


def calculate_correlations(table: Table, method: str, p_adjustment_method: str = 'fdr_bh', n_procs: int = 1) -> pd.DataFrame:
    print("Correlating with %s" % method)
    method = correl_methods[method]
    if method in [spearmanr, pearsonr, kendalltau]:
        correls = ca.calculate_correlations(table, method, p_adjustment_method=p_adjustment_method, nprocs=n_procs)
    elif method == 'sparcc':
        correls = ca.fastspar_correlation(table, verbose=True, nprocs=n_procs)
    else:
        raise ValueError('Provided correlation metric is not an accepted method.')
    return correls


def build_correlation_network_r(correlation_table: pd.DataFrame, min_val: float=.75,
                                cooccur: bool=False) -> nx.Graph:
    correlation_table_filtered = filter_correls(correlation_table, min_r=min_val, conet=cooccur)
    net = correls_to_net(correlation_table_filtered)
    return net


def build_correlation_network_p(correlation_table: pd.DataFrame, max_val: float=.05) -> nx.Graph:
    correlation_table_filtered = filter_correls(correlation_table, min_p=max_val)
    net = correls_to_net(correlation_table_filtered)
    return net


def make_modules_on_correlations(correlation_table: pd.DataFrame, feature_table: Table, min_r: float=.35) -> \
                                     (Table, nx.Graph, pd.Series):
    min_dist = ma.cor_to_dist(min_r)
    cor, labels = ma.correls_to_cor(correlation_table)
    dist = ma.cor_to_dist(cor)
    modules = ma.make_modules(dist, min_dist, obs_ids=labels)
    modules_rev = {asv: module for module, asvs in modules.items() for asv in asvs}
    for asv in feature_table.ids(axis='observation'):
        if asv not in modules_rev:
            modules_rev[asv] = None
    module_membership = pd.Series(modules_rev)
    coll_table = ma.collapse_modules(feature_table, modules)
    metadata = get_metadata_from_table(feature_table)
    metadata = ma.add_modules_to_metadata(modules, metadata)
    correlation_table_filtered = filter_correls(correlation_table, conet=True, min_r=min_r)
    net = correls_to_net(correlation_table_filtered, metadata=metadata)
    return coll_table, net, module_membership
