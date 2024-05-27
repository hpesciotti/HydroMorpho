
# Importing Regular Expression - Regex to validate specific patterns
# for morphometric validation of inputted data.
import re

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
    'urb_degree': r'^0\.([0-9][1-9])$'
}

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


# Method inspired by Code Institue's Love Sandwiches project
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

    ho = basin_variables['elev_outlet_ho']
    hs = basin_variables['elev_b_spring_hs']
    hhp = basin_variables['elev_b_highest_p_hhp']

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
        # print(f'{basin_variables['elev_outlet_ho']}, {basin_variables['elev_b_spring_hs']}, {basin_variables['elev_b_highest_p_hhp']}')
        re_enter_data('elevation', ['elev_outlet_ho', 'elev_b_spring_hs', 'elev_b_highest_p_hhp'], check_elevation)
        return False


def check_dimensional_data(var1, var2, vname_1, vname_2):
    """
    Checks consistency of the dimensional variables.
    """

    print('Running some validations...\n')

    while ((var1 < (var2 *100)) and (var2 < (var1 *100))):
        print('Basin dimensional inputted data is consistent.\n'
              'Proceeding...\n')
        return True
    else:
        print("The dimensional data you entered" 
              " seems to be incorrect.\n")
        print(f"There's discrepancies in between {vname_1}"
              f" and {vname_2}./n")
        re_enter_data('dimensional', ['var1', 'var2'], check_dimensional_data(var1, var2, vname_1, vname_2))
        return False


def re_enter_data(var_name, variables, check_function):
    """
    Allows the user to re-enter the elevation data after check_elevation
    detects a discrepancy. The user can also go back to the main menu.
    """
    while True:
        user_input = input(f"Would you like to re-enter the {var_name}" 
                           f" data? Enter Y or N.\n")
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


def main():
    """
    Run the main functionalities of the app.
    """
    # for key in basin_variables.keys():
    #     get_data(key)
    
    # get_data('elev_outlet_ho')
    # get_data('elev_b_spring_hs')
    # get_data('elev_b_highest_p_hhp')
    get_data('urbanization_level_u')
    check_elevation()

    # check_dimensional_data()

    print(basin_variables)


main()
