import streamlit as st
import streamlit_authenticator as stauth
import os
def intro():
    import streamlit as st

    st.write("# Welcome to TalentTrove! 👋")
    # st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        TalentTrove is an open-source app framework built specifically for
        Tracking and managing your Job Applications.        
    """
    )
    login()

def login():
    import yaml
    from yaml.loader import SafeLoader
    with open('./talenttrove/app/secrets.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    authenticator.login('Login', 'main')
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'sidebar', key='logout')
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
intro()