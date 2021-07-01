import pandas as pd
import requests
import time
from settings import API_KEY, INPUT_FILE_NAME, OUTPUT_FILE_NAME

urls = pd.read_csv(INPUT_FILE_NAME)['URL']

business_urls = []
business_name = []
business_address = []
business_phone_number = []

# for query in urls:
query = "www.furniturevillage.co.uk"
print(f"{query} Start...")

search_place_id_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
get_place_id = requests.get(search_place_id_url + 'query=' + query + '&key=' + API_KEY)

place_id_result = get_place_id.json()['results']

if place_id_result:
    for result in place_id_result:
        place_id = result['place_id']
        print(f"Place ID of {query} is {place_id}")

        time.sleep(3)

        print(f"Starting to get the detailed data of {query}")

        search_place_data_url = "https://maps.googleapis.com/maps/api/place/details/json?"
        place_data = requests.get(search_place_data_url + 'placeid=' + place_id + '&key=' + API_KEY).json()

        business_urls.append(query)

        phone_number_key = 'international_phone_number'
        if phone_number_key in place_data['result']:
            business_phone_number.append(place_data['result'][phone_number_key])
        else:
            business_phone_number.append("None")

        address_key = 'formatted_address'

        if address_key in place_data['result']:
            business_address.append(place_data['result'][address_key])
        else:
            business_address.append("None")

        business_name_key = 'name'
        if business_name_key in place_data['result']:
            business_name.append(place_data['result'][business_name_key])
        else:
            business_name.append("None")

        print(f"Done {query}")
        time.sleep(3)
else:
    business_urls.append(query)
    business_phone_number.append("None")
    business_address.append("None")
    business_name.append("None")
    print(f"{query} No Data...")

data = {
    "URL": business_urls,
    "Business Name": business_name,
    "Business Address": business_address,
    "Business Phone Number": business_phone_number
}

df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE_NAME)
print("Done...")
