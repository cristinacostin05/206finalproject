import json
import unittest
import os
import requests

API_KEY = "da120556-3e37-4b74-9483-63d328069285"

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
    url = f'https://developerservices.itsmarta.com:18096/railrealtimearrivals?apiKey={API_KEY}'

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "atlanta.json"
    cache_filename = dir_path + '/' + filename
    
    #first cachefile
    dict = get_data_using_cache(url, filename)
    write_json(cache_filename, dict)


if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    # unittest.main(verbosity=2)