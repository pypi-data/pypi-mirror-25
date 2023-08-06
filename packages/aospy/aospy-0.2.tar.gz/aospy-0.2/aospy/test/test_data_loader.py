#!/usr/bin/env python
"""Test suite for aospy.data_loader module."""
from datetime import datetime
import os
import unittest

import numpy as np
import xarray as xr

from aospy.data_loader import (DataLoader, DictDataLoader, GFDLDataLoader,
                               NestedDictDataLoader, grid_attrs_to_aospy_names,
                               set_grid_attrs_as_coords, _sel_var,
                               _prep_time_data,
                               _preprocess_and_rename_grid_attrs)
from aospy.internal_names import (LAT_STR, LON_STR, TIME_STR, TIME_BOUNDS_STR,
                                  BOUNDS_STR, SFC_AREA_STR, ETA_STR, PHALF_STR,
                                  TIME_WEIGHTS_STR, GRID_ATTRS)
from aospy.utils import io
from .data.objects.examples import (condensation_rain, convection_rain, precip,
                                    example_run, ROOT_PATH)


class AospyDataLoaderTestCase(unittest.TestCase):
    def setUp(self):
        self.DataLoader = DataLoader()
        self.generate_file_set_args = dict(
            var=condensation_rain, start_date=datetime(2000, 1, 1),
            end_date=datetime(2002, 12, 31), domain='atmos',
            intvl_in='monthly', dtype_in_vert='sigma', dtype_in_time='ts',
            intvl_out=None)
        time_bounds = np.array([[0, 31], [31, 59], [59, 90]])
        bounds = np.array([0, 1])
        time = np.array([15, 46, 74])
        data = np.zeros((3, 1, 1))
        lat = [0]
        lon = [0]
        self.ALT_LAT_STR = 'LATITUDE'
        self.var_name = 'a'
        ds = xr.DataArray(data,
                          coords=[time, lat, lon],
                          dims=[TIME_STR, self.ALT_LAT_STR, LON_STR],
                          name=self.var_name).to_dataset()
        ds[TIME_BOUNDS_STR] = xr.DataArray(time_bounds,
                                           coords=[time, bounds],
                                           dims=[TIME_STR, BOUNDS_STR],
                                           name=TIME_BOUNDS_STR)
        units_str = 'days since 2000-01-01 00:00:00'
        ds[TIME_STR].attrs['units'] = units_str
        ds[TIME_BOUNDS_STR].attrs['units'] = units_str
        self.ds = ds

        inst_time = np.array([3, 6, 9])
        inst_units_str = 'hours since 2000-01-01 00:00:00'
        inst_ds = ds.copy()
        inst_ds.drop(TIME_BOUNDS_STR)
        inst_ds[TIME_STR].values = inst_time
        inst_ds[TIME_STR].attrs['units'] = inst_units_str
        self.inst_ds = inst_ds

    def tearDown(self):
        pass


class TestDataLoader(AospyDataLoaderTestCase):
    def test_rename_grid_attrs_ds(self):
        assert LAT_STR not in self.ds
        assert self.ALT_LAT_STR in self.ds
        ds = grid_attrs_to_aospy_names(self.ds)
        assert LAT_STR in ds

    def test_rename_grid_attrs_dim_no_coord(self):
        bounds_dim = 'nv'
        assert bounds_dim not in self.ds
        assert bounds_dim in GRID_ATTRS[BOUNDS_STR]
        # Create DataArray with all dims lacking coords
        values = self.ds[self.var_name].values
        arr = xr.DataArray(values, name='dummy')
        # Insert name to be replaced (its physical meaning doesn't matter here)
        ds = arr.rename({'dim_0': bounds_dim}).to_dataset()
        assert not ds[bounds_dim].coords
        result = grid_attrs_to_aospy_names(ds)
        assert result[BOUNDS_STR].coords

    def test_rename_grid_attrs_skip_scalar_dim(self):
        phalf_dim = 'phalf'
        assert phalf_dim not in self.ds
        assert phalf_dim in GRID_ATTRS[PHALF_STR]
        ds = self.ds.copy()
        ds[phalf_dim] = 4
        ds = ds.set_coords(phalf_dim)
        result = grid_attrs_to_aospy_names(ds)
        xr.testing.assert_identical(result[phalf_dim], ds[phalf_dim])

    def test_rename_grid_attrs_copy_attrs(self):
        orig_attrs = {'dummy_key': 'dummy_val'}
        ds_orig = self.ds.copy()
        ds_orig[self.ALT_LAT_STR].attrs = orig_attrs
        ds = grid_attrs_to_aospy_names(ds_orig)
        self.assertEqual(ds[LAT_STR].attrs, orig_attrs)

    def test_set_grid_attrs_as_coords_all(self):
        ds = grid_attrs_to_aospy_names(self.ds)
        sfc_area = ds[self.var_name].isel(**{TIME_STR: 0}).drop(TIME_STR)
        ds[SFC_AREA_STR] = sfc_area

        assert SFC_AREA_STR not in ds.coords

        ds = set_grid_attrs_as_coords(ds)
        assert SFC_AREA_STR in ds.coords
        assert TIME_BOUNDS_STR in ds.coords

    def test_set_grid_attrs_as_coords_no_times(self):
        ds = grid_attrs_to_aospy_names(self.ds)
        sfc_area = ds[self.var_name].isel(**{TIME_STR: 0}).drop(TIME_STR)
        ds[SFC_AREA_STR] = sfc_area

        assert SFC_AREA_STR not in ds.coords

        ds = set_grid_attrs_as_coords(ds, set_time_vars=False)
        assert SFC_AREA_STR in ds.coords
        assert TIME_BOUNDS_STR not in ds.coords

    def test_sel_var(self):
        time = np.array([0, 31, 59]) + 15
        data = np.zeros((3))
        ds = xr.DataArray(data,
                          coords=[time],
                          dims=[TIME_STR],
                          name=convection_rain.name).to_dataset()
        condensation_rain_alt_name, = condensation_rain.alt_names
        ds[condensation_rain_alt_name] = xr.DataArray(data, coords=[ds.time])
        result = _sel_var(ds, convection_rain)
        self.assertEqual(result.name, convection_rain.name)

        result = _sel_var(ds, condensation_rain)
        self.assertEqual(result.name, condensation_rain.name)

        with self.assertRaises(LookupError):
            _sel_var(ds, precip)

    def test_maybe_apply_time_shift(self):
        ds = xr.decode_cf(self.ds)
        da = ds[self.var_name]

        result = self.DataLoader._maybe_apply_time_shift(
            da.copy(), **self.generate_file_set_args)[TIME_STR]
        assert result.identical(da[TIME_STR])

        offset = self.DataLoader._maybe_apply_time_shift(
            da.copy(), {'days': 1}, **self.generate_file_set_args)
        result = offset[TIME_STR]

        expected = da[TIME_STR] + np.timedelta64(1, 'D')
        expected[TIME_STR] = expected

        assert result.identical(expected)

    def test_generate_file_set(self):
        with self.assertRaises(NotImplementedError):
            self.DataLoader._generate_file_set()

    def test_prep_time_data(self):
        assert (TIME_WEIGHTS_STR not in self.inst_ds)
        ds, min_year, max_year = _prep_time_data(self.inst_ds)
        assert (TIME_WEIGHTS_STR in ds)
        self.assertEqual(min_year, 2000)
        self.assertEqual(max_year, 2000)

    def test_preprocess_and_rename_grid_attrs(self):
        def preprocess_func(ds, **kwargs):
            # Corrupt a grid attribute name so that we test
            # that grid_attrs_to_aospy_names is still called
            # after
            ds = ds.rename({LON_STR: 'LONGITUDE'})
            ds.attrs['a'] = 'b'
            return ds

        assert LAT_STR not in self.ds
        assert self.ALT_LAT_STR in self.ds
        assert LON_STR in self.ds

        expected = self.ds.rename({self.ALT_LAT_STR: LAT_STR})
        expected.attrs['a'] = 'b'
        result = _preprocess_and_rename_grid_attrs(preprocess_func)(self.ds)
        xr.testing.assert_identical(result, expected)


class TestDictDataLoader(TestDataLoader):
    def setUp(self):
        super(TestDictDataLoader, self).setUp()
        file_map = {'monthly': ['a.nc']}
        self.DataLoader = DictDataLoader(file_map)

    def test_generate_file_set(self):
        result = self.DataLoader._generate_file_set(
            **self.generate_file_set_args)
        expected = ['a.nc']
        self.assertEqual(result, expected)

        with self.assertRaises(KeyError):
            self.generate_file_set_args['intvl_in'] = 'daily'
            result = self.DataLoader._generate_file_set(
                **self.generate_file_set_args)


class TestNestedDictDataLoader(TestDataLoader):
    def setUp(self):
        super(TestNestedDictDataLoader, self).setUp()
        file_map = {'monthly': {'condensation_rain': ['a.nc']}}
        self.DataLoader = NestedDictDataLoader(file_map)

    def test_generate_file_set(self):
        result = self.DataLoader._generate_file_set(
            **self.generate_file_set_args)
        expected = ['a.nc']
        self.assertEqual(result, expected)

        with self.assertRaises(KeyError):
            self.generate_file_set_args['var'] = convection_rain
            result = self.DataLoader._generate_file_set(
                **self.generate_file_set_args)


class TestGFDLDataLoader(TestDataLoader):
    def setUp(self):
        super(TestGFDLDataLoader, self).setUp()
        self.DataLoader = GFDLDataLoader(
            data_direc=os.path.join('.', 'test'),
            data_dur=6,
            data_start_date=datetime(2000, 1, 1),
            data_end_date=datetime(2012, 12, 31)
        )

    def test_overriding_constructor(self):
        new = GFDLDataLoader(self.DataLoader,
                             data_direc=os.path.join('.', 'a'))
        self.assertEqual(new.data_direc, os.path.join('.', 'a'))
        self.assertEqual(new.data_dur, self.DataLoader.data_dur)
        self.assertEqual(new.data_start_date, self.DataLoader.data_start_date)
        self.assertEqual(new.data_end_date, self.DataLoader.data_end_date)
        self.assertEqual(new.preprocess_func,
                         self.DataLoader.preprocess_func)

        new = GFDLDataLoader(self.DataLoader, data_dur=8)
        self.assertEqual(new.data_dur, 8)

        new = GFDLDataLoader(self.DataLoader,
                             data_start_date=datetime(2001, 1, 1))
        self.assertEqual(new.data_start_date, datetime(2001, 1, 1))

        new = GFDLDataLoader(self.DataLoader,
                             data_end_date=datetime(2003, 12, 31))
        self.assertEqual(new.data_end_date, datetime(2003, 12, 31))

        new = GFDLDataLoader(self.DataLoader,
                             preprocess_func=lambda ds: ds)
        xr.testing.assert_identical(new.preprocess_func(self.ds), self.ds)

    def test_maybe_apply_time_offset_inst(self):
        inst_ds = xr.decode_cf(self.inst_ds)
        self.generate_file_set_args['dtype_in_time'] = 'inst'
        self.generate_file_set_args['intvl_in'] = '3hr'
        da = inst_ds[self.var_name]
        result = self.DataLoader._maybe_apply_time_shift(
            da.copy(), **self.generate_file_set_args)[TIME_STR]

        expected = da[TIME_STR] + np.timedelta64(-3, 'h')
        expected[TIME_STR] = expected
        assert result.identical(expected)

        self.generate_file_set_args['intvl_in'] = 'daily'
        da = inst_ds[self.var_name]
        result = self.DataLoader._maybe_apply_time_shift(
            da.copy(), **self.generate_file_set_args)[TIME_STR]

        expected = da[TIME_STR]
        expected[TIME_STR] = expected
        assert result.identical(expected)

    def test_maybe_apply_time_offset_ts(self):
        ds = xr.decode_cf(self.ds)
        da = ds[self.var_name]

        result = self.DataLoader._maybe_apply_time_shift(
            da.copy(), **self.generate_file_set_args)[TIME_STR]
        assert result.identical(da[TIME_STR])

    def test_generate_file_set(self):
        with self.assertRaises(IOError):
            self.DataLoader._generate_file_set(**self.generate_file_set_args)

    def test_input_data_paths_gfdl(self):
        expected = [os.path.join('.', 'test', 'atmos', 'ts', 'monthly', '6yr',
                                 'atmos.200601-201112.temp.nc')]
        result = self.DataLoader._input_data_paths_gfdl(
            'temp', datetime(2010, 1, 1), datetime(2010, 12, 31), 'atmos',
            'monthly', 'pressure', 'ts', None)
        self.assertEqual(result, expected)

        expected = [os.path.join('.', 'test', 'atmos_daily', 'ts', 'daily',
                                 '6yr',
                                 'atmos_daily.20060101-20111231.temp.nc')]
        result = self.DataLoader._input_data_paths_gfdl(
            'temp', datetime(2010, 1, 1), datetime(2010, 12, 31), 'atmos',
            'daily', 'pressure', 'ts', None)
        self.assertEqual(result, expected)

        expected = [os.path.join('.', 'test', 'atmos_level', 'ts', 'monthly',
                                 '6yr', 'atmos_level.200601-201112.temp.nc')]
        result = self.DataLoader._input_data_paths_gfdl(
            'temp', datetime(2010, 1, 1), datetime(2010, 12, 31), 'atmos',
            'monthly', ETA_STR, 'ts', None)
        self.assertEqual(result, expected)

        expected = [os.path.join('.', 'test', 'atmos', 'ts', 'monthly',
                                 '6yr', 'atmos.200601-201112.ps.nc')]
        result = self.DataLoader._input_data_paths_gfdl(
            'ps', datetime(2010, 1, 1), datetime(2010, 12, 31), 'atmos',
            'monthly', ETA_STR, 'ts', None)
        self.assertEqual(result, expected)

        expected = [os.path.join('.', 'test', 'atmos_inst', 'ts', 'monthly',
                                 '6yr', 'atmos_inst.200601-201112.temp.nc')]
        result = self.DataLoader._input_data_paths_gfdl(
            'temp', datetime(2010, 1, 1), datetime(2010, 12, 31), 'atmos',
            'monthly', 'pressure', 'inst', None)
        self.assertEqual(result, expected)

        expected = [os.path.join('.', 'test', 'atmos', 'av', 'monthly_6yr',
                                 'atmos.2006-2011.jja.nc')]
        result = self.DataLoader._input_data_paths_gfdl(
            'temp', datetime(2010, 1, 1), datetime(2010, 12, 31), 'atmos',
            'monthly', 'pressure', 'av', 'jja')
        self.assertEqual(result, expected)

    def test_data_name_gfdl_annual(self):
        for data_type in ['ts', 'inst']:
            expected = 'atmos.2010.temp.nc'
            result = io.data_name_gfdl('temp', 'atmos', data_type,
                                       'annual', 2010, None, 2000, 1)
            self.assertEqual(result, expected)

            expected = 'atmos.2006-2011.temp.nc'
            result = io.data_name_gfdl('temp', 'atmos', data_type,
                                       'annual', 2010, None, 2000, 6)
            self.assertEqual(result, expected)

        for intvl_type in ['annual', 'ann']:
            expected = 'atmos.2010.ann.nc'
            result = io.data_name_gfdl('temp', 'atmos', 'av',
                                       intvl_type, 2010, None, 2000, 1)
            self.assertEqual(result, expected)

            expected = 'atmos.2006-2011.ann.nc'
            result = io.data_name_gfdl('temp', 'atmos', 'av',
                                       intvl_type, 2010, None, 2000, 6)
            self.assertEqual(result, expected)

        expected = 'atmos.2006-2011.01-12.nc'
        result = io.data_name_gfdl('temp', 'atmos', 'av_ts',
                                   'annual', 2010, None, 2000, 6)
        self.assertEqual(result, expected)

    def test_data_name_gfdl_monthly(self):
        for data_type in ['ts', 'inst']:
            expected = 'atmos.200601-201112.temp.nc'
            result = io.data_name_gfdl('temp', 'atmos', data_type,
                                       'monthly', 2010, 'jja', 2000, 6)
            self.assertEqual(result, expected)

        for intvl_type in ['monthly', 'mon']:
            expected = 'atmos.2010.jja.nc'
            result = io.data_name_gfdl('temp', 'atmos', 'av',
                                       intvl_type, 2010, 'jja', 2000, 1)
            self.assertEqual(result, expected)

            expected = 'atmos.2006-2011.jja.nc'
            result = io.data_name_gfdl('temp', 'atmos', 'av',
                                       intvl_type, 2010, 'jja', 2000, 6)
            self.assertEqual(result, expected)

        expected = 'atmos.2006-2011.01-12.nc'
        result = io.data_name_gfdl('temp', 'atmos', 'av_ts',
                                   'monthly', 2010, 'jja', 2000, 6)
        self.assertEqual(result, expected)

    def test_data_name_gfdl_daily(self):
        for data_type in ['ts', 'inst']:
            expected = 'atmos.20060101-20111231.temp.nc'
            result = io.data_name_gfdl('temp', 'atmos', data_type,
                                       'daily', 2010, None, 2000, 6)
            self.assertEqual(result, expected)

        with self.assertRaises(NameError):
            io.data_name_gfdl('temp', 'atmos', 'av',
                              'daily', 2010, None, 2000, 6)

        expected = 'atmos.2006-2011.01-12.nc'
        result = io.data_name_gfdl('temp', 'atmos', 'av_ts',
                                   'daily', 2010, None, 2000, 6)
        self.assertEqual(result, expected)

    def test_data_name_gfdl_hr(self):
        for data_type in ['ts', 'inst']:
            expected = 'atmos.2006010100-2011123123.temp.nc'
            result = io.data_name_gfdl('temp', 'atmos', data_type,
                                       '3hr', 2010, None, 2000, 6)
            self.assertEqual(result, expected)

        with self.assertRaises(NameError):
            io.data_name_gfdl('temp', 'atmos', 'av',
                              '3hr', 2010, None, 2000, 6)

        expected = 'atmos.2006-2011.01-12.nc'
        result = io.data_name_gfdl('temp', 'atmos', 'av_ts',
                                   '3hr', 2010, None, 2000, 6)
        self.assertEqual(result, expected)

    def test_data_name_gfdl_seasonal(self):
        for data_type in ['ts', 'inst']:
            with self.assertRaises(NameError):
                io.data_name_gfdl('temp', 'atmos', data_type,
                                  'seasonal', 2010, None, 2000, 6)

        for intvl_type in ['seasonal', 'seas']:
            expected = 'atmos.2010.JJA.nc'
            result = io.data_name_gfdl('temp', 'atmos', 'av',
                                       intvl_type, 2010, 'jja', 2000, 1)
            self.assertEqual(result, expected)

            expected = 'atmos.2006-2011.JJA.nc'
            result = io.data_name_gfdl('temp', 'atmos', 'av',
                                       intvl_type, 2010, 'jja', 2000, 6)
            self.assertEqual(result, expected)

        expected = 'atmos.2006-2011.01-12.nc'
        result = io.data_name_gfdl('temp', 'atmos', 'av_ts',
                                   'seasonal', 2010, None, 2000, 6)
        self.assertEqual(result, expected)


class LoadVariableTestCase(unittest.TestCase):
    def setUp(self):
        self.data_loader = example_run.data_loader

    def tearDown(self):
        pass

    def test_load_variable(self):
        result = self.data_loader.load_variable(
            condensation_rain, datetime(5, 1, 1), datetime(5, 12, 31),
            intvl_in='monthly')
        filepath = os.path.join(os.path.split(ROOT_PATH)[0], 'netcdf',
                                '00050101.precip_monthly.nc')
        expected = xr.open_dataset(filepath)['condensation_rain']
        np.testing.assert_array_equal(result.values, expected.values)

    def test_load_variable_non_0001_refdate(self):
        def preprocess(ds, **kwargs):
            # This function converts our testing data (encoded with a units
            # attribute with a reference data of 0001-01-01) to one
            # with a reference data of 0004-01-01 (to do so we also need
            # to offset the raw time values by three years).
            three_yrs = 1095.
            ds['time'] = ds['time'] - three_yrs
            ds['time'].attrs['units'] = 'days since 0004-01-01 00:00:00'
            ds['time_bounds'] = ds['time_bounds'] - three_yrs
            ds['time_bounds'].attrs['units'] = 'days since 0004-01-01 00:00:00'
            return ds

        self.data_loader.preprocess_func = preprocess

        for year in [4, 5, 6]:
            result = self.data_loader.load_variable(
                condensation_rain, datetime(year, 1, 1),
                datetime(year, 12, 31),
                intvl_in='monthly')
            filepath = os.path.join(os.path.split(ROOT_PATH)[0], 'netcdf',
                                    '000{}0101.precip_monthly.nc'.format(year))
            expected = xr.open_dataset(filepath)['condensation_rain']
            np.testing.assert_allclose(result.values, expected.values)

    def test_load_variable_preprocess(self):
        def preprocess(ds, **kwargs):
            if kwargs['start_date'] == datetime(5, 1, 1):
                ds['condensation_rain'] = 10. * ds['condensation_rain']
            return ds

        self.data_loader.preprocess_func = preprocess

        result = self.data_loader.load_variable(
            condensation_rain, datetime(5, 1, 1), datetime(5, 12, 31),
            intvl_in='monthly')
        filepath = os.path.join(os.path.split(ROOT_PATH)[0], 'netcdf',
                                '00050101.precip_monthly.nc')
        expected = 10. * xr.open_dataset(filepath)['condensation_rain']
        np.testing.assert_allclose(result.values, expected.values)

        result = self.data_loader.load_variable(
            condensation_rain, datetime(4, 1, 1), datetime(4, 12, 31),
            intvl_in='monthly')
        filepath = os.path.join(os.path.split(ROOT_PATH)[0], 'netcdf',
                                '00040101.precip_monthly.nc')
        expected = xr.open_dataset(filepath)['condensation_rain']
        np.testing.assert_allclose(result.values, expected.values)

    def test_load_variable_mask_and_scale(self):
        def convert_all_to_missing_val(ds, **kwargs):
            ds['condensation_rain'] = 0. * ds['condensation_rain'] + 1.0e20
            ds['condensation_rain'].attrs['_FillValue'] = 1.0e20
            return ds

        self.data_loader.preprocess_func = convert_all_to_missing_val

        data = self.data_loader.load_variable(
            condensation_rain, datetime(5, 1, 1),
            datetime(5, 12, 31),
            intvl_in='monthly')

        num_non_missing = np.isfinite(data).sum().item()
        expected_num_non_missing = 0
        self.assertEqual(num_non_missing, expected_num_non_missing)


if __name__ == '__main__':
    unittest.main()
