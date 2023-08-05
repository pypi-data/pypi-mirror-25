
# Python API for analyzing and manipulating genotype-phenotype maps


[![Join the chat at https://gitter.im/harmslab/gpmap](https://badges.gitter.im/harmslab/gpmap.svg)](https://gitter.im/harmslab/gpmap?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Documentation Status](https://readthedocs.org/projects/gpmap/badge/?version=latest)](http://gpmap.readthedocs.io/en/latest/?badge=latest)

This package defines a standard data-structure for genotype-phenotype (GP) map data.
Subset, manipulate, extend, etc. GP maps. Calculate statistics, model evolutionary
trajectories, predict phenotypes (in combination with the epistasis package). Efficient memory usage,
using numpy arrays to store in memory.

<img src="docs/_img/gpm.png" align="middle">

## Basic example

Import the package's base object.
```python
from gpmap import GenotypePhenotypeMap
```

Load a dataset from disk.
```python
gpm = GenotypePhenotypeMap.read_json("data.json")
```

## Installation

To install this package, clone from source and use pip.
```
git clone https://github.com/harmslab/gpmap
cd gpmap
pip install -e .
```

## Dependencies

The following modules are required. Also, the examples/tutorials are written in Jupyter notebooks and require IPython to be install.

* [Numpy](http://www.numpy.org/)
