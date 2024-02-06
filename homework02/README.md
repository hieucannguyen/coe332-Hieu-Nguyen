# Meteorite Landings Analysis
This project aims to analyze NASA's meteorite data and derive insights such as time distribution, location mass distribution, and finding the closest meteorite to a specified one using the Great-circle distance formula. 
Using Python we extracted the data, analyzed the data, and automated unit tests using pytest.

## File Descriptions
- [gcd_algorithm.py](gcd_algorithm.py): Computing the distance between 2 meteorites using the Great-circle distance formula
- [ml_data_analysis.py](ml_data_analysis.py): Extracting and computing insights from the meteorite data
- [test_gcd_algorithm.py](test_gcd_algorithm.py): Unit tests for my implementation of the Great-circle distance formula
- [test_ml_data_analysis.py](test_ml_data_analysis.py): Unit tests for meteorite data analysis

## Data and Setup
1. Navigate to [https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh/about_data](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh/about_data) and go to export to then download the dataset in CSV format
2. Move the dataset to the appropriate directory (same directory as the Python scripts)
3. Rename the data so that is the same as **Meteorite_Landings.csv** (ensures the Python script can read the file)

## Running the Analysis
Once you have the dataset in the same directory as the Python scripts we can now run the command

~~~
Python3 ml_data_analysis.py
~~~

which should then output this

~~~
Summary Statistics:

Percent fell: 2.0%
Percent found: 98.0%

Average mass of meteorites in each hemisphere:
Northern & Eastern: 19288.2 (g)
Northern & Western: 104550.51 (g)
Southern & Western: 10289.15 (g)
Southern & Eastern: 7438.69 (g)

Number of meteorites grouped by year:
Before 1900: 728 meteorites
1900-1925: 392 meteorites
1926-1950: 605 meteorites
1951-1975: 1757 meteorites
1976-2000: 24014 meteorites
2001-2010: 16970 meteorites
After 2010: 959 meteorites

Closest meteorite to Aachen is Hautes Fagnes with a great circle distance of 22.13km
~~~

To change meteorite used in the Great-circle distance algorithm edit the `summary_statistics` function in [ml_data_analysis.py](ml_data_analysis.py) and then
find the `closest_meteorite` function call. From there change the current meteorite id to the meteorite id of interest

## Testing Python scripts
First install pytest using

~~~
pip3 install --user pytest
~~~

In the same directory as the scripts execute

~~~
pytest
~~~

to see if the Python scripts passed the unit tests
