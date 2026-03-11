from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class ProjectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header with gradient background
        header = QLabel("Buat Project Baru")
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
        
        # Main content container
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content)
        
        # Form fields
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        
        # Project name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Masukkan nama project...")
        
        # Project type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Web Application",
            "Mobile App",
            "Desktop Software",
            "AI/ML Project",
            "Database System"
        ])
        
        # Description
        self.desc_text = QTextEdit()
        self.desc_text.setPlaceholderText("Deskripsi project...")
        self.desc_text.setMinimumHeight(100)
        
        # Style form elements
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
        
        # Add fields to form
        form_layout.addRow("Nama Project:", self.name_input)
        form_layout.addRow("Tipe Project:", self.type_combo)
        form_layout.addRow("Deskripsi:", self.desc_text)
        
        content_layout.addLayout(form_layout)
        
        # Create Project Button
        create_btn = QPushButton("Buat Project Baru")
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #388E3C);
            }
        """)
        
        content_layout.addWidget(create_btn, alignment=Qt.AlignCenter)
        layout.addWidget(content)