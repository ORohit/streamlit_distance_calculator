import streamlit as st
import pandas as pd
import logging

from component_sidebar import sidebar
from component_functions import get_driving_distance, convert_df, api_input_check

# configuring the logger
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(format=' %(asctime)s  %(name)-12s %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__ + " : ")


# st. set_page_config(layout="wide")
st.title("Driving Distance Calculator :car:")
st.write("Upload your <b> CSV file with origin & destination pairs</b> to get driving distance between them. </br>Sample file <a href=""https://shorturl.at/jSXY7"">download here</a> ", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload file -", type='csv')

sidebar()
google_api_key = st.session_state.get("google_api_key")

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file, encoding='latin-1')
    input_df_columns = input_df.columns
    # st.write("Uploaded data (top 5 rows): "), input_df.head(5)

    col1, col2, col3 = st.columns(3)

    with col1:
        orig_loc_col = st.selectbox("Select Origin Column", input_df_columns)
    with col2:
        dest_loc_col = st.selectbox("Select Destination Column", input_df_columns)
    with col3:
        units = st.radio("Select Units", ["imperial", "metric"])

    if st.button('GET DISTANCES'):
        api_input_check()

        miles_or_km = 'miles'
        if units == 'metric':
            miles_or_km = 'km'

        with st.spinner("Fetching distances... This may take a while⏳"):
            for index, row in input_df.iterrows():
                input_df.at[index, 'Driving Distance ('+miles_or_km+')'] = get_driving_distance(row[orig_loc_col], row[dest_loc_col], google_api_key, units=units)
        "Driving distance : ", input_df

        csv = convert_df(input_df)
        st.download_button('DOWNLOAD RESULTS', csv, 'output_drivingdistances.csv', 'text/csv', key='download-csv')
