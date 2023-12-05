# -*- coding: utf-8 -*-
"""
Scans
=====
"""


import numpy as np
from pyscan.general.samelength import same_length
from pyscan.general.itemattribute import ItemAttribute


class MetaScan(ItemAttribute):
    '''
    Meta class for different scan types. Inherits from `.ItemAttribute`.
    '''

    def iterate(self, index, devices):
        '''
        A function to be implemented by inheriting Scan classes
        '''
        pass

    def check_same_length(self):
        '''A function to be implemented by inheriting Scan classes'''
        pass


class PropertyScan(MetaScan):
    '''
    Class for iterating a property of an intruments inside an
    experimental loop. Inherits from `pyscan.measurement.scans.MetaScan`.

    Parameters
    ----------
    input_dict : dict{string:array}
        key:value pairs of device name strings and arrays of values representing the new `prop`
        values you want to set for each device.
    prop : str
        String that indicates the property of the device(s) to be changed
    dt : float
        Wait time in seconds after changing a single property value. Used by sweep classes, defaults to 0.
    '''

    def __init__(self, input_dict, prop, dt=0):
        '''
        Constructor method
        '''
        self.prop = prop
        self.scan_dict = {}
        self.input_dict = input_dict
        for device, array in input_dict.items():
            self.scan_dict['{}_{}'.format(device, prop)] = array

        self.device_names = list(input_dict.keys())

        self.property = prop
        self.dt = dt
        self.check_same_length()
        self.i = 0

    def iterate(self, index, devices):
        '''
        Changes `prop` of the listed `devices` to the value of `PropertyScan`'s input_dict at the given `index`.

        :param index: The index of the data array
        :param devices: ItemAttribute instance of experimental devices
        :type devices: ItemAttribute
        '''
        for dev in self.device_names:
            try:
                devices[dev][self.prop] = self.scan_dict[dev + '_' + self.prop][index]
            except:
                continue

    def check_same_length(self):
        '''Check that the input_dict has values that are arrays of the same length
        '''

        if len(list(self.scan_dict.keys())) > 0:
            if same_length(list(self.scan_dict.values())):
                self.n = len(list(self.scan_dict.values())[0])  # self.n is the length of the input_dict arrays.
                self.nrange = range(self.n)
            else:
                assert 0, 'Values are not of the same length'
        else:
            self.n = 1  # n=1 is required to allow the run() function to proceed atleast once.
            self.nrange = range(1)


class FunctionScan(MetaScan):
    '''Class for iterating a function with input values inside an
    experimental loop. Inherits from `pyscan.measurement.scans.MetaScan`.

    Parameters
    ----------
    function : func
        Function to be applied during each iteration. Must take a single argument representing one 
        item in the `values` array. The function's return value is not used.
    values : list
        An array of values to run the function on.
    dt: float
        Wait time in seconds after running function once. Used by sweep classes, defaults to 0.
    '''

    def __init__(self, function, values, dt=0):

        self.scan_dict = {}

        self.scan_dict[function.__name__] = values

        self.function = function
        self.dt = dt
        self.i = 0
        self.n = len(values)

    def iterate(self, index, devices):
        '''
        Executes function(self.values[index]). Used by a Sweep class's run() function.

        Parameters
        ----------
        index : 
            The index of the `values` array to run the function on. The `FunctionScan`'s `values` at 
            the given `index` will be the function input.
        devices: 
            Not used
        '''
        self.function(self.scan_dict[self.function.__name__][index])

    def check_same_length(self):
        pass


class RepeatScan(MetaScan):
    '''Class for repeating inner loops.

    Parameters
    ----------
    n_repeat : int
        Number of times to repeat inner loops.
    dt : float
        Wait time in seconds after repeat. Used by sweep classes, defaults to 0.
    '''
    def __init__(self, nrepeat, dt=0):
        '''Constructor method
        '''
        self.scan_dict = {}
        if nrepeat is not np.inf:
            self.scan_dict['repeat'] = list(range(nrepeat))

        else:
            self.scan_dict['repeat'] = []  # represents infinity

        self.device_names = ['repeat']
        self.dt = dt

        if nrepeat is not np.inf:
            self.n = nrepeat
            self.nrange = range(self.n)

        else:
            self.n = 0  # represents infinity?
            self.nrange = 0

        self.i = 0

    def iterate(self, index, devices):
        '''Iterates repeat loop
        '''
        if self.n is np.inf:  # bug? when would self.n be np.inf?
            self.scan_dict['repeat'].append(self.n + 1)
            self.nrange += 1
            self.n += 1
        else:
            pass  # ? if not np.inf then the loop doesn't run?

    def check_same_length(self):
        '''
        Not used
        '''
        return 1


class AverageScan(MetaScan):
    '''Class for averaging inner loops.

    Parameters
    ----------
    n_average : int 
        Number of times to average data from inner loops
    dt : float
        Wait time in seconds after each measurement. Used by Sweep classes, defaults to 0.
    '''

    def __init__(self, n_average, dt=0):
        self.scan_dict = {}
        self.n = n_average
        self.nrange = range(self.n) 
        self.scan_dict['average'] = list(self.nrange)
        self.device_names = ['average']
        self.i = 0
        self.dt = dt

    def iterate(self, index, devices):
        '''
        Place holder, does nothing
        '''
        pass

    def check_same_length(self):
        ''' 
        Not used
        ''' 
        return 1
