import numpy as np
import numpy.testing as nptest
import pytest
import scipy

from libemd import pysift


# == Module global fixtures ===================================================

dummyx = np.array([], dtype=float)
dummyt = np.array([], dtype=float)


def returnself(x):
    return x


@pytest.fixture
def sift_master():
    """
    The master sift class.
    """
    return pysift.SiftMaster(x=dummyx, t=dummyt)


@pytest.fixture
def sift_stopsd():
    """
    Custom fixture that allows access to SD methods.
    """
    return pysift.SiftStopStdDev(x=dummyx, t=dummyt)


@pytest.fixture
def sift_stopsn():
    """
    Custom fixture that allows access to SD methods.
    """
    return pysift.SiftStopSNum(x=dummyx, t=dummyt)


@pytest.fixture
def sift_stoptm():
    """
    Custom fixture that allows access to SD methods.
    """
    return pysift.SiftStopThresh(x=dummyx, t=dummyt)


def get_params_pysiftSift_integration():
    """
    Params: 'x', 't', 'max_iterations'.
    """
    params = [
        (np.random.randn(50), np.arange(50), 1),
        (np.random.randn(500), np.arange(500), 10),
        (np.random.randn(5000), np.arange(5000), 100)
    ]
    ids = [
        'Random array (size: {}), {} iterations'.format(
            p[0].size, p[2]) for p in params
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSift_integration())
def params_pysiftSift_integration(request):
    return request.param


# == Function: pysift.get_sifter ==============================================

# -- Unique fixtures ----------------------------------------------------------

def get_params_pysift_get_sifter_instantiates_correct_class():
    """
    Params: 'x', 't', 'method', 'expected_method'
    """
    params = (
        (dict(x=dummyx, t=dummyt, method='sd'), 'sd'),
        (dict(x=dummyx, t=dummyt, method='sn'), 'sn'),
        (dict(x=dummyx, t=dummyt, method='tm'), 'tm'),
        (dict(x=dummyx, t=dummyt, method=('sd', 0.3)), 'sd'),
        (dict(x=dummyx, t=dummyt, method=('sn', 2)), 'sn'),
        (dict(x=dummyx, t=dummyt, method=('tm', 0.05, 0.5, 0.05)), 'tm'),
        (
            dict(
                x=dummyx, t=dummyt, method='sd', peakfilter=returnself,
                peakfindermax=returnself, peakfindermin=returnself
            ), 'sd'
        ),
        (
            dict(
                x=dummyx, t=dummyt, method='sn', peakfilter=returnself,
                peakfindermax=returnself, peakfindermin=returnself
            ), 'sn'
        ),
        (
            dict(
                x=dummyx, t=dummyt, method='tm', peakfilter=returnself,
                peakfindermax=returnself, peakfindermin=returnself
            ), 'tm'
        )
    )
    ids = [
        'Standard deviation (no opts)',
        'S-number (no opts)',
        'Threshold (no opts)',
        'Standard deviation (opts)',
        'S-number (opts)',
        'Threshold (opts)',
        'Standard deviation (no opts, with peak-finding function args)',
        'S-number (no opts, with peak-finding function args)',
        'Threshold (no opts, with peak-finding function args)'
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysift_get_sifter_instantiates_correct_class())
def params_pysift_get_sifter_instantiates_correct_class(request):
    return request.param


def get_params_pysift_get_sifter_unrecognized_method():
    """
    Params: 'x', 't', 'made_up_method'
    """
    params = (
        (dict(x=dummyx, t=dummyt, method='madeup')),
        (dict(x=dummyx, t=dummyt, method=('madeup', 'madeupopt')))
    )
    ids = ['No options', 'With options']
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysift_get_sifter_unrecognized_method())
def params_pysift_get_sifter_unrecognized_method(request):
    return request.param


def get_params_pysift_get_sifter_override_criterion_options():
    """
    Params: 'x', 't', 'method', 'new_method_options'
    """
    params = (
        (dict(x=dummyx, t=dummyt, method=('sd', 0.4)), dict(sdlimit=0.4)),
        (dict(x=dummyx, t=dummyt, method=('sn', 3)), dict(snumber=3)),
        (dict(x=dummyx, t=dummyt, method=('tm', 0.06, 0.6, 0.06)),
            dict(theta1=0.06, theta2=0.6, alpha=0.06)
        )
    )
    ids = ['Standard deviation', 'S-number', 'Threshold']
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysift_get_sifter_override_criterion_options())
def params_pysift_get_sifter_override_criterion_options(request):
    return request.param


def get_params_pysift_get_sifter_incorrect_criterion_options():
    """
    Params: 'x', 't', 'made_up_method_options'
    """
    params = (
        (dict(x=dummyx, t=dummyt, method=('sd', 1, 1))),
        (dict(x=dummyx, t=dummyt, method=('sn', 1, 1))),
        (dict(x=dummyx, t=dummyt, method=('tm', 1)))
    )
    ids = ['Standard deviation', 'S-number', 'Threshold']
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysift_get_sifter_incorrect_criterion_options())
def params_pysift_get_sifter_incorrect_criterion_options(request):
    return request.param


def get_params_pysift_get_sifter_bad_arguments():
    """
    Params: 'x', 't', 'method', 'peakfilter', `peakfindermax`, `peakfindermin`.
    """
    params = (
        (
            dict(
                x='badx', t=dummyt, method='sd', peakfilter=returnself,
                peakfindermax=returnself, peakfindermin=returnself
            )
        ),
        (
            dict(
                x=dummyx, t='badt', method='sd', peakfilter=returnself,
                peakfindermax=returnself, peakfindermin=returnself
            )
        ),
        (
            dict(
                x=dummyx, t=dummyt, method='badmethod', peakfilter=returnself,
                peakfindermax=returnself, peakfindermin=returnself
            )
        ),
        (
            dict(
                x=dummyx, t=dummyt, method='sd', peakfilter='badfilter',
                peakfindermax=returnself, peakfindermin=returnself
            )
        ),
        (
            dict(
                x=dummyx, t=dummyt, method='sd', peakfilter=returnself,
                peakfindermax='badpeakfindermax', peakfindermin=returnself
            )
        ),
        (
            dict(
                x=dummyx, t=dummyt, method='sd', peakfilter=returnself,
                peakfindermax=returnself, peakfindermin='badpeakfindermin'
            )
        )
    )
    ids = [
        'Bad "x"',
        'Bad "t"',
        'Bad "method"',
        'Bad "peakfilter"',
        'Bad "peakfindermax"',
        'Bad "peakfindermin"'
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysift_get_sifter_bad_arguments())
def params_pysift_get_sifter_bad_arguments(request):
    return request.param


# -- Unit tests ---------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.sift_factory
def test_sifter_factory_instantiates_correct_class(
        params_pysift_get_sifter_instantiates_correct_class):
    # GIVEN a method or method/option tuple
    # WHEN sifting method factory is called
    # THEN return sift class with correct stopping criterion
    p = params_pysift_get_sifter_instantiates_correct_class
    test_sifter = pysift.get_sifter(**p[0])
    assert test_sifter.stopping_criterion == p[1]


@pytest.mark.unit
@pytest.mark.sift_factory
def test_sifter_factory_raises_correct_exception_on_unrecognized_method(
        params_pysift_get_sifter_unrecognized_method):
    # GIVEN an invalid method id
    # WHEN sifting method factory is called
    # THEN raise a SiftingProcessException
    p = params_pysift_get_sifter_unrecognized_method
    with pytest.raises(ValueError):
        pysift.get_sifter(**p)


@pytest.mark.unit
@pytest.mark.sift_factory
def test_sifter_factory_overrides_default_stopping_criterion_options(
        params_pysift_get_sifter_override_criterion_options):
    # GIVEN a method/option tuple that overrides default options
    # WHEN sifting method factory is called
    # THEN override default options
    p = params_pysift_get_sifter_override_criterion_options
    test_sifter = pysift.get_sifter(**p[0])
    assert test_sifter.stopping_criterion_options == p[1]


@pytest.mark.unit
@pytest.mark.sift_factory
def test_sifter_factory_raises_correct_exception_on_incorrect_stopping_options(
        params_pysift_get_sifter_incorrect_criterion_options):
    # GIVEN an incorrect method/option tuple
    # WHEN sifting method factory is called
    # THEN raise a SiftingProcessException
    p = params_pysift_get_sifter_incorrect_criterion_options
    with pytest.raises(ValueError):
        pysift.get_sifter(**p)


@pytest.mark.unit
@pytest.mark.sift_factory
def test_sifter_raises_exception_with_bad_function_arguments(
        params_pysift_get_sifter_bad_arguments):
    # GIVEN arguments with the wrong type
    # WHEN sifting method factory is called
    # THEN raise an exception
    p = params_pysift_get_sifter_bad_arguments
    with pytest.raises(ValueError):
        pysift.get_sifter(**p)

    
# == Class: pysift.SiftMaster =================================================

# -- Unique fixtures ----------------------------------------------------------

def get_params_pysiftSiftMaster_extrapolate():
    params = (
        (1, 1, 2, 2, 0, 0),
        (0, 0, 1, 1, 2, 2)
    )
    ids = ['backward', 'forward']
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSiftMaster_extrapolate())
def params_pysiftSiftMaster_extrapolate(request):
    return request.param


def get_params_pysiftSiftMaster_endpoints():
    params = (
        (np.array([0, 1, 3, 1, 0]), np.greater, 0, 0),
        (np.array([0, 3, 1, 3, 0]), np.greater, 5, 5),
        (np.array([0, -1, -3, -1, 0]), np.less, 0, 0),
        (np.array([0, -3, -1, -3, 0]), np.less, -5, -5)
    )
    ids = [
        'endpoints = x_endpoints [maxima]',
        'endpoints = extrapolate [maxima]',
        'endpoints = x_endpoints [minima]',
        'endpoints = extrapolate [minima]'
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSiftMaster_endpoints())
def params_pysiftSiftMaster_endpoints(request):
    return request.param


def get_params_pysiftSiftMaster_fit_splines():
    """
    Params: `e_x`, `e_t`, `tnew`, `e_x_length`, `expected_polynomial_order`
    """
    order_d = {0: None, 1: None, 2: 1, 3: 2}
    params = [
        (np.arange(l), np.arange(l), np.arange(10), l, order_d.get(l, 3)) for
        l in range(4)
    ]
    ids = ['Array length {}'.format(l) for l in range(4)]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSiftMaster_fit_splines())
def params_pysiftSiftMaster_fit_splines(request):
    return request.param


def get_params_pysiftSiftMaster_raise_not_implemented_error():
    params = (
        'stopping_criterion_options',
        'stopsift',
        'prep_stopsift_params',
    )
    ids = [
        f'Class method: {p}' for p in params
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSiftMaster_raise_not_implemented_error())
def params_pysiftSiftMaster_raise_not_implemented_error(request):
    return request.param


# -- Unit tests ---------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_sets_default_t_array():
    # GIVEN a sifting process class
    # WHEN the class is instantiated with no given t-array
    # THEN appropriately set the t-array
    l = np.random.randint(0, 100)
    s = pysift.SiftMaster(np.random.randn(l))
    assert s.t.size == l


@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_generate_component(sift_master):
    # GIVEN a mean envelope and a previous iteration's IMF candidate
    # WHEN the IMF componet is generated
    # THEN make sure it's correct
    s = sift_master
    s._h0 = np.random.randn(10)
    s._env_mean = np.random.randn(10)
    expected = s._h0 - s._env_mean
    s.generate_component()
    nptest.assert_array_equal(s._h, expected)


@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_extrapolate(
        sift_master, params_pysiftSiftMaster_extrapolate):
    # GIVEN a set of x and y points
    # WHEN the points are used for linear extrapolation
    # THEN make sure it's correct
    s = sift_master
    p = params_pysiftSiftMaster_extrapolate
    y_test = s.extrapolate(p[0], p[1], p[2], p[3], p[4])
    assert y_test == p[5]


@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_endpoints(
        sift_master, params_pysiftSiftMaster_endpoints):
    # GIVEN an array of maxima
    # WHEN the endpoint method is called on the array
    # THEN make sure it's correct
    s = sift_master
    p = params_pysiftSiftMaster_endpoints
    t = np.arange(p[0].size)
    arr_test = s.endpoints(p[0], t, p[1])
    assert arr_test[0] == p[2]
    assert arr_test[-1] == p[3]


@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_endpoints_edge_case_array_size_less_than_3(
        sift_master):
    # GIVEN an array of maxima
    # WHEN the length of the array is less than or equal to 2
    # THEN make sure the endpoints method returns the array without error
    s = sift_master
    for l in range(3):
        arr = np.random.randn(l)
        arr_test = s.endpoints(arr, np.arange(l), lambda x: x)
        nptest.assert_array_equal(arr_test, arr)


@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_extrema_indices(monkeypatch, sift_master):
    # GIVEN two methods and an array
    # WHEN the arguments are passed to extrema_inds
    # THEN verify the methods are executed on the array
    s = sift_master
    x = np.random.randn(10)

    def preprocessingfilter(x):
        return x**2

    def peakfinder(x):
        return x / 2

    expected = np.hstack([0, (x**2)/2, x.size-1])
    extrema_inds = s.extrema_indices(x, preprocessingfilter, peakfinder)
    nptest.assert_array_equal(extrema_inds, expected)


@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_locate_extrema(monkeypatch, sift_master):
    # GIVEN a monkeypatched set of indices
    # WHEN the locate_extrema method is called
    # THEN set instance variables and envelopes correctly
    s = sift_master
    maxima_indices = np.unique(np.random.randint(0, 10, 5))
    minima_indices = np.unique(np.random.randint(0, 10, 5))

    def mockreturn(_x, _filter, peakfinder):
        ind_d = {'argrelmax': maxima_indices, 'argrelmin': minima_indices}
        return ind_d[peakfinder.__name__]

    monkeypatch.setattr(s, 'extrema_indices', mockreturn)
    s._h0 = np.random.randn(10)
    s.t = np.arange(10)
    s.locate_extrema()
    nptest.assert_array_equal(s._i_max, maxima_indices)
    nptest.assert_array_equal(s._i_min, minima_indices)
    nptest.assert_array_equal(s._e_x_upper, s._h0[maxima_indices])
    nptest.assert_array_equal(s._e_x_lower, s._h0[minima_indices])
    nptest.assert_array_equal(s._e_t_upper, s.t[maxima_indices])
    nptest.assert_array_equal(s._e_t_lower, s.t[minima_indices])


@pytest.mark.unit
@pytest.mark.sift_master
def test_pysiftSiftMaster_fit_splines(
        sift_master, params_pysiftSiftMaster_fit_splines, mocker):
    # GIVEN an array of a certain length
    # WHEN the sifting process class method to fit splines is called
    # THEN make sure the correct polynomial order is used
    s = sift_master
    p = params_pysiftSiftMaster_fit_splines
    mocker.patch('scipy.interpolate.splrep')
    mocker.patch('scipy.interpolate.splev')
    line = s.fit_splines(*p[0:3])
    if p[3] == 0 or p[3] == 1:
        nptest.assert_array_equal(line, p[0])
    else:
        scipy.interpolate.splrep.assert_called_once_with(p[1], p[0], k=p[4])


@pytest.mark.unit
@pytest.mark.sift_master
def test_sifting_process_master_class_raises_exception_on_abstract_methods(
        sift_master, params_pysiftSiftMaster_raise_not_implemented_error):
    # GIVEN a class method which is not defined in the master sift class
    # WHEN the method is called
    # THEN raise NotImplementedError due to abstract method definition
    s = sift_master
    p = params_pysiftSiftMaster_raise_not_implemented_error
    with pytest.raises(NotImplementedError):
        f = getattr(s, p)
        f()


# == Class: pysift.SiftStopStdDev =============================================

# -- Unique fixtures ----------------------------------------------------------

def get_params_pysiftSiftStopStdDev_stopsift_method():
    """
    Params: 'sd', 'sdlimit', 'expected_return_value'
    """
    params = ((0.2, 0.3, True), (0.4, 0.3, False), (0.3, 0.3, False))
    ids = ['sd: {}, sdlimit: {}'.format(p[0], p[1]) for p in params]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSiftStopStdDev_stopsift_method())
def params_pysiftSiftStopStdDev_stopsift_method(request):
    return request.param


# -- Unit tests ---------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.std_criterion
def test_sifting_process_stopsift_method_for_standard_deviation_criterion(
        params_pysiftSiftStopStdDev_stopsift_method, sift_stopsd):
    # GIVEN an SD of two signals
    # WHEN the SD is less than the SD limit
    # THEN stopsift method returns True
    s = sift_stopsd
    p = params_pysiftSiftStopStdDev_stopsift_method
    s._sd = p[0]
    s.sdlimit = p[1]
    if p[2]:
        assert s.stopsift() is True
    else:
        assert s.stopsift() is not True


@pytest.mark.unit
@pytest.mark.std_criterion
def test_sifting_process_stddev_stoping_criterion_skip_stopcheck(sift_stopsn):
    # GIVEN the standard deviation stopping condition Sift class
    # WHEN on the first iteration of the sifting proess
    # THEN stopsift method returns False
    s = sift_stopsn
    s._i = 0
    assert s.stopsift() is not True


@pytest.mark.unit
@pytest.mark.std_criterion
def test_sifting_process_stddev_stopping_criterion_prepare_next_iteration(
        sift_stopsd):
    # GIVEN a set of initial parameters
    # WHEN the sifting loop does not break, and the next iteration is prepped
    # THEN load the parameter set into the "previous iteration" set
    s = sift_stopsd
    s._h = np.random.randn(10)
    s.prepare_next_iteration()
    nptest.assert_array_equal(s._h0, s._h)


# -- Integration tests --------------------------------------------------------

@pytest.mark.integration
@pytest.mark.std_criterion
def test_sifting_process_stddev_integration(
        params_pysiftSift_integration, sift_stopsd):
    # GIVEN a set of starting parameters
    # WHEN the main sifting loop method is called
    # THEN run iterations return an IMF component gracefully
    s = sift_stopsd
    p = params_pysiftSift_integration
    s._h0 = p[0]
    s.t = p[1]
    s.max_iterations = p[2]
    imf = s.sift()
    assert isinstance(imf, np.ndarray)


@pytest.mark.integration
@pytest.mark.std_criterion
def test_sifting_process_stddev_integration_max_iterations(
        monkeypatch, params_pysiftSift_integration, sift_stopsd):
    # GIVEN a set of starting parameters
    # WHEN the main sifting loop method is called
    # THEN run iterations return an IMF component gracefully
    s = sift_stopsd
    p = params_pysiftSift_integration
    s._h0 = p[0]
    s.t = p[1]
    s.max_iterations = p[2]
    def mockreturn():
        return False
    monkeypatch.setattr(s, 'stopsift', mockreturn)
    imf = s.sift()
    assert type(imf) == np.ndarray
    assert s._i == s.max_iterations - 1


# == Class: pysift.SiftStopSNum ===============================================

# -- Unique fixtures ----------------------------------------------------------

def get_params_pysiftSiftStopSNum_stopsift_method():
    """
    Params: 'extrema_sum', 'scount', 'snumber', 'expected_return_value'
    """
    params = (
        (0, 1, 1, True),
        (1, 1, 1, True),
        (1, 0, 1, False),
        (2, 1, 1, False),
        (0, -1, 1, False)
    )
    ids = [
        'extrema_count: {}, scount: {}, snumber: {}'.format(
            p[0], p[1] + 1, p[2]) for p in params
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSiftStopSNum_stopsift_method())
def params_pysiftSiftStopSNum_stopsift_method(request):
    return request.param


# -- Unit tests ---------------------------------------------------------------

@pytest.mark.snumber_criterion
def test_sifting_process_stopsift_method_for_snumber_criterion(
        params_pysiftSiftStopSNum_stopsift_method, sift_stopsn):
    # GIVEN a sum of extrema, an iteration counter, and an S-number
    # WHEN the extrema sum is less than or equal to one, and the S count
    #      is greater than the S-number
    # THEN stopsift method returns True
    s = sift_stopsn
    p = params_pysiftSiftStopSNum_stopsift_method
    s._extrema_sum = p[0]
    s._scount = p[1]
    s.snumber = p[2]
    if p[3]:
        assert s.stopsift() is True
    else:
        assert s.stopsift() is not True


@pytest.mark.snumber_criterion
def test_sifting_process_snumber_stoping_criterion_skip_iteration_stopcheck(
        sift_stopsn):
    # GIVEN the S-number stopping criterion Sift class
    # WHEN on the first iteration of the sifting process
    # THEN the stopsift method returns False
    s = sift_stopsn
    s._i = 0
    assert s.stopsift() is not True


@pytest.mark.snumber_criterion
def test_sifting_process_snumber_stopping_criterion_prepare_next_iteration(
        sift_stopsn):
    # GIVEN a set of initial parameters
    # WHEN the sifting loop doesn't break and the next iteration is prepped
    # THEN load the parameter set into the "previous iteration" set
    s = sift_stopsn
    s._h = np.random.randn(10)
    s._num_zc = np.random.randn()
    s._num_max = np.random.randn()
    s._num_min = np.random.randn()
    s.prepare_next_iteration()
    nptest.assert_array_equal(s._h0, s._h)
    nptest.assert_array_equal(s._num_zc0, s._num_zc)
    nptest.assert_array_equal(s._num_max0, s._num_max)
    nptest.assert_array_equal(s._num_min0, s._num_min)


# -- Integration tests --------------------------------------------------------

@pytest.mark.integration
@pytest.mark.snumber_criterion
def test_sifting_process_snumber_integration(
        params_pysiftSift_integration, sift_stopsn):
    # GIVEN a set of starting parameters
    # WHEN the main sifting loop method is called
    # THEN run iterations return an IMF component gracefully
    s = sift_stopsn
    p = params_pysiftSift_integration
    s._h0 = p[0]
    s.t = p[1]
    s.max_iterations = p[2]
    imf = s.sift()
    assert type(imf) == np.ndarray


@pytest.mark.integration
@pytest.mark.snumber_criterion
def test_sifting_process_snumber_integration_max_iterations(
        monkeypatch, params_pysiftSift_integration, sift_stopsn):
    # GIVEN a set of starting parameters
    # WHEN the main sifting loop method is called
    # THEN run iterations return an IMF component gracefully
    s = sift_stopsn
    p = params_pysiftSift_integration
    s._h0 = p[0]
    s.t = p[1]
    s.max_iterations = p[2]
    def mockreturn():
        return False
    monkeypatch.setattr(s, 'stopsift', mockreturn)
    imf = s.sift()
    assert type(imf) == np.ndarray
    assert s._i == s.max_iterations - 1


# == Class: pysift.SiftStopThresh =============================================

# -- Unique fixtures ----------------------------------------------------------

def get_params_pysiftSiftStopThresh_stopsift_method():
    """
    Params: 'theta1', 'theta2', 'alpha', 'sigma', 'expected_return_value'
    """
    params = (
        (0.05, 0.5, 0.05, np.hstack([
            np.array([0.04 for _ in range(96)]),
            np.array([0.4 for _ in range(4)])
        ]), True),
        (0.05, 0.5, 0.05, np.hstack([
            np.array([0.04 for _ in range(95)]),
            np.array([0.4 for _ in range(5)])
        ]), True),
        (0.05, 0.5, 0.05, np.hstack([
            np.array([0.04 for _ in range(94)]),
            np.array([0.4 for _ in range(6)])
        ]), False)
    )
    ids = [
        'alpha = 0.05, sigma < theta1 for 96% and < theta2 for 4%',
        'alpha = 0.05, sigma < theta1 for 95% and < theta2 for 5%',
        'alpha = 0.05, sigma < theta1 for 94% and < theta2 for 6%'
    ]
    return {'params': params, 'ids': ids}


@pytest.fixture(**get_params_pysiftSiftStopThresh_stopsift_method())
def params_pysiftSiftStopThresh_stopsift_method(request):
    return request.param


# -- Unit tests ---------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.threshold_criterion
def test_sifting_process_threshold_stopping_criterion_stopsift_method(
        params_pysiftSiftStopThresh_stopsift_method, sift_stoptm):
    # GIVEN threshold paramters and a signal, sigma
    # WHEN sigma is bounded by the conditions in the threshold parameters
    # THEN stopsift method returns True
    s = sift_stoptm
    p = params_pysiftSiftStopThresh_stopsift_method
    s.theta1 = p[0]
    s.theta2 = p[1]
    s.alpha = p[2]
    s._sigma = p[3]
    if p[4]:
        assert s.stopsift() is True
    else:
        assert s.stopsift() is not True


# -- Integration tests --------------------------------------------------------

@pytest.mark.integration
@pytest.mark.threshold_criterion
def test_sifting_process_threshold_integration(
        params_pysiftSift_integration, sift_stoptm):
    # GIVEN a set of starting parameters
    # WHEN the main sifting loop method is called
    # THEN run iterations return an IMF component gracefully
    s = sift_stoptm
    p = params_pysiftSift_integration
    s._h0 = p[0]
    s.t = p[1]
    s.max_iterations = p[2]
    imf = s.sift()
    assert type(imf) == np.ndarray


@pytest.mark.integration
@pytest.mark.threshold_criterion
def test_sifting_process_threshold_integration_max_iterations(
        monkeypatch, params_pysiftSift_integration, sift_stoptm):
    # GIVEN a set of starting parameters
    # WHEN the main sifting loop method is called
    # THEN run iterations return an IMF component gracefully
    s = sift_stoptm
    p = params_pysiftSift_integration
    s._h0 = p[0]
    s.t = p[1]
    s.max_iterations = p[2]

    def mockreturn():
        return False

    monkeypatch.setattr(s, 'stopsift', mockreturn)
    imf = s.sift()
    assert type(imf) == np.ndarray
    assert s._i == s.max_iterations - 1
