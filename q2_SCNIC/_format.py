import qiime2.plugin.model as model
from qiime2.plugin import ValidationError
import networkx as nx
import pandas as pd
from itertools import combinations


class PairwiseFeatureDataFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        if level == 'min':
            nrows = 8
        elif level == 'max':
            nrows = None
        else:
            raise ValueError('Nonstandard level value')
        try:
            frame = pd.read_table(self.path, index_col=(0, 1), sep='\t', nrows=nrows)
        except IndexError:
            raise ValidationError('Only one column in pairwise file')
        if frame.empty:
            raise ValidationError('No data in file')
        if level == 'max':
            # validate
            all_features = set([feature for feature_pair in frame.index for feature in feature_pair])
            all_feature_pairs = set(frozenset(pair) for pair in combinations(all_features, 2))
            all_found_pairs = [frozenset(pair) for pair in frame.index]
            if len(all_found_pairs) != len(set(all_found_pairs)):
                raise ValidationError('pair is repeated')
            if all_feature_pairs != set(all_found_pairs):
                raise ValidationError('Not all features pairs present in table')


PairwiseFeatureDataDirectoryFormat = model.SingleFileDirectoryFormat(
    'PairwiseFeatureDataDirectoryFormat', 'pairwise_comparisons.tsv', PairwiseFeatureDataFormat)


class GraphModelingLanguageFormat(model.TextFileFormat):
    def _validate_(self, level):
        try:
            _ = nx.read_gml(str(self.path))
        except nx.NetworkXError:
            raise ValidationError('Not a valid GML file')


GraphModelingLanguageDirectoryFormat = model.SingleFileDirectoryFormat(
    'GraphModelingLanguageDirectoryFormat', 'network.gml', GraphModelingLanguageFormat)


class ModuleMembershipTSVFormat(model.TextFileFormat):
    def _validate_(self, level):
        if level == 'min':
            nrows = 8
        elif level == 'max':
            nrows = None
        else:
            raise ValueError('Nonstandard level value')
        series = pd.read_table(self.path, header=None, squeeze=True, nrows=nrows, index_col=0)
        if type(series) != pd.Series:
            raise ValidationError('File has more than one column: %s' % series.head())


ModuleMembershipTSVDirectoryFormat = model.SingleFileDirectoryFormat(
    'ModuleMembershipTSVDirectoryFormat', 'module-membership.tsv', ModuleMembershipTSVFormat)
