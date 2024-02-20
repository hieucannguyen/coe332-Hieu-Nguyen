# ISS Tracker: Containerized with Docker
The ISS Tracker project aims to streamline the process of accessing and analyzing positional and velocity data for the International Space Station (ISS).

Must have [Docker](https://docs.docker.com/get-docker/) installed on your system.

## ISS Data Overview
The [ISS Trajectory Data website](https://spotthestation.nasa.gov/trajectory_data.cfm) provides access to data available in both plain text and XML formats. These datasets contain ISS state vectors spanning a 15-day period. State vectors include Cartesian vectors for position {X, Y, Z} and velocity {X_DOT, Y_DOT, Z_DOT}, along with timestamps (EPOCH), describing the complete state of the ISS relative to Earth, based on the J2000 reference frame.

## File Descriptions
- [Dockerfile](Dockerfile) Dockerfile to generate docker image of our application
- [iss_tracker.py](iss_tracker.py) Script to process the ISS dataset
- [test_iss_tracker.py](test_iss_tracker.py) Unit tests for ISS data processing

## Docker: build the image
Navigate into the directory where our scripts and Dockerfile are located.

Run 
~~~
$ docker build -t username/iss_tracker:1.0 .
~~~

## Docker: Run the analysis
There are two ways to run the analysis. First, you can use the interactive mode
~~~
$ docker run --rm -it \
hieucannguyen/iss_tracker:1.0 bin/bash
~~~
then run the executable in the root directory
~~~
root@6fd3cddccea2:/# iss_tracker.py
~~~

Or the second non-interactive way. Run
~~~
$ docker run --rm \
hieucannguyen/iss_tracker:1.0 \
iss_tracker.py
~~~

Both methods should print something similar to this
~~~
ISS SUMMARY

DATE RANGE:
        - 02/16/2024 - 03/02/2024: 15 days

CURRENT STATUS
        - Date/Time: 2024-02-19 22:18:00
        - Coordinates: (961.53855075479203, -4163.0250987990703, 5275.7869654098504) km
        - Velocity vector: (7.58500648215235, 0.75420425895754994, -0.78481222830526998) km/s
        - Speed: 7.662706938949209 km/s

AVERAGE SPEED: 7.6589224391625175 km/s
~~~

## Docker: run unit tests
Using interactive mode
~~~
$ docker run --rm -it \
hieucannguyen/iss_tracker:1.0 bin/bash
~~~

Navigate to code directory and run pytest
~~~
root@68238597887a:/# cd code/
~~~
~~~
root@68238597887a:/code# pytest
~~~
