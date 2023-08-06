[![Build Status](https://travis-ci.org/rjsberry/libemd.svg?branch=master)](https://travis-ci.org/rjsberry/libemd)
[![Coverage Status](https://coveralls.io/repos/github/rjsberry/libemd/badge.svg?branch=master)](https://coveralls.io/github/rjsberry/libemd?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3eb07539be3040afa74ab2d1bb937b09)](https://www.codacy.com/app/rjsberry/libemd?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rjsberry/libemd&amp;utm_campaign=Badge_Grade)

# libemd

`libemd` is a library of functions for Python for computing the empirical mode
decomposition and it's variations.

`libemd` is still in production, but is under active development.

## Installation

```
pip install libemd
```

## Usage

```python
>>> from libemd import emd
>>> imfs = emd(x)
```

By default, `libemd` uses the S-number stoppage criterion with an S-number
of 1. You can adjust this with the `method` keyword argument.

`libemd` uses the SciPy functions `argrelmax` and `argrelmin` for locating the
extrema in signals. You can override this with the `peakfindermax` and
`peakfindermin` keyword arguments, which both accept function objects that
accept a signal as their only argument and return the indices of extrema in a
numpy array.

You can also optionally specify a filter to apply to the signal before any
peakfinding takes place. This filter is just used for peakfinding, and does 
not affect the signal during the decomposition.


## Features

### Algorithms

- [x]  EMD
- [ ]  EEMD
- [ ]  CEEMDAN
- [ ]  *MEMD*

### Stopping criteria

- [x] Standard deviation
- [x] S-number
- [x] Threshold-based

Multivariate algorithms are the exception in this planned feature list, as they
are still somewhat emerging.

Algorithms will, at first, be implemented in Python. On completion, algorithms
will also be implemented in Cython. Ultimately, `libemd` will have a usage
analagous to the code block below, wherein the API for the Python and Cython
algorithms is identical, and they can be easily interchanged with import
statements.

```python
try:
    from libemd import cyemd as emd
except ImportError:
    from libemd import emd
```


## Tests

Tests are designed to utilise pytest. Test source code is organized in the
following form:

```python
# == Class/function testing

# -- pytest fixtures

def get_params_testA():
    return {'params': [], 'ids': []}

@pytest.fixture(**get_params_testA())
def params_testA(request):
    return request.get


# -- Tests

def test_A(params_testA):
    """
    pytest unpacks params and param ids from fixture to use in test.
    """
    pass
```
