import streamlit as st

import streamlit_antd_components as sac


def timeline(step:int,key):
    step_bar = sac.steps(
        items=[
            sac.StepsItem(title='Applied',disabled=True),
            sac.StepsItem(title='OA',subtitle='20/11/2023'),
            sac.StepsItem(title='Interview', disabled=True),
            sac.StepsItem(title='Offer', disabled=True),
        ], index=step, size='default',dot=True,key=key
    )
    return timeline

def get_track_component(company,title,location,image,step:int):
    col1,col2 = st.columns([1,2])
    with col2:
        timeline(step,key = F'{company}{title}-{step}')
    with col1:
        # Title
    
        # Logo, Company Name, and Location in a single column
        col1, col2 = st.columns([1, 2.5])

        with col1:
            st.image(image, use_column_width=True)  # Replace "vatic_logo.png" with the path to your logo image

        with col2:
            st.markdown(f"**{title}**")
            st.write(f"{company}")
            st.caption(f"📍 {location}")
    st.markdown("<br><br>", unsafe_allow_html=True )