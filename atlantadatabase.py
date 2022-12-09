import unittest
import sqlite3
import json
import os


def read_data(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


def make_atlanta_table(data, cur, conn):
    x = dict(data)
    x = x['RailArrivals']
    l = []
    for i in x:
        l.append(i)


    cur.execute('DROP TABLE IF EXISTS Atlanta')
    cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destinations TEXT, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')

    for i in l:
        current_destinations = list(i.values())[0]
        current_directions = list(i.values())[1]
        current_event_times = list(i.values())[2]
        current_head_sign = list(i.values())[3]
        current_line = list(i.values())[4]
        current_next_arr = list(i.values())[5]
        current_station = list(i.values())[6]
        current_train_id= list(i.values())[7]
        current_waiting_seconds = list(i.values())[8]
        current_responsetimestamp = list(i.values())[9]
        current_vehiclelongitude = list(i.values())[10]
        current_vehiclelatitude = list(i.values())[11]
        current_delay = list(i.values())[12]
        cur.execute('INSERT OR IGNORE INTO Atlanta (destinations, directions, event_times, head_sign, line, next_arr,station, train_id, waiting_second, responsetimestamp, vehiclelongitude, vehiclelatitude, delay) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (current_destinations, current_directions, current_event_times, current_head_sign, current_line, current_next_arr, current_station, current_train_id, current_waiting_seconds, current_responsetimestamp, current_vehiclelongitude, current_vehiclelatitude, current_delay))
    
    conn.commit()


     
    # could count how many times going to the airport
    # percentages of where people went. 25% to airport. 10% to mall. etc. 
    # Could say that since it's not varied, transportation isnt varied. like, since not many options

def main():
    json_data = read_data('atlanta.json')
    cur, conn = open_database('atlanta_db.db')
    make_atlanta_table(json_data, cur, conn)
    conn.close()


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
