![Build Status](https://github.com/lozuponelab/q2-SCNIC/actions/workflows/ci.yml/badge.svg)

# NOTE

The most up to date version of the q2-SCNIC repo is [here](https://github.com/lozuponelab/q2-SCNIC)!

# q2-SCNIC

A package for accessing the primary methods of [SCNIC](https://www.github.com/lozuponelab/SCNIC) via QIIME2.

# Installation

First, follow the instructions to install QIIME 2 Amplicon using either Conda or Docker at https://library.qiime2.org/quickstart/amplicon

Next, install the fastspar dependency of SCNIC:

```
mamba install -c bioconda -c conda-forge fastspar 
```

OR

```
conda install -c bioconda -c conda-forge --override-channels fastspar 
```

Next, install SCNIC:

```
pip install scnic
```

OR

```
conda install -q scnic
```

Next to install the plugin:

```
pip install git+https://github.com/lozuponelab/q2-SCNIC.git
qiime dev refresh-cache
```

Finally to see what functions are available, you can use:

```
qiime SCNIC --help
```

# Tutorial

The tutorial for q2-SCNIC can be found at https://github.com/lozuponelab/q2-SCNIC/blob/master/community_tutorial.md
