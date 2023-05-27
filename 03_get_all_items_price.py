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

def request_all_items_daily():
    logger.info("Starting items price request")
    try:
        url = "https://nwmarketprices.com/api/latest-prices/27/"
        payload = ""
        response = requests.request("GET", url, data=payload)
        logger.info("Request completed")
    except Exception as e:
        logger.error(f"Error with the request {e}")

    try:
        logger.info("Saving the response")
        df = pd.read_json(response.text)
        #get a string timestamp for the file name
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        #save as csv file with timestamp
        df.to_csv(f"./data/api_calls/all_items_price/raw/{timestamp}.csv", index=False)
        logger.info(f"Response saved to csv file: {timestamp}.csv")
    except Exception as e:
        logger.error(f"Error saving the response {e}")
        
def main():
    request_all_items_daily()
    
if __name__ == "__main__":
    main()
# %%
