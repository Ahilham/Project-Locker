import requests

class get_loc():

    def get_device_location(self):
        
        try:

            response = requests.get('https://ipinfo.io')
            data = response.json()

            city = data.get('city', 'Unknown')
            region = data.get('region', 'Unknown')
            country = data.get('country', 'Unknown')
            location = data.get('loc', 'Unknown')
            latt, long = map(float, location.split(','))

            array = [city, region, country, location, latt, long]
            return array

        except Exception as e:
            print(f"Error: {e}")
            return None



if __name__ == '__main__':
    test = get_loc()
    print(test.get_device_location())
    