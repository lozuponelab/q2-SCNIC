import pytest
from os import path
import pandas as pd
import networkx as nx
import qiime2

from q2_SCNIC._transformer import _1, _2, _3, _4, _5, _6

@pytest.fixture()
def data_path():
    return path.join(path.realpath(path.dirname(__file__)), 'data')


@pytest.fixture()
def correls_spar(data_path):
    correls = pd.read_table(path.join(data_path, 'fake_correls_spar.txt'), index_col=(0, 1), sep='\t',
                            dtype={'feature1': str, 'feature2': str})
    new_index = pd.MultiIndex.from_tuples([(str(i), str(j)) for i, j in correls.index])
    correls.index = new_index
    return correls


def test_1(correls_spar):
    format = _1(correls_spar)
    assert format.open().read() == correls_spar.to_csv(sep='\t', index_label=('feature1', 'feature2'))


def test_2(data_path, correls_spar):
    df = _2(path.join(data_path, 'fake_correls_spar.txt'))
    assert type(df) == pd.DataFrame
    pd.testing.assert_frame_equal(df, correls_spar)


@pytest.fixture()
def net(data_path):
    return nx.read_gml(path.join(data_path, 'fake_net.gml'))


def test_3(net):
    format = _3(net)
    assert format.open().read() == '%s\n' % '\n'.join(nx.generate_gml(net))


def test_4(data_path, net):
    test_net = _4(path.join(data_path, 'fake_net.gml'))
    assert type(test_net) is nx.Graph
    nx.is_isomorphic(test_net, net)


@pytest.fixture()
def module_membership(data_path):
    df = pd.read_table(path.join(data_path, 'fake_membership.txt'), index_col=0, header=None, dtype=str, squeeze=True)
    return df


def test_5(module_membership):
    format = _5(module_membership)
    assert format.open().read() == module_membership.to_csv(sep='\t')


def test_6(data_path):
    test_meta = _6(path.join(data_path, 'fake_membership.txt'))
    assert type(test_meta) is qiime2.Metadata
