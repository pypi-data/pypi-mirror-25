# encoding: utf-8
from __future__ import print_function, division, absolute_import

# ---> 1.) load required packages (optional)
import os.path
import pandas


def convert(raw_file, output_file):

    # ---> 2.) read file

    if not os.path.isfile(raw_file):
        raise ValueError('Error: Input File does not exist.')

    raw_data = pandas.read_csv(raw_file, sep='\t', encoding="latin-1")
    colNames = ("Date Time", "Water Level", "Average Flow Velocity", "Flow", "Temperature",
                "Surface Flow Velocity", "Distance", "Distance Reading Count", "Surcharge Level",
                "Peak to Mean Ratio", "Number of Samples", "Battery Voltage")
    raw_data.columns = colNames

    # ---> 3.) test properties

    if len(raw_data.columns) != 12:
        raise ValueError('Error: Input File has wrong number of columns.')

    # ---> 4.) add additional information (optional)

    # Define coordinate
    xcoor = 682558
    ycoor = 239404
    zcoor = ""

    # ---> 5.) reformat data

    time = pandas.to_datetime(raw_data['Date Time'], format="%d.%m.%Y %H:%M")
    raw_data['Date Time'] = time.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    data = pandas.melt(raw_data, id_vars=['Date Time'], value_vars=list(raw_data.columns[1:12]))

    data.columns = ['timestamp', 'parameter', 'value']

    data = data.dropna()

    data['x'] = xcoor
    data['y'] = ycoor
    data['z'] = zcoor

    # ---> 6.) write file

    data.to_csv(output_file, sep=";", index=False)
