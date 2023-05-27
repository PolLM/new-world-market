#%%
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
st.set_page_config(layout="wide")

#load merged df
df = pd.read_csv("./data/api_calls/items_price/merged.csv")
df = df[['item_name', 'price_date', 'lowest_price', 'highest_buy_order', 'avg_price', 'avail']]
#load all items df 
df_all_items = pd.read_csv("./data/api_calls/all_items_price/merged.csv")
df_all_items = df_all_items[['ItemName', 'LastUpdated', 'Price', 'HighestBuyOrder', 'Qty',]]
#change the name of the columns
df_all_items.rename(columns={
    "ItemName": "item_name",
    "LastUpdated": "price_date",
    "Price": "lowest_price",
    "HighestBuyOrder": "highest_buy_order",
    "Qty": "avail",
    }, inplace=True)

df_all_items['avg_price'] = np.nan

#df = pd.concat([df, df_all_items])
#df = df_all_items
df.drop_duplicates(inplace=True)
#list of items
items = df["item_name"].unique().tolist()
#find items that has 2 or more records
#items = [item for item in items if len(df[df["item_name"] == item]) > 1]

with st.container():
    st.title("Item Price History (Mochonk nub)")
    #Streamlit dropdown
    item = st.selectbox("Select an item", items)
    #filter df
    df_item = df[df["item_name"] == item]
    #show the pandas df item
    st.write(df_item)
    #convert to datetime
    df_item["price_date"] = pd.to_datetime(df_item["price_date"])
    #date double ended slider
    min_date = df_item["price_date"].min()
    max_date = df_item["price_date"].max()
    st.write(f"Min date: {min_date}")
    st.write(f"Max date: {max_date}")
    #convert timestamps to datetime
    min_date = min_date.to_pydatetime()
    max_date = max_date.to_pydatetime()
    #slider widget for date range
    date_range = st.slider("Select a date range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    #convert back to datetime
    slider_min = pd.to_datetime(date_range[0])
    slider_max = pd.to_datetime(date_range[1])
    #filter df
    df_item = df_item[(df_item["price_date"] >= slider_min) & (df_item["price_date"] <= slider_max)]

    ##plot
    ##make a plotly plot with the data

    fig =  make_subplots(specs=[[{"secondary_y": True}]])

    #add the lowest price
    line_params = dict(color='rgba(255, 0, 0, 0.45)', width=2)
    marker_params = dict(color='rgba(255, 0, 0, 1)', size=6)
    fig.add_trace(go.Scatter(x=df_item["price_date"], y=df_item["lowest_price"],
                        mode='lines+markers',
                        name='Lowest Price',
                        line_shape='spline',
                        line = line_params,
                        marker = marker_params),
                        secondary_y=False)
    #add the highest buy order
    line_params = dict(color='rgba(0, 255, 0, 0.45)', width=2)
    marker_params = dict(color='rgba(0, 255, 0, 1)', size=6)
    fig.add_trace(go.Scatter(x=df_item["price_date"], y=df_item["highest_buy_order"],
                        mode='lines+markers',
                        name='Highest Buy Order',
                        line_shape='spline',
                        line = line_params,
                        marker = marker_params),
                        secondary_y=False)
    ##add the avg price
    #line_params = dict(color='rgba(0, 0, 255, 0.45)', width=2)
    #marker_params = dict(color='rgba(0, 0, 255, 1)', size=6)
    #fig.add_trace(go.Scatter(x=df_item["price_date"], y=df_item["avg_price"],
    #                    mode='lines+markers',
    #                    name='Average Price',
    #                    line_shape='spline',
    #                    line = line_params,
    #                    marker = marker_params),
    #                    secondary_y=False)

    #add available supply
    fig.add_trace(go.Bar(x=df_item["price_date"], y=df_item["avail"],
                        name='Available Supply',
                        marker_color='rgb(55, 83, 109, 0.25)'),
                        secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

col1, col2, = st.columns(2)
with col1:
    df_item["day_of_week"] = df_item["price_date"].dt.day_name()
    st.title("Mean & Std. available supply per day of the week")
    df_item_grouped = df_item.groupby("day_of_week").agg({"avail": ["mean", "std"]})
    fig = go.Figure()
    marker_params = dict(color='rgba(255, 0, 0, 1)', size=8)
    error_params = dict(type='data', array=df_item_grouped["avail"]["std"], visible=True, color='rgba(255, 0, 0, 0.5)')
    fig.add_trace(go.Scatter(x=df_item_grouped.index, y=df_item_grouped["avail"]["mean"],
                        name='Mean Available Supply per day of week',
                        mode='markers',
                        marker = marker_params,
                        error_y=error_params,),)
    #plot the raw datapoints per day of week
    marker_params = dict(color='rgba(0, 0, 255, 0.7)', size=5.5)
    fig.add_trace(go.Scatter(x=df_item["day_of_week"], y=df_item["avail"],
                                mode='markers',
                                name='Available Supply',
                                marker = marker_params,
                                showlegend=False))
    st.plotly_chart(fig)
    
    st.title("Lowest Price vs Available Supply")
    #Make a plotly scatter plot of lowest price vs item availability

    fig = px.scatter(df_item, x="avail", y="lowest_price", color="item_name", trendline="ols", trendline_scope="overall")

    st.plotly_chart(fig)

with col2:
    st.title("Mean & Std. price per day of the week")
    #Groupby df_item to get average and std per day of week
    df_item["day_of_week"] = df_item["price_date"].dt.day_name()
    df_item_grouped = df_item.groupby("day_of_week").agg({"avg_price": ["mean", "std"]})
    #plotly scatter of mean per day of week
    fig = go.Figure()
    
    marker_params = dict(color='rgba(255, 0, 0, 1)', size=8)
    error_params = dict(type='data', array=df_item_grouped["avg_price"]["std"], visible=True, color='rgba(255, 0, 0, 0.5)')
    fig.add_trace(go.Scatter(x=df_item_grouped.index, y=df_item_grouped["avg_price"]["mean"],
                             name='Average Price',
                             mode='markers',
                             marker = marker_params,
                             error_y=error_params,
    ))
    
    #plot the raw datapoints per day of week
    marker_params = dict(color='rgba(0, 0, 255, 0.7)', size=5.5)
    fig.add_trace(go.Scatter(x=df_item["day_of_week"], y=df_item["avg_price"],
                                mode='markers',
                                name='Average Price',
                                marker = marker_params,
                                showlegend=False))
 
    st.plotly_chart(fig)
    


# %%
