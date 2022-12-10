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


def make_atlanta_table(data, cur, conn, index):

    x = dict(data)
    x = x['RailArrivals']
    l = []
    for i in x:
        l.append(i)


    
    for i in range(index, index+25):
        
        current_destinations = list(l[i].values())[0]
        current_directions = list(l[i].values())[1]
        current_event_times = list(l[i].values())[2]
        current_head_sign = list(l[i].values())[3]
        current_line = list(l[i].values())[4]
        current_next_arr = list(l[i].values())[5]
        current_station = list(l[i].values())[6]
        current_train_id= list(l[i].values())[7]
        current_waiting_seconds = list(l[i].values())[8]
        current_responsetimestamp = list(l[i].values())[9]
        current_vehiclelongitude = list(l[i].values())[10]
        current_vehiclelatitude = list(l[i].values())[11]
        current_delay = list(l[i].values())[12]
    
        cur.execute('INSERT OR IGNORE INTO Atlanta (destinations, directions, event_times, head_sign, line, next_arr,station, train_id, waiting_second, responsetimestamp, vehiclelongitude, vehiclelatitude, delay) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (current_destinations, current_directions, current_event_times, current_head_sign, current_line, current_next_arr, current_station, current_train_id, current_waiting_seconds, current_responsetimestamp, current_vehiclelongitude, current_vehiclelatitude, current_delay))
        cur.execute('INSERT OR IGNORE INTO Atlanta_Destinations (train_id, destinations, direction) VALUES (?, ?, ?)', (current_train_id, current_destinations, current_directions))

   
    

    conn.commit()
    amount_of_locations(cur, conn)


def amount_of_locations(cur, conn):
    cur.execute("SELECT train_id, destinations, direction FROM Atlanta_Destinations")
    l1 = cur.fetchall()
    lengthofl1 = len(l1)
    l2 = []
    for i in l1:
        print(i[1])
        if i[1] not in l2:
            l2.append(i[1])
    print(len(l2))
    return len(l2)


     
    # could count how many times going to the airport
    # percentages of where people went. 25% to airport. 10% to mall. etc. 
    # Could say that since it's not varied, transportation isnt varied. like, since not many options

def main():
    json_data = read_data('atlanta.json')
    cur, conn = open_database('atlanta_db.db')
    cur.execute("SELECT COUNT('destinations') FROM Atlanta ")
    count = cur.fetchall()
    count = (count[0])
    count = count[0]
    if count <= 100:
        cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destinations TEXT, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS Atlanta_Destinations (train_id INTEGER, destinations TEXT, direction TEXT)')

        index = 0
        if count== 25:
            index= 25
        elif count == 50:
            index = 50
        elif count == 75:
            index = 75
        else:
            x = 0
        make_atlanta_table(json_data, cur, conn, index)

    if count >= 100:
        cur.execute('DROP TABLE IF EXISTS Atlanta')
        cur.execute('DROP TABLE IF EXISTS Atlanta_Destinations')
        cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destinations TEXT, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS Atlanta_Destinations (destinations TEXT, train_id INTEGER, direction TEXT)')

    conn.close()


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
