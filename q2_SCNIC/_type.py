from qiime2.plugin import SemanticType
from q2_types.feature_data import FeatureData

PairwiseFeatureData = SemanticType('PairwiseFeatureData')

Network = SemanticType('Network')

ModuleMembership = SemanticType('ModuleMembership', variant_of=FeatureData.field['type'])
