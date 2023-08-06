import numpy as np
import numpy.testing as nptest
import pytest

from libemd import pyemd
from libemd import pysift


FUNC_LEN = 200


# -- Fixtures -----------------------------------------------------------------

def get_monotonic_functions():
    params = [
        (np.zeros(FUNC_LEN)),
        (np.arange(FUNC_LEN)),
        (np.arange(FUNC_LEN) * (-1)),
        (np.sort(np.random.randn(FUNC_LEN))),
        (np.sort(np.random.randn(FUNC_LEN))[::-1])
    ]
    ids = [
        'Constant function',
        'df() > 0 (linear)',
        'df() < 0 (linear)',
        'df() > 0 (nonlinear)',
        'df() < 0 (nonlinear)'
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_monotonic_functions())
def monotonic_functions(request):
    return request.param


def get_params_is_monotonic():
    params = [(f, True) for f in get_monotonic_functions()['params']]
    params.append((np.random.randn(FUNC_LEN), False))
    ids = get_monotonic_functions()['ids']
    ids.append('Random data')
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_is_monotonic())
def params_is_monotonic(request):
    return request.param


def get_params_num_imfs():
    params = [(0, 0), (1, 1), (2, 1), (3, 1), (4, 2), (7, 2), (8, 3)]
    ids = ['n = {}'.format(n[0]) for n in params]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_num_imfs())
def params_num_imfs(request):
    return request.param


# -- Unit tests ---------------------------------------------------------------

def test_is_monotonic(params_is_monotonic):
    # GIVEN a monotonic function
    # WHEN the function is tested for it's monotonic property
    # THEN verify it is monotonic
    p = params_is_monotonic
    is_f_monotonic = pyemd.is_monotonic(p[0])
    if p[1] is True:
        assert is_f_monotonic is True
    else:
        assert is_f_monotonic is not True


def test_emd_monotonic_function_returns_self(monotonic_functions, mocker):
    # GIVEN a monotonic function
    # WHEN the function is decomposed via EMD
    # THEN don't initiate the siftng process, just return the function
    f = monotonic_functions
    mocker.patch('libemd.pysift.get_sifter')
    imfs = pyemd.emd(f)
    assert not pysift.get_sifter.called
    nptest.assert_array_equal(imfs, f)


def test_num_imfs(params_num_imfs):
    # GIVEN a signal length
    # WHEN the maximum number of IMFs is calculated
    # THEN make sure it's correct
    p = params_num_imfs
    n_test = pyemd.num_imfs(p[0])
    assert n_test == p[1]


def test_emd_up_to_max_imfs(monkeypatch, mocker):
    # GIVEN a random signal
    # WHEN the residual is never monotonic
    # THEN return an IMF matrix of the correct size
    random_length = np.random.randint(50, 200)
    signal = np.random.randn(random_length)
    num_imfs = int(np.floor(np.log2(random_length)))
    
    mocker.patch('libemd.pyemd.is_monotonic')
    mocker.patch('libemd.pyemd.get_sifter')
    pyemd.is_monotonic.return_value = False
    mock_sift = mocker.MagicMock()
    mock_sift.sift = mocker.MagicMock(return_value=np.zeros(random_length))
    pyemd.get_sifter.return_value = mock_sift

    imfs = pyemd.emd(signal)
    assert pyemd.is_monotonic.call_count == num_imfs
    assert pyemd.get_sifter.call_count == num_imfs
    assert imfs.shape[0] == num_imfs
