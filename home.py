import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

# Streamlit Component
import streamlit as st

from streamlit_bokeh import streamlit_bokeh

# Other Library
from datetime import datetime
from pythainlp.util import thai_strftime

# ============================================================================================================================================ #
# >> CSS Injection
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# >> Page and Navbar Configuration
overview_page = st.Page('overview.py', title='ภาพรวมการทำงาน')
detail_page = st.Page('detail.py', title='รายละเอียดรายมติ')

pg = st.navigation([overview_page, detail_page], position='top')
pg.run()