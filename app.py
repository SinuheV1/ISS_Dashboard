import requests
import pandas as pd
import time
from datetime import datetime as dt
from datetime import UTC
import pytz
import streamlit as st
import pydeck as pdk
from dotenv import load_dotenv
import os


load_dotenv()
api_key=os.getenv("NASA_API_KEY")
#ISS location
def get_iss_location():
    url = 'http://api.open-notify.org/iss-now.json'
    resp = requests.get(url)
    location = resp.json()
    unix_timestamp = location['timestamp']
    lat = location['iss_position']['latitude']
    long = location['iss_position']['longitude']
    #converts the unix time to pst
    utc_time=dt.fromtimestamp(unix_timestamp, UTC)
    pst_timezone=pytz.timezone('America/Los_Angeles')
    pst_datetime=utc_time.astimezone(pst_timezone)
    formatted_pst=pst_datetime.strftime('%Y-%m-%d %I:%M:%S %p %Z')

    return lat, long, formatted_pst

lat, long, formatted_pst = get_iss_location()

#Astronauts in space
def get_astros():
    astros_url='http://api.open-notify.org/astros.json'
    astros_resp=requests.get(astros_url)
    entry=astros_resp.json()
    number=entry['number']
    people = entry['people']

    return number, people

#Nasa Picture of the Day
def get_potd(api_key=api_key):
    url=f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    resp=requests.get(url)
    data=resp.json()
    return data['title'],data['url'],data['explanation'],data['media_type']

lat, lon, formatted_pst = get_iss_location()
number, people=get_astros()
lat=float(lat)
lon=float(lon)
#df of coordinates
df = pd.DataFrame({
    'lat': [lat],
    'lon': [lon]})

#title/subheader and lat/long of the ISS
st.title('Live ISS Location Dashboard')
st.subheader('Current ISS Position')
st.metric('Latitude', lat)
st.metric('Longitude', lon)

#sidebar settings for refresh rate
with st.sidebar:
    refresh_interval=st.slider('Refresh every (seconds):',10,60,30)
    auto_refresh=st.checkbox('Auto-Refresh', value=True)
    st.caption('App updates based on real-time ISS location')
    if not auto_refresh:
         manual_refresh=st.button('Refresh Now')
    
#display last updated time
st.caption(f'Last Updated Time: {formatted_pst}')

#viewstate zoom = 1 for scale to be world
view_state=pdk.ViewState(
    latitude=lat,
    longitude=lon,
    zoom=1)
#setting up the icon in the center to show accurate position of ISS
#sets radius and color
icon_layer=pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[lon, lat]',
    get_radius=50000,
    get_color='[255,0,0,255]',
    pickable=True)
#map
st.pydeck_chart(pdk.Deck(
    map_style='',
    initial_view_state=view_state,
    layers=[icon_layer]))

#setup columns for streamlit
left_col, right_col = st.columns([1,2])
with left_col:
    #filter astronauts
    #crew api depreciated and two astronauts below have made it back home
    #updates to api not made so I will filter them out manually
    not_crew=['Butch Wilmore','Sunita Williams']
    iss_crew=[p for p in people if p['craft']=='ISS' and p['name'] not in not_crew]
    st.subheader(f'Astronauts On Board: {len(iss_crew)}')
    for person in iss_crew:
            st.write(f"- **{person['name']}**")

#right column for NASA's Picture of the Day
with right_col:
    st.subheader(f"NASA's Picture of The Day")
    title,url,explanation,media_type = get_potd(api_key)
    st.markdown(f"**{title}**")
    if media_type== 'image':
          st.image(url, use_container_width=True)
    elif media_type== 'video':
        st.video(url)
    with st.expander("Explanation"):
         st.write(explanation)

#refresh rate   
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
elif not auto_refresh and manual_refresh:
    st.rerun()
