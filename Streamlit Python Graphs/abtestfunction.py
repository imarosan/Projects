import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import streamlit as st
pio.templates.default = "plotly_white"

control_data = pd.read_csv("datasets/control_group.csv", sep = ";")
test_data = pd.read_csv("datasets/test_group.csv", sep = ";")

control_data.columns = ["Campaign Name", "Date", "Amount Spent",
                        "Number of Impressions", "Reach", "Website Clicks",
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]

test_data.columns = ["Campaign Name", "Date", "Amount Spent",
                        "Number of Impressions", "Reach", "Website Clicks",
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]

control_data["Number of Impressions"].fillna(value=round(control_data["Number of Impressions"].mean(),0),
                                             inplace=True)
control_data["Reach"].fillna(value=round(control_data["Reach"].mean(),0),
                             inplace=True)
control_data["Website Clicks"].fillna(value=round(control_data["Website Clicks"].mean(),0),
                                      inplace=True)
control_data["Searches Received"].fillna(value=round(control_data["Searches Received"].mean(),0),
                                         inplace=True)
control_data["Content Viewed"].fillna(value=round(control_data["Content Viewed"].mean(),0),
                                      inplace=True)
control_data["Added to Cart"].fillna(value=round(control_data["Added to Cart"].mean(),0),
                                     inplace=True)
control_data["Purchases"].fillna(value=round(control_data["Purchases"].mean(),0),
                                 inplace=True)

ab_data = control_data.merge(test_data,
                             how="outer").sort_values(["Reach"])
ab_data = ab_data.reset_index(drop=True)

def describe_ab():
    describe = pd.DataFrame(ab_data.describe())
    print(describe)
    return st.dataframe(describe)
def describe_a():
    describe = pd.DataFrame(control_data.describe())
    print(describe)
    return st.dataframe(describe)
def describe_b():
    describe = pd.DataFrame(test_data.describe())
    print(describe)
    return st.dataframe(describe)
def ab():
    return st.dataframe(ab_data)
def a():
    return st.dataframe(control_data)
def b():
    return st.dataframe(test_data)
def Impressions_Spent(ab_data):
    Amount_Number = px.scatter(data_frame = ab_data,
                        x="Number of Impressions",
                        y="Amount Spent",
                        size="Amount Spent",
                        color= "Campaign Name",
                        trendline="ols")
    return st.plotly_chart(Amount_Number)
def Clicks_Viewed(ab_data):
    figure = px.scatter(data_frame=ab_data,
                        x="Content Viewed",
                        y="Website Clicks",
                        size="Website Clicks",
                        color="Campaign Name",
                        trendline="ols")
    return st.plotly_chart(figure)
def cart_viewed(ab_data):
    figure = px.scatter(data_frame=ab_data,
                        x="Added to Cart",
                        y="Content Viewed",
                        size="Added to Cart",
                        color="Campaign Name",
                        trendline="ols")
    return st.plotly_chart(figure)

def cart_purchases(ab_data):
    figure = px.scatter(data_frame=ab_data,
                        x="Purchases",
                        y="Added to Cart",
                        size="Purchases",
                        color="Campaign Name",
                        trendline="ols")
    return st.plotly_chart(figure)

def spent_purchases(ab_data):
    figure = px.scatter(data_frame=ab_data,
                        x="Purchases",
                        y="Amount Spent",
                        size="Purchases",
                        color="Campaign Name",
                        trendline="ols")
    return st.plotly_chart(figure)
def searches(control_data, test_data):
    label = ["Total Searches from Control Campaign",
             "Total Searches from Test Campaign"]
    counts = [sum(control_data["Searches Received"]),
              sum(test_data["Searches Received"])]
    colors = ['gold','lightgreen']
    Control_Test_Searches = go.Figure(data=[go.Pie(labels=label, values=counts)])
    Control_Test_Searches.update_layout(title_text='Control Vs Test: Searches')
    Control_Test_Searches.update_traces(hoverinfo='label+percent', textinfo='value',
                      textfont_size=30,
                      marker=dict(colors=colors,
                                  line=dict(color='black', width=3)))
    return st.plotly_chart(Control_Test_Searches)

def clicks(control_data, test_data):
    label = ["Website Clicks from Control Campaign",
             "Website Clicks from Test Campaign"]
    counts = [sum(control_data["Website Clicks"]),
              sum(test_data["Website Clicks"])]
    colors = ['gold','lightgreen']
    Control_Test_Clicks = go.Figure(data=[go.Pie(labels=label, values=counts)])
    Control_Test_Clicks.update_layout(title_text='Control Vs Test: Website Clicks')
    Control_Test_Clicks.update_traces(hoverinfo='label+percent', textinfo='value',
                      textfont_size=30,
                      marker=dict(colors=colors,
                                  line=dict(color='black', width=3)))
    return st.plotly_chart(Control_Test_Clicks)


def views(control_data, test_data):
    label = ["Content Viewed from Control Campaign",
             "Content Viewed from Test Campaign"]
    counts = [sum(control_data["Content Viewed"]),
              sum(test_data["Content Viewed"])]
    colors = ['gold','lightgreen']
    Control_Test_Viewed = go.Figure(data=[go.Pie(labels=label, values=counts)])
    Control_Test_Viewed.update_layout(title_text='Control Vs Test: Content Viewed')
    Control_Test_Viewed.update_traces(hoverinfo='label+percent', textinfo='value',
                      textfont_size=30,
                      marker=dict(colors=colors,
                                  line=dict(color='black', width=3)))
    return st.plotly_chart(Control_Test_Viewed)

def add(control_data, test_data):
    label = ["Products Added to Cart from Control Campaign",
             "Products Added to Cart from Test Campaign"]
    counts = [sum(control_data["Added to Cart"]),
              sum(test_data["Added to Cart"])]
    colors = ['gold','lightgreen']
    Control_Test_Added = go.Figure(data=[go.Pie(labels=label, values=counts)])
    Control_Test_Added.update_layout(title_text='Control Vs Test: Added to Cart')
    Control_Test_Added.update_traces(hoverinfo='label+percent', textinfo='value',
                      textfont_size=30,
                      marker=dict(colors=colors,
                                  line=dict(color='black', width=3)))
    return st.plotly_chart(Control_Test_Added)

def purchases(control_data, test_data):
    label = ["Purchases Made by Control Campaign",
             "Purchases Made by Test Campaign"]
    counts = [sum(control_data["Purchases"]),
              sum(test_data["Purchases"])]
    colors = ['gold', 'lightgreen']
    fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
    fig.update_layout(title_text='Control Vs Test: Purchases')
    fig.update_traces(hoverinfo='label+percent', textinfo='value',
                      textfont_size=30,
                      marker=dict(colors=colors,
                                  line=dict(color='black', width=3)))
    return st.plotly_chart(fig)

def spent(control_data, test_data):
    label = ["Amount Spent in Control Campaign",
             "Amount Spent in Test Campaign"]
    counts = [sum(control_data["Amount Spent"]),
              sum(test_data["Amount Spent"])]
    colors = ['gold', 'lightgreen']
    fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
    fig.update_layout(title_text='Control Vs Test: Amount Spent')
    fig.update_traces(hoverinfo='label+percent', textinfo='value',
                      textfont_size=30,
                      marker=dict(colors=colors,
                                  line=dict(color='black', width=3)))
    return st.plotly_chart(fig)

def main():
    st.title("A/B Test")
    pie_charts = {
        'Control Vs Test: Searches': searches,
        'Control Vs Test: Website Clicks': clicks,
        'Control Vs Test: Content Viewed': views,
        'Control Vs Test: Added to Cart': add,
        'Control Vs Test: Purchases': purchases,
        'Control Vs Test: Amount Spent': spent
    }
    scatter_plots = {
        'Amount Spent = Number of Impressions': Impressions_Spent,
        'Website Clicks = Content Viewed': Clicks_Viewed,
        'Added to Cart = Content Viewed': cart_viewed,
        'Added to Cart = Purchases': cart_purchases,
        'Amount Spent = Purchases': spent_purchases
    }
    dataframes = {
        'A/B': ab,
        'A': a,
        'B': b
    }
    describe = {
        'Both Datasets': describe_ab,
        'Control': describe_a,
        'Test': describe_b
    }
    nav_container = st.container()
    with nav_container:
        st.sidebar.header("DataSets")
        dataframe = st.sidebar.radio('Select', list(dataframes.keys()))
        st.sidebar.header("DataSets")
        desc = st.sidebar.radio('Select', list(describe.keys()))
        st.sidebar.header("Scatter Plots")
        scatter_plot = st.sidebar.radio('Select', list(scatter_plots.keys()))
        st.sidebar.header("Pie Charts")
        pie_chart = st.sidebar.radio('Select', list(pie_charts.keys()))

    st.header("DataSets")
    dataframes[dataframe]()
    st.header("Describe")
    describe[desc]()
    st.header("Scatter Plots")
    scatter_plots[scatter_plot](ab_data)
    st.header("Pie Charts")
    pie_charts[pie_chart](control_data, test_data)
main()



