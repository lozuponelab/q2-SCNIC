import pytest
from numpy.testing import assert_allclose
from os import path
import pandas as pd
from biom import load_table

from q2_SCNIC._SCNIC_methods import sparcc_filter, calculate_correlations, build_correlation_network_r, \
                                    build_correlation_network_p, make_modules_on_correlation_table


@pytest.fixture()
def data_path():
    return path.join(path.realpath(path.dirname(__file__)), 'data')


@pytest.fixture()
def table(data_path):
    return load_table(path.join(data_path, 'fake_data.biom'))


@pytest.fixture()
def correls_spar(data_path):
    correls = pd.read_table(path.join(data_path, 'fake_correls_spar.txt'), index_col=(0, 1), sep='\t',
                            dtype={'feature1': str, 'feature2': str})
    new_index = pd.MultiIndex.from_tuples([(str(i), str(j)) for i, j in correls.index])
    correls.index = new_index
    return correls


@pytest.fixture()
def correls_pear(data_path):
    correls = pd.read_table(path.join(data_path, 'fake_correls_pear.txt'), index_col=(0, 1), sep='\t',
                            dtype={'feature1': str, 'feature2': str})
    new_index = pd.MultiIndex.from_tuples([(str(i), str(j)) for i, j in correls.index])
    correls.index = new_index
    return correls


def test_sparcc_filter(table):
    table_filt = sparcc_filter(table)
    assert table_filt.shape == table.shape


def test_calculate_correlations(table, correls_spar, correls_pear):
    test_correls_pear = calculate_correlations(table, method='pearson')
    assert_allclose(test_correls_pear.values, correls_pear.values, atol=.05)
    test_correls_spar = calculate_correlations(table, method='sparcc')
    assert_allclose(test_correls_spar.values, correls_spar.values, atol=.1)


def test_build_correlation_network_r(correls_spar):
    test_net = build_correlation_network_r(correls_spar, min_val=.5)
    assert len(test_net.nodes) == 4
    assert len(test_net.edges) == 2


def test_build_correlation_network_p(correls_pear):
    test_net = build_correlation_network_p(correls_pear, max_val=1e-10)
    assert len(test_net.nodes) == 18
    assert len(test_net.edges) == 18


def test_make_modules_on_correlation_table(correls_spar, table):
    test_collapsed, test_net, test_modules = make_modules_on_correlation_table(correls_spar, table, min_r=.5)
    assert test_collapsed.shape == (49, 200)
    assert table.sum() == test_collapsed.sum()
    assert len(test_net.nodes) == 2
    assert len(test_net.edges) == 1
    assert len(test_modules) == table.shape[0]
