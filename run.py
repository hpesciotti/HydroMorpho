# Importing Regular Expression - RegEX to validate specific patterns for morphometric input data. 
# I used as fonts the following links:
# How I found out about RegEX: https://stackoverflow.com/questions/18632491/how-do-i-check-for-an-exact-word-or-phrase-in-a-string-in-python
# RegEx Calculator: https://regex101.com/
# RegEx reading material: https://www.w3schools.com/python/python_regex.asp

import re

#Constants

#RegEx Constants
RE_PATTERNS = {
    'decimal_degrees': r'^[+-]\d{2}\.\d{6}$',
    'four_digits': r'^\d{4}$',
    'three_digits_point': r'^\d{3}\.d{3}$',
    'basin_naming': r'^b_[a-z0-9_]{0,23}$',
}

#Basin Variables: object with provisory data before approval and transition to Google Sheets
basin_variables = {
    'basin_name': [],
    'lat_centroid': [],
    'long_centroid': [],
    'elevation_outlet_ho': [],
    'basin_length_lb': [],    
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
        elif variable_input == 'elevation_outlet_ho':
            pattern = RE_PATTERNS['four_digits']
            print("Please enter the elevation of the basin outlet in meters.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 0966\n")
        elif variable_input == 'basin_length_lb':
            pattern = RE_PATTERNS['three_digits_point']
            print("Please enter the basin's length in kilometres.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 001.546\n")
        elif variable_input == 'basin_name':
            pattern = RE_PATTERNS['three_digits_point']
            print("Please enter the basin's length in kilometres.")
            print("Please adhere to the specified format of the example with the exact number of digits.")
            print("e.g.: 001.546\n")

        data_str = input("Input the basin's data here:\n")

        if validate_data(data_str, pattern, variable_input):
            basin_variables[variable_input].append(data_str)
            break
        return data_str


# Function to validate the RegEx pattern, inspired by Code Institue's Love Sandwiches project 
def validate_data(data, pattern, variable_input):
    """
    Run RegEx based on the input data's type and re-run input if there's an error
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

        

def main():
    get_data('basin_name')
    get_data('lat_centroid')
    get_data('long_centroid')

    print(f"Latitude:{basin_variables['lat_centroid']}, Longitude:{basin_variables['long_centroid']}")

    # print(f"Latitude:{latitude}, Longitude:{longitude}, Elevation:{altitude}, Lenght:{lenght}")

main()