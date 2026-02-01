# q2-SCNIC: Community Tutorial

SCNIC (Sparse Cooccurrence Network Investigation for Compositional data) is a tool for building correlation networks from feature tables, finding modules in said networks and summarizing those modules. Access to all these functionalities is available to qiime2 users via the q2-SCNIC plugin.

The SCNIC method serves three main purposes:
1. Making it easy for qiime 2 users to generate correlationt networks using a variety of metrics.
2. Increasing statistical power by summarizing non-independent features into modules.
3. Detecting modules of features which may be of biological interest.

q2-SCNIC: https://github.com/lozuponelab/q2-SCNIC

SCNIC: https://github.com/lozuponelab/SCNIC

## Installing q2-SCNIC

First install q2-SCNIC using the instructions that are at https://github.com/lozuponelab/q2-SCNIC/blob/master/README.md

## Getting data for q2-SCNIC
To run q2-SCNIC you need to start with a QIIME 2 [Feature table.](https://docs.qiime2.org/2024.10/semantic-types/) You can do this tutorial with one of your own that you have imported or generate with qiime 2 or with a sample one. If you already have a feature table to start with you can skip to Running q2-SCNIC.

### Downloading an example feature table
Use this command to download a sample feature table for analysis with q2-SCNIC.
```
wget https://github.com/lozuponelab/q2-SCNIC/blob/master/q2_SCNIC/tests/data/fake_data.biom
```
Then import this table into qiime 2 using this command.
```
qiime tools import \
  --input-path fake_data.biom \
  --type 'FeatureTable[Frequency]' \
  --input-format BIOMV210Format \
  --output-path fake_data.qza
```
Now you have a filtered `.qza` file of your feature table to run q2-SCNIC.

## Running q2-SCNIC
SCNIC can be broken up into three main steps:
1. Filtering your data so that it is useful for correlation analysis
2. Making a correlation table and network
3. Finding modules in the correlation network

We will run through these steps with the fake_data.qza generated above but you can run it with any feature table by changing the name of fake_data.qza to whatever your qza is called.

### 1. Filtering your data
Correlational analyses are hampered by having large numbers of zeroes. Therefore we are first going to remove these from our data. In the q2-SCNIC plugin a method called `sparcc-filter` to do this based on the parameters used in [Friedman et al.](https://doi.org/10.1371/journal.pcbi.1002687) This method removes all samples with a feature abundance total below 500 and all features witht an average abundance less than 2 across all samples. You do not need to use these parameters and can use any method you chose to do this. Other methods for filtering feature tables are outlined [here.](https://docs.qiime2.org/2018.8/tutorials/filtering/)

To use the sparcc filter use this command:
```
qiime SCNIC sparcc-filter \
  --i-table fake_data.qza \
  --o-table-filtered fake_data.filtered.qza
```

### 2. Calculating correlations and making your network
With your filtered data you can calculate your correlation table and make a network to visualize your correlations.

#### Generating a correlation table
To calculate all pairwise correlations between features in your filtered table use the following command:
```
qiime SCNIC calculate-correlations \
  --i-table fake_data-filtered.qza \
  --p-method sparcc \
  --o-correlation-table fake_correls.qza
```
Here we use the [sparCC](https://doi.org/10.1371/journal.pcbi.1002687) metric for measuring the strength of our correlation. This metric is recommended when you data is in the form of OTUs or ASVs ([Weiss et al. 2017](https://doi.org/10.1038/ismej.2015.235)). You may also use Pearson, Spearman or Kendall-Tau correlation.

#### (Optional) Making a correlation network
From `fake_correls.qza` we can generate a network based on a minimum R value cutoff. A network will also be generated when finding modules but if you only want to make a network and not find modules you can do this and finish the tutorial here. This can be done using this command:
```
qiime SCNIC build-correlation-network-r \
  --i-correlation-table fake_correls.qza \
  --p-min-val .35 \
  --o-correlation-network fake_net.qza
```
The `--p-min-val` parameter sets the minimum R value required to call a correlation between two features significant and therefore draw an edge between them. In this example we used a minimum value of .35. This is a common cutoff used with the sparCC correlation metric when used with 16S data.

If you want to make a correlation network based on a maximum significant p-value using the `build-correlation-network-p` method. NOTE: calculating p-values on sparCC correlation values is not currently supported. If you would like to see this feature added [leave an issue.](https://github.com/shafferm/q2-SCNIC)

### 3. Detecting and summarizing modules of features
Areas of a network which are strongly interconnected are called modules. With this step we detect these modules and summarize the features in them. The summarization is a simple sum of all features in your modules across samples. This makes it so that sample abundance counts remain the same after summarization and therefore this table can be used for further statistical tests like [ANCOM](https://docs.qiime2.org/2018.8/tutorials/moving-pictures/#differential-abundance-testing-with-ancom) for testing for differential abundance.

To detect and summarize modules use this command:
```
qiime SCNIC make-modules-on-correlation-table \
  --i-correlation-table fake_correls.qza \
  --i-feature-table fake_data.qza \
  --p-min-r .35 \
  --o-collapsed-table fake_data.collapsed.qza \
  --o-correlation-network fake_net.modules.qza \
  --o-module-membership fake_membership.qza
```
The `fake_data.collapsed.qza` is a feature table you can use with any further non-phylogenetic analysis. `fake_net.modules.qza` is a network that is annotated with correlation information as well as module membership and can be exported from the `.qza` to visualize with tools such as [Cytoscape.](http://www.cytoscape.org/)

The `fake_membership.qza` is viewable as metadata and can be turned into a visualization via this command:
```
qiime meta tabulate \
  --m-input-file fake_membership.qza \
  --o-visualization fake_membership.qzv
```
This visualization can then be used to see what features are in each module.

With that you have ran SCNIC and have a feature table with fewer features giving you more power for further analyses and a correlation network investigate correlations between features in your community of interest.
