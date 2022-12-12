import json
import unittest
import os
import requests

API_KEY = '4f22263f69671d7f49726c3011333e527368211f'

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
    url = f'https://mna.mecatran.com/utw/ws/gtfsfeed/realtime/valleymetro?apiKey={API_KEY}&asJson=true'

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "phoenix.json"

    cache_filename = dir_path + '/' + filename

    #first cachefile
    dict = get_data_using_cache(url, filename)
    write_json(cache_filename, dict)


 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    # unittest.main(verbosity=2)
