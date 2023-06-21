import requests
import json
import logging
import streamlit as st

# configuring the logger
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(format=' %(asctime)s  %(name)-12s %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__ + " : ")


def get_driving_distance(orig_loc, dest_loc, google_api_key, units='imperial'):
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


def api_input_check():
    if not st.session_state.get("google_api_key"):
        st.error(
            "Enter your API key in the sidebar!"
        )
        st.stop
