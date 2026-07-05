"""
Step 4 Page - API Keys & Database Configuration
Halaman untuk konfigurasi API key dan database
"""

import streamlit as st
from api_client import api_client
from typing import Any, Dict, List


def render_step4_page():
    """Render halaman Step 4 - API & Database Configuration"""
    
    st.title("🔐 Step 4: Konfigurasi API & Database")
    
    # Initialize session state for step 4
    if 'step4_data' not in st.session_state:
        st.session_state.step4_data = {
            'openai_key': '',
            'db_host': 'localhost',
            'db_port': '5432',
            'db_name': '',
            'db_user': '',
            'db_password': ''
        }
    
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["API Keys", "Database Config"])
    
    # ==================== TAB 1: API KEYS ====================
    with tab1:
        st.subheader("🔑 API Keys Configuration")
        
        st.write("Konfigurasi API key yang diperlukan untuk integrasi layanan.")
        st.caption("*Semua field opsional - anda dapat mengisinya nanti*")
        
        # OpenAI API Key
        openai_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.step4_data['openai_key'],
            placeholder="sk-...",
            type="password",
            key="openai_key_input"
        )
        
        if openai_key:
            st.session_state.step4_data['openai_key'] = openai_key
        
        with st.expander("ℹ️ Petunjuk OpenAI API Key"):
            st.write("""
            1. Kunjungi https://platform.openai.com/
            2. Login atau daftar akun
            3. Pergi ke "API Keys"
            4. Klik "Create new secret key"
            5. Copy dan paste key di sini
            """)
        
        st.divider()
        
        # Additional API keys section
        st.subheader("API Keys Lainnya (Opsional)")
        
        with st.expander("Claude API Key"):
            claude_key = st.text_input(
                "Claude API Key",
                placeholder="sk-ant-...",
                type="password",
                key="claude_key_input"
            )
            if claude_key:
                st.session_state.step4_data['claude_key'] = claude_key
        
        with st.expander("Google API Key"):
            google_key = st.text_input(
                "Google API Key",
                placeholder="AIza...",
                type="password",
                key="google_key_input"
            )
            if google_key:
                st.session_state.step4_data['google_key'] = google_key
    
    # ==================== TAB 2: DATABASE CONFIG ====================
    with tab2:
        st.subheader("🗄️ Database Configuration")
        
        st.write("Konfigurasi koneksi database untuk aplikasi anda.")
        st.caption("*Semua field opsional - anda dapat mengisinya nanti*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # DB Host
            db_host = st.text_input(
                "Database Host",
                value=st.session_state.step4_data['db_host'],
                placeholder="localhost",
                key="db_host_input"
            )
            st.session_state.step4_data['db_host'] = db_host
            
            # DB Name
            db_name = st.text_input(
                "Database Name",
                value=st.session_state.step4_data['db_name'],
                placeholder="database_name",
                key="db_name_input"
            )
            st.session_state.step4_data['db_name'] = db_name
        
        with col2:
            # DB Port
            db_port = st.text_input(
                "Database Port",
                value=st.session_state.step4_data['db_port'],
                placeholder="5432",
                key="db_port_input"
            )
            st.session_state.step4_data['db_port'] = db_port
        
        st.divider()
        
        # Database Credentials
        st.subheader("Kredensial Database")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # DB User
            db_user = st.text_input(
                "Database User",
                value=st.session_state.step4_data['db_user'],
                placeholder="username",
                key="db_user_input"
            )
            st.session_state.step4_data['db_user'] = db_user
        
        with col2:
            # DB Password
            db_password = st.text_input(
                "Database Password",
                value=st.session_state.step4_data['db_password'],
                placeholder="password",
                type="password",
                key="db_password_input"
            )
            st.session_state.step4_data['db_password'] = db_password
        
        # Database type selection
        st.divider()
        st.subheader("Tipe Database")
        
        db_type = st.selectbox(
            "Pilih tipe database yang digunakan",
            ["PostgreSQL", "MySQL", "SQLite", "MongoDB", "Firebase"],
            key="db_type_select"
        )
        
        st.session_state.step4_data['db_type'] = db_type
        
        # Database connection example
        with st.expander("📋 Format Koneksi Database"):
            st.code(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
                   language="text")
    
    # ==================== ACTION BUTTONS ====================
    st.divider()
    
    st.subheader("🎉 Finalisasi Setup Project")
    st.write("Anda sudah menyelesaikan semua step konfigurasi project.")
    
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1.5])
    
    with button_col1:
        if st.button("⬅️ Kembali ke Step 3", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()
    
    with button_col3:
        if st.button("✓ SELESAIKAN SETUP ✓", use_container_width=True, 
                    type="primary"):
            with st.spinner("Menyimpan konfigurasi..."):
                # Save configuration
                setup_data = {
                    'project_id': st.session_state.get('current_project_id'),
                    'api_keys': {
                        'openai': st.session_state.step4_data.get('openai_key', ''),
                        'claude': st.session_state.step4_data.get('claude_key', ''),
                        'google': st.session_state.step4_data.get('google_key', '')
                    },
                    'database': {
                        'type': st.session_state.step4_data.get('db_type', 'PostgreSQL'),
                        'host': st.session_state.step4_data['db_host'],
                        'port': st.session_state.step4_data['db_port'],
                        'name': st.session_state.step4_data['db_name'],
                        'user': st.session_state.step4_data['db_user'],
                        'password': st.session_state.step4_data['db_password']
                    }
                }
                
                # Simulate saving
                import time
                time.sleep(1)
                
                st.session_state.current_step = None
                st.success("🎉 Setup project berhasil diselesaikan!")
                st.info("Anda dapat sekarang melihat project di halaman Projects.")
                
                import time
                time.sleep(2)
                st.rerun()


if __name__ == "__main__":
    render_step4_page()
