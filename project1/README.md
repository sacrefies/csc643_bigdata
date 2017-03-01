# The Project
This project is a experimental project which works with MongoDB.
All source is implemented in Python 2.7.

# To Run

## Initialization
1. You need a running MongoDB service
2. Import the json source data, ```zipcodes.json```, into your MongoDB.

## Configuration
1. Use any text editor open up ```settings.py``` and set appropriate values to the below variables:

```
# database related
DB_NAME = "zipcodes"
DB_PROTOCOL = "mongodb://"
DB_HOST = "localhost"
DB_PORT = "27017"
COLLECTION = "zipcodes"
```

## Run
To show the program results, use the following command in a terminal/cmd:

```# python queries.py```
