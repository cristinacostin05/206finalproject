import json
import unittest
import os
import requests



def write_json(cache_filename, dict):
    with open(cache_filename, 'w') as file:
        json_file = json.dumps(dict, indent=4)
        file.write(json_file)


def get_data_using_cache(url, filename):
    print(f"Fetching data for {filename}")
    data = requests.get(url)
    dict = json.loads(data.text)
    return dict



def main():
    #general info
    url = 'http://www3.septa.org/hackathon/TransitViewAll/'
    #locations
    url2 = 'http://www3.septa.org/hackathon/locations/get_locations.php?lon=-75.33299748&lat=40.11043326&radius=3' 
    #alert messages
    url3 = 'http://www3.septa.org/hackathon/Alerts/get_alert_data.php?req1=all'
    #detours
    url4 = 'http://www3.septa.org/hackathon/BusDetours/'



    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "septa.json"
    filename2 = "locations.json"
    filename3 = "alerts.json"
    filename4 = "detours.json"
    cache_filename = dir_path + '/' + filename
    cache_filename2 = dir_path + '/' + filename2
    cache_filename3 = dir_path + '/' + filename3
    cache_filename4 = dir_path + '/' + filename4
    
    #first cachefile
    dict = get_data_using_cache(url, filename)
    print(dict)
    write_json(cache_filename, dict)

    #second cachefile
    dict = get_data_using_cache(url2, filename2)
    write_json(cache_filename2, dict)

    #third cachefile
    dict = get_data_using_cache(url3, filename3)
    write_json(cache_filename3, dict)

    #fourth cachefile
    dict = get_data_using_cache(url4, filename4)
    write_json(cache_filename4, dict)


 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    # unittest.main(verbosity=2)
