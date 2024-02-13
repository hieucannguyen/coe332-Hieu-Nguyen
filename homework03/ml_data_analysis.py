#!/usr/bin/env python3
import csv
from gcd_algorithm import great_circle_distance
from typing import List
import sys

import argparse
import logging
import socket

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--loglevel', type=str, required=False, default='WARNING',
                    help='set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL')
parser.add_argument('-f', '--filename', type=str, required=False, default='Meteorite_Landings.csv',
                    help='set to file name of the meteorite landings data set')
args = parser.parse_args()

format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=args.loglevel, format=format_str)

def get_dataclass(data: List[dict], dataclass: str) -> List:
    """
    Retrieve a list of specified data from meteorite data set

    Args:
        data (List[dict]): meteorite data set
        dataclass (string): specified column in the data set

    Returns:
        result (List): list of the specified column of data
    """

    result = []
    for meteor in data:
        result.append(meteor[dataclass])

    return result

def fall_percent(data: List[dict]) -> tuple:
    """
    Get the percentages of meteorites that fell vs found

    Args:
        data (List[dict]): meteorite data set

    Returns:
        fell percetage (float): percent of meteorites that fell
        found percetage (float): percent of meteorites that were found
    """    

    fall = get_dataclass(data, 'fall')
    fell = 0
    found = 0
    for f in fall:
        if f == 'Fell':
            fell += 1
        if f == 'Found':
            found += 1

    fell_percentage = round(fell / len(fall), 2) * 100.
    found_percentage = round(found / len(fall), 2) * 100.
    logging.debug(f'Fall percentage: {fell_percentage}%, Found percentage: {found_percentage}%')
    return fell_percentage, found_percentage

def date_distribution(data: List[dict]) -> dict:
    """
    Counts the meteorites that landed within a certain time period

    Args:
        data (List[dict]): meteorite data set

    Returns:
        result (dictionary): counts of meteorites within a time range
    """

    years = get_dataclass(data, 'year')
    result = {}
    
    result['Before 1900'] = 0
    result['1900-1925'] = 0
    result['1926-1950'] = 0
    result['1951-1975'] = 0
    result['1976-2000'] = 0
    result['2001-2010'] = 0
    result['After 2010'] = 0

    for y in years:
        if y == '': # error handling
            logging.debug(y)
            continue
        year = int(y)
        if year < 1900:
            result['Before 1900'] = result['Before 1900'] + 1
        elif year >= 1900 and year <= 1925:
            result['1900-1925'] = result['1900-1925'] + 1
        elif year >= 1926 and year <= 1950:
            result['1926-1950'] = result['1926-1950'] + 1
        elif year >= 1951 and year <= 1975:
            result['1951-1975'] = result['1951-1975'] + 1
        elif year >= 1976 and year <= 2000:
            result['1976-2000'] = result['1976-2000'] + 1
        elif year >= 2001 and year <= 2010:
            result['2001-2010'] = result['2001-2010'] + 1
        else:
            result['After 2010'] = result['After 2010'] + 1

    return result

def check_hemisphere(latitude: float, longitude: float) -> str:
    """
    Determines which hemisphere the meteorite is located

    Args:
        latitude (float): latitude of meteorite
        longitude (float): longitude of meteorite

    Returns:
        location (string): hemisphere the meteorite is located
    """

    location = ''
    if (latitude > 0):
        location = 'Northern'
    else:
        location = 'Southern'
    if (longitude > 0):
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'
    logging.debug(f'({latitude}, {longitude}): {location}')
    return(location)

def location_mass_distribution(data: List[dict]) -> dict:
    """
    Finds the average mass of a meteorite in a specific hemisphere

    Args:
        data (List[dict]): meteorite data set

    Returns:
        result (dictionary): average mass of meteorite in a specific hemisphere
    """

    latitude = get_dataclass(data, "reclat")
    longitude = get_dataclass(data, "reclong")
    masses = get_dataclass(data, 'mass (g)')

    logging.debug(f'Data length: latitude: {len(latitude)}, longitude: {len(longitude)}, masses: {len(masses)}')
    count_NE = 0
    count_NW = 0
    count_SE = 0
    count_SW = 0

    result = {}
    for i in range(len(latitude)):
        # check for valid data
        if latitude[i] == '' or longitude[i] == '':
            continue
        if masses[i] == '':
            continue
        logging.debug(f'latitude: {latitude[i]}, longitude: {longitude[i]}, mass: {masses[i]}')
        # sums the masses by hemisphere
        hemisphere = check_hemisphere(float(latitude[i]), float(longitude[i]))
        if hemisphere == "Northern & Eastern":
            result["Northern & Eastern"] = result.get("Northern & Eastern", 0) + float(masses[i])
            count_NE += 1

        if hemisphere == "Northern & Western":
            result["Northern & Western"] = result.get("Northern & Western", 0) + float(masses[i])
            count_NW += 1

        if hemisphere == "Southern & Eastern":
            result["Southern & Eastern"] = result.get("Southern & Eastern", 0) + float(masses[i])
            count_SE += 1

        if hemisphere == "Southern & Western":
            result["Southern & Western"] = result.get("Southern & Western", 0) + float(masses[i])
            count_SW += 1

    # average the masses by hemisphere
    if count_NE == 0:
        result['Northern & Eastern'] = 0
    else:
        result['Northern & Eastern'] = round(result['Northern & Eastern'] / count_NE, 2)
    if count_NW == 0:
        result['Northern & Western'] = 0
    else:
        result['Northern & Western'] = round(result['Northern & Western'] / count_NW, 2)
    if count_SE == 0:
        result['Southern & Eastern'] = 0
    else:
        result['Southern & Eastern'] = round(result['Southern & Eastern'] / count_SE, 2)
    if count_SW == 0:
        result['Southern & Western'] = 0
    else:
        result['Southern & Western'] = round(result['Southern & Western'] / count_SW, 2)

    return result

def closest_meteorite(data: List[dict], meteor_id: int) -> tuple:
    """
    Finds the closest meteorite to a specified one

    Args:
        data (List[dict]): meteorite data set
        meteor_id (int): id number of the meteorite

    Returns:
        meteor (dictionary): specific row in the meteorite data set
        closest_meteor (string): name of the closest meteor
        min_distance (float): great circle distance of the closest meteor
    """
    if meteor_id < 0:
        logging.warning('negative id, not possible')

    # find matching meteor id
    meteor = ''
    if meteor_id != 0:
        for m in data:
            if m['id'] != '' and m['id'] == str(meteor_id):
                meteor = m
                break

    if meteor == '':
        logging.error('id not found')
        return 'Invalid meteorite id'

    latitude1 = float(meteor['reclat'])
    longitude1 = float(meteor['reclong'])

    # find closest meteor using great circle distace
    min_distance = float("inf")
    closest_meteor = ''
    for i in range(len(data)):
        if data[i]['reclat'] == '' or data[i]['reclong'] == '': # error handling 
            continue
        if float(data[i]['reclat']) == latitude1 or float(data[i]['reclong']) == longitude1: # ensure we don't compare the same meteorite
            continue

        distance = great_circle_distance((latitude1, longitude1), (float(data[i]['reclat']), float(data[i]['reclong'])))
        logging.debug(f'great circle distance: {distance}')
        if distance < min_distance:
            min_distance = distance
            closest_meteor = data[i]['name']

    return meteor, closest_meteor, min_distance

def summary_statistics(data: List[dict]) -> None:
    """
    Prints a summary of the meteorite data set

    Args:
        data (List[dict]): meteorite data set
    """

    print("Summary Statistics: \n")

    fell, found = fall_percent(data)
    if fell > 100 or fell < 0 or found > 100 or found < 0:
        logging.warning('percents cannt be above 100 or below 0')

    print(f'Percent fell: {fell}%')
    print(f'Percent found: {found}%')

    print('\nAverage mass of meteorites in each hemisphere:')
    location_mass = location_mass_distribution(data)
    for l in location_mass:
        print(f'{l}: {location_mass[l]} (g)')
    
    print('\nNumber of meteorites grouped by year:')
    years = date_distribution(data)
    for group in years:
        print(f'{group}: {years[group]} meteorites')

    original_meteor, closest, distance = closest_meteorite(data, 1) # meteorite id can change
    original_name = original_meteor['name']
    print(f'\nClosest meteorite to {original_name} is {closest} with a great circle distance of {round(distance,2)}km')

def main():
    data = {}
    data['meteorite_landings'] = []

    try:
        # read from csv file
        with open(args.filename, 'r', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data['meteorite_landings'].append(dict(row))

            summary_statistics(data["meteorite_landings"])
    except FileNotFoundError:
        logging.error('CSV file not found. Make sure the file exists and the path is correct.')
        raise

if __name__ == '__main__':
    main()
