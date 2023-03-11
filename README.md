[![Build Status](https://travis-ci.com/lozuponelab/q2-SCNIC.svg?branch=master)](https://travis-ci.com/lozuponelab/q2-SCNIC) [![Coverage Status](https://coveralls.io/repos/github/lozuponelab/q2-SCNIC/badge.svg?branch=master)](https://coveralls.io/github/lozuponelab/q2-SCNIC?branch=master) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/3bcffec347f84d70b473dbe9c4192083)](https://www.codacy.com/gh/lozuponelab/q2-SCNIC/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lozuponelab/q2-SCNIC&amp;utm_campaign=Badge_Grade)

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
