from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class ArchivePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Arsip Project")
        header.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 10px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Cari project...")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 14px;
            }
        """)
        layout.addWidget(search_box)
        
        # Projects list
        self.projects_list = QListWidget()
        self.projects_list.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                color: white;
                padding: 15px;
                margin: 5px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        
        # Add sample projects
        sample_projects = [
            "E-Commerce Website",
            "Mobile Banking App",
            "School Management System",
            "AI Chat Bot",
            "Inventory System"
        ]
        self.projects_list.addItems(sample_projects)
        layout.addWidget(self.projects_list)
