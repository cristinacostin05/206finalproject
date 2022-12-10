import sqlite3
import logging

logger = logging.getLogger()


# ===================================================================================================================
# SQLite Code
# ===================================================================================================================
def create_connection(db_name) -> sqlite3.Connection:
    return sqlite3.connect(db_name)


def create_tables(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS 
        Agencies(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title VARCHAR UNIQUE, 
            tag VARCHAR UNIQUE, 
            region_title VARCHAR
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS 
        Routes(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tag INTEGER UNIQUE, 
            title VARCHAR, 
            agency_id INTEGER, 
            FOREIGN KEY (agency_id) 
                REFERENCES Agencies (id)
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS
        Stops(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stop_id INTEGER UNIQUE,
            tag INTEGER,
            title VARCHAR,
            agency_id INTEGER,
            route_id INTEGER,
            FOREIGN KEY (agency_id)
                REFERENCES Agencies (id),
            FOREIGN KEY (route_id)
                REFERENCES Routes (id)
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS
        Predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_tag INTEGER,
            direction TEXT,
            epoch_time INTEGER,
            minutes INTEGER,
            seconds INTEGER,
            vehicle TEXT,
            stop_id INTEGER,
            agency_id INTEGER,
            route_id INTEGER,
            FOREIGN KEY (agency_id)
                REFERENCES Agencies (id),
            FOREIGN KEY (route_id)
                REFERENCES Routes (id),
            FOREIGN KEY (stop_id)
                REFERENCES Stops (id)
        )""")
    conn.commit()
    conn.close()


def insert_agency_record(conn: sqlite3.Connection, agency: dict):
    cur = conn.cursor()
    result = cur.execute(f"SELECT * FROM Agencies WHERE tag = '{agency['tag']}'")
    if len(result.fetchone()) == 0:
        logger.info(f"Inserting Agency: {agency['tag']} into database.")
        cur.execute("INSERT INTO Agencies(title, tag, region_title) values(?, ?, ?)",
                    (agency['title'], agency['tag'], agency['regionTitle']))
        conn.commit()


def insert_route_record(conn: sqlite3.Connection, route: dict, agency_id: int):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Routes(tag, title, agency_id) values(?, ?, ?)",
                    (route['tag'], route['title'].replace(f"{route['tag']} ", ""), agency_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        logger.warning(f"{e}, {route['title']} already exists")


def insert_stop_record(conn: sqlite3.Connection, stop: dict, agency_id: int, route_id: int):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Stops(tag, stop_id, title, agency_id, route_id) values(?, ?, ?, ?, ?)",
                    (stop['tag'], stop['stopId'], stop['title'], agency_id, route_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        logger.warning(f"{e}, {stop['stopId']}:{stop['title']} already exists")


def insert_prediction_record(conn: sqlite3.Connection, prediction: dict, agency_id: int,
                             route_id: int, stop_id: int):
    cur = conn.cursor()
    try:
        """
            
        """
        cur.execute("INSERT INTO Predictions(trip_tag, direction, epoch_time, minutes, seconds, vehicle, stop_id, "
                    "agency_id, route_id) values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (prediction['trip_tag'], prediction['direction'], prediction['epoch_time'], prediction['minutes'],
                     prediction['seconds'], prediction['vehicle'], stop_id, agency_id, route_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        logger.warning(f"{e}, {prediction['trip_tag']}:{prediction['direction']} already exists")
