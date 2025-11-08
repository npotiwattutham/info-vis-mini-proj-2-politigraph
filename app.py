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

# >> Set Page Layout
st.set_page_config(page_title="Voting Details",
                   page_icon="📊",
                   layout='wide')

# >> Set Sidebar
st.sidebar.header('Voting Details')

# >> Title
st.header('ร่างพระราชบัญญัตินิรโทษกรรมแก่บุคคลซึ่งได้กระทำความผิดอันเนื่องมาจากเหตุการณ์ความขัดแย้งทางการเมือง พ.ศ. .... ซึ่ง นายชัยธวัช ตุลาธน กับคณะ เป็นผู้เสนอ')
st.markdown(f'**วันที่:** {thai_strftime(datetime(2025, 7, 16), fmt='%d %B %Y')}')
st.markdown(f'**คำอธิบาย:** _ไม่มีคำอธิบาย_')
st.markdown(f'**ผลการลงมติ:** :red-badge[:material/close: ไม่ผ่าน]')
st.divider()

# >> สรุปผลการลงมติ

# Data
vote_types = ['เห็นด้วย', 'ไม่เห็นด้วย', 'งดออกเสียง', 'ไม่ลงคะแนน', 'ลา/ขาดลงมติ']
vote_results = [147, 319, 6, 1, 20]
vote_colors = ['#2EC4B6', '#E71D36', '#FF9F1C', '#011627', '#7F8B92']

# Wide-format data
data = pd.DataFrame([vote_results], columns=vote_types)
data['y'] = 0  # single horizontal bar

# Add percentage columns for each vote type
total_votes = sum(vote_results)
for vt in vote_types:
    data[f'{vt}_pct'] = data[vt] / total_votes * 100  # percentage

print(data)

st.subheader('สรุปผลการลงมติ')
columns = st.columns(6)
for i, col in enumerate(columns):
    if i == 0: # องค์ประชุมรวม
        with col:
            st.metric('องค์ประชุม', f'{sum(vote_results)}', border=True)
    else:
        with col:
            st.metric(vote_types[i-1], f'{vote_results[i-1]} ({vote_results[i-1]*100/sum(vote_results):.2f}%)', border=True)
# >> BOKEH Chart


# ColumnDataSource
source = ColumnDataSource(data)

# Figure
p = figure(sizing_mode='stretch_width',
           y_range=(-0.1, 0.4),
           height=40,
           toolbar_location=None,)

# Stacked bars
renderers = p.hbar_stack(stackers=vote_types,
                         y='y',
                         height=0.25,
                         color=vote_colors,
                         source=source,
                         legend_label=vote_types)

# Add hover tool **one per renderer**
for r, vt in zip(renderers, vote_types):
    hover = HoverTool(tooltips=[
        (vt, f"@{{{vt}}}"),         # wrap column name in {}
        ('Percentage', f"@{{{vt}_pct}}{{0.00}}%")
    ], renderers=[r])
    p.add_tools(hover)

# Formatting
p.ygrid.grid_line_color = None
p.x_range.start = 0
p.yaxis.visible = False
p.legend.orientation = "horizontal"
p.legend.location = "top_left"

# Show plot
streamlit_bokeh(p, use_container_width=True)




st.divider()



# >> from streamlit_card import card
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Pass")
    
with col2:
    st.header("In Progress")
    st.metric(label="In Progress", value=100, border=True)

with col3:
    st.header("Withdrawn")
