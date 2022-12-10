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


def make_philadelphia_table(data, cur, conn, index):

    
    routes = data['routes'][0]
    route_names  = list(data['routes'][0].keys())

    new_list = []

    for names in route_names:
        current_route = routes[names]
        for i in range(0, len(current_route)):
            data_entry = []
            data_entry.append(names)
            data_entry.append(current_route[i])
            new_list.append(data_entry)

    
    for i in range(index, index+25):
        
        route = new_list[i][0]
        latitude = new_list[i][1]['lat']
        longitude = new_list[i][1]['lng']
        label = new_list[i][1]['label']
        vehicle_id = new_list[i][1]['VehicleID']
        block_id = new_list[i][1]['BlockID']
        direction = new_list[i][1]['Direction']
        destination = new_list[i][1]['destination']
        offset= new_list[i][1]['Offset']
        heading = new_list[i][1]['heading']
        late = new_list[i][1]['late']
        original_late = new_list[i][1]['original_late']
        offset_sec = new_list[i][1]['Offset_sec']
        trip = new_list[i][1]['trip']
        nextstop_id = new_list[i][1]['next_stop_id']
        nextstop_name = new_list[i][1]['next_stop_name']
        nextstop_sequence = new_list[i][1]['next_stop_sequence']
        estimated_seat_availability = new_list[i][1]['estimated_seat_availability']
        timestamp = new_list[i][1]['timestamp']

        
        cur.execute('INSERT OR IGNORE INTO Philadelphia (route, latitude, longitude, label, vehicle_id, block_id, direction, destination, offset, heading,late, original_late, offset_sec,trip, nextstop_id, nextstop_name, nextstop_sequence, estimated_seat_availability, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (route, latitude, longitude, label, vehicle_id, block_id, direction, destination, offset, heading,late, original_late, offset_sec,trip, nextstop_id, nextstop_name, nextstop_sequence, estimated_seat_availability, timestamp))

        conn.commit()
    



     
    # could count how many times going to the airport
    # percentages of where people went. 25% to airport. 10% to mall. etc. 
    # Could say that since it's not varied, transportation isnt varied. like, since not many options

def main():
    json_data = read_data('septa.json')
    cur, conn = open_database('philadelphia.db')

    cur.execute('CREATE TABLE IF NOT EXISTS Philadelphia (route TEXT, latitude INT, longitude INT, label INT, vehicle_id INT, block_id INT, direction TEXT, destination TEXT, offset INT, heading,late INT, original_late INT, offset_sec,trip INT, nextstop_id INT, nextstop_name TEXT, nextstop_sequence, estimated_seat_availability TEXT, timestamp INT)')

    cur.execute("SELECT COUNT('route') FROM Philadelphia ")
    count = cur.fetchall()
    count = (count[0])[0]

    index = count
    
    if index < 325:
        make_philadelphia_table(json_data, cur, conn, index)
    conn.close()


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
