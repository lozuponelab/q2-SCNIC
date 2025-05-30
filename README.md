![Build Status](https://github.com/lozuponelab/q2-SCNIC/actions/workflows/ci.yml/badge.svg)

# NOTE

The most up to date version of the q2-SCNIC repo is [here](https://github.com/lozuponelab/q2-SCNIC)!

# q2-SCNIC

A package for accessing the primary methods of [SCNIC](https://www.github.com/lozuponelab/SCNIC) via QIIME2.

# Installation

First, make sure you have SCNIC installed:

```
conda install -q scnic
```

OR

```
pip install scnic
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

The tutorial for q2-SCNIC can be found in `community_tutorial.md`.