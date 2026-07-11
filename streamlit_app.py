"""
Streamlit Integration dengan Flask API
Menghubungkan Streamlit frontend dengan Flask backend melalui API client
"""

import streamlit as st
from api_client import api_client
import time
from typing import Any, Dict

# Import step pages
from pages.step1_page import render_step1_page
from pages.step2_page import render_step2_page
from pages.step3_page import render_step3_page
from pages.step4_page import render_step4_page

# Set page config
st.set_page_config(
    page_title="Soft AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 20px;
    }
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    .error-box {
        padding: 15px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
    }
    .info-box {
        padding: 15px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'api_connected' not in st.session_state:
    st.session_state.api_connected = False  # bool
    st.session_state.current_project = None  # Optional[Dict[str, Any]]
    st.session_state.projects = []  # List[Dict[str, Any]]
    st.session_state.current_step = None  # Optional[int] - Track current step (1-4) in wizard
    st.session_state.current_project_id = None  # Optional[int]


def check_api_connection():
    """Check if API is available"""
    status = api_client.health_check()
    return status.get('success', False)


def display_success(message: str):
    """Display success message"""
    st.markdown(f'<div class="success-box">{message}</div>', unsafe_allow_html=True)


def display_error(message: str):
    """Display error message"""
    st.markdown(f'<div class="error-box">{message}</div>', unsafe_allow_html=True)


def display_info(message: str):
    """Display info message"""
    st.markdown(f'<div class="info-box">{message}</div>', unsafe_allow_html=True)


# ======================== STEP WIZARD NAVIGATION ========================

# Show step pages if in wizard mode
if st.session_state.current_step is not None:
    st.sidebar.title("📋 Project Wizard")
    
    # Progress tracking
    step_labels = {
        1: "📋 Step 1: Info Project",
        2: "🎨 Step 2: Design Figma",
        3: "🔧 Step 3: Komponen UI",
        4: "🔐 Step 4: API & Database"
    }
    
    st.sidebar.progress((st.session_state.current_step - 1) / 4)
    st.sidebar.write(f"**Progress:** Step {st.session_state.current_step}/4")
    
    # Display current step
    if st.session_state.current_step == 1:
        render_step1_page()
    elif st.session_state.current_step == 2:
        render_step2_page()
    elif st.session_state.current_step == 3:
        render_step3_page()
    elif st.session_state.current_step == 4:
        render_step4_page()
    
    st.stop()


# ======================== SIDEBAR ========================

with st.sidebar:
    st.title("🔧 Soft AI Pro")
    
    # Check API connection
    if st.button("🔌 Cek Koneksi API"):
        with st.spinner("Checking connection..."):
            status = api_client.get_status()
            if status.get('success'):
                st.session_state.api_connected = True
                display_success("✓ API terhubung!")
            else:
                st.session_state.api_connected = False
                display_error("✗ Gagal menghubung ke API")
    
    # Navigation
    st.divider()
    st.subheader("📌 Navigasi")
    
    page = st.radio(
        "Pilih halaman:",
        ["🏠 Dashboard", "📋 Projects", "⚙️ Pengaturan"]
    )
    
    st.divider()
    
    # API Status
    st.subheader("📊 Status API")
    if st.session_state.api_connected:
        st.success("API: Connected")
    else:
        st.error("API: Disconnected")


# ======================== MAIN CONTENT ========================

if page == "🏠 Dashboard":
    st.title("Dashboard")
    
    # Check API connection
    if not st.session_state.api_connected:
        st.session_state.api_connected = check_api_connection()
    
    if st.session_state.api_connected:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Projects", "0", "Loading...")
        with col2:
            st.metric("Active Users", "0", "Loading...")
        with col3:
            st.metric("API Status", "Online", "✓")
        
        # Load projects
        projects_response = api_client.get_all_projects()
        if projects_response.get('success'):
            projects = projects_response.get('data', [])
            st.session_state.projects = projects
            
            if projects:
                st.subheader("📊 Recent Projects")
                for project in projects[:5]:
                    with st.expander(f"📁 {project.get('name', 'Unnamed')}"):
                        st.write(f"**ID:** {project.get('id')}")
                        st.write(f"**Type:** {project.get('project_type')}")
                        st.write(f"**Language:** {project.get('programming_language')}")
                        st.write(f"**Description:** {project.get('description')}")
            else:
                display_info("Belum ada project. Buat project baru untuk memulai!")
        else:
            display_error(projects_response.get('error', 'Error loading projects'))
    else:
        display_error("❌ API tidak terhubung. Hubungkan API terlebih dahulu dari sidebar.")


elif page == "📋 Projects":
    st.title("Manajemen Projects")
    
    if not st.session_state.api_connected:
        st.session_state.api_connected = check_api_connection()
    
    if st.session_state.api_connected:
        tab1, tab2, tab3 = st.tabs(["Buat Project", "Daftar Projects", "Kelola Project"])
        
        # ======================== TAB 1: Buat Project ========================
        with tab1:
            st.subheader("Buat Project Baru")
            
            # Option to use wizard or simple form
            create_option = st.radio(
                "Pilih metode pembuatan project:",
                ["🚀 Wizard Lengkap (Step 1-4)", "⚡ Form Cepat"]
            )
            
            if create_option == "🚀 Wizard Lengkap (Step 1-4)":
                st.info("📝 Wizard akan memandu Anda melalui 4 langkah untuk membuat project dengan lengkap.")
                
                if st.button("🚀 Mulai Wizard Buat Project", use_container_width=True, type="primary", key="start_wizard"):
                    st.session_state.current_step = 1
                    st.rerun()
            
            else:  # Simple form
                col1, col2 = st.columns(2)
                
                with col1:
                    project_name = st.text_input("Nama Project", key="project_name")
                    project_type = st.selectbox(
                        "Tipe Project",
                        ["Web Application", "Mobile App", "Desktop Software", "AI/ML Project", "Database System"]
                    )
                
                with col2:
                    programming_language = st.selectbox(
                        "Bahasa Pemrograman",
                        ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#"]
                    )
                    description = st.text_area("Deskripsi Project")
                
                if st.button("➕ Buat Project", use_container_width=True, key="create_project_btn"):
                    if not project_name:
                        display_error("⚠️ Nama project tidak boleh kosong!")
                    else:
                        with st.spinner("Membuat project..."):
                            response = api_client.create_project(
                                name=project_name,
                                description=description,
                                project_type=project_type,
                                programming_language=programming_language
                            )
                            
                            if response.get('success'):
                                display_success(f"✓ Project '{project_name}' berhasil dibuat! (ID: {response.get('project_id')})")
                                st.session_state.current_project = response.get('data')
                                time.sleep(1)
                                st.rerun()
                            else:
                                display_error(f"❌ Error: {response.get('error')}")
        
        # ======================== TAB 2: Daftar Projects ========================
        with tab2:
            st.subheader("Daftar Semua Projects")
            
            if st.button("🔄 Refresh", key="refresh_projects"):
                with st.spinner("Loading projects..."):
                    response = api_client.get_all_projects()
                    if response.get('success'):
                        st.session_state.projects = response.get('data', [])
            
            if st.session_state.projects:  # type: ignore
                for project in st.session_state.projects:  # type: ignore
                    project_name: str = project.get('name', 'Unnamed') if isinstance(project, dict) else 'Unnamed'  # type: ignore
                    project_id: Any = project.get('id') if isinstance(project, dict) else None  # type: ignore
                    with st.expander(f"📁 {project_name} (ID: {project_id})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Tipe:** {project.get('project_type', 'N/A')}")  # type: ignore
                            st.write(f"**Bahasa:** {project.get('programming_language', 'N/A')}")  # type: ignore
                            st.write(f"**Deskripsi:** {project.get('description', 'N/A')}")  # type: ignore
                        
                        with col2:
                            if st.button("✏️ Edit", key=f"edit_{project_id}"):
                                st.session_state.current_project = project
                            if st.button("🗑️ Hapus", key=f"delete_{project_id}"):
                                if project_id:
                                    response = api_client.delete_project(project_id)  # type: ignore
                                    if response.get('success'):
                                        display_success("✓ Project berhasil dihapus")
                                        time.sleep(1)
                                        st.rerun()
            else:
                display_info("Tidak ada projects.")
        
        # ======================== TAB 3: Kelola Project ========================
        with tab3:
            st.subheader("Kelola Project")
            
            if st.session_state.current_project:  # type: ignore
                project: Dict[str, Any] = st.session_state.current_project  # type: ignore
                project_name: str = project.get('name', 'Unnamed') if isinstance(project, dict) else 'Unnamed'  # type: ignore
                project_id: Any = project.get('id') if isinstance(project, dict) else None  # type: ignore
                
                st.write(f"**Project:** {project_name} (ID: {project_id})")
                
                # Figma Integration
                st.divider()
                st.subheader("🎨 Integrasi Figma")
                
                col1, col2 = st.columns(2)
                with col1:
                    figma_url = st.text_input("Figma URL")
                with col2:
                    figma_token = st.text_input("Figma Token", type="password")
                
                if st.button("📥 Fetch Design dari Figma"):
                    if not figma_url or not figma_token:
                        display_error("⚠️ Figma URL dan Token harus diisi!")
                    else:
                        with st.spinner("Fetching Figma design..."):
                            if project_id:
                                response = api_client.fetch_figma_design(
                                    project_id,  # type: ignore
                                    figma_url,
                                    figma_token
                                )
                                
                                if response.get('success'):
                                    display_success("✓ Design berhasil diambil dari Figma!")
                                else:
                                    display_error(f"❌ Error: {response.get('error')}")
                
                # Components
                st.divider()
                st.subheader("🧩 Generate Komponen")
                
                if st.button("🔨 Generate Komponen"):
                    with st.spinner("Generating components..."):
                        if project_id:
                            response = api_client.get_figma_components(project_id)  # type: ignore
                            
                            if response.get('success'):
                                st.json(response.get('data'))
                            else:
                                display_info("Belum ada design dari Figma. Fetch design terlebih dahulu.")
            else:
                display_info("Pilih project dari tab 'Daftar Projects' untuk mengelolanya.")
    else:
        display_error("❌ API tidak terhubung. Hubungkan API terlebih dahulu dari sidebar.")


elif page == "⚙️ Pengaturan":
    st.title("Pengaturan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Konfigurasi API")
        api_base_url = st.text_input("API Base URL", value="http://127.0.0.1:5000")
        
        if st.button("💾 Simpan Pengaturan"):
            display_success("✓ Pengaturan berhasil disimpan")
    
    with col2:
        st.subheader("💾 Database")
        
        if st.button("🔄 Backup Database"):
            with st.spinner("Backing up database..."):
                response = api_client.backup_database()
                if response.get('success'):
                    display_success(f"✓ Backup berhasil! Path: {response.get('backup_path')}")
                else:
                    display_error(f"❌ Error: {response.get('error')}")
    
    st.divider()
    st.subheader("ℹ️ Informasi Sistem")
    
    status_response = api_client.get_status()
    if status_response.get('success'):
        st.json(status_response)
