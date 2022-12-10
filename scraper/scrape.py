import logging.config
import os.path

import bs4.element
import requests
from bs4 import BeautifulSoup
import xml_parsing as xp
import database as db

logging.config.fileConfig('logging.conf')

logger = logging.getLogger(str(__file__).split('/')[-1])
logger.setLevel(logging.INFO)

"""
Goal is to collect data about multiple transportations systems

Collect data about:
  - Kid of transportation that is used
  - the destinations
  - departure times
  - arrival times
  - total travel time for each type of transportation
"""


class Commands:
    """
    Enumerated Type for using specific endpoints
    """
    agencyList = "agencyList"
    routeList = "routeList"
    routeConfig = "routeConfig"
    predictions = "predictions"


def get_command(command: str, agency_tag: str = None, route_tag: str = None, stop_id: str = None):
    """Returns an API endpoint for a given command. The additional tags and stop_id are used for the different commands.

    :param command:
    :param agency_tag:
    :param route_tag:
    :param stop_id:
    :return:
    :rtype:
    """
    url_command = f"https://retro.umoiq.com/service/publicXMLFeed?command={command}"
    if agency_tag:
        url_command = url_command + f"&a={agency_tag}"
    if stop_id:
        url_command = url_command + f"&stopId={stop_id}"
    if route_tag:
        url_command = url_command + f"&r={route_tag}"

    logger.debug(f"URL_COMMAND={url_command}")
    return url_command


def get_agencies() -> BeautifulSoup:
    """

    :return:
    :rtype:
    """
    page = requests.get(get_command(command=Commands.agencyList))
    soup = BeautifulSoup(page.content, "xml")
    logger.debug("Agencies:")
    logger.debug(soup.prettify())
    return soup


#  Create a for loop that goes through all the agencies and gets their routes
# Iterate through each agency to get routes, save these into database
def get_route_list(agency_tag: str) -> BeautifulSoup:
    """

    :param agency_tag:
    :return:
    :rtype:
    """
    page = requests.get(get_command(command=Commands.routeList, agency_tag=agency_tag))
    soup = BeautifulSoup(page.content, 'xml')
    logger.debug(f"Route List: a={agency_tag}")
    logger.debug(soup.prettify())
    return soup


# For each agency and route tag, go through and get the routeConfig. This is the extent of the route
def get_route_config(agency_tag: str, route_tag: str) -> BeautifulSoup:
    """

    :param agency_tag:
    :param route_tag:
    :return:
    :rtype:
    """
    page = requests.get(get_command(command=Commands.routeConfig, agency_tag=agency_tag, route_tag=route_tag))
    soup = BeautifulSoup(page.content, 'xml')
    logger.debug(f"Route Config: a={agency_tag},r={route_tag}")
    logger.debug(soup.prettify())
    return soup


def get_stops_from_route_config(route_config: BeautifulSoup) -> bs4.ResultSet:
    """

    :param route_config:
    :return:
    :rtype:
    """
    stops = route_config.find_all('stop')
    logger.debug("Stops")
    logger.debug(stops)
    return stops


# For each stop get the predictions. This is the departure and arrival predictions
def get_predictions(agency_tag: str, route_tag: str, stop_id: str) -> BeautifulSoup:
    """Returns the predictions for a given agency, route, and stop id

    :param str agency_tag: Agency tag name, not the title
    :param str route_tag: tag id extracted from route
    :param str stop_id: stop id extracted from stops / route config
    :return: Set of Predictions in XML format
    :rtype: BeautifulSoup
    """
    page = requests.get(get_command(
        command=Commands.predictions,
        agency_tag=agency_tag,
        route_tag=route_tag,
        stop_id=stop_id)
    )
    soup = BeautifulSoup(page.content, 'xml')
    logger.debug(f"Route Prediction: a={agency_tag},r={route_tag},stopId={stop_id}")
    logger.debug(soup.prettify())
    return soup


def extract_agency(agency_tag: str, xml_dir: str = 'data'):
    """Queries the API for an agency then walks the API to retrieve the routes, stops, and predicted arrival and
    departure times.

    :param agency_tag:
    :param xml_dir:
    :return:
    :rtype:
    """
    logger.info(f"Extracting information for Agency: {agency_tag}")
    agency_dir = f'{xml_dir}/{agency_tag}'
    if not os.path.isdir(agency_dir):
        os.mkdir(agency_dir)
    write_route_list(agency_tag)
    route_list_file = f'{agency_dir}/route_list.xml'
    if not os.path.isfile(route_list_file):
        logger.info(f"Downloading Route List: {agency_tag}")
        get_route_list(agency_tag)
    route_tags = xp.get_route_tags(xp.open_xml_file(route_list_file))

    for route_tag in route_tags:
        route_tag_dir = f'{agency_dir}/{route_tag["tag"]}'
        logger.info(f"Starting Route Config: {agency_tag} - {route_tag['tag']}")
        if not os.path.isdir(route_tag_dir):
            os.mkdir(route_tag_dir)
        if not os.path.isfile(f'{route_tag_dir}/route_config.xml'):
            logger.info(f"Downloading Route Config: {agency_tag} - {route_tag['tag']}")
            get_route_config(agency_tag, route_tag['tag'])
            write_route_config(agency_tag, route_tag['tag'])

    for route_name in os.listdir(agency_dir):
        if 'xml' in route_name:
            continue
        logger.debug(f'Agency Route List: {route_name}')
        route_config_xml = f'{agency_tag}/{route_name}/route_config.xml'
        logger.info(f"Parsing Route Config: {route_config_xml}")
        stops = xp.get_stops(xp.open_xml_file(f"./{xml_dir}/{route_config_xml}"))
        for stop in stops:
            prediction_dir = f'{xml_dir}/{agency_tag}/{route_name}/{stop["stopId"]}'
            if not os.path.isdir(prediction_dir):
                os.mkdir(prediction_dir)
            prediction_xml = f'{prediction_dir}/predictions.xml'
            if not os.path.isfile(prediction_xml):
                logger.info(f"Downloading Route Prediction: {agency_tag} - {route_name} - {stop['stopId']}")
                write_predictions(agency_tag=agency_tag, route_tag=route_name, stop_id=stop['stopId'])


def write_route_list(agency_tag, output_dir="data"):
    routes_list = get_route_list(agency_tag)
    with open(f'./{output_dir}/{agency_tag}/route_list.xml', 'w') as f:
        f.write(routes_list.prettify())


def write_route_config(agency_tag, route_tag, output_dir="data"):
    route_config_list = get_route_config(agency_tag, route_tag)
    with open(f'./{output_dir}/{agency_tag}/{route_tag}/route_config.xml', 'w') as f:
        f.write(route_config_list.prettify())


def write_predictions(agency_tag, route_tag, stop_id, output_dir="data"):
    predictions_list = get_predictions(agency_tag, route_tag, stop_id)

    with open(f'./{output_dir}/{agency_tag}/{route_tag}/{stop_id}_predictions.xml', 'w') as f:
        f.write(predictions_list.prettify())


def propagate_database(database_name: str, agency_dict: dict, data_dir: str = 'data'):
    agency_dir = f"{data_dir}/{agency_dict['tag']}"
    conn = db.create_connection(database_name)
    db.insert_agency_record(conn, agency_dict)
    cur = conn.cursor()
    result = cur.execute(f"SELECT * FROM Agencies WHERE tag = '{agency['tag']}'").fetchone()
    for root, dirs, files in os.walk(agency_dir):
        for filename in files:
            xml_file = os.path.join(root, filename)
            xml_object = xp.open_xml_file(xml_file)
            if 'route_list' in filename:
                logger.info(f"Reading Route List: {xml_file}")
                route_tags = xp.get_route_tags(xml_object)
                for route_tag in route_tags:
                    db.insert_route_record(conn, route_tag, result[0])
            elif 'route_config' in filename:
                logger.info(f"Reading Route Config: {xml_file}")
                route_tag = xml_file.split('/')[-2]
                stop_tags = xp.get_stops(xml_object)
                route_result = cur.execute(f"SELECT * FROM Routes WHERE tag = '{route_tag}' AND agency_id = "
                                           f"'{result[0]}'").fetchone()
                for stop in stop_tags:
                    db.insert_stop_record(conn, stop, result[0], route_result[0])

            elif 'prediction' in filename:
                logger.info(f"Reading Predictions: {filename}")
                stop_id = xml_file.split('/')[-2]
                stop_result = cur.execute(f"SELECT agency_id,  route_id, stop_id FROM Stops WHERE stop_id = '{stop_id}' "
                                          f"and agency_id = '{result[0]}'").fetchone()
                predictions = xp.get_prediction_tags(xml_object)
                if predictions:
                    for prediction in predictions:
                        db.insert_prediction_record(conn, prediction, stop_result[0], stop_result[1], stop_result[2])

    conn.close()


if __name__ == "__main__":
    """
    Setup
    ---
    I. Create Database
    II. Create connection
    III. Create Tables
    
    Data Ingestion
    ----
    1. get all agencies
        a. store agencies in a table
    2. get all agency tags from table
        a. select each agency tag and ID from table
        b. get route list for each agency tag & ID
        c. store each route list in a table
    3. get all routes from route table
        a. for each route, query for route config
        b. for each route config, store in sql db
        c. extract each stop information from route configs
    4. for each agency, route, route config, and stop id
        a. query prediction and route information
        b. this may Gor may not have arrival and departure times.
        
    Clean-up
    --------
    I. Close Connection
    """
    all_agencies = False

    agencies_xml = get_agencies()
    with open('data/agencies.xml', 'w') as f:
        f.write(agencies_xml.prettify())
    if all_agencies:
        # Only do this to get information on all agencies
        agencies = xp.open_xml_file('data/agencies.xml')
        for agency in agencies.body:
            if agency != '\n' and agency:
                extract_agency(agency['tag'])

    else:
        agency_name = 'lametro'
        agencies = xp.get_agency_tags(xp.open_xml_file('data/agencies.xml'))
        agency = [a for a in agencies if a['tag'] == agency_name][0]
        extract_agency(agency)
        database_file = 'final_project.db'
        db.create_tables(db.create_connection(database_file))
        propagate_database(database_file, agency)
