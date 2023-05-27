#%%
import requests
import pandas as pd
import os
from logger import initialize_logger

logger_file_name = os.path.basename(__file__)
logger = initialize_logger(logger_file_name)

def main():
    try:
        logger.info("Starting items catalog request")
        logger.info("Requesting items catalog")
        URL = "https://nwmarketprices.com/api/typeahead"
        PATH = "./data/api_calls/items_catalog/"
        payload = ""
        response = requests.request("GET", URL, data=payload)
        logger.info("Request completed")
        #convert json to dataframe
        logger.info("Converting json to dataframe")
        df = pd.read_json(response.text)
        #get a string timestamp for the file name
        logger.info("Getting timestamp")
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        #save the dataframe to a csv file
        logger.info("Saving dataframe to csv")
        df.to_csv(os.path.join(PATH, f"{timestamp}.csv"), index=False)
        logger.info(f"Response saved to csv file: {timestamp}.csv")
    except Exception as e:
        logger.error(f"Error with the request {e}")

if __name__ == "__main__":
    main()
