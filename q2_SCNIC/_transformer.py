import pandas as pd
import networkx as nx
import qiime2

from .plugin_setup import plugin
from ._format import PairwiseFeatureDataFormat, GraphModelingLanguageFormat, ModuleMembershipTSVFormat


@plugin.register_transformer
def _1(data: pd.DataFrame) -> PairwiseFeatureDataFormat:
    ff = PairwiseFeatureDataFormat()
    with ff.open() as fh:
        data.to_csv(fh, sep='\t', index_label=('feature1', 'feature2'))
    return ff


@plugin.register_transformer
def _2(ff: PairwiseFeatureDataFormat) -> pd.DataFrame:
    df = pd.read_table(str(ff), index_col=(0, 1), sep='\t')
    new_index = pd.MultiIndex.from_tuples([(str(i), str(j)) for i, j in df.index])
    df.index = new_index
    return df


@plugin.register_transformer
def _3(data: nx.Graph) -> GraphModelingLanguageFormat:
    ff = GraphModelingLanguageFormat()
    nx.write_gml(data, str(ff.path))
    return ff


@plugin.register_transformer
def _4(ff: GraphModelingLanguageFormat) -> nx.Graph:
    return nx.read_gml(str(ff))


@plugin.register_transformer
def _5(data: pd.Series) -> ModuleMembershipTSVFormat:
    ff = ModuleMembershipTSVFormat()
    with ff.open() as fh:
        data.to_csv(fh, sep='\t')
    return ff


@plugin.register_transformer
def _6(ff: ModuleMembershipTSVFormat) -> qiime2.Metadata:
    df = pd.read_table(str(ff), index_col=0, header=None, dtype=str)
    df.columns = ['module_membership']
    df.index = [str(i) for i in df.index]
    df.index.name = '#OTU ID'
    return qiime2.Metadata(df)
