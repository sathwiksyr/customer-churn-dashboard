# components/auth.py
import os
import json
import hashlib
import streamlit as st
 
USERS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "users.json"
)
 
def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
 
def _load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}
 
def _save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
 
def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)
 
def current_user() -> str:
    return st.session_state.get("username", "")
 
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"]  = ""
    st.session_state["mode"]      = None
    st.rerun()
 
def _header():
    st.markdown("""
    <div style="text-align:center; margin: 50px auto 28px;">
        <div style="font-size:36px; margin-bottom:10px;">📊</div>
        <div style="margin-bottom:6px;">
            <span style="font-size:24px; font-weight:700; color:#1D9E75;">ChurnIQ</span>
            <span style="font-size:18px; color:#ccc; margin:0 10px;">×</span>
            <span style="font-size:24px; font-weight:700; color:#378ADD;">DataLens</span>
        </div>
        <div style="font-size:11px; color:#aaa; letter-spacing:0.08em; margin-bottom:4px;">
            INTELLIGENCE PLATFORM
        </div>
        <div style="display:flex; justify-content:center; gap:8px; margin-top:8px;">
            <span style="background:#E1F5EE; color:#0F6E56; padding:2px 10px;
                         border-radius:20px; font-size:11px;">Churn Intelligence</span>
            <span style="background:#E6F1FB; color:#0C447C; padding:2px 10px;
                         border-radius:20px; font-size:11px;">Universal Analytics Studio</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
def show_login_page():
    _header()
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("""
        <p style='text-align:center; color:#888; font-size:14px; margin-bottom:1.2rem;'>
            Sign in to your account
        </p>
        """, unsafe_allow_html=True)
        email    = st.text_input("Email", placeholder="you@email.com",  key="login_email")
        password = st.text_input("Password", type="password",
                                 placeholder="••••••••",                key="login_pass")
 
        if st.button("Sign in", use_container_width=True, key="login_btn"):
            users = _load_users()
            if email in users and users[email]["password"] == _hash(password):
                st.session_state["logged_in"] = True
                st.session_state["username"]  = users[email]["name"]
                st.rerun()
            else:
                st.error("Invalid email or password")
 
        st.markdown("""
        <div style='text-align:center; margin-top:1rem; font-size:13px; color:#888;'>
            Don't have an account?
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create account →", use_container_width=True, key="goto_signup"):
            st.session_state["auth_page"] = "signup"
            st.rerun()
 
def show_signup_page():
    _header()
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("""
        <p style='text-align:center; color:#888; font-size:14px; margin-bottom:1.2rem;'>
            Create your account
        </p>
        """, unsafe_allow_html=True)
        name     = st.text_input("Full name",        placeholder="Your name",          key="signup_name")
        email    = st.text_input("Email",            placeholder="you@email.com",      key="signup_email")
        password = st.text_input("Password",         type="password",
                                 placeholder="Min 6 characters",                       key="signup_pass")
        confirm  = st.text_input("Confirm password", type="password",
                                 placeholder="Re-enter password",                      key="signup_confirm")
 
        if st.button("Create account", use_container_width=True, key="signup_btn"):
            if not name or not email or not password:
                st.error("All fields are required")
            elif "@" not in email:
                st.error("Enter a valid email address")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif password != confirm:
                st.error("Passwords do not match")
            else:
                users = _load_users()
                if email in users:
                    st.error("An account with this email already exists")
                else:
                    users[email] = {"name": name, "password": _hash(password)}
                    _save_users(users)
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = name
                    st.rerun()
 
        st.markdown("""
        <div style='text-align:center; margin-top:1rem; font-size:13px; color:#888;'>
            Already have an account?
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sign in →", use_container_width=True, key="goto_login"):
            st.session_state["auth_page"] = "login"
            st.rerun()
 
def show_auth():
    if "auth_page" not in st.session_state:
        st.session_state["auth_page"] = "login"
    if st.session_state["auth_page"] == "signup":
        show_signup_page()
    else:
        show_login_page()