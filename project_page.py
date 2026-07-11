from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import os
import json
from api_client import api_client
from project_manager import ProjectManager
from streamlit_builder import StreamlitUIBuilder

class ProjectWizard(QWidget):
    def __init__(self):
        super().__init__()
        self.project_manager = ProjectManager()
        self.streamlit_builder = StreamlitUIBuilder()
        self.api_client = api_client
        self.current_step = 0
        self.project_data = {}
        self.dragged_components = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("Buat Project Baru - Wizard")
        header.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a237e, stop:1 #4CAF50);
                padding: 20px;
                border-radius: 15px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Progress indicator with step names
        self.progress_layout = QHBoxLayout()
        self.step_labels = []
        step_names = [
            "1. Informasi Dasar",
            "2. Figma Design",
            "3. Komponen UI",
            "4. API & Database"
        ]
        for i, step_name in enumerate(step_names):
            step_container = QVBoxLayout()
            step_label = QLabel(step_name)
            step_label.setStyleSheet("""
                QLabel {
                    color: white;
                    padding: 10px 15px;
                    border-radius: 10px;
                    background: rgba(255, 255, 255, 0.1);
                    font-weight: bold;
                    text-align: center;
                }
            """)
            step_label.setAlignment(Qt.AlignCenter)
            self.step_labels.append(step_label)
            self.progress_layout.addWidget(step_label)
            
            # Add separator line between steps (except last one)
            if i < len(step_names) - 1:
                separator = QLabel("→")
                separator.setStyleSheet("color: rgba(255, 255, 255, 0.3); font-size: 16px;")
                separator.setAlignment(Qt.AlignCenter)
                self.progress_layout.addWidget(separator)
        
        self.progress_layout.addStretch()
        layout.addLayout(self.progress_layout)

        # Stacked widget for steps
        self.stacked_widget = QStackedWidget()

        # Step 1: Project Name and Description
        self.step1_widget = self.create_step1()
        self.stacked_widget.addWidget(self.step1_widget)

        # Step 2: Upload Figma Design
        self.step2_widget = self.create_step2()
        self.stacked_widget.addWidget(self.step2_widget)

        # Step 3: Drag n Drop Streamlit Components
        self.step3_widget = self.create_step3()
        self.stacked_widget.addWidget(self.step3_widget)

        # Step 4: API Key and User Data
        self.step4_widget = self.create_step4()
        self.stacked_widget.addWidget(self.step4_widget)

        layout.addWidget(self.stacked_widget)

        # Navigation buttons
        nav_layout = QHBoxLayout()

        self.back_btn = QPushButton("Kembali")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 10px 20px;
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)
        nav_layout.addWidget(self.back_btn)

        nav_layout.addStretch()

        self.next_btn = QPushButton("Selanjutnya")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #388E3C);
            }
        """)
        self.next_btn.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_btn)

        layout.addLayout(nav_layout)

        self.update_progress()

    def create_step1(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        title = QLabel("Step 1: Informasi Dasar Project")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        # Project name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Masukkan nama project...")
        self.name_input.textChanged.connect(self.update_project_data)

        # Project type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Web Application",
            "Mobile App",
            "Desktop Software",
            "AI/ML Project",
            "Database System"
        ])
        self.type_combo.currentTextChanged.connect(self.update_project_data)

        # Programming language
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Python",
            "JavaScript",
            "TypeScript",
            "Java",
            "C#",
            "Go",
            "Rust"
        ])
        self.language_combo.currentTextChanged.connect(self.update_project_data)

        # Description
        self.desc_text = QTextEdit()
        self.desc_text.setPlaceholderText("Deskripsi project...")
        self.desc_text.setMinimumHeight(100)
        self.desc_text.textChanged.connect(self.update_project_data)

        # Style
        input_style = """
            QLineEdit, QComboBox, QTextEdit {
                padding: 12px;
                background: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 2px solid #4CAF50;
                background: rgba(255, 255, 255, 0.2);
            }
        """
        self.name_input.setStyleSheet(input_style)
        self.type_combo.setStyleSheet(input_style)
        self.desc_text.setStyleSheet(input_style)

        form_layout.addRow("Nama Project:", self.name_input)
        form_layout.addRow("Tipe Project:", self.type_combo)
        form_layout.addRow("Bahasa Pemrograman:", self.language_combo)
        form_layout.addRow("Deskripsi:", self.desc_text)

        layout.addLayout(form_layout)
        layout.addStretch()
        return widget

    def create_step2(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        title = QLabel("Step 2: Upload Figma Design UI/UX")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget {
                color: white;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
            }
        """)

        # Tab 1: Upload File
        upload_widget = QWidget()
        upload_layout = QVBoxLayout(upload_widget)

        self.figma_file_label = QLabel("Belum ada file yang dipilih")
        self.figma_file_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        upload_layout.addWidget(self.figma_file_label)

        browse_btn = QPushButton("Pilih File Figma (XD, Sketch, Figma)")
        browse_btn.clicked.connect(self.browse_figma_file)
        browse_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        upload_layout.addWidget(browse_btn)

        upload_info = QLabel("📁 Didukung: .fig, .xd, .sketch\n💾 Max size: 100MB")
        upload_info.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 12px;")
        upload_layout.addWidget(upload_info)

        upload_layout.addStretch()
        tabs.addTab(upload_widget, "Upload File")

        # Tab 2: Figma Link (via API)
        api_widget = QWidget()
        api_layout = QVBoxLayout(api_widget)

        url_label = QLabel("URL Figma:")
        url_label.setStyleSheet("color: white; font-size: 14px;")
        self.figma_url_input = QLineEdit()
        self.figma_url_input.setPlaceholderText("https://www.figma.com/file/...")
        self.figma_url_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 12px;
            }
        """)

        key_label = QLabel("Figma API Key:")
        key_label.setStyleSheet("color: white; font-size: 14px;")
        self.figma_api_key = QLineEdit()
        self.figma_api_key.setPlaceholderText("Masukkan Figma API key...")
        self.figma_api_key.setEchoMode(QLineEdit.Password)
        self.figma_api_key.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 12px;
            }
        """)

        fetch_btn = QPushButton("Ambil dari Figma")
        fetch_btn.clicked.connect(self.fetch_figma_design)
        fetch_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #0b7dda;
            }
        """)

        api_layout.addWidget(url_label)
        api_layout.addWidget(self.figma_url_input)
        api_layout.addWidget(key_label)
        api_layout.addWidget(self.figma_api_key)
        api_layout.addWidget(fetch_btn)
        api_layout.addStretch()
        tabs.addTab(api_widget, "Link Figma (API)")

        layout.addWidget(tabs)
        layout.addStretch()
        return widget

    def create_step3(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        title = QLabel("Step 3: Drag n Drop Streamlit Components")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Main container
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
            }
        """)
        main_layout = QHBoxLayout(main_frame)

        # Components panel (left)
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border-radius: 10px;
            }
        """)
        left_layout = QVBoxLayout(left_panel)

        comp_title = QLabel("🔧 Komponen Tersedia")
        comp_title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        left_layout.addWidget(comp_title)

        # Components list
        self.components_list = QListWidget()
        self.components_list.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                padding: 5px;
            }
            QListWidget::item:hover {
                background: rgba(76, 175, 80, 0.3);
            }
        """)

        for component in self.streamlit_builder.available_components:
            item = QListWidgetItem(f"{component['icon']} {component['name']}")
            item.setData(Qt.UserRole, component['id'])
            self.components_list.addItem(item)

        left_layout.addWidget(self.components_list)
        main_layout.addWidget(left_panel, 1)

        # Canvas area (right)
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                border: 2px dashed rgba(76, 175, 80, 0.3);
            }
        """)
        right_layout = QVBoxLayout(right_panel)

        canvas_title = QLabel("🎨 Canvas - Drag komponen ke sini")
        canvas_title.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px; text-align: center;")
        right_layout.addWidget(canvas_title)

        # Canvas area
        self.canvas_area = QListWidget()
        self.canvas_area.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                padding: 10px;
                min-height: 300px;
            }
            QListWidget::item {
                background: rgba(76, 175, 80, 0.2);
                padding: 8px;
                border-radius: 5px;
                margin: 5px 0px;
            }
        """)
        self.canvas_area.setSelectionMode(QListWidget.SingleSelection)
        right_layout.addWidget(self.canvas_area)

        # Canvas buttons
        canvas_btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Tambah Komponen")
        add_btn.clicked.connect(self.add_component_to_canvas)
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
        """)

        remove_btn = QPushButton("❌ Hapus Komponen")
        remove_btn.clicked.connect(self.remove_component_from_canvas)
        remove_btn.setStyleSheet("""
            QPushButton {
                background: #f44336;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
        """)

        canvas_btn_layout.addWidget(add_btn)
        canvas_btn_layout.addWidget(remove_btn)
        canvas_btn_layout.addStretch()
        right_layout.addLayout(canvas_btn_layout)

        main_layout.addWidget(right_panel, 1)

        layout.addWidget(main_frame)
        layout.addStretch()
        return widget

    def create_step4(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        title = QLabel("Step 4: Input Data User & API Key")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Scroll area
        scroll = QScrollArea()
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(20)

        # API Keys Section
        api_title = QLabel("🔐 API Keys")
        api_title.setStyleSheet("color: #4CAF50; font-size: 16px; font-weight: bold;")
        form_layout.addRow(api_title)

        self.openai_key = QLineEdit()
        self.openai_key.setPlaceholderText("sk-...")
        self.openai_key.setEchoMode(QLineEdit.Password)

        self.claude_key = QLineEdit()
        self.claude_key.setPlaceholderText("sk-ant-...")
        self.claude_key.setEchoMode(QLineEdit.Password)

        self.google_key = QLineEdit()
        self.google_key.setPlaceholderText("Google API Key...")
        self.google_key.setEchoMode(QLineEdit.Password)

        self.github_token = QLineEdit()
        self.github_token.setPlaceholderText("ghp_...")
        self.github_token.setEchoMode(QLineEdit.Password)

        # Database Section
        db_title = QLabel("🗄️ Database Configuration")
        db_title.setStyleSheet("color: #4CAF50; font-size: 16px; font-weight: bold;")

        self.db_host = QLineEdit()
        self.db_host.setPlaceholderText("localhost")

        self.db_port = QLineEdit()
        self.db_port.setPlaceholderText("5432")

        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText("database_name")

        self.db_user = QLineEdit()
        self.db_user.setPlaceholderText("username")

        self.db_password = QLineEdit()
        self.db_password.setPlaceholderText("password")
        self.db_password.setEchoMode(QLineEdit.Password)

        # Cloud Services Section
        cloud_title = QLabel("☁️ Cloud Services")
        cloud_title.setStyleSheet("color: #4CAF50; font-size: 16px; font-weight: bold;")

        self.aws_access_key = QLineEdit()
        self.aws_access_key.setPlaceholderText("AWS Access Key")
        self.aws_access_key.setEchoMode(QLineEdit.Password)

        self.aws_secret_key = QLineEdit()
        self.aws_secret_key.setPlaceholderText("AWS Secret Key")
        self.aws_secret_key.setEchoMode(QLineEdit.Password)

        # Style input fields
        input_style = """
            QLineEdit {
                padding: 10px;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background: rgba(255, 255, 255, 0.15);
            }
        """

        # Add fields to form
        form_layout.addRow(api_title)
        form_layout.addRow("OpenAI API Key:", self.openai_key)
        form_layout.addRow("Claude API Key:", self.claude_key)
        form_layout.addRow("Google API Key:", self.google_key)
        form_layout.addRow("GitHub Token:", self.github_token)

        form_layout.addRow(db_title)
        form_layout.addRow("DB Host:", self.db_host)
        form_layout.addRow("DB Port:", self.db_port)
        form_layout.addRow("Database Name:", self.db_name)
        form_layout.addRow("DB User:", self.db_user)
        form_layout.addRow("DB Password:", self.db_password)

        form_layout.addRow(cloud_title)
        form_layout.addRow("AWS Access Key:", self.aws_access_key)
        form_layout.addRow("AWS Secret Key:", self.aws_secret_key)

        # Apply styles
        for i in range(form_layout.rowCount()):
            widget_item = form_layout.itemAt(i, QFormLayout.FieldRole)
            if widget_item and isinstance(widget_item.widget(), QLineEdit):
                widget_item.widget().setStyleSheet(input_style)

        scroll.setWidget(form_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        # Info
        info = QLabel("ℹ️ Semua data sensitif akan dienkripsi dan disimpan secara aman")
        info.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 12px;")
        layout.addWidget(info)

        return widget

    def update_project_data(self):
        if hasattr(self, 'name_input'):
            self.project_data['name'] = self.name_input.text()
        if hasattr(self, 'type_combo'):
            self.project_data['project_type'] = self.type_combo.currentText()
        if hasattr(self, 'language_combo'):
            self.project_data['programming_language'] = self.language_combo.currentText()
        if hasattr(self, 'desc_text'):
            self.project_data['description'] = self.desc_text.toPlainText()

    def browse_figma_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File Figma Design",
            "",
            "Design Files (*.fig *.xd *.sketch *.pdf);;All Files (*)"
        )
        
        if file_path:
            # Local preview path from Figma files stays local, backend uses Figma API URL path
            self.figma_file_label.setText(f"📁 File siap diproses: {os.path.basename(file_path)}")
            self.project_data['figma_local_file'] = file_path
            QMessageBox.information(self, "Berhasil", "File desain siap digunakan secara lokal.")

    def fetch_figma_design(self):
        url = self.figma_url_input.text().strip()
        api_key = self.figma_api_key.text().strip()

        if not url or not api_key:
            QMessageBox.warning(self, "Error", "URL dan API Key harus diisi!")
            return

        if 'id' not in self.project_data:
            QMessageBox.warning(self, "Error", "Project belum disimpan! Silakan buat project di Step 1 terlebih dahulu.")
            return

        try:
            response = self.api_client.fetch_figma_design(
                self.project_data['id'],
                url,
                api_key
            )
            if response.get('success'):
                self.figma_file_label.setText("✅ Design berhasil diambil dari Figma")
                self.project_data['figma_data'] = response.get('data')
                QMessageBox.information(self, "Berhasil", "Design Figma berhasil disimpan di backend!")
            else:
                QMessageBox.warning(self, "Error", response.get('error', 'Gagal mengambil design dari Figma'))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil design: {str(e)}")

    def add_component_to_canvas(self):
        current_item = self.components_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Pilih komponen terlebih dahulu!")
            return

        component_id = current_item.data(Qt.UserRole)
        component_name = current_item.text()

        # Add to canvas
        canvas_item = QListWidgetItem(component_name)
        canvas_item.setData(Qt.UserRole, component_id)
        self.canvas_area.addItem(canvas_item)
        
        self.dragged_components.append(component_id)

    def remove_component_from_canvas(self):
        current_row = self.canvas_area.currentRow()
        if current_row >= 0:
            item = self.canvas_area.takeItem(current_row)
            component_id = item.data(Qt.UserRole)
            if component_id in self.dragged_components:
                self.dragged_components.remove(component_id)

    def update_progress(self):
        """Update progress indicator styling untuk semua 4 steps"""
        for i, label in enumerate(self.step_labels):
            if i < self.current_step:
                # Completed steps - green
                label.setStyleSheet("""
                    QLabel {
                        color: white;
                        padding: 10px 15px;
                        border-radius: 10px;
                        background: #4CAF50;
                        font-weight: bold;
                    }
                """)
            elif i == self.current_step:
                # Current step - orange
                label.setStyleSheet("""
                    QLabel {
                        color: white;
                        padding: 10px 15px;
                        border-radius: 10px;
                        background: #FF9800;
                        font-weight: bold;
                        border: 2px solid #FFC107;
                    }
                """)
            else:
                # Future steps - gray
                label.setStyleSheet("""
                    QLabel {
                        color: white;
                        padding: 10px 15px;
                        border-radius: 10px;
                        background: rgba(255, 255, 255, 0.1);
                        font-weight: bold;
                    }
                """)

    def go_next(self):
        """Navigate to next step (total 4 steps: 0-3)"""
        if self.current_step < 3:  # Max step is 3 (0-indexed)
            if self.validate_current_step():
                # Save project on first step if not already saved
                if self.current_step == 0 and 'id' not in self.project_data:
                    try:
                        response = self.api_client.create_project(
                            name=self.project_data.get('name', ''),
                            description=self.project_data.get('description', ''),
                            project_type=self.project_data.get('project_type', ''),
                            programming_language=self.project_data.get('programming_language', 'Python')
                        )
                        if response.get('success'):
                            self.project_data['id'] = response.get('project_id')
                        else:
                            QMessageBox.critical(self, "Error", f"Gagal membuat project: {response.get('error', 'Unknown error')}")
                            return
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Gagal menyimpan project: {str(e)}")
                        return
                
                self.current_step += 1
                self.stacked_widget.setCurrentIndex(self.current_step)
                self.update_progress()
                self.update_navigation_buttons()

                if self.current_step == 2:  # Step 3 - Streamlit components
                    self.project_data['streamlit_components'] = self.dragged_components
        else:
            # Finish wizard at step 3 (the 4th step)
            self.finish_wizard()

    def go_back(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.update_progress()
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """Update navigation buttons based on current step"""
        # Back button enabled if not on first step
        self.back_btn.setEnabled(self.current_step > 0)
        
        # Update next button text and state
        if self.current_step == 3:  # Last step (Step 4)
            self.next_btn.setText("✅ Selesai & Buat Project")
            self.next_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4CAF50, stop:1 #45a049);
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #45a049, stop:1 #388E3C);
                }
            """)
        else:
            self.next_btn.setText("Selanjutnya ➜")
            self.next_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4CAF50, stop:1 #45a049);
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #45a049, stop:1 #388E3C);
                }
            """)

    def validate_current_step(self):
        """Validate data for each step before proceeding"""
        if self.current_step == 0:  # Step 1: Basic Info
            if not self.project_data.get('name', '').strip():
                QMessageBox.warning(self, "Error", "Nama project harus diisi!")
                return False
            if not self.project_data.get('description', '').strip():
                QMessageBox.warning(self, "Error", "Deskripsi project harus diisi!")
                return False
            return True
            
        elif self.current_step == 1:  # Step 2: Figma Design
            if 'figma_design' not in self.project_data and 'figma_data' not in self.project_data:
                reply = QMessageBox.question(
                    self, 
                    "Warning", 
                    "Belum ada design Figma yang diupload.\n\nLanjutkan ke step berikutnya?",
                    QMessageBox.Yes | QMessageBox.No
                )
                return reply == QMessageBox.Yes
            return True
            
        elif self.current_step == 2:  # Step 3: Components
            if not self.dragged_components:
                reply = QMessageBox.question(
                    self,
                    "Warning",
                    "Belum ada komponen yang ditambahkan ke canvas.\n\nLanjutkan ke step berikutnya?",
                    QMessageBox.Yes | QMessageBox.No
                )
                return reply == QMessageBox.Yes
            return True
            
        elif self.current_step == 3:  # Step 4: API & Database
            # Optional validation - user can skip
            return True
            
        return True

    def save_user_data(self):
        """Save user data including API keys and credentials using ProjectManager"""
        credentials = {
            'api_keys': {
                'openai': self.openai_key.text(),
                'google': self.google_key.text(),
                'github': self.github_token.text()
            },
            'database': {
                'host': self.db_host.text(),
                'port': self.db_port.text(),
                'name': self.db_name.text(),
                'user': self.db_user.text(),
                'password': self.db_password.text()
            },
            'cloud_services': {
                'aws_access_key': self.aws_access_key.text(),
                'aws_secret_key': self.aws_secret_key.text()
            }
        }

        # Save using backend API
        try:
            if 'id' in self.project_data:
                response = self.api_client.save_project_credentials(
                    self.project_data['id'],
                    api_keys={
                        'openai': self.openai_key.text(),
                        'claude': self.claude_key.text(),
                        'google': self.google_key.text(),
                        'github': self.github_token.text()
                    },
                    database={
                        'host': self.db_host.text(),
                        'port': self.db_port.text(),
                        'name': self.db_name.text(),
                        'user': self.db_user.text(),
                        'password': self.db_password.text()
                    },
                    cloud_services={
                        'aws_access_key': self.aws_access_key.text(),
                        'aws_secret_key': self.aws_secret_key.text()
                    }
                )
                if response.get('success'):
                    self.project_data['credentials'] = {
                        'api_keys': {
                            'openai': self.openai_key.text(),
                            'claude': self.claude_key.text(),
                            'google': self.google_key.text(),
                            'github': self.github_token.text()
                        },
                        'database': {
                            'host': self.db_host.text(),
                            'port': self.db_port.text(),
                            'name': self.db_name.text(),
                            'user': self.db_user.text(),
                            'password': self.db_password.text()
                        },
                        'cloud_services': {
                            'aws_access_key': self.aws_access_key.text(),
                            'aws_secret_key': self.aws_secret_key.text()
                        }
                    }
                    QMessageBox.information(self, "Berhasil", "Kredensial berhasil disimpan di backend!")
                    return True
                else:
                    QMessageBox.warning(self, "Error", response.get('error', 'Gagal menyimpan kredensial!'))
                    return False
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Error: {str(e)}")
            return False

        return False

    def finish_wizard(self):
        """Generate Streamlit app and finalize project using ProjectManager"""
        try:
            if 'id' not in self.project_data:
                QMessageBox.warning(self, "Error", "Project tidak valid!")
                return

            # Ensure user credentials are stored before finalizing
            if not self.save_user_data():
                return

            # Persist component list to backend as project features
            if self.dragged_components and not self.project_data.get('backend_features_saved'):
                backend_features = [
                    self.canvas_area.item(i).text()
                    for i in range(self.canvas_area.count())
                ]
                for feature_name in backend_features:
                    try:
                        self.api_client.create_project_feature(
                            self.project_data['id'],
                            feature_name,
                            description="Generated from wizard UI",
                            priority="medium"
                        )
                    except Exception:
                        continue
                self.project_data['backend_features_saved'] = True

            # Build Streamlit app using ProjectManager
            app_path = self.project_manager.build_streamlit_app(
                self.dragged_components,
                self.project_data['id']
            )

            if app_path:
                # Try backend analysis for project components if available
                if self.dragged_components:
                    features = [
                        {'name': self.canvas_area.item(i).text(), 'priority': 'medium'}
                        for i in range(self.canvas_area.count())
                    ]
                    try:
                        analysis_response = self.api_client.analyze_project(
                            self.project_data['id'],
                            features
                        )
                        if analysis_response.get('success'):
                            analysis_file = analysis_response['data'].get('file_path', 'N/A')
                            QMessageBox.information(
                                self,
                                "AI Analysis",
                                f"Analisis AI berhasil dibuat di backend.\nPath: {analysis_file}"
                            )
                    except Exception:
                        pass

                # Generate deployment guide
                guide = self.project_manager.generate_deployment_guide(self.project_data['id'])
                
                QMessageBox.information(
                    self,
                    "✅ Berhasil",
                    f"Project berhasil dibuat!\n\n"
                    f"📱 Streamlit App: {app_path}\n\n"
                    f"Untuk menjalankan:\nstreamlit run {app_path}"
                )
                
                # Reset wizard
                self.reset_wizard()
            else:
                QMessageBox.warning(self, "Error", "Gagal membuat Streamlit app!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyelesaikan project: {str(e)}")

    def reset_wizard(self):
        """Reset wizard to initial state"""
        self.current_step = 0
        self.stacked_widget.setCurrentIndex(0)
        self.update_progress()
        self.update_navigation_buttons()
        self.project_data = {}
        self.dragged_components = []
        
        # Clear inputs
        if hasattr(self, 'name_input'):
            self.name_input.clear()
        if hasattr(self, 'desc_text'):
            self.desc_text.clear()
        if hasattr(self, 'type_combo'):
            self.type_combo.setCurrentIndex(0)
        if hasattr(self, 'figma_file_label'):
            self.figma_file_label.setText("Belum ada file yang dipilih")
        if hasattr(self, 'canvas_area'):
            self.canvas_area.clear()

# Keep the old class name for compatibility
class ProjectPage(ProjectWizard):
    pass