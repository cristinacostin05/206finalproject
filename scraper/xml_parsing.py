from bs4 import BeautifulSoup


# ===================================================================================================================
# BeautifulSoup and XML parsing
# ===================================================================================================================
def open_xml_file(xml_file_name):
    with open(xml_file_name) as fp:
        soup = BeautifulSoup(fp, 'xml')
    return soup


def get_agency_tags(soup: BeautifulSoup) -> [dict]:
    """Extracts the Agency tag, title, and region title from the XML/HTML using BeautifulSoup"""
    return [{'tag': agency['tag'], 'title': agency['title'], 'regionTitle': agency['regionTitle']} for agency in
            soup.body if agency != '\n']


def get_route_tags(soup: BeautifulSoup) -> [dict]:
    """Extracts the route tag and title of the route from the XML/HTML using BeautifulSoup"""
    return [{'tag': route['tag'], 'title': route['title']} for route in soup.body if route != '\n']


def get_stops(soup: BeautifulSoup) -> [dict]:
    route = soup.body.route
    return [{
        'tag': stop['tag'],
        'title': stop['title'],
        'stopId': stop['stopId']
    } for stop in route if route != '\n'
                           and stop is not None
                           and stop.name
                           and stop.name == 'stop'
                           and stop.has_attr('stopId')]


def get_prediction_tags(soup: BeautifulSoup) -> [dict]:
    predictions_tag = soup.body.predictions
    predictions = []
    if not predictions_tag.has_attr('dirTitleBecauseNoPredictions'):
        direction_title = predictions_tag.direction['title']
        for prediction in predictions_tag.direction:
            if prediction != '\n':
                predictions.append({
                    'trip_tag': prediction['tripTag'],
                    'direction': direction_title,
                    'epoch_time': prediction['epochTime'],
                    'minutes': prediction['minutes'],
                    'seconds': prediction['seconds'],
                    'vehicle': prediction['vehicle']
                })

    return predictions
