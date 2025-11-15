import pandas as pd
import plotly.express as px

def overview_vote_ratio(pivoted_df):
    # Plot horizontal stacked bar with Plotly Express
    fig = px.bar(
        pivoted_df,
        x="count",      # proportion of each vote
        y="dummy",    # dummy y-axis, same for all
        orientation='h',
        color="option",
        color_discrete_sequence=[x for x in pivoted_df['color']],
        hover_data={"count": True, "option": True, 'dummy': False}
    )

    fig.update_layout(
        barmode='stack',
        height=100,
        margin=dict(l=0, r=0, t=0, b=0),
        
        xaxis=dict(title='', range=[0, pivoted_df['count'].sum()], visible=False, fixedrange=True),
        yaxis=dict(title='', visible=False, fixedrange=True),

        legend=dict(title='', orientation='h', yanchor='bottom',y=1, xanchor='left', x=-0.01, visible=True, itemclick=False, itemdoubleclick=False),
        
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        
    )

    return fig