import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

# Streamlit Component
import streamlit as st

from streamlit_bokeh import streamlit_bokeh
from streamlit_extras.metric_cards import style_metric_cards

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

#region # รายละเอียดของการลงมติ #######################################################################################################################
st.header('ร่างพระราชบัญญัตินิรโทษกรรมแก่บุคคลซึ่งได้กระทำความผิดอันเนื่องมาจากเหตุการณ์ความขัดแย้งทางการเมือง พ.ศ. .... ซึ่ง นายชัยธวัช ตุลาธน กับคณะ เป็นผู้เสนอ วาระที่ 1')
st.badge('ไม่ผ่าน', icon=':material/close:' ,color='red')
st.markdown(f'**วันที่:** {thai_strftime(datetime(2025, 7, 16), fmt='%d %B %Y')}')
st.markdown(f'**คำอธิบาย:** _ไม่มีคำอธิบาย_')
st.divider()
#endregion ########################################################################################################################################

#region # สรุปคะแนนการลงมติ (ภาพรวม) ##################################################################################################################
# Data
vote_types = ['เห็นด้วย', 'ไม่เห็นด้วย', 'งดออกเสียง', 'ไม่ลงคะแนน', 'ลา/ขาดลงมติ']
vote_results = [147, 319, 6, 1, 20]
vote_colors = ['#2EC4B6', '#E71D36', '#FF9F1C', "#00325A", '#7F8B92']

# Wide-format data
data = pd.DataFrame([vote_results], columns=vote_types)
data['y'] = 0  # single horizontal bar

# Add percentage columns for each vote type
total_votes = sum(vote_results)
for vt in vote_types:
    data[f'{vt}_pct'] = data[vt] / total_votes * 100  # percentage

st.subheader('📊 ภาพรวมผลการลงมติ')

def metric_card(
    label,
    value,
    delta=None,
    border_left_color="#4CAF50",
    background_color="#ffffff",
    border_color="#e0e0e0",
    border_radius_px=8,
    box_shadow=True
):
    shadow = "box-shadow: 0 2px 6px rgba(0,0,0,0.08);" if box_shadow else ""

    # 🚨 FIX: Use 'border-left-width' and 'border-left-style' separately
    # Streamlit’s internal sanitizer can ignore shorthand `border-left: ... solid ...`
    st.markdown(f"""
        <div class="text" style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 1px solid {border_color};
            border-left-width: 12px;
            border-left-style: solid;
            border-left-color: {border_left_color};
            background-color: {background_color};
            border-radius: {border_radius_px}px;
            padding: 1rem 1.2rem;
            margin: 0.5rem 0;
            {shadow}
        ">
            <div style="font-size: 0.9em; color: #000;">{label}</div>
            <div style="font-size: 1.6em; font-weight: 600; color: #000;">{value}</div>
             <div style="font-size: 0.8em; font-weight: 400; color: #666;">{delta}</div>
        </div>
    """, unsafe_allow_html=True)

    
columns = st.columns(6)
for i, col in enumerate(columns):
    if i == 0: # องค์ประชุมรวม
        with col:
            metric_card('องค์ประชุม', f'{sum(vote_results)}', f'คิดเป็นสัดส่วน 100.00%', border_left_color='#000000')
    else:
        with col:
            metric_card(f'{vote_types[i-1]}', f'{vote_results[i-1]}', f'คิดเป็นสัดส่วน {vote_results[i-1]*100/sum(vote_results):.2f}%',  border_left_color=vote_colors[i-1])

# >> BOKEH Chart
source = ColumnDataSource(data)

p = figure(sizing_mode='stretch_width',
           y_range=(-0.1, 0.4),
           height=40,
           toolbar_location=None,)

renderers = p.hbar_stack(stackers=vote_types,
                         y='y',
                         height=0.25,
                         color=vote_colors,
                         source=source,
                         legend_label=vote_types)

# Add hover tool **one per renderer**
for r, vt in zip(renderers, vote_types):
    hover = HoverTool(tooltips=[
        (vt, f"@{{{vt}}}"),
        ('Percentage', f"@{{{vt}_pct}}{{0.00}}%")
    ], renderers=[r])
    p.add_tools(hover)

# Formatting
p.ygrid.grid_line_color = None
p.yaxis.visible = False
p.xaxis.visible = False
p.legend.orientation = "horizontal"
p.legend.location = "top_left"

# Show plot
streamlit_bokeh(p, use_container_width=True)
st.divider()

#endregion ########################################################################################################################################

st.subheader('👥 ผลการลงมติรายสังกัด')
# Bokeh Chart
# --- Create Bokeh figures ---
p1 = figure(title="Bokeh Chart 1", width=500, height=400)
p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=10, color="navy", alpha=0.5)

p2 = figure(title="Bokeh Chart 2", width=500, height=400)
p2.line([1, 2, 3, 4, 5], [5, 3, 4, 2, 6], line_width=3, color="firebrick")

# --- Use tabs for switching ---
tab1, tab2 = st.tabs(["แสดงผลตามจำนวนสมาชิก", "แสดงผลตามสัดส่วน"])

with tab1:
    streamlit_bokeh(p1)

with tab2:
    streamlit_bokeh(p2)