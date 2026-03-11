from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class CloudPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title Section
        title = QLabel("Cloud Integration")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32pt;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)

        # Cloud Services Grid
        services_grid = QGridLayout()
        services = [
            {
                "name": "GitHub Integration",
                "desc": "Sync your projects with GitHub repositories",
                "icon": "github.png"
            },
            {
                "name": "Google Drive",
                "desc": "Backup your projects to Google Drive",
                "icon": "gdrive.png"
            },
            {
                "name": "Dropbox",
                "desc": "Share and collaborate via Dropbox",
                "icon": "dropbox.png"
            },
            {
                "name": "OneDrive",
                "desc": "Microsoft OneDrive integration",
                "icon": "onedrive.png"
            }
        ]

        for i, service in enumerate(services):
            card = self.create_service_card(service)
            services_grid.addWidget(card, i//2, i%2)

        layout.addLayout(services_grid)
        layout.addStretch()

    def create_service_card(self, service):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)

        card_layout = QVBoxLayout(card)
        
        name = QLabel(service["name"])
        name.setStyleSheet("color: white; font-size: 18pt; font-weight: bold;")
        
        desc = QLabel(service["desc"])
        desc.setStyleSheet("color: #e0e0e0; font-size: 12pt;")
        desc.setWordWrap(True)
        
        card_layout.addWidget(name)
        card_layout.addWidget(desc)
        
        return card