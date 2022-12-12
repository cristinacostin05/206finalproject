import json
import unittest
import os
import requests

API_KEY = 'cdaf41f252ec436396bbd760c8bda897'

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
    url = f'https://mna.mecatran.com/utw/ws/gtfsfeed/realtime/valleymetro?apiKey=4f22263f69671d7f49726c3011333e527368211f&asJson=true'
    url2 = f'https://mna.mecatran.com/utw/ws/gtfsfeed/vehicles/valleymetro?apiKey=4f22263f69671d7f49726c3011333e527368211f&asJson=true'

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "phoenix_trips.json"
    filename2 = "phoenix2_vehicles.json"

    cache_filename = dir_path + '/' + filename
    cache_filename2 = dir_path + '/' + filename2

    #first cachefile
    dict = get_data_using_cache(url, filename)
    write_json(cache_filename, dict)

    #first cachefile
    dict = get_data_using_cache(url2, filename2)
    write_json(cache_filename2, dict)

 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    # unittest.main(verbosity=2)
