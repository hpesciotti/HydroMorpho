# Importing Regular Expression - Regex to validate specific patterns for morphometric input data. 
# I used as fonts the following links:
# How I found out about Regex: https://stackoverflow.com/questions/18632491/how-do-i-check-for-an-exact-word-or-phrase-in-a-string-in-python
# Regex Calculator: https://regex101.com/
# Regex reading material: https://www.w3schools.com/python/python_regex.asp
# Regex negative and positive lookahead assertions: https://www.regextutorial.org/positive-and-negative-lookahead-assertions.php

import re

#Constants

#Regex Constants
RE_PATTERNS = {
    'decimal_degrees': r'^(?![+-]00\.000000$)[+-]\d{2}\.\d{6}$',
    'four_digits': r'^(?!0000$)\d{4}$',
    'three_digits': r'^(?!000\.000$)\d{3}\.\d{3}$',
    'basin_naming': r'^b_[a-z0-9_]{0,23}$',
    'urb_degree': r'^[1-4]$'
}

#Basin Variables: object with provisory data before approval and transition to Google Sheets
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
    'elev_b_highest_p_hhp':[],
    'urbanization_level_u': [],
}

#Method inspired by Code Institue's Love Sandwiches project 
def get_data(variable_input):
    """
    Get the basin data inputed by the user 
    """
    while True:
        if variable_input == 'basin_name':
            pattern = RE_PATTERNS['basin_naming']
            print("Please enter the basin's name. Up to 25 lowercase characters and numbers are aloud.")
            print('As shown in the example, use the prefix "b_" and separate words with the "_" underscore.')
            print("e.g.: b_river_suir_02\n")
        elif variable_input == 'lat_centroid':
            pattern = RE_PATTERNS['decimal_degrees']
            print("Please enter the latitude coordinate in the Decimal Degrees format of the basin's centroid.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: -20.102852\n")
        elif variable_input == 'long_centroid':
            pattern = RE_PATTERNS['decimal_degrees']
            print("Please enter the longitude coordinate in the Decimal Degrees format of the basin's centroid.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: -43.453612\n")
        elif variable_input == 'area_sqkm':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the basin's area in km².")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 002.708\n")
        elif variable_input == 'perimeter_km':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the basin's perimeter in km².")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 007.289\n")
        elif variable_input == 'main_length_ls':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the main stream length in kilometres.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 001.612\n")
        elif variable_input == 'basin_length_lb':
            pattern = RE_PATTERNS['three_digits']
            print("Please enter the basin's length in kilometres.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 001.761\n")
        elif variable_input == 'elev_outlet_ho':
            pattern = RE_PATTERNS['four_digits']
            print("Please enter the elevation of the basin's outlet in meters.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 0961\n")
        elif variable_input == 'elev_b_spring_hs':
            pattern = RE_PATTERNS['four_digits']
            print("Please enter the elevation of the main stream start of the channel (spring) in meters.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 1378\n")
        elif variable_input == 'elev_b_highest_p_hhp':
            pattern = RE_PATTERNS['four_digits']
            print("Please enter the elevation of the basin's highest poin in meters.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 1413\n")
        elif variable_input == 'urbanization_level_u':
            pattern = RE_PATTERNS['urb_degree']
            print("Please enter the urbanization level in the studied basin. Limit the input to number assigned to")
            print("degree of urbanization, according to the following values:")
            print("1 - Low")
            print("2 - Moderate")
            print("3 - Consolidated")
            print("4 - Highly Developed")


        data_str = input("Input the basin's data here:\n")

        if validate_data(data_str, pattern, variable_input):
            basin_variables[variable_input].append(data_str)
            break
        return data_str


# Function to validate the Regex pattern, inspired by Code Institue's Love Sandwiches project 
def validate_data(data, pattern, variable_input):
    """
    Run Regex based on the input data's type and re-run input if there's an error
    """
    if re.match(pattern, data):
        print(f"'Data is valid, {data} matches the pattern\n")
        return True
    else:
        print(f"Invalid input, {data} does not match the pattern")
        print('If unsure, go back to "Main Menu > Instructions" to better understand the data to be provided.')
        print('You can also return to Main Menu by typping "exit"\n')
        get_data(variable_input)
        return False


def app_exit():
    if data_str == 'Exit' or 'exit':
        main()

def main():
    for key in basin_variables.keys():
        get_data(key)

    print(basin_variables)

main()