import pandas as pd

# Visualization
from visualizations.overview_vote_ratio import overview_vote_ratio
from visualizations.vote_metric_cards import metric_card
# Streamlit Component
import streamlit as st
from streamlit_autocomplete import st_textcomplete_autocomplete

# Other Library
from datetime import datetime
from pythainlp.util import thai_strftime

# ============================================================================================================================================ #
# >> CSS Injection
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# >> Set Page Layout
st.set_page_config(page_title="Voting Details",
                   page_icon="📊",
                   layout='wide')

with st.spinner('Loading data', show_time=True):
    data_df = pd.read_pickle('./data/VOTE_RESULTS_2.pkl')
    all_bill_name = list(data_df['title'].unique())

# User Input
st.subheader(':material/search: ค้นหา')
selected_bill = st.selectbox("เลือกร่างกฎหมายที่ต้องการ:", all_bill_name)
st.divider()

with st.spinner('Loading Data', show_time=True):
    df = data_df[data_df['title'] == selected_bill]
    # st.dataframe(df)
    
    bill_title = df['title'].iloc[0]
    
    if df['result'].iloc[0] == 'ผ่าน':
        bill_status = dict(text='ผ่าน', icon=':material/check:', color='green')
    elif df['result'].iloc[0] == 'ไม่ผ่าน':
        bill_status = dict(text='ไม่ผ่าน', icon=':material/close:', color='red')
    elif pd.isna(df['result'].iloc[0]):
        bill_status = dict(text='รอผลพิจารณา', icon=':material/hourglass:', color='violet')
    else:
        bill_status = dict(text=df['result'].iloc[0], icon=':material/info:', color='blue')
        
    bill_date = thai_strftime(pd.to_datetime(df['start_date'].iloc[0]), fmt='%d %B %Y')
    
    bill_senate_only = df['voter_party'].unique()

#region # รายละเอียดของการลงมติ #######################################################################################################################
st.header(bill_title)
st.badge(bill_status['text'], icon=bill_status['icon'] ,color=bill_status['color'])
st.markdown(f'**วันที่:** {bill_date}')
st.markdown(f'**คำอธิบาย:** _ไม่มีคำอธิบาย_')
#endregion ########################################################################################################################################

#region # สรุปคะแนนการลงมติ (ภาพรวม) ##################################################################################################################
# Data
color_df = pd.DataFrame([
    dict(option='เห็นด้วย',           color='#2EC4B6'),
    dict(option='ไม่เห็นด้วย',         color='#E71D36'),
    dict(option='งดออกเสียง',        color='#FF9F1C'),
    dict(option='ไม่ลงคะแนนเสียง',    color='#00325A'),
    dict(option='ลา / ขาดลงมติ',     color='#7F8B92'),
])

pivoted_df = df.groupby(['option'], as_index=False)[['vote_id']].count().rename(columns={'vote_id': 'count'})

pivoted_df = pd.merge(left=color_df, right=pivoted_df, how='left')
pivoted_df['count'] = pivoted_df['count'].fillna(0)
pivoted_df['dummy'] = 1

# Metric Card
columns = st.columns(6)
for i, col in enumerate(columns):
    if i == 0: # องค์ประชุมรวม
        with col:
            metric_card('องค์ประชุม', f'{int(pivoted_df['count'].sum()):d}', f'คิดเป็นสัดส่วน 100.00%', border_left_color='#000000')
    else:
        with col:
            metric_card(f'{pivoted_df['option'].iloc[i-1]}', f'{int(pivoted_df['count'].iloc[i-1]):d}', f'คิดเป็นสัดส่วน {pivoted_df['count'].iloc[i-1]*100/pivoted_df['count'].sum():.2f}%',  border_left_color=pivoted_df['color'].iloc[i-1])

# Stacked Bar Chart
viz_overview_stacked_bar_ratio = st.empty()
st.divider()

# Load Visualizations
with viz_overview_stacked_bar_ratio:
    with st.spinner('Loading Visualization', show_time=True):
        fig = overview_vote_ratio(pivoted_df)
viz_overview_stacked_bar_ratio.plotly_chart(figure_or_data=fig, config = {'width': 'stretch'})

#endregion ########################################################################################################################################

st.subheader('👥 ผลการลงมติรายสังกัด')

tab1, tab2 = st.tabs(["แสดงผลตามจำนวนสมาชิก", "แสดงผลตามสัดส่วน"])

with tab1:
    pass

with tab2:
    pass


