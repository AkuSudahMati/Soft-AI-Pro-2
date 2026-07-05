"""
Step 2 Page - Figma Design Pages
Halaman untuk input design pages dari Figma (minimal 10 halaman)
"""

import streamlit as st
from api_client import api_client
from typing import Any, Dict, List


def render_step2_page():
    """Render halaman Step 2 - Figma Design"""
    
    st.title("🎨 Step 2: Upload Figma Design UI/UX")
    st.write("Masukkan minimal 10 halaman desain UI/UX dari Figma Anda")
    
    # Initialize session state for step 2
    if 'step2_data' not in st.session_state:
        st.session_state.step2_data = {
            'design_pages': []
        }
    
    # ==================== DESIGN PAGE INPUT ====================
    st.subheader("TAMBAH HALAMAN DESAIN")
    
    # Form untuk menambah page
    col1, col2 = st.columns(2)
    
    with col1:
        page_name = st.text_input(
            "Nama Halaman",
            placeholder="Contoh: Dashboard, Login, User Profile...",
            key="page_name_input"
        )
        page_url = st.text_input(
            "URL Figma",
            placeholder="https://www.figma.com/file/...",
            key="page_url_input"
        )
    
    with col2:
        page_desc = st.text_area(
            "Deskripsi Halaman",
            placeholder="Jelaskan fungsi dan fitur halaman ini...",
            height=106,
            key="page_desc_input"
        )
    
    # Button to add page
    if st.button("Tambah Halaman", key="add_page_btn", use_container_width=True):
        if page_name.strip():
            if len(st.session_state.step2_data['design_pages']) < 10:
                page_data = {
                    'page_name': page_name.strip(),
                    'page_url': page_url.strip(),
                    'description': page_desc.strip(),
                    'page_number': len(st.session_state.step2_data['design_pages']) + 1
                }
                st.session_state.step2_data['design_pages'].append(page_data)
                st.success(f"✓ Halaman '{page_name}' ditambahkan!")
                st.rerun()
            else:
                st.error("⚠️ Anda sudah mencapai maksimal 10 halaman!")
        else:
            st.error("⚠️ Masukkan nama halaman terlebih dahulu!")
    
    # ==================== PAGES LIST ====================
    st.subheader("DAFTAR HALAMAN DESAIN")
    
    pages = st.session_state.step2_data['design_pages']
    
    if pages:
        # Display as expandable items
        for i, page in enumerate(pages, 1):
            with st.expander(f"[{i}] {page['page_name']} {'🔗' if page['page_url'] else ''}"):
                col_info1, col_info2 = st.columns([3, 1])
                
                with col_info1:
                    st.caption(f"**URL:** {page['page_url'] if page['page_url'] else 'N/A'}")
                    st.caption(f"**Deskripsi:** {page['description']}")
                
                with col_info2:
                    if st.button("🗑️ Hapus", key=f"remove_page_{i}"):
                        st.session_state.step2_data['design_pages'].pop(i-1)
                        st.rerun()
    else:
        st.info("Belum ada halaman desain. Tambahkan halaman menggunakan form di atas.")
    
    # Pages count info
    pages_count = len(pages)
    progress = min(pages_count / 10, 1.0)
    st.progress(progress)
    st.info(f"✓ Total Halaman: {pages_count}/10")
    
    # ==================== ACTION BUTTONS ====================
    st.divider()
    
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1.5])
    
    with button_col1:
        if st.button("⬅️ Kembali ke Step 1", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    
    with button_col3:
        if st.button("✓ SIMPAN & LANJUT STEP 3 ➔", use_container_width=True, 
                    type="primary"):
            if pages_count < 10:
                st.error(f"⚠️ Masukkan minimal 10 halaman! (Saat ini: {pages_count}/10)")
            else:
                st.session_state.current_step = 3
                st.success("✓ Design pages berhasil disimpan!")
                import time
                time.sleep(1)
                st.rerun()


if __name__ == "__main__":
    render_step2_page()
