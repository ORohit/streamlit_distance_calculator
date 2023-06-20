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
# google_api_key = "**hardcoded API key"

# st. set_page_config(layout="wide")
st.title("Driving Distance Calculator :car:")
st.write("Upload your <b> CSV file with origin & destination pairs</b> to get driving distance between them. </br>Sample file <a href=""https://shorturl.at/jSXY7"">download here</a> ", unsafe_allow_html=True)
# orig_loc_col = st.text_input("Origin Column")
# dest_loc_col = st.text_input("Destination Column")
uploaded_file = st.file_uploader("Upload file -", type='csv')


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

with st.sidebar:

    st.markdown(
        "# HOW TO USE\n"
        "1. Enter your [Google API key](https://developers.google.com/maps/documentation/distance-matrix/overview) below🔑\n"  # noqa: E501
        "2. Upload your file📄\n"
        "3. Specify *Origin & Destination* columns 💬\n"
        "4. Review results and download if needed :100:\n"
    )
    api_key_input = st.text_input(
        "Google API Key",
        type="password",
        placeholder="Paste your Google API key here ",
        help="You can get your API key from https://developers.google.com/maps/documentation/distance-matrix/overview.",  # noqa: E501
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )
    if api_key_input:
        google_api_key = api_key_input

    st.markdown("---")
    st.markdown(
        "# ABOUT\n"
        "* Demonstrates a use case for building *Self-Serve* applications using *Streamlit*.\n"  # noqa: E501
        "* Fetches driving distances using Google API. \n"
        "*  Git link: [DistanceApp](https://github.com/ORohit/stremlit_test)\n"
    )

    st.markdown("---")
    st.markdown(
        """
        # FAQ
        ## How does this application work?
        When you upload the file and hit *Calculate Distance*,
        the code will fetch driving distances row by row by making API calls to Google.
        ## Do I need to have API key to use this application?
        Yes, an API key is needed by the application to talk to Google servers. 
        Since this is just a demo, I have embeded my personal API key within the code so that you need not get one.
        ## How long it takes to get the distances?
        It usually takes less than minute to fetch distances for about 100 records. """)

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file, encoding='latin-1')
    input_df_columns = input_df.columns
    # st.write("Uploaded data (top 5 rows): "), input_df.head(5)

    col1, col2 = st.columns(2)

    with col1:
        orig_loc_col = st.selectbox("Origin Column", input_df_columns)
    with col2:
        dest_loc_col = st.selectbox("Destination Column", input_df_columns)


    if st.button('GET DISTANCES (click & wait)'):
        # input_df['Driving Distance'] = input_df.apply(
        # lambda row: get_driving_distance(row[orig_loc_col], row[dest_loc_col], units=units), axis=1)

        for index, row in input_df.iterrows():
            input_df.at[index, 'Driving Distance'] = get_driving_distance(row[orig_loc_col], row[dest_loc_col], units=units)
        "Driving distance : ", input_df

        csv = convert_df(input_df)
        st.download_button('DOWNLOAD RESULTS', csv, 'output_drivingdistances.csv', 'text/csv', key='download-csv')
