import streamlit as st

google_api_singup = "https://developers.google.com/maps/documentation/javascript"

def set_openai_api_key(api_key: str):
    st.session_state["google_api_key"] = api_key

def sidebar():
    with st.sidebar:
        st.markdown(
            "# HOW TO USE\n"
            "1. Enter your [Google API key]({}) below🔑\n"
            "2. Upload your file📄\n"
            "3. Specify *Origin, Destination* columns & *Units* 💬\n"
            "4. Review results and download if needed!\n".format(google_api_singup)
        )
        api_key_input = st.text_input(
            "Google API Key",
            type="password",
            placeholder="Paste your Google API key here ",
            help="You can get your API key from {}.".format(google_api_singup),
            # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )
        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")

        st.markdown(
            """
            # FAQ
            ## How does this application work?
            When you upload the file and hit *Calculate Distance*,
            the code will fetch driving distances row by row by making API calls to Google.
            ## Do I need to have API key to use this application?
            Yes, an API key is needed by the application to talk to Google servers. Get yours [here]({}).
            ## How long it takes to get the distances?
            It usually takes less than minute to fetch distances for about 100 records. 
            ## Is it possible to obtain the source code? 
            Yes, GitHub link: [DistanceCalculator](https://github.com/ORohit/stremlit_test)""".format(google_api_singup))

