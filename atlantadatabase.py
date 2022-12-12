import unittest
import sqlite3
import json
import plotly.graph_objects as go
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

def visualizataion_atlanta(cur, conn):
    loc = amount_of_locations(cur, conn)
    percents = percentages(cur,conn)  
    fig = go.Figure(data = [go.Bar(name = "Atlanta", x = loc, y= percents, marker_color = 'rgb(0, 0, 0)')])
    fig.show()

def main():
    json_data = read_data('atlanta.json')
    cur, conn = open_database('atlanta_db.db')
    # cur.execute('DROP TABLE IF EXISTS Atlanta')
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
    #     amount_of_locations(cur, conn)
    #     percentages(cur,conn)  
    #     visualizataion_atlanta(cur,conn)
    #     cur.execute('DROP TABLE IF EXISTS Atlanta')
    #     cur.execute('DROP TABLE IF EXISTS Atlanta_Destinations')
    #     cur.execute('CREATE TABLE IF NOT EXISTS Atlanta (destinations TEXT, directions TEXT, event_times TEXT, head_sign TEXT, line TEXT, next_arr TEXT, station TEXT, train_id INTEGER, waiting_second INTEGER, waiting_time TEXT, responsetimestamp DOUBLE, vehiclelongitude DOUBLE, vehiclelatitude DOUBLE, delay TEXT)')
    #     cur.execute('CREATE TABLE IF NOT EXISTS Atlanta_Destinations (id INT, destinations TEXT)')





    
    conn.close()
    


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)