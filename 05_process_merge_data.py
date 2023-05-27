
#%%
import pandas as pd
import json
import os
from logger import initialize_logger

logger_file_name = os.path.basename(__file__)
logger = initialize_logger(logger_file_name)

logger.info("Starting merging items process")
df_graph = pd.DataFrame()
#load the items json
PATH_API_RAW = "./data/api_calls/items_price/raw"
for dayfolder in os.listdir(PATH_API_RAW):
    PATH_TIMESTAMP = os.path.join(PATH_API_RAW, dayfolder)
    #get a string timestamp for the file name
    timestamp = pd.to_datetime(dayfolder.split(".")[0], format="%Y%m%d_%H%M%S")
    logger.info(f"Merging {timestamp}")
    for filename in os.listdir(PATH_TIMESTAMP):
        PATH_FILE = os.path.join(PATH_TIMESTAMP, filename)
        with open(PATH_FILE, "r") as f:
            item_dict = json.load(f)
        print(filename)
        print(item_dict)
        #if item_dict ha sno item name
        if "item_name" not in item_dict.keys():
            logger.error(f"Skipping {filename}")
            continue
        item_name = item_dict["item_name"]
        item_id = item_dict["item_id"]
        price_datetime = item_dict["price_datetime"]
        graph_data = item_dict["graph_data"]
        detail_view = item_dict["detail_view"]
        
        #create a dataframe with the graph data
        df_graph_item = pd.DataFrame(graph_data)
        #create a dataframe with the detail view
        df_detail_view = pd.DataFrame(detail_view)
        
        #add the item name, id and price datetime to the dataframes
        df_graph_item["item_name"] = item_name
        df_graph_item["item_id"] = item_id
        df_graph_item["query_datetime"] = price_datetime
        
        #concatenate the dataframes
        df_graph = pd.concat([df_graph, df_graph_item])
        logger.info(f"Added {item_name}")

logger.info("Saving merged dataframe")
#reset the index
df_graph.reset_index(drop=True, inplace=True)
#drop duplicates
df_graph.drop_duplicates(inplace=True)
#convert the price date to datetime
df_graph["price_date"] = pd.to_datetime(df_graph["price_date"])
#save the dataframe to a csv file
df_graph.to_csv("./data/api_calls/items_price/merged.csv", index=False)
# %%
