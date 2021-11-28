import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
import io
import warnings
import seaborn as sns
warnings.filterwarnings('ignore')

st.title('Uber Data Analysis')
st.write('Insight About Given Data:')
st.markdown('. Georgraphy : USA, Sri lanka and pakistan')
st.markdown('. Time period : jan-dec 2016')
st.markdown('. Unit of analysis : Drives')
st.markdown('. Total Drives :1,155')
st.markdown(' . Total miles : 12,204')
st.markdown(' The dataset contains start date, end date, start location, end location, miles driven, and purpose of drive( business, personal, meals, meetings)')


data=pd.read_csv('uberdataraw.csv',encoding='latin1')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Cleaning of Data:')
st.write('Code to remove star sign from columns:')
st.write('```data.columns = data.columns.str.replace("*","")```')
data.columns = data.columns.str.replace("*","")

if st.checkbox('Show New Changes'):
    st.subheader('Data')
    st.write(data)

st.write('Code to get Info of Data:')


buffer = io.StringIO() 
data.info(buf=buffer)
s = buffer.getvalue() 
with open("df_info.txt", "w", 
     encoding="utf-8") as f:
     f.write(s)

if st.checkbox('Show Data Info'):
    st.subheader('Info')
    st.write(s)


st.write('Shape of Data:')
st.write(data.shape)

st.write('Data Describe:')
if st.checkbox('Show Data Describe'):    
    st.write(data.describe())

st.subheader('Handling missing  Data:')
if st.checkbox('Getting Null Values'):
    st.subheader('Null Value Sum:')
    st.write(data.isnull().sum())

if st.checkbox('Show Data Null Values Heatmap'):
    st.subheader('Heatmap')
    fig, ax = plt.subplots()
    sns.heatmap(data.isnull(), ax=ax,cmap='viridis')
    st.write(fig)

import  missingno as msno

if st.checkbox('Show Missing Data chart'):
    fig, ax = plt.subplots()
    msno.bar(data,ax=ax)
    st.write(fig)


if st.checkbox('Show Sum of Null Values in Columns'):
    null_columns = data.columns[data.isnull().any()]
    st.write(data[null_columns].isnull().sum())

st.write('We Observe last row contains Null values so Lets remove it')
st.write('Code to remove last Row:')
st.write('``` data.drop(index=1155,axis=0,inplace=True)```')

data.drop(index=1155,axis=0,inplace=True)
if st.checkbox('Show Data after Deleting Last Row'):
    st.write(data.isnull().sum())

st.write('Lets see Average Null Values in Purpose Column:')
st.write('Code to get Average:')
st.write('```data["PURPOSE"].isnull().sum()/len(data)```')
st.write('Average occurance of Null values in Purpose Column:')

st.write(data["PURPOSE"].isnull().sum()/len(data))

st.write('We can fill Purpose Null values with ```ffill```(Forward Fill) method')
st.write('Code to Do it:')
st.write('```data[''PURPOSE''].fillna(method=''ffill'',inplace=True)```')

data['PURPOSE'].fillna(method='ffill',inplace=True)

if st.checkbox('Show Null values Now'):
    st.write(data.isnull().sum())

st.write('Converting "START_DATE" and "END_DATE" cols data types to Datetime type:')
st.write('Code to Do it :')
st.write('```data[''START_DATE''] = pd.to_datetime(data[''START_DATE''],errors=''coerce'') ```')
st.write('```data[''END_DATE''] = pd.to_datetime(data[''END_DATE''],errors=''coerce'') ```')
data['START_DATE'] = pd.to_datetime(data['START_DATE'],errors='coerce')
data['END_DATE'] = pd.to_datetime(data['END_DATE'],errors='coerce')

buffer1 = io.StringIO() 
data.info(buf=buffer1)
s1 = buffer1.getvalue() 
with open("df_info1.txt", "w", 
     encoding="utf-8") as f:
     f.write(s1)
if st.checkbox('Show Data Info '):
    st.write(s1)

if st.checkbox('Show Missing Data chart Now'):
    fig, ax = plt.subplots()
    msno.bar(data,ax=ax)
    st.write(fig)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
st.subheader('Analysis:')
st.write('Getting Count of Trips by there Catergory:')
category = pd.crosstab(index=data['CATEGORY'],columns = 'count of travel as per category')
st.write(category)



if st.checkbox('Show Barchart of Category of Trips:'):
    st.subheader('Category of Trips')
    fig, ax = plt.subplots()
    category.plot(kind='bar',color='#fd971f',ax=ax)
    st.write(fig)

st.write('Counting Starting points of Trips:')
start_point=data.START.value_counts()
if st.checkbox('Show Start Points count:'):
    st.write(start_point)
start_min = st.slider("Minimum Start Points:", 200, 0)
st.write(start_point[start_point>start_min])

if st.checkbox('Show Start Points Pie Chart:'):
    fig, ax = plt.subplots()
    start_point[start_point>10].plot(kind='pie',ax=ax)
    st.write(fig)

# STOP POINTS SE KARNA H 

st.write('Stop Points :')
stop_point=data.STOP.value_counts()
if st.checkbox('Show Stop Points count:'):
    st.write(stop_point)
stop_min = st.slider("Minimum Stop Points:", 202, 0)
st.write(stop_point[stop_point>stop_min])

if st.checkbox('Show Stop Points Pie Chart:'):
    fig, ax = plt.subplots()
    stop_point[stop_point>10].plot(kind='pie',ax=ax)
    st.write(fig)

miles = data.MILES.value_counts()

st.write('Trip Purpose Value Count:')
st.write(data.PURPOSE.value_counts())

if st.checkbox('Show Trip Purpose Plot'):
    fig, ax = plt.subplots()
    sns.countplot(data['PURPOSE'],order = data['PURPOSE'].value_counts().index,palette='viridis',ax=ax)
    plt.xticks(rotation=45)
    st.write(fig)

st.write('Lets calculate the duration, as there might be some relation of it with purpose of ride:')
st.write('Code to make the column and have Duration of Ride:')
st.write('``` data[''minutes''] = data.END_DATE - data.START_DATE```')
data['minutes'] = data.END_DATE - data.START_DATE

if st.checkbox('Show Data With New Column:'):
    st.write(data)
st.write('Doing Conversion:')
data['minutes']= data['minutes'].dt.total_seconds()/60
st.write(data)
st.write('Purpose And Miles Relationship:')
data1=pd.DataFrame({'Mean':data.groupby(['PURPOSE'])['MILES'].mean().round(1),
             'Min': data.groupby(['PURPOSE'])['MILES'].min(),
             'Max':data.groupby(['PURPOSE'])['MILES'].max()}).reset_index()

st.write(data1)

st.write('Lets Check for Round Trip:')
def round(x):
    if x['START']==x['STOP']:
        return 'yes'
    else:
        return 'no'
data['Round_TRIP'] = data.apply(round,axis=1)
if st.checkbox('Show Round Trip Data and Graph:'):
    fig, ax = plt.subplots()
    sns.countplot(data['Round_TRIP'],order = data['Round_TRIP'].value_counts().index,ax=ax)
    st.write(fig)

st.write('Entering Month data And evalualting its frequency of Trip in each month:')
st.write('Making Month Column:')
st.write('Code to do it:')
st.write('```data[''month'']= pd.DatetimeIndex(data[''START_DATE'']).month ```')
data['month']= pd.DatetimeIndex(data['START_DATE']).month

dic = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',9:'sept',10:'oct',11:'nov',12:'dec'}
data['month'] =data['month'].map(dic)

if st.checkbox('Show Data:'):
    st.write(data)

if st.checkbox('Trip count in Month:'):
    fig, ax = plt.subplots()
    sns.countplot(data['month'],ax=ax,order = data['month'].value_counts().index,palette='deep')
    st.write(fig)

if st.checkbox('Round Trip in Month:'):
    fig, ax = plt.subplots()
    sns.countplot(data['Round_TRIP'],ax=ax,hue=data['month'])
    st.write(fig)

if st.checkbox('Show Minute and Miles relationship Graph:'):
    if st.checkbox('Show Line Plot:'):
        fig, ax = plt.subplots()
        sns.lineplot(data=data,x=data.minutes,y=data.MILES)
        st.write(fig)
    if st.checkbox('Show Scatter Plot:'):
        fig, ax = plt.subplots()
        sns.scatterplot(data=data,x=data.minutes,y=data.MILES)
        st.write(fig)

st.write('Category-Purpose Trip')
if st.checkbox("Show The Chart:"):
    fig,ax=plt.subplots()
    sns.countplot(data=data,x='PURPOSE',hue='CATEGORY',dodge=False)
    plt.xticks(rotation=45)
    st.write(fig)

st.write('Car rides start location frequency:')
if st.checkbox("Show The start location Frequency:"):
    fig,ax=plt.subplots()
    pd.Series(data['START']).value_counts()[:25].plot(kind='bar')
    plt.xticks(rotation=90)
    st.write(fig)

st.write('Car rides start location frequency:')
if st.checkbox("Show The Stop location Frequency:"):
    fig,ax=plt.subplots()
    pd.Series(data['STOP']).value_counts()[:25].plot(kind='bar')
    plt.xticks(rotation=90)
    st.write(fig)

st.header('Conclusion:')
st.markdown('1. Business cabs were not only used more in volumne but also have travelled more distance.')
st.markdown('2. Round trips were more in decemnber')
st.markdown('3. december can prove to be the best month for earning profit by raising fare as demand is more')
st.markdown('4. Seasonal pattern is there')
st.markdown('5. Cab traffic was high in just 5 cities comparitevely')
st.markdown('6. most of the cab rides are within a distance of 35 miles taking about 30 minutes')
st.markdown('7. For Airport cabs are taking more time than usual.')
