import pytest
from os import path

from  q2_SCNIC._format import PairwiseFeatureDataFormat, GraphModelingLanguageFormat


@pytest.fixture()
def data_path():
    return path.join(path.realpath(path.dirname(__file__)), 'data')


@pytest.fixture()
def correls_file_path(data_path):
    return path.join(data_path, 'fake_correls_spar.txt')


def test_PairwiseFeatureDataFormat(correls_file_path):
    format = PairwiseFeatureDataFormat(correls_file_path, mode='r')
    format.validate('min')
    format.validate('max')


@pytest.fixture()
def gml_file_path(data_path):
    return path.join(data_path, 'fake_net.gml')


def test_GraphModelingLanguageFormat(gml_file_path):
    format = GraphModelingLanguageFormat(gml_file_path, mode='r')
    format.validate('min')
    format.validate('max')
