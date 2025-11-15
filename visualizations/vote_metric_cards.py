import streamlit as st

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
    card = st.markdown(f"""
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
    
    return card