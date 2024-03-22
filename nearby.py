import streamlit as st
import requests

def fetch_nearby_places():
    url = "https://trueway-places.p.rapidapi.com/FindPlacesNearby"
    querystring = {"location":"28.4089,77.3178","radius":"180","language":"en"}
    headers = {
        'x-rapidapi-key': "e2aff922bemsh1a5ae21cd965b02p12fccdjsndb11a7adf5d2",
        'x-rapidapi-host': "trueway-places.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def main():
    st.title("Nearby Places")

    try:
        places = fetch_nearby_places()["results"]
        for place in places:
            st.write(f"**Name:** {place['name']}")
            st.write(f"**Address:** {place['address']}")
            st.write(f"**Phone Number:** {place['phone_number']}")
            st.write(f"**Website:** [{place['website']}]({place['website']})")
            st.write(f"**Location:** ({place['location']['lat']}, {place['location']['lng']})")
            st.write(f"**Types:** {', '.join(place['types'])}")
            st.write(f"**Distance:** {place['distance']} meters")
            st.write("---")
    except Exception as e:
        st.error(f"Error fetching nearby places: {e}")

if __name__ == "__main__":
    main()
