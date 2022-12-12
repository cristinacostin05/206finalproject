import unittest
import sqlite3
import json
import plotly.graph_objects as go
import os


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def print_calculations(cur, conn, filename):
    delays = get_average_delay(conn)
    avg_philly_delay = delays[0]
    avg_phoenix_delay = delays[1]
    avg_atlanta_delay = delays[2]

    percentage = percentages(cur, conn)[1]

    atlanta_locations_amount = atlanta_amount_of_locations(cur, conn)[1]

    with open(filename, 'w') as f:
        f.write(f"Average Train Delay Calculations\n")
        f.write("----------------------------------\n")
        f.write(f"Average Philly delay = {avg_philly_delay} seconds\n")
        f.write(f"Average Phoenix delay = {avg_phoenix_delay} seconds\n")
        f.write(f"Average Atlanta delay = {avg_atlanta_delay} seconds\n")

        f.write("\n")

        f.write("\nLocations Visited in Atlanta Calculations\n")
        f.write("-----------------------------------------------------\n")
        f.write(str(atlanta_locations_amount[0]) + " of train transports in Atlanta went to Doraville.")
        f.write("\n")
        f.write(str(atlanta_locations_amount[1]) + " of train transports in Atlanta went to Doraville.")
        f.write("\n")
        f.write(str(atlanta_locations_amount[2]) + " of train transports in Atlanta went to North Springs.")
        f.write("\n")
        f.write(str(atlanta_locations_amount[3]) + " of train transports in Atlanta went to Bankhead.")
        f.write("\n")
        f.write(str(atlanta_locations_amount[4]) + " of train transports in Atlanta went to Candler Park.")
        f.write("\n")
        f.write(str(atlanta_locations_amount[5]) + " of train transports in Atlanta went to He Holmes.")
        f.write("\n")
        f.write(str(atlanta_locations_amount[6]) + " of train transports in Atlanta went to Indian Creek.\n")

        f.write("\n")


        f.write("\nPercentages of locations visited by train in Atlanta Calculations\n")
        f.write("-----------------------------------------------------\n")
        f.write(str(percentage[0]) + " of train transportation in Atlanta went to the Airport.")
        f.write("\n")
        f.write(str(percentage[1]) + " of train transportation in Atlanta went to Doraville.")
        f.write("\n")
        f.write(str(percentage[2]) + " of train transportation in Atlanta went to North Springs.")
        f.write("\n")
        f.write(str(percentage[3]) + " of train transportation in Atlanta went to Bankhead.")
        f.write("\n")
        f.write(str(percentage[4]) + " of train transportation in Atlanta went to Candler Park.")
        f.write("\n")
        f.write(str(percentage[5]) + " of train transportation in Atlanta went to He Holmes.")
        f.write("\n")
        f.write(str(percentage[6]) + " of train transportation in Atlanta went to Indian Creek.")



def get_average_delay(conn):
    cur = conn.cursor()

    philly_delays = cur.execute('SELECT late*60 FROM Philadelphia WHERE late < 900').fetchall()

    phoenix_delays = cur.execute('SELECT delay FROM Phoenix').fetchall()

    atlanta_delays = cur.execute('SELECT delay FROM Atlanta').fetchall()

    atlanta_delays = [int(atl_delay[0].replace('T', '').replace('S', '')) for atl_delay in atlanta_delays]

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
        f.write(f"Average Train Delay Calculations\n")
        f.write("----------------------------------\n")
        f.write(f"Average Philly delay = {avg_philly_delay}\n")
        f.write(f"Average Phoenix delay = {avg_phoenix_delay}\n")
        f.write(f"Average Atlanta delay = {avg_atlanta_delay}\n")


    return avg_philly_delay, avg_phoenix_delay, avg_atlanta_delay


def delay_visualization(conn): 
    x = get_average_delay(conn)
    avg_philly_delay = x[0]
    avg_phoenix_delay = x[1]
    avg_atlanta_delay = x[2]
    fig = go.Figure(data = [go.Bar(name = "Delays", x = ["Philadelphia", "Phoenix", "Atlanta"], y = [ avg_philly_delay, avg_phoenix_delay, avg_atlanta_delay], marker_color = 'rgb(15, 30, 70)')])

    fig.update_layout(
        title="Average Train Delays",
        xaxis_title="Cities",
        yaxis_title="Average Time (seconds)",
        font=dict(
            family="Palatino",
            size = 18
        )
    )
    
    fig.show()


def philadelphia_seat_availability(cur, conn):
    cur.execute("SELECT estimated_seat_availability FROM Philadelphia")

    seats_availbility = cur.fetchall()
    seats_dict = {}
    for seats in seats_availbility:
        seats_dict[seats[0]] = seats_dict.get(seats[0], 0) + 1

    seats = []
    amounts = []
    for keys in seats_dict.keys():
        seats.append(keys)

    for values in seats_dict.values():
        amounts.append(values)


    return(seats, amounts)


def seat_availability_graph(cur, conn):
    seats = philadelphia_seat_availability(cur, conn)[0]
    amounts = philadelphia_seat_availability(cur, conn)[1]
    fig = go.Figure(data=[go.Pie(labels=seats, values = amounts)])

    
    fig.update_layout(
        title="Philadelphia Train Seat Availability",
        font=dict(
            family="Palatino",
            size = 18
        )
    )
    fig.show()

def philly_amount_of_locations(cur, conn):
    cur.execute("SELECT destination FROM Philadelphia")

    all_destinations = cur.fetchall()
    destinations_dict = {}
    for destination in all_destinations:
        destinations_dict[destination[0]] = destinations_dict.get(destination[0], 0) + 1
  
    locations = []
    amounts = []
    for keys in destinations_dict.keys():
        locations.append(keys)

    for values in destinations_dict.values():
        amounts.append(values)


    return(locations, amounts)

def philly_amount_pie_chart(cur, conn):
    locations = philly_amount_of_locations(cur, conn)[0]
    amounts = philly_amount_of_locations(cur, conn)[1]
    fig = go.Figure(data = [go.Bar(name = "Philadelphia", x = locations, y= amounts, marker_color = 'rgb(0, 0, 0)')])

    fig.update_layout(
    title="Philadelphia Locations Visited",
    xaxis_title="Location Names",
    yaxis_title="Number of Visits",
    font=dict(
        family="Palatino",
        )
    )
    
    fig.show()

def atlanta_amount_of_locations(cur, conn):
    cur.execute("SELECT destination FROM Atlanta_Destinations JOIN Atlanta ON destination_id = id")

    all_destinations = cur.fetchall()
    destinations_dict = {}
    for destination in all_destinations:
        destinations_dict[destination[0]] = destinations_dict.get(destination[0], 0) + 1
  
    locations = []
    amounts = []
    for keys in destinations_dict.keys():
        locations.append(keys)

    for values in destinations_dict.values():
        amounts.append(values)


    return(locations, amounts)


def visualization_atlanta(cur, conn):
    locations = atlanta_amount_of_locations(cur, conn)[0]
    percents = atlanta_amount_of_locations(cur,conn)[1]
    fig = go.Figure(data = [go.Bar(name = "Atlanta", x = locations, y= percents, marker_color = 'rgb(76, 0, 153)')])

    fig.update_layout(
    title="Frequency of Locations Visited in Atlanta",
    xaxis_title="Location Names",
    yaxis_title="Number of Visits",
    font=dict(
        family="Palatino",
        size=18
        )
    )
    fig.show()


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
     
    percentage = []
    percentage.append(airport/100)
    percentage.append(doraville/100)
    percentage.append(north_springs/100)
    percentage.append(bankhead/100)
    percentage.append(candler_park/100)
    percentage.append(he_holmes/100)
    percentage.append(indian_creek/100)

    locations = atlanta_amount_of_locations(cur, conn)[0]

    return (locations, percentage)



    
def main():


    cur, conn = open_database('allcities.db')

    seat_availability_graph(cur, conn)
    philly_amount_pie_chart(cur, conn)
    visualization_atlanta(cur, conn)
    delay_visualization(conn)

    print_calculations(cur, conn, 'calculations.txt')
    
    #close database
    conn.close()



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)