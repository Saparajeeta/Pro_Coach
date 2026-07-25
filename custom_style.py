import streamlit as st
import base64
import os

def apply_custom_style():
    """Injects premium CSS and loads custom background if available."""
    
    # 1. Check for custom background image (background.jpg)
    bg_css = ""
    bg_path = "background.jpg"
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        bg_css = f"""
        .stApp {{
            background-image: linear-gradient(rgba(10, 10, 12, 0.8), rgba(10, 10, 12, 0.9)), url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
    else:
        bg_css = """
        .stApp {
            background-color: #0c0c0e;
        }
        """

    # 2. Main CSS Injection
    st.markdown(f"""
        <style>
        /* Import premium font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap');

        /* Base Typography */
        html, body, [class*="css"]  {{
            font-family: 'Outfit', sans-serif !important;
            color: #E2E8F0;
        }}

        /* Apply Background */
        {bg_css}

        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: #ffffff;
            font-weight: 700;
        }}

        h1 {{
            background: -webkit-linear-gradient(45deg, #FF6B00, #FBB034);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            letter-spacing: -1px;
        }}

        /* Custom Metric Cards */
        .premium-card {{
            background: rgba(30, 30, 35, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 20px;
        }}
        .premium-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(255, 107, 0, 0.15);
            border-color: rgba(255, 107, 0, 0.3);
        }}
        .premium-card h2 {{
            color: #FBB034 !important;
            font-size: 3rem;
            margin: 10px 0;
            text-shadow: 0 0 20px rgba(251, 176, 52, 0.4);
        }}
        .premium-card p {{
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-size: 0.85rem;
            margin: 0;
        }}
        .premium-card .sub-text {{
            color: #64748B;
            font-size: 0.8rem;
            margin-top: 5px;
            text-transform: none;
            letter-spacing: 0;
        }}

        /* WebRTC Camera Window Fixes */
        .stWebRtc, video {{
            width: 100% !important;
            max-width: 720px !important;
            height: auto !important;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            border: 2px solid rgba(255, 255, 255, 0.05);
            margin: 0 auto;
            display: block;
            object-fit: cover !important;
        }}

        /* Buttons */
        .stButton>button {{
            background: linear-gradient(90deg, #FF6B00 0%, #FBB034 100%);
            color: white !important;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            letter-spacing: 0.5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: scale(1.02);
            box-shadow: 0 0 15px rgba(255, 107, 0, 0.4);
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background: rgba(15, 15, 18, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        /* Divider */
        hr {{
            border-color: rgba(255, 255, 255, 0.1);
        }}
        </style>
    """, unsafe_allow_html=True)
