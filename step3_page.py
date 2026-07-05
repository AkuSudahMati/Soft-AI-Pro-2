"""
Step 3 Page - UI Components
Halaman untuk menambah komponen UI (Button, Input, Chart, dll)
"""

import streamlit as st
from api_client import api_client
from typing import Any, Dict, List


def render_step3_page():
    """Render halaman Step 3 - Komponen UI"""
    
    st.title("🔧 Step 3: Tambah Komponen UI")
    
    # Initialize session state for step 3
    if 'step3_data' not in st.session_state:
        st.session_state.step3_data = {
            'components': []
        }
    
    # ==================== COMPONENT INPUT ====================
    st.subheader("Tambah Komponen Baru")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        component_name = st.text_input(
            "Nama Komponen",
            placeholder="Contoh: Button, Input Field, Chart, Card, Navigation...",
            key="component_name_input"
        )
    
    with col2:
        st.write("")  # Spacing
        if st.button("➕ Tambah", key="add_component_btn", use_container_width=True):
            if component_name.strip():
                new_component = {
                    'name': component_name.strip(),
                    'id': len(st.session_state.step3_data['components']) + 1
                }
                st.session_state.step3_data['components'].append(new_component)
                st.success(f"✓ Komponen '{component_name}' ditambahkan!")
                st.rerun()
            else:
                st.error("⚠️ Masukkan nama komponen terlebih dahulu!")
    
    # ==================== COMPONENTS LIST ====================
    st.subheader("📋 Daftar Komponen UI")
    
    components = st.session_state.step3_data['components']
    
    if components:
        # Display as columns (grid layout)
        cols = st.columns(3)
        
        for i, component in enumerate(components):
            with cols[i % 3]:
                with st.container(border=True):
                    st.write(f"🔧 **{component['name']}**")
                    if st.button("🗑️ Hapus", key=f"remove_component_{i}"):
                        st.session_state.step3_data['components'].pop(i)
                        st.rerun()
        
        st.divider()
        st.info(f"✓ Total Komponen: {len(components)}")
    else:
        st.info("Belum ada komponen. Tambahkan komponen menggunakan form di atas.")
    
    # ==================== COMPONENT SUGGESTIONS ====================
    with st.expander("💡 Saran Komponen Umum"):
        st.write("""
        Berikut adalah komponen UI yang umum digunakan:
        - **Input Fields**: Text Input, Password Input, Email Input, Search Bar
        - **Buttons**: Primary Button, Secondary Button, Icon Button, Floating Action Button
        - **Cards**: User Card, Product Card, Article Card, Statistics Card
        - **Navigation**: Top Navigation, Side Navigation, Breadcrumb, Tabs
        - **Data Display**: Table, List, Grid, Chart/Graph
        - **Modal & Dialog**: Modal Dialog, Alert Dialog, Toast Notification
        - **Form**: Form Input, Checkbox, Radio Button, Select Dropdown
        - **Others**: Loading Spinner, Avatar, Badge, Progress Bar
        """)
    
    # ==================== ACTION BUTTONS ====================
    st.divider()
    
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1.5])
    
    with button_col1:
        if st.button("⬅️ Kembali ke Step 2", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
    
    with button_col3:
        if st.button("✓ SIMPAN & LANJUT STEP 4 ➔", use_container_width=True, 
                    type="primary"):
            if len(components) == 0:
                st.error("⚠️ Tambahkan setidaknya 1 komponen!")
            else:
                st.session_state.current_step = 4
                st.success(f"✓ {len(components)} komponen berhasil disimpan!")
                import time
                time.sleep(1)
                st.rerun()


if __name__ == "__main__":
    render_step3_page()
