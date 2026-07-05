from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeWidget, 
    QTreeWidgetItem, QSplitter, QTextBrowser
)
from PySide6.QtCore import Qt

class DocsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Documentation Tree
        tree = QTreeWidget()
        tree.setHeaderLabel("Documentation")
        tree.setStyleSheet("""
            QTreeWidget {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 15px;
                color: white;
                font-size: 12pt;
            }
            QTreeWidget::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)

        # Add documentation sections
        sections = {
            "Getting Started": ["Installation", "Quick Start", "Basic Concepts"],
            "Features": ["AI Integration", "Code Generation", "Project Management"],
            "Tutorials": ["Creating New Project", "Using AI Assistant", "Cloud Sync"],
            "API Reference": ["Core API", "AI Models", "Cloud Services"],
            "Advanced Topics": ["Custom AI Models", "Performance Tuning"]
        }

        for section, topics in sections.items():
            parent = QTreeWidgetItem([section])
            for topic in topics:
                child = QTreeWidgetItem([topic])
                parent.addChild(child)
            tree.addTopLevelItem(parent)

        # Right side - Content Viewer
        content = QTextBrowser()
        content.setStyleSheet("""
            QTextBrowser {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 15px;
                color: white;
                font-size: 12pt;
                padding: 20px;
            }
        """)
        content.setOpenExternalLinks(True)

        splitter.addWidget(tree)
        splitter.addWidget(content)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        layout.addWidget(splitter)
