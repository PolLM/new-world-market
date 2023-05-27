#%%
import pandas as pd
import json
import os
from logger import initialize_logger

logger_file_name = os.path.basename(__file__)
logger = initialize_logger(logger_file_name)

logger.info("Starting merging items process")
df_graph = pd.DataFrame()

try:
    #load the csvs with the items
    PATH_API_RAW = "./data/api_calls/all_items_price/raw"
    #loop for each csv in the folder
    for filename in os.listdir(PATH_API_RAW):
        logger.info(f"Merging {filename}")
        PATH_FILE = os.path.join(PATH_API_RAW, filename)
        #read the csv
        df = pd.read_csv(PATH_FILE)
        #concatenate the dataframes
        df_graph = pd.concat([df_graph, df])
        #drop duplicates
        df_graph.drop_duplicates(inplace=True)
except Exception as e:
    logger.error(f"Error merging the csvs {e}")

try: 
    logger.info("Convert the data types")
    #convert the price date to datetime
    df_graph["price_date"] = pd.to_datetime(df_graph["price_date"])
    #reset the index
    df_graph.reset_index(drop=True, inplace=True)
except Exception as e:
    logger.error(f"Error converting the data types {e}")

try:
    logger.info("Saving merged dataframe")
    #save the dataframe to a csv file
    df_graph.to_csv("./data/api_calls/all_items_price/merged.csv", index=False)
except Exception as e:
    logger.error(f"Error saving the dataframe {e}")
    
# %%
