#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:28:10 2024
@author: ekaterinasivokon
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
from itertools import islice
import numpy as np
import math

DIRECTORY = "/Users/ekaterinasivokon/Desktop/Harvard Cohen Lab/fluorescence-microscope-spectra-analysis/Spectra_Data"
DIRECTORY_EXC = "/Users/ekaterinasivokon/Desktop/Harvard Cohen Lab/fluorescence-microscope-spectra-analysis/excel_spectra_data"
# =============================================================================
# # Dichroics Spectra 350 - 750 nm
# dichr = "5323-ascii.txt" #T612lpxr
# # Emission Filters Spectra 350 - 750 nm
# em = "5085-ascii.txt" #ET640_30x
# # Excitation Filters Spectra 350 - 750 nm
# exc = "5750-ascii.txt" #ET590_33m
# =============================================================================

def read_txt_files(DIRECTORY):  
    '''Reads numerical data from text files in a specified directory,
       creates dictionaries where keys are values from the 1st column (wavelength)
       and values are values from the 2nd column. 
       Returns 3 dictionaries for data about dichroic, em & exc filters.
    '''
    dict_dichr = {}
    dict_em = {}
    dict_exc = {}

    for filename in os.listdir(DIRECTORY):
        if filename.endswith(".txt"):
            with open(os.path.join(DIRECTORY, filename), 'r') as file:
                data = file.readlines()
                data_dict = {float(line.split()[0]): float(line.split()[1]) for line in data}
                
                if filename == dichr:
                    dict_dichr = data_dict
                elif filename == em:
                    dict_em = data_dict
                elif filename == exc:
                    dict_exc = data_dict

    return dict_dichr, dict_em, dict_exc

def create_dictionary_from_string(input_str):
    dict_from_string = {}
    lines = input_str.strip().split('\n')
    for line in lines:
        key, value = line.split(', ')
        dict_from_string[float(key)] = float(value)
    
    return  dict_from_string

def normalize_spectra(dictionary):
    
    # Filter the dictionary in case it has NaN values
    # The normalization calculation is performed only on non-NaN values
    valid_values = [v for v in dictionary.values() if not math.isnan(v)]
    
    if not valid_values:
        return {}  # Return an empty dictionary if all values are NaN
    
    x_min = min(valid_values)
    x_max = max(valid_values)
    
    normalized_dict = {k: (v - x_min) / (x_max - x_min) if not math.isnan(v) else math.nan for k, v in dictionary.items()}
    
    return normalized_dict

def plot_dicts(*dicts):
    '''
    Plots graphs for all input dictionaries and a graph for the overlapping part.
    Creates a new dictionary with just the overlapping x and y values.
    Returns a dictionary containing the overlapping x and y values.
    '''
    legend_labels = []
    # Plot all graphs
    for d in dicts:
        x_values = list(d.keys())
        y_values = list(d.values())
        plt.plot(x_values, y_values, label=f'Dict {len(legend_labels) + 1}')
        legend_labels.append(f'{len(legend_labels) + 1}')
    
    plt.title('All Graphs')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Transmission %')
    
    # Display legend
    plt.legend(legend_labels)
    
    plt.show()
    
    return 

def cutoff_dicts(*dicts, minwavelength, maxwavelength):
    '''Takes in several dictionaries and two values.
        returns dictionaries with the same values, but with keys only in the
        range of minwavelength and maxwavelength. For example:
        dict1 = {1: 10, 2: 20, 3: 30, 4: 120}
        dict2 = {1: 5, 2: 15, 3: 25, 4: 108}
        minwavelength = 2
        maxwavelength = 3
        Returns:
        newdict1 = {2: 20, 3: 30}
        newdict1 = {2: 20, 3: 30}
    '''
    new_dicts = ()
   
    for d in dicts:
       new_dict = {k: v for k, v in d.items() if minwavelength <= k <= maxwavelength}
       new_dicts += (new_dict,)
   
    return new_dicts

def read_excel_to_dicts(filepath):
    data = pd.read_excel(filepath)
    dict1, dict2, dict3 = {}, {}, {}  
    for index, row in data.iterrows():
       dict1[row['Wavelength (nm)']] = row[data.columns[1]]
       dict2[row['Wavelength (nm)']] = row[data.columns[2]]
       dict3[row['Wavelength (nm)']] = row[data.columns[3]]
   
    return dict1, dict2, dict3

def main():
    
    print("Specify filenames for dichroic&filters (dichr, em, exc). \n")
    print("Specify amber_led_intensity. \n")
    print("Specify cutoff wavelengths. \n")
    minwavelength = 500
    maxwavelength = 700
    
    # Read dichr, em and exc data
    filename = "JF608 set.xlsx"
    filepath = f"{DIRECTORY_EXC}/{filename}"
    dict_exc, dict_dichr, dict_em = read_excel_to_dicts(filepath)

    # Read led intensity, flem and flex data
    filename = "led_and_fluorophores.xlsx"
    filepath = f"{DIRECTORY_EXC}/{filename}"
    dict_led_intensity, dict_flex, dict_flem = read_excel_to_dicts(filepath)
         
    # Normalize all data
    dict_dichr = normalize_spectra(dict_dichr)
    dict_exc = normalize_spectra(dict_exc)
    dict_em = normalize_spectra(dict_em)
    dict_led_intensity = normalize_spectra(dict_led_intensity)
    dict_flem = normalize_spectra(dict_flem)
    dict_flex = normalize_spectra(dict_flex)
    
    # Cutoff irrelevant wavelengths
    cut_dict_dichr, cut_dict_led_intensity, cut_dict_em, cut_dict_exc, cut_dict_flem, cut_dict_flex = cutoff_dicts(dict_dichr, dict_led_intensity, dict_em, dict_exc, dict_flem, dict_flex, minwavelength=minwavelength, maxwavelength=maxwavelength)

    # Plot
    plotted_dicts = plot_dicts(cut_dict_dichr, cut_dict_em, cut_dict_exc, cut_dict_flem, cut_dict_flex)

if __name__ == "__main__":
    main()
