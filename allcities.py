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


def get_average_delay(conn):
    cur = conn.cursor()

    philly_delays = cur.execute('SELECT late*60 FROM Philadelphia WHERE late < 900').fetchall()
    # print(f"Philly Delays: {philly_delays}")

    phoenix_delays = cur.execute('SELECT delay FROM Phoenix').fetchall()
    # print(f"Phoenix Delays: {phoenix_delays}")

    atlanta_delays = cur.execute('SELECT delay FROM Atlanta').fetchall()

    atlanta_delays = [int(atl_delay[0].replace('T', '').replace('S', '')) for atl_delay in atlanta_delays]
    #print(f"Atlanta Delays: {atlanta_delays}")

    delay_sum = 0
    for pd in philly_delays:
        if pd[0] != 'null':
            delay_sum += int(pd[0])

    # Calculate average philly delay
    avg_philly_delay = delay_sum/len(philly_delays)

    delay_sum = 0
    for pd in phoenix_delays:
        if pd[0] != 'null':
            delay_sum += int(pd[0])
    # Calculate average phoenix delay
    avg_phoenix_delay = delay_sum/len(phoenix_delays)

        # Calculate average atlanta delay
    avg_atlanta_delay = sum(atlanta_delays)/len(atlanta_delays)


    with open('calculations.txt', 'w') as f:
        f.write(f"Average Philly delay = {avg_philly_delay}")
        f.write("\n")
        f.write(f"Average Phoenix delay = {avg_phoenix_delay}")
        f.write("\n")
        f.write(f"Average Atlanta delay = {avg_atlanta_delay}")


    return avg_philly_delay, avg_phoenix_delay

    # TODO: Use this return statement
    # return avg_philly_delay, avg_phoenix_delay, avg_atlanta_delay

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
    
def make_atlanta_destinations_table(cur, conn):
    destinations = ["AIRPORT", "DORAVILLE", "NORTH SPRINGS", "BANKHEAD", "CANDLER PARK", "HE HOLMES", "INDIAN CREEK"]
    for destination in destinations:
        cur.execute('INSERT OR IGNORE INTO Atlanta_Destinations (id, destination) VALUES (?, ?)', (destinations.index(destination), destination))
        
    conn.commit()

def make_atlanta_table(data, cur, conn, index):
    # cur.execute('DROP TABLE IF EXISTS Atlanta')
    # cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destinations TEXT, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, waiting_time TEXT, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')

    x = dict(data)
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
    
def amount_of_locations(cur, conn):
    cur.execute("SELECT destination FROM Atlanta_Destinations JOIN Atlanta ON destination_id = id")

    all_destinations = cur.fetchall()
    destinations_dict = {}
    for destination in all_destinations:
        destinations_dict[destination[0]] = destinations_dict.get(destination[0], 0) + 1
  
    print(destinations_dict)
    return(destinations_dict)
    # returns dict with destinations names and amount of destinations

def percentages(cur,conn):
    # pass
#['AIRPORT', 'NORTH SPRINGS', 'DORAVILLE', 'BANKHEAD', 'HE HOLMES', 'INDIAN CREEK']
    cur.execute("SELECT destination_id FROM Atlanta")
    airport = 0
    doraville = 0
    north_springs = 0
    bankhead = 0
    candler_park = 0
    he_holmes = 0
    indian_creek = 0

    
    x = cur.fetchall()
    
    for i in x: 
        a = i[0]
   
        if a == 0:
            airport += 1
        elif a == 1:
            doraville+=1
        elif a == 2:
            north_springs += 1
        elif a == 3:
            bankhead += 1
        elif a == 4:
            candler_park += 1
        elif a == 5:
            he_holmes += 1
        elif a == 6:
            indian_creek += 1
     
    l3 = []
    l3.append(airport/100)
    l3.append(doraville/100)
    l3.append(north_springs/100)
    l3.append(bankhead/100)
    l3.append(candler_park/100)
    l3.append(he_holmes/100)
    l3.append(indian_creek/100)
    print(l3)
    return l3

    # could count how many times going to the airport
    # percentages of where people went. 25% to airport. 10% to mall. etc. 
    # Could say that since it's not varied, transportation isnt varied. like, since not many options



def main():
    json_data = read_data('atlanta.json')
    json_data2 = read_data('septa.json')
    json_data3 = read_data('phoenix_trips.json')

    
    cur, conn = open_database('allcities.db')

    # Atlanta Table
    cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destination_id INTEGER, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, waiting_time TEXT, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')

    cur.execute('CREATE TABLE IF NOT EXISTS Atlanta_Destinations (id INTEGER, destination TEXT)')

    cur.execute("SELECT COUNT('destination') FROM Atlanta_Destinations ")
    d_count = cur.fetchall()
    d_count = (d_count[0])
    d_count = d_count[0]
    if d_count == 0:
        make_atlanta_destinations_table(cur, conn)

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
        make_atlanta_table(json_data, cur, conn, index)

    if count == 100:
        amount_of_locations(cur, conn)
        percentages(cur,conn)  



    # if count >= 100:
    #     cur.execute('DROP TABLE IF EXISTS Atlanta')
    #     cur.execute('DROP TABLE IF EXISTS Atlanta_Destinations')
    #     cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destinations TEXT, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, waiting_time TEXT, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')
    #     cur.execute('CREATE TABLE IF NOT EXISTS Atlanta_Destinations (destinations TEXT, train_id INTEGER, direction TEXT)')



    # Philadelphia Table
    cur.execute('CREATE TABLE IF NOT EXISTS Philadelphia (route TEXT, latitude INT, longitude INT, label INT, vehicle_id INT, block_id INT, direction TEXT, destination TEXT, offset INT, heading,late INT, original_late INT, offset_sec,trip INT, nextstop_id INT, nextstop_name TEXT, nextstop_sequence, estimated_seat_availability TEXT, timestamp INT)')

    cur.execute("SELECT COUNT('route') FROM Philadelphia ")
    count = cur.fetchall()
    count = (count[0])[0]

    index = count
    
    if index < 150:
        make_philadelphia_table(json_data2, cur, conn, index)

    
    #Phoenix Table
    cur.execute('CREATE TABLE IF NOT EXISTS Phoenix (rttu INT, trip_id INT, schedule_relationship TEXT, routeid INT, stop_sequence TEXT, delay TEXT, time TEXT, uncertainity TEXT, vehicle_id INT, timestamp INT)')
    

    cur.execute("SELECT COUNT('rttu') FROM Phoenix ")
    count = cur.fetchall()
    count = (count[0])[0]

    index = count
    
    if index < 150:
        make_phoenix_table(json_data3, cur, conn, index)


    get_average_delay(conn)

    #close database
    conn.close()



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
