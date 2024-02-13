# Meteorite Landings Analysis- Using Docker
This project utilizes Docker to build and run our Python scripts to analyze NASA's meteorite data and derive insights such as time distribution, location mass distribution, and finding the closest meteorite to a specified one using the Great-circle distance formula. 

## File Descriptions
- [Dockerfile](Dockerfile): Dockerfile to generate docker image of our application
- [gcd_algorithm.py](gcd_algorithm.py): Computing the distance between 2 meteorites using the Great-circle distance formula
- [ml_data_analysis.py](ml_data_analysis.py): Extracting and computing insights from the meteorite data
- [test_gcd_algorithm.py](test_gcd_algorithm.py): Unit tests for my implementation of the Great-circle distance formula
- [test_ml_data_analysis.py](test_ml_data_analysis.py): Unit tests for meteorite data analysis

## Software Diagram
![image](coe332_hw3_diagram.svg)

*Software diagram of the development environment and Python scripts. Visualization of the application workflow and what the functions and outputs are in the Python scripts.*

## Data and Setup
1. Navigate to [https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh/about_data](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh/about_data) and go to export to then download the dataset in CSV format
2. Move the dataset to the appropriate directory (same directory as the Python scripts)

**Note:** Using API endpoint to download the dataset only gets a sample of the full dataset. Use the download file option or the scripts will not work. 

## Docker: build the image
Navigate into the directory where our scripts and Dockerfile are located.

Run 
~~~
$ docker build -t username/ml_data_analysis:1.0 .
~~~

## Docker: Running the Analysis
Once you have built the docker image using the Dockerfile we can now run the analysis.

### Mount the data inside the container
To mount our dataset into the container we use `-v $PWD/name_of_dataset.csv:/data/name_of_dataset.csv` in docker run.

Example:
~~~
$ docker run --rm -it -v $PWD/Meteorite_Landings.csv:/data/Meteorite_Landings.csv hieucannguyen/ml_data_analysis.py bin/bash
~~~

### Run the analysis
There are two ways to run the analysis. First, you can use the interactive mode
~~~
$ docker run --rm -it -v $PWD/Meteorite_Landings.csv:/data/Meteorite_Landings.csv hieucannguyen/ml_data_analysis.py bin/bash
~~~
then run
~~~
$ Python3 ml_data_analysis.py -f /data/Meteorite_Landings.csv
~~~

Or the second way non-interactive way. Run
~~~
$ docker run --rm -it -v $PWD/Meteorite_Landings.csv:/data/Meteorite_Landings.csv hieucannguyen/ml_data_analysis:1.0 ml_data_analysis.py -f /data/Meteorite_Landings.csv
~~~

Both methods should print this
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
