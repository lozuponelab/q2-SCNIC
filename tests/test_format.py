import pytest
from os import path

from  q2_SCNIC._format import PairwiseFeatureDataFormat, GraphModelingLanguageFormat, ModuleMembershipTSVFormat


@pytest.fixture()
def data_path():
    return path.join(path.realpath(path.dirname(__file__)), 'data')


def test_PairwiseFeatureDataFormat(data_path):
    format = PairwiseFeatureDataFormat(path.join(data_path, 'fake_correls_spar.txt'), mode='r')
    format.validate('min')
    format.validate('max')


def test_GraphModelingLanguageFormat(data_path):
    format = GraphModelingLanguageFormat(path.join(data_path, 'fake_net.gml'), mode='r')
    format.validate('min')
    format.validate('max')


def test_ModuleMembershipTSVFormat(data_path):
    format = ModuleMembershipTSVFormat(path.join(data_path, 'fake_membership.txt'), mode='r')
    format.validate('min')
    format.validate('max')
