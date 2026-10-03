import os
import streamlit as st

if not st.session_state.get('authentication_status'):
    st.info('Please login from the Homepage to access this module.')
    st.stop()

st.title('Games')
st.info('Games are coming soon.')
