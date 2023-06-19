import streamlit as st
import pandas as pd
import requests
import json
import logging

# configuring the logger
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(format=' %(asctime)s  %(name)-12s %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__ + " : ")

orig_loc_col = 'Origin'                             # column containing origin location details (address/zip/geocodes)
dest_loc_col = 'Destination'

units = 'imperial'
google_api_key = "AIzaSyCn_mtafoVGuSVjcYhj_2_lUVX57F9xDso"

st.header("GET DRIVING DISTANCES")
st.write("Upload file with geocodes to get the driving distance between them - ")
orig_loc_col = st.text_input("Origin Column")
dest_loc_col = st.text_input("Destination Column")
# st.write("Note: Name your origin location as Origin and destination as Destination")
uploaded_file = st.file_uploader("Choose a file", type='csv')


def get_driving_distance(orig_loc, dest_loc, units='imperial'):
    if units:
        if units == 'imperial':
            driving_distance_uom = 'mi'
            conv_factor = 1609.34
        elif units == 'metric':
            driving_distance_uom = 'km'
            conv_factor = 1000.00
        else:
            raise ValueError("Invalid units : ", units)
    try:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&departure_time=now&key={2}".format(orig_loc, dest_loc, google_api_key)
        payload = {}
        headers = {}
        # print(url)
        response = requests.request("GET", url, headers=headers, data=payload)
        api_output_dict = json.loads(response.text)
        # print(response.text)
        driving_distance_mtr = api_output_dict['rows'][0]['elements'][0]['distance']['value']
        driving_distance = round(driving_distance_mtr/conv_factor, 1)
        status = 'SUCCESS'
    except:
        driving_distance = -1
        status = 'FAILURE'
    logger.info("{0} | {1} | {2} | {3}".format(status, orig_loc, dest_loc, str(driving_distance)+' '+driving_distance_uom))
    return driving_distance

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file, encoding='latin-1')
    st.write("Uploaded data : "), input_df


    if st.button('GET DISTANCES'):
        input_df['Driving Distance'] = input_df.apply(
        lambda row: get_driving_distance(row[orig_loc_col], row[dest_loc_col], units=units), axis=1)
        st.write("Driving distance : "), input_df

        csv = convert_df(input_df)
        st.download_button('DOWNLOAD RESULTS', csv, 'output_drivingdistances.csv', 'text/csv', key='download-csv')
