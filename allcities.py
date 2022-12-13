import unittest
import sqlite3
import json
import plotly.graph_objects as go
import requests
import os



def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


def make_philadelphia_table(cur, conn, index):
    url = 'http://www3.septa.org/hackathon/TransitViewAll/'
    data = requests.get(url)
    dict_philly = json.loads(data.text)
    
    
    routes = dict_philly['routes'][0]
    route_names  = list(dict_philly['routes'][0].keys())

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
    
def make_atlanta_id_tables(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Atlanta_Destinations (id INTEGER, destination TEXT)')

    destinations = ["AIRPORT", "DORAVILLE", "NORTH SPRINGS", "BANKHEAD", "CANDLER PARK", "HE HOLMES", "INDIAN CREEK"]
    for destination in destinations:
        cur.execute('INSERT OR IGNORE INTO Atlanta_Destinations (id, destination) VALUES (?, ?)', (destinations.index(destination), destination))
        
    conn.commit()


def make_atlanta_table(cur, conn, index):
    API_KEY = "da120556-3e37-4b74-9483-63d328069285"
    url = f'https://developerservices.itsmarta.com:18096/railrealtimearrivals?apiKey={API_KEY}'
    data = requests.get(url)
    dict_atlanta = json.loads(data.text)


    x = dict(dict_atlanta)
    x = x['RailArrivals']
    l = []
    for i in x:
        l.append(i)

    cur.execute("SELECT destination FROM Atlanta_Destinations")
    types = cur.fetchall()
    destination_list = []
    for type in types:
        destination_list.append(type[0])
    
    
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
        current_waiting_time= list(l[i].values())[9]
        current_responsetimestamp = list(l[i].values())[10]
        current_vehiclelongitude = list(l[i].values())[11]
        current_vehiclelatitude = list(l[i].values())[12]
        current_delay = list(l[i].values())[13]

        destination_id = destination_list.index(current_destinations)
        
    
        cur.execute('INSERT OR IGNORE INTO Atlanta (destination_id, directions, event_times, head_sign, line, next_arr,station, train_id, waiting_second, waiting_time, responsetimestamp, vehiclelongitude, vehiclelatitude, delay) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (destination_id, current_directions, current_event_times, current_head_sign, current_line, current_next_arr, current_station, current_train_id, current_waiting_seconds, current_waiting_time, current_responsetimestamp, current_vehiclelongitude, current_vehiclelatitude, current_delay))        

    conn.commit()

    

def make_phoenix_table(cur, conn, index):
    API_KEY = '4f22263f69671d7f49726c3011333e527368211f'
    url = f'https://mna.mecatran.com/utw/ws/gtfsfeed/realtime/valleymetro?apiKey={API_KEY}&asJson=true'
    data = requests.get(url)
    dict_phoenix = json.loads(data.text)


    routes = dict_phoenix['entity']

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
    

def main():
    
    cur, conn = open_database('allcities.db')

    # Atlanta Table
    cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destination_id INTEGER, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, waiting_time TEXT, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Atlanta_Destinations (id INTEGER, destination TEXT)')

    cur.execute("SELECT COUNT('destination') FROM Atlanta_Destinations ")
    d_count = cur.fetchall()
    d_count = (d_count[0])
    d_count = d_count[0]
    if d_count == 0:
        make_atlanta_id_tables(cur, conn)

    cur.execute("SELECT COUNT('destination_id') FROM Atlanta ")
    count = cur.fetchall()
    count = (count[0])
    count = count[0]
    if count < 100:
        cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destination_id TEXT, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, waiting_time TEXT, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')

       


        index = 0
        if count== 25:
            index= 25
        elif count == 50:
            index = 50
        elif count == 75:
            index = 75
            
        else:
            x = 0
        make_atlanta_table(cur, conn, index)




    # Philadelphia Table
    cur.execute('CREATE TABLE IF NOT EXISTS Philadelphia (route TEXT, latitude INT, longitude INT, label INT, vehicle_id INT, block_id INT, direction TEXT, destination TEXT, offset INT, heading,late INT, original_late INT, offset_sec,trip INT, nextstop_id INT, nextstop_name TEXT, nextstop_sequence, estimated_seat_availability TEXT, timestamp INT)')
    

    cur.execute("SELECT COUNT('route') FROM Philadelphia ")
    count = cur.fetchall()
    count = (count[0])[0]

    index = count
    
    if index < 150:
        make_philadelphia_table(cur, conn, index)

    
    #Phoenix Table
    cur.execute('CREATE TABLE IF NOT EXISTS Phoenix (rttu INT, trip_id INT, schedule_relationship TEXT, routeid INT, stop_sequence TEXT, delay TEXT, time TEXT, uncertainity TEXT, vehicle_id INT, timestamp INT)')
    

    cur.execute("SELECT COUNT('rttu') FROM Phoenix ")
    count = cur.fetchall()
    count = (count[0])[0]

    index = count
    
    if index < 150:
        make_phoenix_table(cur, conn, index)



    #close database
    conn.close()



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
