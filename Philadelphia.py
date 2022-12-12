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


    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "philadelphia.json"

    cache_filename = dir_path + '/' + filename

    dict = get_data_using_cache(url, filename)

    write_json(cache_filename, dict)

 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    # unittest.main(verbosity=2)
