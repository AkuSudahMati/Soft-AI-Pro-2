from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QComboBox, QSpinBox,
    QCheckBox, QTabWidget, QScrollArea
)
from PySide6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Settings Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget {
                background: transparent;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 10px 20px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background: rgba(255, 255, 255, 0.2);
            }
        """)

        # Add settings sections
        tabs.addTab(self.create_general_tab(), "General")
        tabs.addTab(self.create_ai_tab(), "AI Settings")
        tabs.addTab(self.create_appearance_tab(), "Appearance")
        tabs.addTab(self.create_cloud_tab(), "Cloud Settings")

        layout.addWidget(tabs)

    def create_general_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Language Selection
        lang_group = self.create_setting_group("Language")
        lang_combo = QComboBox()
        lang_combo.addItems(["English", "Indonesian", "Japanese"])
        lang_group.layout().addWidget(lang_combo)
        
        # Auto-save Settings
        save_group = self.create_setting_group("Auto-save")
        save_check = QCheckBox("Enable auto-save")
        save_check.setStyleSheet("color: white;")
        save_interval = QSpinBox()
        save_interval.setSuffix(" minutes")
        save_interval.setValue(5)
        save_group.layout().addWidget(save_check)
        save_group.layout().addWidget(save_interval)

        layout.addWidget(lang_group)
        layout.addWidget(save_group)
        layout.addStretch()
        
        return widget

    def create_ai_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # AI Model Settings
        model_group = self.create_setting_group("AI Model")
        model_combo = QComboBox()
        model_combo.addItems(["GPT-4", "Claude 3", "Custom Model"])
        model_group.layout().addWidget(model_combo)
        
        # Code Generation Settings
        gen_group = self.create_setting_group("Code Generation")
        gen_check = QCheckBox("Enable type hints")
        gen_check.setStyleSheet("color: white;")
        gen_group.layout().addWidget(gen_check)

        layout.addWidget(model_group)
        layout.addWidget(gen_group)
        layout.addStretch()
        
        return widget

    def create_setting_group(self, title):
        group = QFrame()
        group.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
                margin: 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: white;
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        
        layout.addWidget(title_label)
        return group

    def create_appearance_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Theme Selection
        theme_group = self.create_setting_group("Theme")
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark", "Light", "System"])
        theme_group.layout().addWidget(theme_combo)
        
        # Animation Settings
        anim_group = self.create_setting_group("Animations")
        anim_check = QCheckBox("Show animations")
        anim_check.setStyleSheet("color: white;")
        anim_group.layout().addWidget(anim_check)

        layout.addWidget(theme_group)
        layout.addWidget(anim_group)
        layout.addStretch()
        
        return widget

    def create_cloud_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Cloud Sync Settings
        sync_group = self.create_setting_group("Cloud Sync")
        sync_check = QCheckBox("Enable cloud sync")
        sync_check.setStyleSheet("color: white;")
        sync_group.layout().addWidget(sync_check)
        
        # Cloud Provider Selection
        provider_group = self.create_setting_group("Cloud Provider")
        provider_combo = QComboBox()
        provider_combo.addItems(["Provider A", "Provider B", "Provider C"])
        provider_group.layout().addWidget(provider_combo)

        layout.addWidget(sync_group)
        layout.addWidget(provider_group)
        layout.addStretch()
        
        return widget