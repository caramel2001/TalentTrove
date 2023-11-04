import streamlit as st

import streamlit_antd_components as sac


def timeline(step:int,date,key,rejected=True):
    steps = ['Applied','OA','Interview','Offer']
    items=[]
    for i,j in zip(steps,range(0,4)):
        if step == j and not rejected:
            items.append(sac.StepsItem(title=i,subtitle=date,icon='check-circle-fill'))
        else:
            items.append(sac.StepsItem(title=i,disabled=True,icon='dot'))
    if rejected:
        items.append(sac.StepsItem(title='Rejected',icon='x-circle-fill'))
        step=4
    step_bar = sac.steps(
        items=items, index=step, size='default',key=key
    )
    return timeline

def get_track_component(company,title,location,image,step:int,date:str,rejected:bool):
    col1,col2 = st.columns([1,2])
    with col2:
        timeline(step,date,key = F'{company}{title}-{step}',rejected=rejected)
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