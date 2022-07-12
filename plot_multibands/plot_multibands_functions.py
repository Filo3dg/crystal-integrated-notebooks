# This file contains the functions that are specific to this notebook.
from posixpath import split
from crystal_functions.file_readwrite import Properties_output
import crystal_functions.plot as cfplt
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys

BR = ['blue', 'darkorchid', 'slateblue', 'thistle',
      'purple', 'magenta', 'orchid', 'crimson']

GR = ['darkgreen', 'limegreen', 'lawngreen', 'yellowgreen',
      'yellow', 'gold', 'orange', 'saddlebrown']

NOSOC = ['dimgrey', 'blue', 'indigo', 'slateblue',
         'thistle', 'purple', 'orchid', 'crimson']

cmap = {'BR': BR, 'GR': GR, 'NOSOC': NOSOC}

Fermi = {'BR': 'forestgreen', 'GR': 'blue', 'NOSOC': 'red'}


def selection_input():
    Tk().withdraw()
    file_list = askopenfilename(multiple=True, filetypes=[
                                ("Band Files", ".f24 .band .BAND .DAT")])

    if len(file_list) > len(BR) or len(file_list) > len(GR):
        print('Error!, You have exceeded the maximum number of file comparable')
        sys.exit(1)

    return file_list


def labels_def(file_list):
    if len(file_list) <= 1:
        labels = None
        print('Done')

    else:
        positive_feedback = ['y', 'Yes', 'YES', 'Y', 'yes']
        negative_feedback = ['n', 'No', 'NO', 'N', 'no']
        lblyn = input(
            'Do you want to define a label for each file [y/n]? \n').split()

        if lblyn in positive_feedback:
            labels = input('Enter a label for each of the file selected:\n')
            if len(labels) < len(file_list):
                l_add = str(len(file_list)-len(labels))
                ls_add = input(
                    'You have enetered a number of labels lower than the number of files. Please enter the '+l_add+' missing ones: \n')
                ls_add = ls_add.split()
                labels = labels+ls_add

            elif len(labels) > len(file_list):
                print('Error!, you have more labels than the file selected!')
                sys.exit(1)

        elif lblyn in negative_feedback:
            labels = None

    return labels


def color_def(file_list):
    negative_feedback = ['n', 'No', 'NO', 'N', 'no']
    cmap = input(
        'Do you want to use a default colormap [BR/GR/NOSOC/n]?\n')
    if file_list > 1:
        if cmap in negative_feedback:
            cmap = input('Specify your own colormap:\n').split()
            if len(cmap) < len(file_list):
                difference = str(len(file_list)-len(cmap))
                add = input('Warning! You are lacking '+difference +
                            ' colors, please enter the missing ones here:\n')
                add = add.split()
                for i in add:
                    cmap.append(i)

            elif len(cmap) > len(file_list):
                difference = len(cmap)-len(file_list)
                print('Warning! You have '+difference +
                      ' colors more than the file you want to plot')

    else:
        if cmap in negative_feedback:
            cmap = input(
                'Please enter the color that you want to use for the band plot: \n')
        else:
            cmap = None

    if cmap in negative_feedback:
        fermi = input(
            'Do you want to change the fermi level color (default: forestgreen)?')
    else:
        fermi = None

    return cmap, fermi


def path_def(file_list):

    if isinstance(file_list, list):
        file_list = paths
        for index, bands in enumerate(file_list):
            file_list[index] = Properties_output().read_cry_bands(bands)
        if (file_list[0] == file_list[1]) and (file_list[0] == file_list[len(file_list)-1]):
            for index, file in enumerate(file_list):
                if file.n_kpoints != file_list[0].n_kpoints:
                    print('Error! the number of k point in the file: ' +
                          paths[index] + ' is different from the other ones')

        no_kpoints = file_list[0].n_kpoints

    else:
        no_kpoints = Properties_output().read_cry_bands(file_list)
        no_kpoints = no_kpoints.n_kpoints

    user_path = input('Enter the path for the band structure: \n')
    user_path = user_path.split()

    if len(user_path) != no_kpoints:
        diff = len(user_path) = no_kpoints
        if diff > 0:
            print(
                'Error! the number of k points defined is greater than the ones present in the file')
            sys.exit(1)
        elif diff < 0:
            print(
                'Warning! the number of k points defined is smaller than the ones in the file')
            choice = input('Do you want to introduce the ' +
                           str(-diff) + ' lacking k points [y/n]')
            if choice == 'y':
                user_add = input('Please enter the missing k points:')
                user_add = user_add.split()
                for element in user_add:
                    user_path.append(element)
            else:
                sys.exit(0)

    return user_path
