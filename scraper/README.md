# Project Readme

## Project Description

When running the application, it will only hit a single endpoint once entirely. 
It stores the results of each API request into an XML file that is used for parsing and storing the data
into the SQL database.

## Data Directory Format

```shell
data
|-- agency
    |-- route
        |-- route information / stops
            |-- Arrival and Departure Prediction Times
------
data
|-- ccrta
|-- jhu-apl
|-- lametre               # Agency
    |-- route_list.xml    # Agency Routes
    |-- 10                # Specific Route
    |-- 102
    |-- 105
        |-- route_config.xml  # Route Information / Stops
        |-- 04251
        |-- 04908
            |-- predictions.xml # Predicted Arrival and Departure times
 ...
```