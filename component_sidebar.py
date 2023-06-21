import streamlit as st

def set_openai_api_key(api_key: str):
    st.session_state["google_api_key"] = api_key

def sidebar():
    with st.sidebar:
        st.markdown(
            "# HOW TO USE\n"
            "1. Enter your [Google API key](https://developers.google.com/maps/documentation/distance-matrix/overview) below🔑\n"  # noqa: E501
            "2. Upload your file📄\n"
            "3. Specify *Origin, Destination* columns & *Units* 💬\n"
            "4. Review results and download if needed!\n"
        )
        api_key_input = st.text_input(
            "Google API Key",
            type="password",
            placeholder="Paste your Google API key here ",
            help="You can get your API key from https://developers.google.com/maps/documentation/distance-matrix/overview.",
            # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )
        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown(
            "# ABOUT\n"
            "* Demonstrates a use case for building *Self-Serve* applications using *Streamlit*.\n"  # noqa: E501
            # "* Fetches driving distances using Google API. \n"
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
            ## How long it takes to get the distances?
            It usually takes less than minute to fetch distances for about 100 records. """)