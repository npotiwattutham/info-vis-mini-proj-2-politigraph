import pandas as pd
import numpy as np
import plotly.graph_objects as go


def calendar_heatmap_chart():
    # Example list of parliamentary vote dates
    vote_dates = [
        "2025-01-03", "2025-01-07", "2025-01-15", "2025-02-20",
        "2025-02-25", "2025-03-05", "2025-03-12"
    ]

    # Convert to datetime
    vote_dates = pd.to_datetime(vote_dates)

    # Generate a full date range for the year
    year = 2025
    all_dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31")

    # Create a DataFrame with week number and weekday
    df = pd.DataFrame({'date': all_dates})
    df['week'] = df['date'].dt.isocalendar().week
    df['weekday'] = df['date'].dt.weekday  # Monday=0, Sunday=6
    df['vote'] = df['date'].isin(vote_dates).astype(int)  # 1 if vote occurred, else 0

    # Pivot table for heatmap: weekdays as y-axis, weeks as x-axis
    heatmap_data = df.pivot(index='weekday', columns='week', values='vote')

    # Plotly heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        colorscale='Blues',
        hovertemplate='Week %{x}, %{y}<br>Vote: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title=f'Parliamentary Votes Calendar {year}',
        yaxis=dict(autorange="reversed")  # So Monday is at the top
    )

    return fig

# Test
calendar_heatmap_chart().show()
