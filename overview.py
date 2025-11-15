import pandas as pd

# Bokeh Related Imports
from streamlit_bokeh import streamlit_bokeh
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

# Plotly Related Imports
from visualizations.absent_graph import absent_graph
from visualizations.timeline_gantt_chart import timeline_gantt_chart
# from visualizations.calendar_map import calendar_heatmap_chart

# Streamlit Component
import streamlit as st

# Other Library
from datetime import datetime
from pythainlp.util import thai_strftime

# ============================================================================================================================================ #
# >> CSS Injection
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# >> Set Page Layout
st.set_page_config(page_title="ภาพรวม",
                   page_icon="📊",
                   layout='wide')

#region # Page Heading ############################################################################################################################
st.header('ภาพรวมการทำงานของสมาชิกสภาผู้แทนราษฎรและสมาชิกวุฒิสภา')
st.markdown('เนื่องจากเงินเดือนของสมาชิกสภาผู้แทนราษฎร (สส.) และสมาชิกวุฒิสภา (สว.) รวมไปถึงค่าใช้จ่ายต่าง ๆ ในการจัดประชุมสภา ล้วนมาจากภาษีของประชาชน')

st.divider()
#endregion ########################################################################################################################################

#region # Timeline ###############################################################################################################################
st.subheader('วาระของสภาผู้แทนราษฎรและวุฒิสภา')
viz_timeline = st.empty()

st.divider()
#endregion ########################################################################################################################################

#region # CALENDAR HEATMAP ###############################################################################################################################
st.subheader('วาระของสภาผู้แทนราษฎรและวุฒิสภา')
viz_calendar = st.empty()

st.divider()
#endregion ########################################################################################################################################

#region # Absent Rate #############################################################################################################################
st.subheader('อัตราการลาหรือขาดประชุมของสมาชิก')
st.warning(f"""**หมายเหตุ:** อัตราการลาหรือขาดประชุมของสมาชิก อาจเกิดขึ้นจากหลายสาเหตุ เช่น การติดภารกิจอื่น การลาป่วย หรือเหตุผลส่วนตัวอื่น ๆ 
        **จึงไม่ได้สะท้อนถึงความไม่รับผิดชอบของสมาชิกเสมอไป**""", icon=':material/warning:')

columns = st.columns(3)

with columns[0]:
    st.markdown('#### ภาพรวม')

with columns[1]:
    st.markdown('#### รายสมาชิก')
    viz_packed_bubble_chart = st.empty()
    
with columns[2]:
    st.markdown('#### รายสังกัด')
    

st.divider()
#endregion ########################################################################################################################################

# Render Visualization
with viz_timeline:
    with st.spinner('Loading Visualization', show_time=True):
        fig = timeline_gantt_chart()
viz_timeline.plotly_chart(figure_or_data=fig, config = {'width': 'stretch'})

# with viz_calendar:
    # with st.spinner('Loading Visualization', show_time=True):
        # fig = calendar_heatmap_chart()
# viz_calendar.plotly_chart(figure_or_data=fig, config = {'width': 'stretch'})

with viz_packed_bubble_chart:
    with st.spinner('Loading Visualization', show_time=True):
        fig = absent_graph()
viz_packed_bubble_chart.plotly_chart(figure_or_data=fig, config = {'width': 'stretch',
                                                                   'dragMode': 'pan'})