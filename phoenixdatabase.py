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


def make_phoenix_table(data, cur, conn, index):

    routes = data['entity']

    new_list = []

    for i in range(0, len(routes)):
        data_entry = []
        rttu0 = routes[i]['id']
        trip_id0 = routes[i]['tripUpdate']['trip']['tripId']
        schedule_relationship0 = routes[i]['tripUpdate']['trip']['scheduleRelationship']
        routeid0 = routes[i]['tripUpdate']['trip']['routeId']

        if 'stopTimeUpdate' in routes[i]['tripUpdate']:
            stop_sequence0 = routes[i]['tripUpdate']['stopTimeUpdate'][0]['stopSequence']
            if 'arrival' in routes[i]['tripUpdate']['stopTimeUpdate'][0]:
                delay0 = routes[i]['tripUpdate']['stopTimeUpdate'][0]['arrival']['delay']
                time0 = routes[i]['tripUpdate']['stopTimeUpdate'][0]['arrival']['time']
                uncertainity0 = routes[i]['tripUpdate']['stopTimeUpdate'][0]['arrival']['uncertainty']
            else:
                delay0 = "null"
                time0 = "null"
                uncertainity0 = "null"
        else:
            stop_sequence0 = "null"
            delay0 = "null"
            time0 = "null"
            uncertainity0 = "null"

        vehicle_id0 = routes[0]['tripUpdate']['vehicle']['id']
        timestamp0 = routes[i]['tripUpdate']['timestamp']

        data_entry.append(rttu0)
        data_entry.append(trip_id0)
        data_entry.append(schedule_relationship0)
        data_entry.append(routeid0)
        data_entry.append(stop_sequence0)
        data_entry.append(delay0)
        data_entry.append(time0)
        data_entry.append(uncertainity0)
        data_entry.append(vehicle_id0)
        data_entry.append(timestamp0)
        new_list.append(data_entry)

    for i in range(index, index+25):
        
        rttu = new_list[i][0]
        trip_id = new_list[i][1]
        schedule_relationship = new_list[i][2]
        routeid = new_list[i][3]
        stop_sequence = new_list[i][4]
        delay = new_list[i][5]
        time = new_list[i][6]
        uncertainity = new_list[i][7]
        vehicle_id = new_list[i][8]
        timestamp = new_list[i][9]
        
        cur.execute('INSERT OR IGNORE INTO Phoenix (rttu, trip_id, schedule_relationship, routeid, stop_sequence, delay, time, uncertainity, vehicle_id, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (rttu, trip_id, schedule_relationship, routeid, stop_sequence, delay, time, uncertainity, vehicle_id, timestamp))

        conn.commit()
    



     
    # could count how many times going to the airport
    # percentages of where people went. 25% to airport. 10% to mall. etc. 
    # Could say that since it's not varied, transportation isnt varied. like, since not many options

def main():
    json_data3 = read_data('phoenix_trips.json')
    cur, conn = open_database('phoenix.db')
    
    cur.execute('CREATE TABLE IF NOT EXISTS Phoenix (rttu INT, trip_id INT, schedule_relationship TEXT, routeid INT, stop_sequence TEXT, delay TEXT, time TEXT, uncertainity TEXT, vehicle_id INT, timestamp INT)')
    

    cur.execute("SELECT COUNT('rttu') FROM Phoenix ")
    count = cur.fetchall()
    count = (count[0])[0]

    index = count
    
    if index < 323:
        make_phoenix_table(json_data3, cur, conn, index)
    conn.close()


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
