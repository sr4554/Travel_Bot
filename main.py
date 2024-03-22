import streamlit as st
import streamlit.components.v1 as components
import requests
from requests.exceptions import RequestException
import geocoder
# import pandas as pd
from streamlit_folium import folium_static
import folium

def app_homepage():
    st.title("""Hey! I am Travis.
             Let me help you plan your trip!""")
    st.image("img/bot intro.jpg", caption='Explore the World with Us',width = 550)
    st.markdown("""
    ## Discover, Plan, and Explore
    G'day there! It's me, Travis. I'm your friendly guide to your wanderlust soul.
    So let's start planning your dream trip! I can help you make your journey a very memorable one!

    ### Features:
    - **Ask Me Anything**: Get answers to your travel-related questions.
    - **Lets Plan a Trip**: Plan your trip with information on modes of transport, costs, and booking links.
    - **Find My Fit**: Discover places that match your interests.
    - **Explore Locals**: Explore attractions near your current location.
    
    Enjoy !
    """, unsafe_allow_html=True)

def app_user_queries():
    st.subheader('Ask any travel-related question:')
    user_query = st.text_input("Enter your question here", help="Input your travel query here")
    
    if user_query:
        api_url = 'https://simple-chatgpt-api.p.rapidapi.com/ask'
        api_key = 'e2aff922bemsh1a5ae21cd965b02p12fccdjsndb11a7adf5d2'
        api_host = 'simple-chatgpt-api.p.rapidapi.com'

        headers = {
            'content-type': 'application/json',
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': api_host
        }

        data = {
            'question': f'Act as a travel guide and answer: {user_query}'
        }

        try:
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()
            travel_guide_response = response_data.get('answer', 'Sorry, I couldn\'t generate a travel guide for your query.')
            st.success(travel_guide_response)
        except Exception as error:
            st.error(f"Error: {error}")


def app_trip_planner():
    st.subheader('Plan Your Trip:')
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input("Origin", help="Where are you starting your journey?")
    with col2:
        destination = st.text_input("Destination", help="Where do you want to go?")
    
    if origin and destination:
        api_url = 'https://simple-chatgpt-api.p.rapidapi.com/ask'
        api_key = 'e2aff922bemsh1a5ae21cd965b02p12fccdjsndb11a7adf5d2'
        api_host = 'simple-chatgpt-api.p.rapidapi.com'

        headers = {
            'content-type': 'application/json',
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': api_host
        }

        data = {
            'question': f'Plan a trip from {origin} to {destination} with detailed budgeting and travel options in a very systematic manner'
        }

        try:
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()
            trip_info = response_data.get('answer', 'Sorry, I couldn\'t generate trip information.')
            st.info("Trip Information: " + trip_info)
        except Exception as error:
            st.error(f"Error: {error}")



def app_place_suggester():
    st.subheader('Discover Places:')
    
    preferences = ["Beaches", "Mountains", "Historic Sites", "Parks"]
    preference = st.selectbox("What are you interested in?", preferences, help="Select your preference")

    if preference:
        additional_preference = st.text_input("Other Preferences", help="Enter any additional preferences")
        combined_preference = f'{preference} {additional_preference}' if additional_preference else preference

        api_url = 'https://simple-chatgpt-api.p.rapidapi.com/ask'
        api_key = 'e2aff922bemsh1a5ae21cd965b02p12fccdjsndb11a7adf5d2'
        api_host = 'simple-chatgpt-api.p.rapidapi.com'

        headers = {
            'content-type': 'application/json',
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': api_host
        }

        data = {
            'question': f'Suggest places for {combined_preference}'
        }

        try:
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()
            places = response_data.get('answer', 'Sorry, I couldn\'t suggest places based on your preference.')
            st.success("Suggested Places: " + places)
        except Exception as error:
            st.error(f"Error: {error}")


def fetch_nearby_places(latitude, longitude):
    url = "https://trueway-places.p.rapidapi.com/FindPlacesNearby"
    querystring = {"location": f"{latitude},{longitude}", "radius": "1800", "language": "en"}
    headers = {
        'x-rapidapi-key': "e2aff922bemsh1a5ae21cd965b02p12fccdjsndb11a7adf5d2",
        'x-rapidapi-host': "trueway-places.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        st.error(f"Error fetching nearby places: {e}")
        return []

def app_nearby_places_finder():
    st.subheader('Find Places Near You:')
    location = geocoder.ip('me').latlng
    
    if location:
        latitude, longitude = location
        st.write(f"Current Latitude: {latitude}")
        st.write(f"Current Longitude: {longitude}")
        
        nearby_places = fetch_nearby_places(latitude, longitude)
        if nearby_places:
            for place in nearby_places:
                st.subheader(place.get('name', 'Unknown Place'))
                map_center = [place['location']['lat'], place['location']['lng']]
                m = folium.Map(location=map_center, zoom_start=15)
                folium.Marker(location=map_center, popup=place['name']).add_to(m)
                folium.Circle(location=map_center, radius=180, color='blue', fill=True, fill_color='blue').add_to(m)
                folium_static(m)
                
                st.write(f"**Address:** {place.get('address', 'N/A')}")
                st.write(f"**Phone Number:** {place.get('phone_number', 'N/A')}")
                st.write(f"**Website:** [{place.get('website', 'N/A')}]({place.get('website', 'N/A')})")
                st.write(f"**Types:** {', '.join(place.get('types', ['N/A']))}")
                st.write(f"**Distance:** {place.get('distance', 'N/A')} meters")
                st.write("---")
        else:
            st.write("No nearby places found.")

            
# Enhanced layout and styling
st.set_page_config(page_title="Travel Companion App", layout="wide", page_icon="✈️")
app_navigation = st.sidebar.selectbox("Navigate to", ["Home", "Ask Me Anything", "Lets Plan a Trip", "Find My Fit", "Explore Locals"], index=0)

if app_navigation == "Home":
    app_homepage()
elif app_navigation == "Ask Me Anything":
    app_user_queries()
elif app_navigation == "Lets Plan a Trip":
    app_trip_planner()
elif app_navigation == "Find My Fit":
    app_place_suggester()
elif app_navigation == "Explore Locals":
    app_nearby_places_finder()

# Custom CSS for additional beautification
st.markdown("""
<style>
.stTextInput>div>div>input {
    border-radius: 20px;
}
.stSelectbox>div>div>select {
    border-radius: 20px;
}
.stButton>button {
    border-radius: 20px;
    border: 1px solid #4CAF50;
    color: white;
    background-color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)
