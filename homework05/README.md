# ISS Tracker Flask Application: Containerized with Docker
The ISS Tracker Flask Application builds on homework04 making it a web application capable of querying and retrieving insightful information from the ISS dataset.

Must have [Docker](https://docs.docker.com/get-docker/) installed on your system.

## ISS Data Overview
The [ISS Trajectory Data website](https://spotthestation.nasa.gov/trajectory_data.cfm) provides access to data available in both plain text and XML formats. These datasets contain ISS state vectors spanning a 15-day period. State vectors include Cartesian vectors for position {X, Y, Z} and velocity {X_DOT, Y_DOT, Z_DOT}, along with timestamps (EPOCH), describing the complete state of the ISS relative to Earth, based on the J2000 reference frame.

## File Descriptions
- [Dockerfile](Dockerfile) Dockerfile to generate docker image of our application
- [docker-compose.yml](docker-compose.yml) docker-compose file to run the containerized Flask application
- [requirements.txt](requirements.txt) required dependencies for the project
- [iss_tracker.py](iss_tracker.py) Script to process the ISS dataset
- [test_iss_tracker.py](test_iss_tracker.py) Unit tests for ISS data processing
- [app.py](app.py) Flask application for API endpoints

## Software Diagram
![image](hw5_software_diagram.svg)

*Software diagram of the Flask Application. Visualization of the application workflow using Docker and how to API endpoints interact between the code and web server.*

## Docker: build the image
Navigate into the directory where our app, Dockerfile, and docker-compose.yml are located.

Run 
~~~
$ docker build -t username/iss_tracker_app:1.0 .
~~~

## Docker: Run Flask Application Container
Using the [docker-compose.yml](docker-compose.yml) file we can run it to start the Flask application container
~~~
$ docker-compose up -d
~~~
**Note:** -d starts the application in the background

Since we mapped to port 5000 in the [docker-compose.yml](docker-compose.yml) to interact with the Flask microservices we can use `curl`
### API Endpoints
| Example usage                        | Method | Output                                                             |
|------------------------------|--------|-------------------------------------------------------------------------|
| localhost:5000/epochs                      | GET    | Returns the entire data set of epochs.                                  |
| localhost:5000/epochs?limit=2&offset=3 | GET    | Returns a modified list of epochs based on query parameters for pagination. |
| localhost:5000/epochs/<epoch>              | GET    | Returns state vectors for a specific epoch from the data set.           |
| localhost:5000/epochs/<epoch>/speed        | GET    | Returns instantaneous speed for a specific epoch in the data set. (Math required!) |
| localhost:5000/now                         | GET    | {
  "EPOCH": "2024-058T01:26:32.672Z",
  "Speed (km/s)": 7.657973107188885,
  "X": {
    "#text": "-1853.7367198354",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-6.5416079487151402",
    "@units": "km/s"
  },
  "Y": {
    "#text": "5134.78947360452",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "0.72374511091354998",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-4048.5531539581202",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "3.91511309800417",
    "@units": "km/s"
  }
} |


## Run unit tests
In the working directory run
~~~
$ pytest
~~~