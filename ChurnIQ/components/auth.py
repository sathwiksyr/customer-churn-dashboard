import os
import json
import hashlib
import streamlit as st
 
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "users.json")
 
 
# ── Helpers ──────────────────────────────────
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
 
 
# ── Public API ───────────────────────────────
def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)
 
 
def current_user() -> str:
    return st.session_state.get("username", "")
 
 
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()
 
 
# ── Login Page ───────────────────────────────
def show_login_page():
    _inject_auth_css()
 
    st.markdown("""
    <div class="auth-card">
        <div class="auth-header">
            <span class="auth-icon">📊</span>
            <h2>ChurnIQ</h2>
            <p>Sign in to your account</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    col = st.columns([1, 2, 1])[1]
    with col:
        email    = st.text_input("Email", placeholder="you@email.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
 
        if st.button("Sign in", use_container_width=True, key="login_btn"):
            users = _load_users()
            if email in users and users[email]["password"] == _hash(password):
                st.session_state["logged_in"] = True
                st.session_state["username"]  = users[email]["name"]
                st.rerun()
            else:
                st.error("Invalid email or password")
 
        st.markdown("<div style='text-align:center; margin-top:1rem; font-size:13px; color:#888;'>Don't have an account?</div>", unsafe_allow_html=True)
 
        if st.button("Create account →", use_container_width=True, key="goto_signup"):
            st.session_state["auth_page"] = "signup"
            st.rerun()
 
 
# ── Signup Page ──────────────────────────────
def show_signup_page():
    _inject_auth_css()
 
    st.markdown("""
    <div class="auth-card">
        <div class="auth-header">
            <span class="auth-icon">📊</span>
            <h2>ChurnIQ</h2>
            <p>Create your account</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    col = st.columns([1, 2, 1])[1]
    with col:
        name     = st.text_input("Full name", placeholder="Sathwik S.Y.R", key="signup_name")
        email    = st.text_input("Email", placeholder="you@email.com", key="signup_email")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="signup_pass")
        confirm  = st.text_input("Confirm password", type="password", placeholder="Re-enter password", key="signup_confirm")
 
        if st.button("Create account", use_container_width=True, key="signup_btn"):
            # Validations
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
                    st.success(f"Account created! Welcome, {name} 🎉")
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = name
                    st.rerun()
 
        st.markdown("<div style='text-align:center; margin-top:1rem; font-size:13px; color:#888;'>Already have an account?</div>", unsafe_allow_html=True)
 
        if st.button("Sign in →", use_container_width=True, key="goto_login"):
            st.session_state["auth_page"] = "login"
            st.rerun()
 
 
# ── Auth Router ──────────────────────────────
def show_auth():
    if "auth_page" not in st.session_state:
        st.session_state["auth_page"] = "login"
    if st.session_state["auth_page"] == "signup":
        show_signup_page()
    else:
        show_login_page()
 
 
# ── CSS ──────────────────────────────────────
def _inject_auth_css():
    st.markdown("""
    <style>
    .auth-card {
        max-width: 400px;
        margin: 60px auto 0;
        text-align: center;
    }
    .auth-header .auth-icon { font-size: 32px; }
    .auth-header h2 {
        font-size: 22px;
        font-weight: 600;
        color: #111;
        margin: 8px 0 4px;
    }
    .auth-header p { font-size: 13px; color: #888; margin: 0 0 24px; }
    </style>
    """, unsafe_allow_html=True)