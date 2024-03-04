## Hotel Room Booking Engine

This is a simplified version of a reservation engine for a hotel.
The project was designed around the `availability` functionality, since it is the main scope of the
project.

### Endpoints

For the scope of this project, there is one endpoint available:

`get_availability`

This endpoint simply returns the availability of rooms based on the input parameters.
The input parameters are:

| Parameter | Description |
| ------- | ----------- |
| check_in | A string representation of the check in date |
| nights | Number of nights to stay |
| adults | Number of adults |
| children | [Optional] Number of children |
| infants | [Optional] Number of infants |

### Initialization

Upon the initialization of the app, a SQLite database is created (if it doesn't exist already), and 
the necessary tables are created.

There is an option to populate the database with dummy data for testing purposes. Dummy data 
includes a hotel entity, rooms and reservations for each room (randomized). The data also includes
photos.

In order to do this:

Open the `.env` file and ensure the variable `POPULATE_DUMMY_HOTEL_DATA` is set to True.
The function that populates the dummy data is located in `booking_engine/utility/initiate_functions.py`.

### Running the app

The app runs on localhost port 8000.
In order to run the main app, open a terminal in the project root directory and run the following 
commands:

#### Windows

It is recommended you create a virtual environment:

`python -m venv venv`

Install requirements:

`pip install -r requirements.txt`

Run the app:

`python main.py`

#### Linux / Mac OS

It is recommended you create a virtual environment:

`python3 -m venv venv`

Install requirements:

`pip3 install -r requirements.txt`

Run the app:

`python3 main.py`

#### Docker

The code is dockerized and ready to be run via docker-compose:

Build the image:

`docker build -t api_v1 .`

Run docker-compose:

`docker-compose up`

Run in the background:

`docker-compose up -d`

### Testing

There are unit tests in the code with the purpose of testing the `get_availability` functionality.

In order to run the tests, simply open a terminal/command prompt in the root directory of the 
project and run the following command:

`pytest`

A test Database is created (if not exists) in order to seperate the test data from the app data.

### Tech Stack

- Python 3.8
- FastAPI
- SQLite
- Peewee ORM
- Pytest
- Docker