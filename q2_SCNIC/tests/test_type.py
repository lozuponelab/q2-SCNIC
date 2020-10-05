import pytest
from qiime2.plugin.testing import TestPluginBase

from q2_SCNIC._type import PairwiseFeatureData, Network
from q2_SCNIC._format import PairwiseFeatureDataDirectoryFormat, GraphModelingLanguageDirectoryFormat

class TestTypes(TestPluginBase):
    package = 'q2_SCNIC'

    def test_type_registration(self):
        self.assertRegisteredSemanticType(PairwiseFeatureData)
        self.assertRegisteredSemanticType(Network)

    def test(self):
        self.assertSemanticTypeRegisteredToFormat(PairwiseFeatureData, PairwiseFeatureDataDirectoryFormat)
        self.assertSemanticTypeRegisteredToFormat(Network, GraphModelingLanguageDirectoryFormat)
