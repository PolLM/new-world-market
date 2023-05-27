#%%
import os
import pandas as pd
import requests
import json
import time
import random
from logger import initialize_logger

logger_file_name = os.path.basename(__file__)
logger = initialize_logger(logger_file_name)

def find_last_catalog(PATH):
    #check all the files in the folder
    files = os.listdir(PATH)
    #convert filename to datetime
    file_dates = [pd.to_datetime(file.split(".")[0], format="%Y%m%d_%H%M%S") for file in files]
    #find the most recent file
    last_file = max(file_dates)
    #load the csv file
    df = pd.read_csv(os.path.join(PATH, f"{last_file.strftime('%Y%m%d_%H%M%S')}.csv"))
    return df

def load_tracking_items(PATH):
    #load the items json
    tracking_items = pd.read_json(os.path.join(PATH, "items.json"))
    return tracking_items.T

def request_items_chart():
    logger.info("Starting items price request")
    PATH_CATALOG = "./data/api_calls/items_catalog"
    df_catalog = find_last_catalog(PATH_CATALOG)

    logger.info("Loading tracking items")
    PATH_ITEMS = "./data/tracking_items"
    df_items = load_tracking_items(PATH_ITEMS)

    #items index to list
    item_names = df_items.index.tolist()

    #get a string timestamp for the file name
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")

    #check if timestamp dir exists if not create it
    PATH_API_RAW = "./data/api_calls/items_price/raw"
    path_items_timestamp = os.path.join(PATH_API_RAW, timestamp)
    if not os.path.exists(path_items_timestamp):
        os.mkdir(path_items_timestamp)
        
    logger.info("Requesting items prices")
    for item_n in item_names:
        logger.info(f"Getting {item_n}")
        #check if the item is in the catalog
        if not df_catalog[df_catalog["name"] == item_n]["id"].empty:
            #match the item id with the catalog
            item_id = df_catalog[df_catalog["name"] == item_n]["id"].values[0]
        else:
            logger.error(f"Item {item_n} not found in the catalog")
            continue
        
        try:
            url = f"https://nwmarketprices.com/api/price-data/27/{item_id}"
            payload = ""
            response = requests.request("GET", url, data=payload)
            #request to dictionary
            item_dict = response.json()
            #save the dictionary to a json file
            with open(os.path.join(path_items_timestamp, f"{item_n}.json"), "w") as f:
                json.dump(item_dict, f)
            logger.info(f"Saved {item_n}")
        except Exception as e:
            logger.error(f"Error with {item_n}: {e}")
            continue
        wait_time = 3 + random.random()
        logger.info(f"Waiting {wait_time} seconds")
        time.sleep(wait_time)
    logger.info("Request completed")
    
def main():
    request_items_chart()

if __name__ == "__main__":
    main()
# %%
