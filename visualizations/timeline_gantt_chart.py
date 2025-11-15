import plotly.express as px
import pandas as pd
from pythainlp.util import thai_strftime
from datetime import datetime

def timeline_gantt_chart():
    df = pd.DataFrame([
        dict(role='สภาผู้แทนราษฎร', term='สภาผู้แทนราษฎร ชุดที่ 25', term_start=datetime(2019, 3, 24), term_end=datetime(2023, 3, 20)),
        dict(role='สภาผู้แทนราษฎร', term='สภาผู้แทนราษฎร ชุดที่ 26', term_start=datetime(2023, 5, 14), term_end=pd.NaT),
        dict(role='วุฒิสภา', term='วุฒิสภา ชุดที่ 12', term_start=datetime(2019, 5, 11), term_end=datetime(2024, 7, 9)),
        dict(role='วุฒิสภา', term='วุฒิสภา ชุดที่ 13', term_start=datetime(2024, 7, 10), term_end=pd.NaT)
    ])
    
    # Fill missing end dates with today
    today = datetime.today()
    df['term_end'] = df['term_end'].fillna(today)
    
    # Create timeline chart
    fig = px.timeline(
        df,
        x_start="term_start",
        x_end="term_end",
        y="role",
        color="term",
    )
    
    # Reverse the y-axis so earliest term is on top
    fig.update_yaxes(autorange="reversed", fixedrange=True)
    
    # Limit x-axis range: cannot scroll past today
    start = df['term_start'].min()
    end = today
    fig.update_xaxes(range=[start, end])
    
    # Tick frequency: use yearly ticks to reduce crowding
    ticks = [x for i,x in enumerate(pd.date_range(start=start, end=end, freq='QS')) if i%2 == 0]  # 'YS' = Year Start
    tick_labels = [thai_strftime(d.to_pydatetime(), '%b %Y') for d in ticks]
    
    fig.update_xaxes(
        tickvals=ticks,
        ticktext=tick_labels,
        fixedrange=False  # allow horizontal zoom but still restricted to max today
    )
    
    # Optional: layout adjustments
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        height=300,
    )
    
    return fig
