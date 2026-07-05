"""
Step 1 Page - Project Information
Halaman untuk input nama project, tipe, bahasa, dan fitur-fitur
"""

import streamlit as st
from api_client import api_client
from typing import Any, Dict, List


def render_step1_page():
    """Render halaman Step 1 - Informasi Project"""
    
    st.title("📋 Step 1: Informasi Project Dasar")
    
    # Initialize session state for step 1
    if 'step1_data' not in st.session_state:
        st.session_state.step1_data = {
            'project_name': '',
            'project_type': 'Web Application',
            'programming_language': 'Python',
            'description': '',
            'features': []
        }
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    # ==================== FRAME KIRI ====================
    with col1:
        st.subheader("📝 Informasi Project")
        
        # Project Name
        st.session_state.step1_data['project_name'] = st.text_input(
            "Nama Project",
            value=st.session_state.step1_data['project_name'],
            placeholder="Contoh: E-Commerce Platform...",
            key="project_name_input"
        )
        
        # Project Type
        st.session_state.step1_data['project_type'] = st.selectbox(
            "Tipe Project",
            [
                "Web Application",
                "Mobile App",
                "Desktop Software",
                "AI/ML Project",
                "Database System",
                "Hybrid Application"
            ],
            index=0 if st.session_state.step1_data['project_type'] == 'Web Application' else 3,
            key="project_type_select"
        )
        
        # Programming Language
        st.session_state.step1_data['programming_language'] = st.selectbox(
            "Bahasa Pemrograman",
            [
                "Python",
                "JavaScript / Node.js",
                "Java",
                "C#",
                "PHP",
                "Go",
                "Rust"
            ],
            index=0 if st.session_state.step1_data['programming_language'] == 'Python' else 1,
            key="lang_select"
        )
        
        # Project Description
        st.session_state.step1_data['description'] = st.text_area(
            "Deskripsi Project",
            value=st.session_state.step1_data['description'],
            placeholder="Jelaskan tujuan dan detail project Anda...",
            height=150,
            key="desc_textarea"
        )
    
    # ==================== FRAME KANAN ====================
    with col2:
        st.subheader("✨ Fitur-Fitur Project")
        st.caption("(Minimal 1, Maksimal 10)")
        
        # Feature input form
        feature_name = st.text_input(
            "Nama Fitur",
            placeholder="Nama fitur...",
            key="feature_name_input"
        )
        
        feature_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            key="feature_priority_select"
        )
        
        # Add feature button
        if st.button("➕ Tambah Fitur", key="add_feature_btn"):
            if feature_name.strip():
                if len(st.session_state.step1_data['features']) < 10:
                    new_feature = {
                        'name': feature_name.strip(),
                        'priority': feature_priority
                    }
                    st.session_state.step1_data['features'].append(new_feature)
                    st.success(f"✓ Fitur '{feature_name}' ditambahkan!")
                    st.rerun()
                else:
                    st.error("⚠️ Maksimal 10 fitur!")
            else:
                st.error("⚠️ Masukkan nama fitur terlebih dahulu!")
        
        # Display features list
        if st.session_state.step1_data['features']:
            st.markdown("**Daftar Fitur:**")
            for i, feature in enumerate(st.session_state.step1_data['features'], 1):
                col_feat_a, col_feat_b = st.columns([3, 1])
                with col_feat_a:
                    st.caption(f"{i}. {feature['name']} ({feature['priority']})")
                with col_feat_b:
                    if st.button("🗑️", key=f"delete_feature_{i}"):
                        st.session_state.step1_data['features'].pop(i-1)
                        st.rerun()
        
        # Features count
        features_count = len(st.session_state.step1_data['features'])
        st.divider()
        st.info(f"✓ Total Fitur: {features_count}/10")
    
    # ==================== ACTION BUTTONS ====================
    st.divider()
    
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1.5])
    
    with button_col1:
        if st.button("❌ Batal", use_container_width=True):
            st.session_state.current_step = None
            st.rerun()
    
    with button_col3:
        if st.button("✓ LANJUTKAN KE STEP 2 ➔", use_container_width=True, 
                    type="primary"):
            # Validate input
            if not st.session_state.step1_data['project_name'].strip():
                st.error("⚠️ Nama project tidak boleh kosong!")
            elif len(st.session_state.step1_data['features']) == 0:
                st.error("⚠️ Tambahkan setidaknya 1 fitur!")
            else:
                # Save project via API
                with st.spinner("Menyimpan project..."):
                    response = api_client.create_project(
                        name=st.session_state.step1_data['project_name'],
                        description=st.session_state.step1_data['description'],
                        project_type=st.session_state.step1_data['project_type'],
                        programming_language=st.session_state.step1_data['programming_language']
                    )
                    
                    if response.get('success'):
                        st.session_state.current_project_id = response.get('project_id')
                        st.session_state.current_step = 2
                        st.success(f"✓ Project '{st.session_state.step1_data['project_name']}' berhasil dibuat!")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.get('error', 'Unknown error')}")


if __name__ == "__main__":
    render_step1_page()
