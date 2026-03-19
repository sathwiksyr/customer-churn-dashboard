import streamlit as st
from Config import VALID_USERNAME, VALID_PASSWORD
 
 
def show_login():
    st.markdown("""
    <div style="max-width:380px; margin:80px auto 0; background:#fff;
                border:1px solid #eaeaea; border-radius:16px; padding:40px 36px;
                box-shadow:0 4px 20px rgba(0,0,0,0.07);">
        <div style="text-align:center; margin-bottom:28px;">
            <span style="font-size:28px;">📊</span>
            <h2 style="font-size:20px; font-weight:600; color:#111; margin-top:8px;">ChurnIQ</h2>
            <p style="font-size:13px; color:#888;">Sign in to continue</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    col = st.columns([1, 2, 1])[1]
    with col:
        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••")
        if st.button("Sign in", use_container_width=True):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state["login"] = True
                st.rerun()
            else:
                st.error("Invalid credentials")
 