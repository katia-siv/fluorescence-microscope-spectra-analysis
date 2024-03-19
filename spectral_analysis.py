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
from scipy.integrate import simps

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

def plot_dicts(dicts, names):
    '''
    A list of names is passed along with the dictionaries. 
    Plots graphs for all input dictionaries with specified names.
    '''
    # Plot all graphs
    for d, name in zip(dicts, names):
        x_values = list(d.keys())
        y_values = list(d.values())
        plt.plot(x_values, y_values, label=name)
    
    plt.title('All Graphs')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Transmission %')
    
    # Adjust legend's position
    plt.legend(loc='center left', bbox_to_anchor=(0.78, 0.7))
    plt.grid(True, which='both', linestyle=':', linewidth=0.7)
    plt.show()
    
    return

def integrate_and_visualize(graphs):
  
    # Initialize the total area
    total_area = 0
    
    # Create a figure for plotting
    fig, ax = plt.subplots()
    
    # Find the minimum y-value for each x across all graphs, treating nan values as 0
    min_y_values = {}
    for graph in graphs:
        for x, y in graph.items():
            if not np.isnan(y):
                if x not in min_y_values or (np.isnan(min_y_values[x]) or y < min_y_values[x]):
                    min_y_values[x] = y if not np.isnan(y) else 0
    
    # Sort the x-values and corresponding minimum y-values
    sorted_x = sorted(min_y_values.keys())
    sorted_min_y = [min_y_values[x] for x in sorted_x]
    
    # Plot and shade the minimum graph
    ax.plot(sorted_x, sorted_min_y, label='Minimum Graph', color='black')
    ax.fill_between(sorted_x, sorted_min_y, color='red', alpha=0.5)
    
    # Iterate over each graph (dictionary) in the list
    for graph in graphs:
        # Filter out NaN values from the dictionary and treat them as 0
        graph = {k: v if not np.isnan(v) else 0 for k, v in graph.items()}
        
        # Extract x and y values
        x_values = list(graph.keys())
        y_values = list(graph.values())
        
        # Sort the x and y values according to x
        sorted_pairs = sorted(zip(x_values, y_values))
        x_sorted, y_sorted = zip(*sorted_pairs)
        
        # Plot each graph
        ax.plot(x_sorted, y_sorted, label=f'Graph')
        
        # Calculate the area under the minimum graph
        if graph == graphs[-1]:  # Assuming the last graph is cut_dict_flex
            area = simps(sorted_min_y, sorted_x)
            total_area += area
    
    # Set plot labels and legend
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.legend()
    
    # Show the plot
    plt.show()
    
    return total_area

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
    dicts = [cut_dict_dichr, cut_dict_em, cut_dict_exc, cut_dict_flem, cut_dict_flex]
    names = ["Dichroic", "Emission Filter", "Excitation Filter", "Fluorescence Emission", "Fluorescence Excitation"]
    plotted_dicts = plot_dicts(dicts, names)
    
    # Find area under graphs
    graphs = [cut_dict_dichr, cut_dict_flem, cut_dict_flex]
    # print(graphs)
    print('Area under is [cut_dict_dichr, cut_dict_flem, cut_dict_flex] is ', integrate_and_visualize(graphs), '\n')


if __name__ == "__main__":
    main()
