from __future__ import print_function

# Importing Regular Expression - Regex to validate specific patterns
# for morphometric validation of inputted data.
import re

# Importing os library for clear screen
# Inspired by Amy Richardson PP3 project 
import os

# Importing os library for clear screen
# Inspired by Amy Richardson PP3 project
import time,sys

# Importing terminal table
# source: https://pypi.org/project/terminaltables/

from terminaltables import AsciiTable, DoubleTable, SingleTable

import gspread

from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hydromorpho')


# Constants

# For Regex, I used as fonts the following links:
# How I found out about Regex: https://stackoverflow.com/questions/18632491/how-do-i-check-for-an-exact-word-or-phrase-in-a-string-in-python
# Regex Calculator: https://regex101.com/
# Regex reading material: https://www.w3schools.com/python/python_regex.asp
# Regex negative and positive lookahead assertions: https://www.regextutorial.org/positive-and-negative-lookahead-assertions.php

# Regex Constants
RE_PATTERNS = {
    'decimal_degrees': r'^(?![+-]00\.000000$)[+-]\d{2}\.\d{6}$',
    'four_digits': r'^(?!0000$)\d{4}$',
    'three_digits': r'^(?!000\.000$)\d{3}\.\d{3}$',
    'basin_naming': r'^b_[a-z0-9_]{0,23}$',
    'urb_degree': r'^(?!0.00$)0\.([0-9][0-9])$'
}


# Variables
v_data_sheet = SHEET.worksheet('v_data')
f_data_sheet = SHEET.worksheet('f_data')

# Basin Variables: object with provisory data before approval and
# transition to Google Sheets
basin_variables = {
    'basin_name': [],
    'lat_centroid': [],
    'long_centroid': [],
    'area_sqkm': [],
    'perimeter_km': [],
    'main_length_ls': [],
    'basin_length_lb': [],
    'elev_outlet_ho': [],
    'elev_b_spring_hs': [],
    'elev_b_highest_p_hhp': [],
    'urbanization_level_u': [],
}


# Returned user data from Google Sheets used on item 2
returned_user_data = []

# Credit: Amy Richardson PP3 
# https://www.101computing.net/python-typing-text-effect/
def clear_screen():
    """
    Clears the screen from previous outputs and inputs
    """
    os.system("clear")


# Inspired by Code Institue's Love Sandwiches project
def get_data(variable_input):
    """
    Get the basin data inputed by the user
    """

    while True:
        if variable_input == 'basin_name':
            pattern = RE_PATTERNS['basin_naming']
            print("Please enter the basin's name. Up to 25 lowercase"
                  " characters and numbers are allowed.")
            print('As shown in the example, use the prefix "b_" and separate'
                  ' words with the "_" underscore.\n'
                  'e.g.: b_river_suir_02\n')
        elif variable_input == 'lat_centroid':
            pattern = RE_PATTERNS['decimal_degrees']
            print("Please enter the latitude coordinate in the Decimal Degrees"
                  " format of the basin's centroid.")
            please_ahere()
            print("e.g.: -20.102852\n")
        elif variable_input == 'long_centroid':
            pattern = RE_PATTERNS['decimal_degrees']
            print("Please enter the longitude coordinate in the Decimal"
                  " Degrees format of the basin's centroid.")
            please_ahere()
            print("e.g.: -43.453612\n")
        elif variable_input == 'area_sqkm':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the basin's area in km².")
            please_ahere()
            print("e.g.: 002.708\n")
        elif variable_input == 'perimeter_km':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the basin's perimeter in km².")
            please_ahere()
            print("e.g.: 007.289\n")
        elif variable_input == 'main_length_ls':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the main stream length in kilometres.")
            please_ahere()
            print("e.g.: 001.612\n")
        elif variable_input == 'basin_length_lb':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the basin's length in kilometres.")
            please_ahere()
            print("e.g.: 001.761\n")
        elif variable_input == 'elev_outlet_ho':
            pattern = RE_PATTERNS['four_digits']
            print("Please enter the elevation of the basin's outlet"
                  " point in meters.")
            please_ahere()
            print("e.g.: 0961\n")
        elif variable_input == 'elev_b_spring_hs':
            pattern = RE_PATTERNS['four_digits']
            print("Please enter the elevation of the main stream start of the"
                  " channel (spring) in meters.")
            please_ahere()
            print("e.g.: 1378\n")
        elif variable_input == 'elev_b_highest_p_hhp':
            pattern = RE_PATTERNS['four_digits']
            print("Please enter the elevation of the basin's highest point"
                  "in meters.")
            please_ahere()
            print("e.g.: 1413\n")
        elif variable_input == 'urbanization_level_u':
            pattern = RE_PATTERNS['urb_degree']
            print("Please enter the urbanization level in the studied basin."
                  " Degree of urbanization should be based on the ratio"
                  " urbanized area and the basin total area:\n"
                  "u = urbanized area / basin total area.\n"
                  "The input should vary from 0.01 to 0.99.\n"
                  "e.g.: 0.64\n")

        data_str = input("Input the basin's data here:\n")

        if validate_data(data_str, pattern, variable_input):
            basin_variables.update({variable_input: data_str})
            break
        return data_str


# Function to validate the Regex pattern, inspired by Code Institue's
# Love Sandwiches project
def validate_data(data, pattern, variable_input):
    """
    Run Regex based on input data's type and re-run input if there's an error
    """
    if re.match(pattern, data):
        print(f'Data is valid, {data} matches the pattern\n')
        return True
    elif data.lower() == 'exit':
        main()
    else:
        print(f"Invalid input, {data} does not match the pattern."
              'If unsure, go back to "Main Menu > Instructions" to'
              ' better understand the data to be provided.\n'
              'You can also return to Main Menu by typping "exit"\n')
        get_data(variable_input)
        return False


# This line was being reproduced several times through the input data.
# So, I thought It would be better to transform the print statment
# into a function.
# For the sake of eliminating reapeated code several times.
def please_ahere():
    """
    Returns a sentence used several times through data input.
    """
    print("Please adhere to the specified format of the example"
          " with the exact number of digits.")


def check_elevation():
    """
    Checks elevation based on the inputted variables.

    Following the physiographic arrangement of the relief, the output elevation
    can't be greater than the other two variables.
    Likewise, the spring elevation is positioned in a lower quota than the
    highest point of the watershed.
    Taking into account those facts, this function was built.
    """

    print('Running some validations...\n')

    ho = int(basin_variables['elev_outlet_ho'])
    hs = int(basin_variables['elev_b_spring_hs'])
    hhp = int(basin_variables['elev_b_highest_p_hhp'])

    if ho < hs < hhp:
        print('Elevation inputted data is consistent.\n'
              'Proceeding...\n')
        return True
    else:
        print("The elevation data you entered is invalid.\n"
              "The outlet elevation must be inferior to the basin's"
              " main channel initial point elevation.\n"
              "In addition, the latter has to be inferior to"
              " the highest point in the basin.\n")
        re_enter_data('elevation', ['elev_outlet_ho',
                      'elev_b_spring_hs', 'elev_b_highest_p_hhp'],
                      check_elevation)
        return False


def check_dimensional_data():
    """
    Checks consistency of the dimensional variables.
    """

    print('Running some validations...\n')

    area_b = float(basin_variables['area_sqkm'])
    pmt_b = float(basin_variables['perimeter_km'])
    ls = float(basin_variables['main_length_ls'])
    lb = float(basin_variables['basin_length_lb'])

    if (((area_b < (pmt_b * 20)) and (pmt_b < (area_b * 20))
        and (ls < (lb * 20)) and (lb < (ls * 20))) and
       ((area_b != pmt_b) and (lb != ls))):
        print('Basin dimensional inputted data is consistent.\n'
              'Proceeding...\n')
        return True
    else:
        print("There's discrepancies in between area and perimeter"
              " or basin's length and main stream length.\n")
        re_enter_data('dimensional', ['area_sqkm', 'perimeter_km',
                      'main_length_ls', 'basin_length_lb'],
                      check_dimensional_data)
        return False


def re_enter_data(var_name, variables, check_function):
    """
    Allows the user to re-enter the elevation data after check_elevation
    detects a discrepancy. The user can also go back to the main menu.
    """
    while True:
        user_input = input(f"Would you like to re-enter the {var_name}"
                           f" data?\nEnter Y or N.\n")
        if user_input.lower() == 'y':
            print("\n")
            for variable in variables:
                get_data(variable)
            if check_function():
                break
        elif user_input.lower() == 'n':
            main()
        else:
            print('Incorrect input. Please try again.')
        break


def print_input_data_table():
    """
    Create table with the values enter by the user.
    """
    name_b = basin_variables['basin_name']
    lat = basin_variables['lat_centroid']
    # Long is a system name
    longc = basin_variables['long_centroid']
    area_b = float(basin_variables['area_sqkm'])
    pmt_b = float(basin_variables['perimeter_km'])
    ls = float(basin_variables['main_length_ls'])
    lb = float(basin_variables['basin_length_lb'])
    ho = int(basin_variables['elev_outlet_ho'])
    hs = int(basin_variables['elev_b_spring_hs'])
    hhp = int(basin_variables['elev_b_highest_p_hhp'])
    urb = float(basin_variables['urbanization_level_u'])

    table_data = (
                   ('Variables', 'Data'),
                   ('Basin Name', name_b),
                   ('Latitude', lat),
                   ('Longitude', longc),
                   ('Area', area_b),
                   ('Perimeter', pmt_b),
                   ('Main Stream Length', ls),
                   ('Basin Length', lb),
                   ('Outlet Elevation', ho),
                   ('Spring Elevation', hs),
                   ("Basin's Highest Point", hhp),
                   ('Urbanization Level', urb)
                   )

    table_title = "Basin Data"

    table_instance = SingleTable(table_data, table_title)
    table_instance.justify_columns[2] = "right"
    print(table_instance.table)
    print()


def approve_transfered_data():
    """
    Approve data presented by the chart and return basin index number
    """
    while True:
        user_input = input("Are the data correct? Would you like" 
                           " to proceed?\n"
                           "Enter Y or N.\n")
        if user_input.lower() == 'y':
            print("\n")
            transfer_data = []
            for values in basin_variables.values():
                transfer_data.append(values)
            v_data_sheet.append_row(transfer_data)
            user_basin_n = len(v_data_sheet.get_all_values())
            print(f'All data sent with success! Your basin index' 
                  f' number is "{user_basin_n}"\n'
                   'Save this number, it will be used' 
                   'in "2-Run Morphometric Indices"\n')
            break
        elif user_input.lower() == 'n' and 'exit':
            main()
        else:
            print('Incorrect input. Please try again.\n')
        break


def validate_retrive():
    """
    Retrive user data for running morphometric indices.
    The data is retrived from v_data sheet
    """
    global returned_user_data
    max_rows_gsheets = 983
    b_name_clm = 1
    while True:
        b_index = input("Please insert your basin index number\n")

        if b_index.lower() == 'exit':
            print("Exiting...")
            return False

        if b_index.isdigit():
            if int(b_index) < max_rows_gsheets:
                print("Format is valid.\n")
                print("Checking Database...\n")
                b_name = v_data_sheet.cell(int(b_index), b_name_clm).value
                if re.match(RE_PATTERNS['basin_naming'], str(b_name)):
                    print("Retriving basin's data...\n")
                    returned_user_data = v_data_sheet.row_values(int(b_index))
                    approve_retrieved_data()
                    return returned_user_data
                    print(returned_user_data)
                else:
                    print("There's no data with that basin index\n")
                    validate_retrive()
            break
        else:
            print('Incorrect input. Please try again.\n')
            validate_retrive()
        break


def approve_retrieved_data():
    """
    Allows to user to validate fetched data from v_data by returning 
    the basin name. If not valid the user can try other entries.
    """
    b_name = returned_user_data[0]
    print('Type Y to confirm or N pick another basin'
          ' index number. You can also escape to '
          'main menu by entering "exit"\n' )
    user_input = input(f"Is {b_name} the desired basin?\n")
    while True:
        if user_input.lower() == 'y':
            print('Running Morphometric Indices...\n')
            break
        elif user_input.lower() == 'n' and 'exit':
            validate_retrive()
        else:
            print('Incorrect input. Please try again.\n')
        break


def get_user_basin_data():
    """
    Center all the functions involved on collectiong the user 
    basin data.
    """
    for key in basin_variables.keys():
        get_data(key)
    clear_screen()
    check_elevation()
    clear_screen()
    check_dimensional_data()
    clear_screen()
    print_input_data_table()


# Morphometric Indices
def morphometric_indices():
    """
    Calculates morphometric indices based on
    values stored in returned_user_data, and returns the results.
    """
    # Variables
    pi_n = 3.141
    basin_name = returned_user_data[0]
    area = float(returned_user_data[3])
    perimeter = float(returned_user_data[4])
    main_length_ls = float(returned_user_data[5])
    basin_length_lb = float(returned_user_data[6])
    elev_outlet_ho = float(returned_user_data[7])
    elev_spring_hs = float(returned_user_data[8])
    elev_highest_hhp = float(returned_user_data[9])
    urbanization = float(returned_user_data[10])

    all_vb = [
        basin_name, area, perimeter, main_length_ls, basin_length_lb,
        elev_outlet_ho, elev_spring_hs, elev_highest_hhp, urbanization
    ]
    print("Input Variables:", all_vb)

    # Average Slope
    avg_raw_slope = (
        (elev_spring_hs - elev_outlet_ho) / (main_length_ls * 1000)
    ) * 100
    avg_slope = round(avg_raw_slope, 2)

    # Compactness Coefficient
    result_cc = round(perimeter / (2 * ((pi_n * area) ** 0.5)), 2)

    # Form Factor
    result_ff = round(area / (basin_length_lb ** 2), 2)

    # Elongation Ratio
    result_re = round(((2 * ((area / pi_n) ** 0.5)) / basin_length_lb), 2)

    # Time of Concentration
    raw_tc = 0.3 * ((main_length_ls / (avg_slope ** 0.25)) ** 0.76)
    result_tc = round((raw_tc * 60), 2)
    tcf_denominator = 1 + (3 * (pi_n * (2 - urbanization)) ** 0.5)
    result_tcf = raw_tc / tcf_denominator
    result_tcf = round((result_tcf * 60), 2)

    # Relative Relief
    result_rr = elev_highest_hhp - elev_outlet_ho

    # Form Factor Classification
    if result_ff < 0.5:
        description_ff = "basin not prone to floods events"
    elif 0.5 <= result_ff < 0.75:
        description_ff = "basin with medium tendency to floods events"
    else:
        description_ff = "basin prone to floods events"

    # Compactness Coefficient Classification
    if result_cc > 1.5:
        description_cc = "basin not prone to large floods"
    elif 1.25 < result_cc <= 1.5:
        description_cc = "basin with medium tendency to large floods"
    else:
        description_cc = "basin with high propensity for large floods"
    
    # Elongation Ratio Classification
    if result_re < 0.5:
        description_re = "more elongated"
    elif 0.5 <= result_re < 0.7:
        description_re = "elongated"
    elif 0.7 <= result_re < 0.8:
        description_re = "less elongated"
    elif 0.8 <= result_re < 0.9:
        description_re = "oval"
    else:
        description_re = "circular"

    all_results = [
        basin_name,
        result_cc, 
        description_cc, 
        result_ff, 
        description_ff,
        result_re,
        description_re,
        result_tc, 
        result_tcf, 
        result_rr
    ]
    
    f_data_sheet.append_row(all_results)
    
    print(all_results)

    return all_results


def run_morphometric_indices():
    """
    This function aggregates the all the functions / steps
    involving the run morphometric indices main feat.
    """
    validate_retrive()
    clear_screen()
    morphometric_indices()



def return_main():
    """
    Returns to main menu option through 'exit' input.
    """
    while True:
        print("\n")
        choice = input("To return to Main Menu, please enter 'exit'.\n")
        if choice.lower() == 'exit':
            main()
            break
        else:
            print("Invalid input, please try again.")
            continue


def instructions():
    """
    Displays basic intructions to collect the necessary data
    to be user as input for the app.
    """
    print("Beforehand, the user needs to collect data on relief,\n"
          "including linear and areal features. This can be done\n"
          "in various ways, such as consulting a topographic map\n"
          "or using a Geographic Information System (GIS).\n"
          "For users less familiar with GIS, it is recommended to\n"
          "use Google Earth Pro. The pro version allows users to\n"
          "draw the basin/watershed and obtain the necessary metrics\n"
          "to input into the app.\n"
          "\n"
          "The required inputs are:\n"
          "Latitude of the basin's centroid\n"
          "\n"
          "Longitude of the basin's centroid\n"
          "\n"
          "Basin area in km² (with 3 significant digits after the decimal\n"
          "point)\n"
          "\n"
          "Basin perimeter in km (with 3 significant digits after the\n"
          "decimal point)\n"
          "\n"
          "Main stream length in km (with 3 significant digits after\n"
          "the decimal point)\n"
          "\n"
          "Basin length, from the furthest point of the basin to\n"
          "the other, with 3 significant digits\n"
          "\n"
          "Main stream outlet elevation in meters\n"
          "\n"
          "Spring elevation, the starting point of the main stream,\n"
          "in meters\n"
          "\n"
          "Basin's highest point in meters\n"
          "\n"
          "An estimate Urbanization level as a percentage of\n" 
          "constructed area\n")
    return_main()


def about():
    """
    Displays the basic information about the web application.
    """
    print("The analysis of morphometric parameters is essential for\n"
          "understanding and managing watersheds, making it a fundamental\n"
          "component of hydrological investigations.\n" 
          "\n"
          "This application provides a quick and accessible tool\n"
          "for obtaining hydrological and geomorphological \n"
          "morphometric parameters using collected data on relief,\n"
          "linear, and areal features.\n"
          "\n"
          "Through a variety of scientifically renowned methods,\n"
          "this application offers an overview of a basin's\n"
          "hydrological behavior, particularly regarding flood\n"
          "propensity.\n"
          "\n"
          "It caters to the needs of students,hydrology and\n" 
          "geomorphology professionals, and the community, addressing\n"
          "the evolving demands of planning for climate-related disasters.\n")
    return_main()   

# Inspired by Amy Richardson BakeStock PP3 project
def main():
    """
    Displays the main menu with options for users to 
    choose the application's functionalities.
    """
    print("_____WELCOME__TO__HYDROMORPHO_____\n")
    print('\n')
    print("Please choose from the options below.\n")
    print("1. Insert Basin Data\n")
    print("2. Run Morphometric Indices\n")
    print("3. Instructions\n")
    print("4. About\n")
    print("5. Exit\n")
    while True:
        try:
            choice = int(input("Enter a number for the desired feature: \n"))
            if choice == 1:
                get_user_basin_data()
                break
            elif choice == 2:
                run_morphometric_indices()
                break
            elif choice == 3:
                instructions()
                break
            elif choice == 4:
                about()
                break
            elif choice == 5:
                exit()
                break
        except ValueError:
            print("Invalid input. Enter a number according to"
                  " the desired feature.\n")
            continue


main()
