#!/usr/bin/env python
"""Test suite for aospy.timedate module."""
import datetime

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from aospy.data_loader import set_grid_attrs_as_coords
from aospy.internal_names import (
    TIME_STR, TIME_BOUNDS_STR, BOUNDS_STR, TIME_WEIGHTS_STR,
    RAW_START_DATE_STR, RAW_END_DATE_STR, SUBSET_START_DATE_STR,
    SUBSET_END_DATE_STR
)
from aospy.utils.times import (
    apply_time_offset,
    average_time_bounds,
    monthly_mean_ts,
    monthly_mean_at_each_ind,
    ensure_datetime,
    datetime_or_default,
    numpy_datetime_range_workaround,
    numpy_datetime_workaround_encode_cf,
    month_indices,
    _month_conditional,
    extract_months,
    ensure_time_avg_has_cf_metadata,
    _assert_has_data_for_time,
    add_uniform_time_weights,
    assert_matching_time_coord,
    ensure_time_as_dim,
    convert_scalar_to_indexable_coord,
    sel_time,
    yearly_average
)


_INVALID_DATE_OBJECTS = [1985, True, None, '2016-04-07', np.datetime64(1, 'Y')]


def test_apply_time_offset():
    start = datetime.datetime(1900, 5, 10)
    years, months, days, hours = -2, 1, 7, 3
    # test lengths 0, 1, and >1 of input time array
    for periods in range(3):
        times = pd.date_range(start=start, freq='M', periods=periods)
        actual = apply_time_offset(xr.DataArray(times), years=years,
                                   months=months, days=days, hours=hours)
        desired = (times + pd.tseries.offsets.DateOffset(
            years=years, months=months, days=days, hours=hours
        ))
        assert actual.identical(desired)


def test_monthly_mean_ts_single_month():
    time = pd.date_range('2000-01-01', freq='6H', periods=4 * 31)
    arr = xr.DataArray(np.random.random(time.shape), dims=[TIME_STR],
                       coords={TIME_STR: time})
    desired = arr.mean(TIME_STR)
    actual = monthly_mean_ts(arr)
    np.testing.assert_allclose(actual, desired)


def test_monthly_mean_ts_submonthly():
    time = pd.date_range('2000-01-01', freq='1D', periods=365 * 3)
    arr = xr.DataArray(np.random.random(time.shape), dims=[TIME_STR],
                       coords={TIME_STR: time})
    desired = arr.resample('1M', TIME_STR, how='mean')
    actual = monthly_mean_ts(arr)
    assert desired.identical(actual)


def test_monthly_mean_ts_monthly():
    time = pd.date_range('2000-01-01', freq='1M', periods=120)
    arr = xr.DataArray(np.random.random(time.shape), dims=[TIME_STR],
                       coords={TIME_STR: time})
    actual = monthly_mean_ts(arr)
    assert arr.identical(actual)


def test_monthly_mean_ts_na():
    time = pd.to_datetime(['2000-06-01', '2001-06-01'])
    arr = xr.DataArray(np.random.random(time.shape), dims=[TIME_STR],
                       coords={TIME_STR: time}).resample('1M', TIME_STR)
    actual = monthly_mean_ts(arr)
    desired = arr.dropna(TIME_STR)
    assert desired.identical(actual)


def test_monthly_mean_at_each_ind():
    times_submonthly = pd.to_datetime(['2000-06-01', '2000-06-15',
                                       '2000-07-04', '2000-07-19'])
    times_means = pd.to_datetime(['2000-06-01', '2000-07-01'])
    len_other_dim = 2
    arr_submonthly = xr.DataArray(
        np.random.random((len(times_submonthly), len_other_dim)),
        dims=[TIME_STR, 'dim0'], coords={TIME_STR: times_submonthly}
    )
    arr_means = xr.DataArray(
        np.random.random((len(times_means), len_other_dim)),
        dims=arr_submonthly.dims, coords={TIME_STR: times_means}
    )
    actual = monthly_mean_at_each_ind(arr_means, arr_submonthly)
    desired_values = np.stack([arr_means.values[0]] * len_other_dim +
                              [arr_means.values[1]] * len_other_dim,
                              axis=0)
    desired = xr.DataArray(desired_values, dims=arr_submonthly.dims,
                           coords=arr_submonthly.coords)
    assert actual.identical(desired)


def test_ensure_datetime_valid_input():
    for date in [datetime.datetime(1981, 7, 15),
                 datetime.datetime(1, 1, 1)]:
        assert ensure_datetime(date) == date


def test_ensure_datetime_invalid_input():
    with pytest.raises(TypeError):
        for obj in _INVALID_DATE_OBJECTS:
            ensure_datetime(obj)


def test_datetime_or_default():
    date = datetime.datetime(1, 2, 3)
    assert datetime_or_default(None, 'dummy') == 'dummy'
    assert datetime_or_default(date, 'dummy') == ensure_datetime(date)


def test_numpy_datetime_range_workaround():
    assert (numpy_datetime_range_workaround(
        datetime.datetime(pd.Timestamp.min.year + 1, 1, 1),
        pd.Timestamp.min.year + 1, pd.Timestamp.min.year + 2) ==
            datetime.datetime(pd.Timestamp.min.year + 1, 1, 1))

    assert (
        numpy_datetime_range_workaround(datetime.datetime(3, 1, 1), 1, 6) ==
        datetime.datetime(pd.Timestamp.min.year + 3, 1, 1)
    )

    assert (
        numpy_datetime_range_workaround(datetime.datetime(5, 1, 1), 4, 6) ==
        datetime.datetime(pd.Timestamp.min.year + 2, 1, 1)
    )

    # Test min_yr outside valid range
    assert (
        numpy_datetime_range_workaround(
            datetime.datetime(pd.Timestamp.min.year + 3, 1, 1),
            pd.Timestamp.min.year, pd.Timestamp.min.year + 2) ==
        datetime.datetime(pd.Timestamp.min.year + 4, 1, 1)
    )

    # Test max_yr outside valid range
    assert (
        numpy_datetime_range_workaround(
            datetime.datetime(pd.Timestamp.max.year + 2, 1, 1),
            pd.Timestamp.max.year - 1, pd.Timestamp.max.year) ==
        datetime.datetime(pd.Timestamp.min.year + 4, 1, 1))


def test_numpy_datetime_workaround_encode_cf():
    def create_test_data(days, ref_units, expected_units):
        # 1095 days corresponds to three years in a noleap calendar
        # This allows us to generate ranges which straddle the
        # Timestamp-valid range
        three_yrs = 1095.
        time = xr.DataArray([days, days + three_yrs], dims=[TIME_STR])
        ds = xr.Dataset(coords={TIME_STR: time})
        ds[TIME_STR].attrs['units'] = ref_units
        ds[TIME_STR].attrs['calendar'] = 'noleap'
        actual, min_yr, max_yr = numpy_datetime_workaround_encode_cf(ds)

        time_desired = xr.DataArray([days, days + three_yrs],
                                    dims=[TIME_STR])
        desired = xr.Dataset(coords={TIME_STR: time_desired})
        desired[TIME_STR].attrs['units'] = expected_units
        desired[TIME_STR].attrs['calendar'] = 'noleap'
        return actual, min_yr, max_yr, desired

    # 255169 days from 0001-01-01 corresponds to date 700-02-04.
    actual, min_yr, max_yr, desired = create_test_data(
        255169., 'days since 0001-01-01 00:00:00',
        'days since 979-01-01 00:00:00')
    xr.testing.assert_identical(actual, desired)
    assert xr.decode_cf(actual).time.values[0] == np.datetime64('1678-02-04')
    assert min_yr == 700
    assert max_yr == 703

    # Test a case where times are in the Timestamp-valid range
    actual, min_yr, max_yr, desired = create_test_data(
        10., 'days since 2000-01-01 00:00:00',
        'days since 2000-01-01 00:00:00')
    xr.testing.assert_identical(actual, desired)
    assert xr.decode_cf(actual).time.values[0] == np.datetime64('2000-01-11')
    assert min_yr == 2000
    assert max_yr == 2003

    # Regression tests for GH188
    actual, min_yr, max_yr, desired = create_test_data(
        732., 'days since 0700-01-01 00:00:00',
        'days since 1676-01-01 00:00:00')
    xr.testing.assert_identical(actual, desired)
    assert xr.decode_cf(actual).time.values[0], np.datetime64('1678-01-03')
    assert min_yr == 702
    assert max_yr == 705

    # Non-January 1st reference date
    actual, min_yr, max_yr, desired = create_test_data(
        732., 'days since 0700-05-03 00:00:00',
        'days since 1676-05-03 00:00:00')
    xr.testing.assert_identical(actual, desired)
    assert xr.decode_cf(actual).time.values[0], np.datetime64('1678-05-05')
    assert min_yr == 702
    assert max_yr == 705

    # Above Timestamp.max
    actual, min_yr, max_yr, desired = create_test_data(
        732., 'days since 2300-01-01 00:00:00',
        'days since 1676-01-01 00:00:00')
    xr.testing.assert_identical(actual, desired)
    assert xr.decode_cf(actual).time.values[0], np.datetime64('1678-01-03')
    assert min_yr == 2302
    assert max_yr == 2305

    # Straddle lower bound
    actual, min_yr, max_yr, desired = create_test_data(
        2., 'days since 1677-01-01 00:00:00',
        'days since 1678-01-01 00:00:00')
    xr.testing.assert_identical(actual, desired)
    assert xr.decode_cf(actual).time.values[0], np.datetime64('1678-01-03')
    assert min_yr == 1677
    assert max_yr == 1680

    # Straddle upper bound
    actual, min_yr, max_yr, desired = create_test_data(
        2., 'days since 2262-01-01 00:00:00',
        'days since 1678-01-01 00:00:00')
    xr.testing.assert_identical(actual, desired)
    assert xr.decode_cf(actual).time.values[0], np.datetime64('1678-01-03')
    assert min_yr == 2262
    assert max_yr == 2265


def test_month_indices():
    np.testing.assert_array_equal(month_indices('ann'), range(1, 13))
    np.testing.assert_array_equal(month_indices('jja'),
                                  np.array([6, 7, 8]))
    with pytest.raises(ValueError):
        month_indices('dfm')
        month_indices('j')
        month_indices('q')
    assert month_indices('s') == [9]
    np.testing.assert_array_equal(month_indices('djf'),
                                  np.array([12, 1, 2]))
    assert month_indices(12) == [12]


def test_month_conditional():
    test = pd.date_range('2000-01-01', '2000-03-01', freq='M')
    test = xr.DataArray(test, dims=[TIME_STR], coords=[test])
    result_jan = _month_conditional(test, [1])
    np.testing.assert_array_equal(result_jan, np.array([True, False]))

    result_jan_feb = _month_conditional(test, [1, 2])
    np.testing.assert_array_equal(result_jan_feb, np.array([True, True]))

    result_march = _month_conditional(test, [3])
    np.testing.assert_array_equal(result_march, np.array([False, False]))

    test = pd.date_range('1999-12-31 18:00:00', '2000-01-01 00:00:00',
                         freq='6H')
    test = xr.DataArray(test, dims=[TIME_STR])
    result_jan = _month_conditional(test, [1])
    np.testing.assert_array_equal(result_jan,
                                  np.array([False, True]))

    result_jd = _month_conditional(test, [1, 12])
    np.testing.assert_array_equal(result_jd,
                                  np.array([True, True]))

    # Test month not in range
    result_march = _month_conditional(test, [3])
    np.testing.assert_array_equal(result_march,
                                  np.array([False, False]))


def test_extract_months():
    time = xr.DataArray(pd.date_range(start='2001-02-18', end='2002-07-12',
                                      freq='1D'), dims=[TIME_STR])
    months = 'mam'  # March-April-May
    desired = xr.concat([
        xr.DataArray(pd.date_range(start='2001-03-01', end='2001-05-31',
                                   freq='1D'), dims=[TIME_STR]),
        xr.DataArray(pd.date_range(start='2002-03-01', end='2002-05-31',
                                   freq='1D'), dims=[TIME_STR])
    ], dim=TIME_STR)
    actual = extract_months(time, months)
    xr.testing.assert_identical(actual, desired)


def test_extract_months_single_month():
    time = xr.DataArray(pd.date_range(start='1678-01-01', end='1678-01-31',
                                      freq='1M'), dims=[TIME_STR])
    months = 1
    desired = time
    actual = extract_months(time, months)
    xr.testing.assert_identical(actual, desired)


@pytest.fixture
def ds_time_encoded_cf():
    time_bounds = np.array([[0, 31], [31, 59], [59, 90]])
    nv = np.array([0, 1])
    time = np.array([15, 46, 74])
    data = np.zeros((3))
    ds = xr.DataArray(data,
                      coords=[time],
                      dims=[TIME_STR],
                      name='a').to_dataset()
    ds[TIME_BOUNDS_STR] = xr.DataArray(time_bounds,
                                       coords=[time, nv],
                                       dims=[TIME_STR, BOUNDS_STR],
                                       name=TIME_BOUNDS_STR)
    units_str = 'days since 2000-01-01 00:00:00'
    cal_str = 'noleap'
    ds[TIME_STR].attrs['units'] = units_str
    ds[TIME_STR].attrs['calendar'] = cal_str
    return ds


def test_ensure_time_avg_has_cf_metadata(ds_time_encoded_cf):
    ds = ds_time_encoded_cf
    time = ds[TIME_STR].values
    time_bounds = ds[TIME_BOUNDS_STR].values
    units_str = ds[TIME_STR].attrs['units']
    cal_str = ds[TIME_STR].attrs['calendar']

    with pytest.raises(KeyError):
        ds[TIME_BOUNDS_STR].attrs['units']
    with pytest.raises(KeyError):
        ds[TIME_BOUNDS_STR].attrs['calendar']

    ds = ensure_time_avg_has_cf_metadata(ds)

    result = ds[TIME_BOUNDS_STR].attrs['units']
    assert result == units_str
    result = ds[TIME_BOUNDS_STR].attrs['calendar']
    assert result == cal_str

    avg_DT_data = np.diff(time_bounds, axis=1).squeeze()
    average_DT_expected = xr.DataArray(avg_DT_data,
                                       coords=[time],
                                       dims=[TIME_STR],
                                       name=TIME_WEIGHTS_STR)
    average_DT_expected[TIME_STR].attrs['units'] = units_str
    average_DT_expected.attrs['units'] = 'days'
    average_DT_expected[TIME_STR].attrs['calendar'] = cal_str
    assert ds[TIME_WEIGHTS_STR].identical(average_DT_expected)

    assert ds[RAW_START_DATE_STR].values == [0]
    assert ds[RAW_START_DATE_STR].attrs['units'] == units_str
    assert ds[RAW_START_DATE_STR].attrs['calendar'] == cal_str

    assert ds[RAW_END_DATE_STR].values == [90]
    assert ds[RAW_END_DATE_STR].attrs['units'] == units_str
    assert ds[RAW_END_DATE_STR].attrs['calendar'] == cal_str


def test_add_uniform_time_weights():
    time = np.array([15, 46, 74])
    data = np.zeros((3))
    ds = xr.DataArray(data,
                      coords=[time],
                      dims=[TIME_STR],
                      name='a').to_dataset()
    units_str = 'days since 2000-01-01 00:00:00'
    cal_str = 'noleap'
    ds[TIME_STR].attrs['units'] = units_str
    ds[TIME_STR].attrs['calendar'] = cal_str

    with pytest.raises(KeyError):
        ds[TIME_WEIGHTS_STR]

    ds = add_uniform_time_weights(ds)
    time_weights_expected = xr.DataArray(
        [1, 1, 1], coords=ds[TIME_STR].coords, name=TIME_WEIGHTS_STR)
    time_weights_expected.attrs['units'] = 'days'
    assert ds[TIME_WEIGHTS_STR].identical(time_weights_expected)


def test_assert_has_data_for_time():
    time_bounds = np.array([[0, 31], [31, 59], [59, 90]])
    nv = np.array([0, 1])
    time = np.array([15, 46, 74])
    data = np.zeros((3))
    var_name = 'a'
    ds = xr.DataArray(data,
                      coords=[time],
                      dims=[TIME_STR],
                      name=var_name).to_dataset()
    ds[TIME_BOUNDS_STR] = xr.DataArray(time_bounds,
                                       coords=[time, nv],
                                       dims=[TIME_STR, BOUNDS_STR],
                                       name=TIME_BOUNDS_STR)
    units_str = 'days since 2000-01-01 00:00:00'
    ds[TIME_STR].attrs['units'] = units_str
    ds = ensure_time_avg_has_cf_metadata(ds)
    ds = set_grid_attrs_as_coords(ds)
    ds = xr.decode_cf(ds)
    da = ds[var_name]

    start_date = np.datetime64('2000-01-01')
    end_date = np.datetime64('2000-03-31')
    _assert_has_data_for_time(da, start_date, end_date)

    start_date_bad = np.datetime64('1999-12-31')
    end_date_bad = np.datetime64('2000-04-01')

    with pytest.raises(AssertionError):
        _assert_has_data_for_time(da, start_date_bad, end_date)

    with pytest.raises(AssertionError):
        _assert_has_data_for_time(da, start_date, end_date_bad)

    with pytest.raises(AssertionError):
        _assert_has_data_for_time(da, start_date_bad, end_date_bad)


def test_assert_matching_time_coord():
    rng = pd.date_range('2000-01-01', '2001-01-01', freq='M')
    arr1 = xr.DataArray(rng, coords=[rng], dims=[TIME_STR])
    arr2 = xr.DataArray(rng, coords=[rng], dims=[TIME_STR])
    assert_matching_time_coord(arr1, arr2)

    arr2 = arr2.sel(**{TIME_STR: slice('2000-03', '2000-05')})
    with pytest.raises(ValueError):
        assert_matching_time_coord(arr1, arr2)


def test_ensure_time_as_dim():
    arr = xr.DataArray([3, 4], coords=[[1, 2]], dims=[TIME_STR])
    arr[TIME_STR].attrs['units'] = 'days since 2000-01-01 00:00:00'
    arr[TIME_STR].attrs['calendar'] = 'standard'
    ds = arr.to_dataset(name='a')
    assert TIME_STR in ds.dims
    assert ds.identical(ensure_time_as_dim(ds))

    scalar_time_in_ds = ds.isel(**{TIME_STR: 0})
    assert TIME_STR not in scalar_time_in_ds.dims
    result = ensure_time_as_dim(scalar_time_in_ds)

    arr = xr.DataArray([3], coords=[[1]], dims=[TIME_STR])
    arr[TIME_STR].attrs['units'] = 'days since 2000-01-01 00:00:00'
    arr[TIME_STR].attrs['calendar'] = 'standard'
    expected = arr.to_dataset(name='a')
    xr.testing.assert_identical(result, expected)


def test_convert_scalar_to_indexable_coord():
    da = xr.DataArray([3, 4], coords=[[1, 2]], dims=['a'], name='b')
    da['a'].attrs['test'] = 'c'
    scalar_coord = da.isel(a=0)['a']
    assert 'a' not in scalar_coord.dims

    indexable_coord = convert_scalar_to_indexable_coord(scalar_coord)
    assert 'a' in indexable_coord.dims

    expected = xr.DataArray([1], coords=[[1]], dims=['a'], name='a')
    expected.attrs['test'] = 'c'
    xr.testing.assert_identical(indexable_coord, expected)


def test_sel_time():
    time_bounds = np.array([[0, 31], [31, 59], [59, 90]])
    nv = np.array([0, 1])
    time = np.array([15, 46, 74])
    data = np.zeros((3))
    var_name = 'a'
    ds = xr.DataArray(data,
                      coords=[time],
                      dims=[TIME_STR],
                      name=var_name).to_dataset()
    ds[TIME_BOUNDS_STR] = xr.DataArray(time_bounds,
                                       coords=[time, nv],
                                       dims=[TIME_STR, BOUNDS_STR],
                                       name=TIME_BOUNDS_STR)
    units_str = 'days since 2000-01-01 00:00:00'
    ds[TIME_STR].attrs['units'] = units_str
    ds = ensure_time_avg_has_cf_metadata(ds)
    ds = set_grid_attrs_as_coords(ds)
    ds = xr.decode_cf(ds)
    da = ds[var_name]

    start_date = np.datetime64('2000-02-01')
    end_date = np.datetime64('2000-03-31')
    result = sel_time(da, start_date, end_date)
    assert result[SUBSET_START_DATE_STR].values == start_date
    assert result[SUBSET_END_DATE_STR].values == end_date


def test_yearly_average_no_mask():
    times = pd.to_datetime(['2000-06-01', '2000-06-15',
                            '2001-07-04', '2001-10-01', '2001-12-31',
                            '2004-01-01'])
    arr = xr.DataArray(np.random.random((len(times),)),
                       dims=[TIME_STR], coords={TIME_STR: times})
    dt = arr.copy(deep=True)
    dt.values = np.random.random((len(times),))

    actual = yearly_average(arr, dt)

    yr2000 = (arr[0]*dt[0] + arr[1]*dt[1]) / (dt[0] + dt[1])
    yr2001 = ((arr[2]*dt[2] + arr[3]*dt[3] + arr[4]*dt[4]) /
              (dt[2] + dt[3] + dt[4]))
    yr2004 = arr[-1]
    yrs_coord = [2000, 2001, 2004]
    yr_avgs = np.array([yr2000, yr2001, yr2004])
    desired = xr.DataArray(yr_avgs, dims=['year'], coords={'year': yrs_coord})
    xr.testing.assert_allclose(actual, desired)


def test_yearly_average_masked_data():
    times = pd.to_datetime(['2000-06-01', '2000-06-15',
                            '2001-07-04', '2001-10-01', '2001-12-31',
                            '2004-01-01'])
    arr = xr.DataArray(np.random.random((len(times),)),
                       dims=[TIME_STR], coords={TIME_STR: times})
    arr[0] = -999
    arr = arr.where(arr != -999)
    dt = arr.copy(deep=True)
    dt.values = np.random.random((len(times),))

    actual = yearly_average(arr, dt)

    yr2000 = arr[1]
    yr2001 = ((arr[2]*dt[2] + arr[3]*dt[3] + arr[4]*dt[4]) /
              (dt[2] + dt[3] + dt[4]))
    yr2004 = arr[-1]
    yrs_coord = [2000, 2001, 2004]
    yr_avgs = np.array([yr2000, yr2001, yr2004])
    desired = xr.DataArray(yr_avgs, dims=['year'], coords={'year': yrs_coord})
    xr.testing.assert_allclose(actual, desired)


def test_average_time_bounds(ds_time_encoded_cf):
    ds = ds_time_encoded_cf
    actual = average_time_bounds(ds)[TIME_STR]

    desired_values = ds[TIME_BOUNDS_STR].mean(dim=BOUNDS_STR).values
    desired = xr.DataArray(desired_values, dims=[TIME_STR],
                           coords={TIME_STR: desired_values}, name=TIME_STR)

    xr.testing.assert_identical(actual, desired)
