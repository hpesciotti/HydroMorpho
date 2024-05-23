# Importing Regular Expression - RegEX to validate specific patterns for morphometric input data. 
# I used as fonts the following links:
# How I found out about RegEX: https://stackoverflow.com/questions/18632491/how-do-i-check-for-an-exact-word-or-phrase-in-a-string-in-python
# RegEx Calculator: https://regex101.com/
# RegEx reading material: https://www.w3schools.com/python/python_regex.asp

import re

#Constants

#RegEx Constant
RE_PATTERNS = {
    'Lat_Centroid': r'^[+-]\d{2}\.\d{6}$',
    'Long_Centroid': r'^[+-]\d{2}\.\d{6}$',
    'Elevation_Basin_Outlet_HBO': r'^\d{4}$',
    'Basin_Length_Lb': r'^\d{3}\.d{3}$'
}

#Function inspired by Code Institue's Love Sandwiches project 
def get_data(variable_input):
    """
    Get the basin data inputed by the user 
    """
    while True:
        if variable_input == RE_PATTERNS['Lat_Centroid']:
            print("Please enter the latitude coordinate in the Decimal Degrees format of the basin's centroid.\n")
            print("Please adhere to the specified format of the example with the exact number of digits.\n")
            print("e.g.: -20.102852\n")
            print('If unsure, go back to "Main Menu>Instructions" to better understand the data to be provided.\n')
        elif variable_input == RE_PATTERNS['Long_Centroid']:
            print("Please enter the longitude coordinate in the Decimal Degrees format of the basin's centroid..\n")
            print("Please adhere to the specified format of the example with the exact number of digits.\n")
            print("e.g.: -43.453612\n")
            print('If unsure, go back to "Main Menu>Instructions" to better understand the data to be provided.\n')
        elif variable_input == RE_PATTERNS['Elevation_Basin_Outlet_HBO']:
            print("Please enter the elevation of the basin outlet in meters.\n")
            print("Please adhere to the specified format of the example with the exact number of digits.\n")
            print("e.g.: 0966\n")
            print('If unsure, go back to "Main Menu>Instructions" to better understand the data to be provided.\n')
        elif variable_input == RE_PATTERNS['Basin_Length_Lb']:
            print("Please enter the basin's length in kilometres.\n")
            print("Please adhere to the specified format of the example with the exact number of digits.\n")
            print("e.g.: 001.546\n")
            print('If unsure, go back to "Main Menu>Instructions" to better understand the data to be provided.\n')
        
        data_str = input("Input the basin's data here:\n")

        if validate_data(data_str, variable_input):
            print("Data is valid")
            break
        return data_str
    
# Function to validate the RegEx pattern, inspired by Code Institue's Love Sandwiches project 
def validate_data(data, pattern):
    """
    Run RegEx based on the input data's type 
    """
    if re.match(pattern, data):
        print(f"'{data}' matches the pattern")
        return True
    else:
        print(f"'{data}' does not match the pattern")
        return False

def main():
    latitude = get_data(RE_PATTERNS['Lat_Centroid'])
    longitude = get_data(RE_PATTERNS['Long_Centroid'])
    altitude = get_data(RE_PATTERNS['Elevation_Basin_Outlet_HBO'])
    lenght = get_data(RE_PATTERNS['Basin_Length_Lb'])

    print(f"Latitude:{latitude}, Longitude:{longitude}, Elevation:{altitude}, Lenght:{lenght}")