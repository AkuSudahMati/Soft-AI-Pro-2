"""
⚙️ MODERN SETTINGS PAGE - Enhanced UI/UX
========================================

Settings with beautiful UI/UX design
Includes Gemini API integration
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QComboBox, QSpinBox,
    QCheckBox, QTabWidget, QScrollArea, QLineEdit,
    QMessageBox, QProgressBar, QFileDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont, QColor
from typing import Optional
from gemini_integration import get_gemini_manager
import logging

logger = logging.getLogger(__name__)


class ModernSettingGroup(QFrame):
    """Modern reusable settings group with gradient background"""
    def __init__(self, title: str, description: str = ""):
        super().__init__()
        self.title = title
        self.description = description
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                           stop:0 rgba(124,58,237,0.08),
                           stop:1 rgba(6,182,212,0.08));
                border: 1px solid rgba(124,58,237,0.3);
                border-radius: 12px;
                padding: 20px;
                margin: 8px 0px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #F0F4F8;")
        layout.addWidget(title_label)
        
        # Description
        if self.description:
            desc_label = QLabel(self.description)
            desc_font = QFont()
            desc_font.setPointSize(9)
            desc_label.setFont(desc_font)
            desc_label.setStyleSheet("color: #94A3B8; font-style: italic;")
            layout.addWidget(desc_label)
        
        # Content layout (will be filled by subclasses)
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(12)
        layout.addLayout(self.content_layout)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.gemini_manager = get_gemini_manager()
        self.init_ui()

    def init_ui(self):
        """Initialize modern settings UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Page Title
        title = QLabel("⚙️ Settings & Configuration")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #F0F4F8;")
        layout.addWidget(title)

        # Settings Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(self.get_tab_stylesheet())

        # Create tabs
        tabs.addTab(self.create_gemini_tab(), "🤖 Gemini AI")
        tabs.addTab(self.create_general_tab(), "⚙️ General")
        tabs.addTab(self.create_appearance_tab(), "🎨 Appearance")
        tabs.addTab(self.create_performance_tab(), "⚡ Performance")
        tabs.addTab(self.create_advanced_tab(), "🔧 Advanced")

        layout.addWidget(tabs)

        # Footer
        footer = QLabel("💡 Tips: All settings are saved automatically")
        footer.setStyleSheet("color: #94A3B8; font-style: italic; padding-top: 10px;")
        layout.addWidget(footer)

    def create_gemini_tab(self) -> QWidget:
        """Gemini API Configuration Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # ===== GEMINI STATUS =====
        status_group = ModernSettingGroup(
            "🤖 Gemini API Status",
            "Check and manage your Gemini API connection"
        )
        
        # Status indicator
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: rgba(16,185,129,0.15);
                border: 1px solid rgba(16,185,129,0.3);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        
        status_text = QLabel("Status: ")
        if self.gemini_manager.is_configured:
            status_text.setText("✅ Connected - Gemini API is ready to use")
            status_text.setStyleSheet("color: #10B981; font-weight: bold;")
        else:
            status_text.setText("❌ Not Connected - Please configure API key below")
            status_text.setStyleSheet("color: #EF4444; font-weight: bold;")
        
        status_layout.addWidget(status_text)
        status_group.content_layout.addWidget(status_frame)
        
        # Test connection button
        test_btn = QPushButton("🧪 Test Connection")
        test_btn.setMinimumHeight(40)
        test_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #3B82F6,
                           stop:1 #1E40AF);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #60A5FA,
                           stop:1 #3B82F6);
            }
        """)
        test_btn.clicked.connect(self.test_gemini_connection)
        status_group.content_layout.addWidget(test_btn)
        
        layout.addWidget(status_group)

        # ===== API KEY CONFIGURATION =====
        api_config_group = ModernSettingGroup(
            "🔑 API Key Configuration",
            "Enter your Google Gemini API key"
        )
        
        # API Key input
        api_key_label = QLabel("API Key:")
        api_key_label.setStyleSheet("color: #CBD5E1; font-weight: bold;")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("paste your Gemini API key here...")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setMinimumHeight(45)
        self.api_key_input.setStyleSheet("""
            QLineEdit {
                background: rgba(15,23,42,0.8);
                color: #F0F4F8;
                border: 2px solid rgba(124,58,237,0.3);
                border-radius: 8px;
                padding: 12px;
                font-size: 11pt;
                selection-background-color: #7C3AED;
            }
            QLineEdit:focus {
                border: 2px solid #7C3AED;
                background: rgba(15,23,42,1);
            }
        """)
        
        api_config_group.content_layout.addWidget(api_key_label)
        api_config_group.content_layout.addWidget(self.api_key_input)
        
        # Show/Hide toggle
        show_toggle = QCheckBox("👁️ Show API Key")
        show_toggle.setStyleSheet("color: #CBD5E1;")
        show_toggle.toggled.connect(
            lambda checked: self.api_key_input.setEchoMode(
                QLineEdit.Normal if checked else QLineEdit.Password
            )
        )
        api_config_group.content_layout.addWidget(show_toggle)
        
        # Save API Key button
        save_api_btn = QPushButton("💾 Save API Key")
        save_api_btn.setMinimumHeight(40)
        save_api_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #7C3AED,
                           stop:1 #5B21B6);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #A78BFA,
                           stop:1 #7C3AED);
            }
        """)
        save_api_btn.clicked.connect(self.save_gemini_api_key)
        api_config_group.content_layout.addWidget(save_api_btn)
        
        # Remove API Key button
        remove_api_btn = QPushButton("🗑️ Remove API Key")
        remove_api_btn.setMinimumHeight(40)
        remove_api_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #EF4444,
                           stop:1 #991B1B);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #F87171,
                           stop:1 #EF4444);
            }
        """)
        remove_api_btn.clicked.connect(self.remove_gemini_api_key)
        api_config_group.content_layout.addWidget(remove_api_btn)
        
        layout.addWidget(api_config_group)

        # ===== QUICK LINKS =====
        links_group = ModernSettingGroup(
            "📚 Resources",
            "Get help and documentation"
        )
        
        get_key_btn = QPushButton("📖 Get API Key (Google AI Studio)")
        get_key_btn.setMinimumHeight(40)
        get_key_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #F59E0B,
                           stop:1 #B45309);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                           stop:0 #FBBF24,
                           stop:1 #F59E0B);
            }
        """)
        get_key_btn.clicked.connect(lambda: self.open_link("https://aistudio.google.com/app/apikey"))
        links_group.content_layout.addWidget(get_key_btn)
        
        layout.addWidget(links_group)

        layout.addStretch()
        return widget

    def create_general_tab(self) -> QWidget:
        """General Settings Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Language
        lang_group = ModernSettingGroup("🌐 Language", "Select your preferred language")
        lang_combo = QComboBox()
        lang_combo.addItems(["English", "Indonesian (Bahasa)", "Japanese (日本語)", "Spanish (Español)"])
        lang_combo.setMinimumHeight(40)
        lang_group.content_layout.addWidget(QLabel("Language:"))
        lang_group.content_layout.addWidget(lang_combo)
        layout.addWidget(lang_group)

        # Auto-save
        save_group = ModernSettingGroup("💾 Auto-save Settings", "Configure automatic saving")
        save_check = QCheckBox("Enable auto-save")
        save_check.setChecked(True)
        save_check.setStyleSheet("color: #F0F4F8; font-weight: bold;")
        save_group.content_layout.addWidget(save_check)
        
        interval_label = QLabel("Save interval (minutes):")
        interval_label.setStyleSheet("color: #CBD5E1;")
        save_interval = QSpinBox()
        save_interval.setMinimumHeight(40)
        save_interval.setSuffix(" minutes")
        save_interval.setValue(5)
        save_interval.setMinimum(1)
        save_interval.setMaximum(60)
        save_group.content_layout.addWidget(interval_label)
        save_group.content_layout.addWidget(save_interval)
        layout.addWidget(save_group)

        layout.addStretch()
        return widget

    def create_appearance_tab(self) -> QWidget:
        """Appearance/Theme Settings Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Theme
        theme_group = ModernSettingGroup("🎨 Theme", "Customize your UI theme")
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #CBD5E1; font-weight: bold;")
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark (Default)", "Light", "System"])
        theme_combo.setMinimumHeight(40)
        theme_group.content_layout.addWidget(theme_label)
        theme_group.content_layout.addWidget(theme_combo)
        layout.addWidget(theme_group)

        # Animations
        anim_group = ModernSettingGroup("✨ Effects", "Enable visual enhancements")
        anim_check = QCheckBox("Enable smooth animations")
        anim_check.setChecked(True)
        anim_check.setStyleSheet("color: #F0F4F8; font-weight: bold;")
        anim_group.content_layout.addWidget(anim_check)
        
        shadow_check = QCheckBox("Enable shadow effects")
        shadow_check.setChecked(True)
        shadow_check.setStyleSheet("color: #F0F4F8; font-weight: bold;")
        anim_group.content_layout.addWidget(shadow_check)
        layout.addWidget(anim_group)

        layout.addStretch()
        return widget

    def create_performance_tab(self) -> QWidget:
        """Performance Settings Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Cache
        cache_group = ModernSettingGroup("⚡ Caching", "Improve performance with caching")
        cache_check = QCheckBox("Enable cache")
        cache_check.setChecked(True)
        cache_check.setStyleSheet("color: #F0F4F8; font-weight: bold;")
        cache_group.content_layout.addWidget(cache_check)
        
        cache_size_label = QLabel("Cache size (MB):")
        cache_size_label.setStyleSheet("color: #CBD5E1;")
        cache_size = QSpinBox()
        cache_size.setMinimumHeight(40)
        cache_size.setSuffix(" MB")
        cache_size.setValue(256)
        cache_size.setMinimum(50)
        cache_size.setMaximum(2048)
        cache_group.content_layout.addWidget(cache_size_label)
        cache_group.content_layout.addWidget(cache_size)
        layout.addWidget(cache_group)

        # Optimization
        optim_group = ModernSettingGroup("🚀 Optimization", "Optimize resource usage")
        thread_label = QLabel("Worker threads:")
        thread_label.setStyleSheet("color: #CBD5E1;")
        thread_spin = QSpinBox()
        thread_spin.setMinimumHeight(40)
        thread_spin.setValue(4)
        thread_spin.setMinimum(1)
        thread_spin.setMaximum(16)
        optim_group.content_layout.addWidget(thread_label)
        optim_group.content_layout.addWidget(thread_spin)
        layout.addWidget(optim_group)

        layout.addStretch()
        return widget

    def create_advanced_tab(self) -> QWidget:
        """Advanced Settings Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Logging
        log_group = ModernSettingGroup("📝 Logging", "Configure debug logging")
        log_check = QCheckBox("Enable debug logging")
        log_check.setStyleSheet("color: #F0F4F8; font-weight: bold;")
        log_group.content_layout.addWidget(log_check)
        
        log_level_label = QLabel("Log level:")
        log_level_label.setStyleSheet("color: #CBD5E1;")
        log_level_combo = QComboBox()
        log_level_combo.addItems(["INFO", "DEBUG", "WARNING", "ERROR"])
        log_level_combo.setMinimumHeight(40)
        log_group.content_layout.addWidget(log_level_label)
        log_group.content_layout.addWidget(log_level_combo)
        layout.addWidget(log_group)

        # About
        about_group = ModernSettingGroup("ℹ️  About", "Soft AI Pro Information")
        about_label = QLabel("Version: 2.0.0 (Modern UI)\nBuild: 2026.05.17\n\n✨ Modern UI/UX Redesign\n🤖 Gemini API Integration\n🎨 Enhanced Visual Design")
        about_label.setStyleSheet("color: #CBD5E1; line-height: 1.8;")
        about_group.content_layout.addWidget(about_label)
        layout.addWidget(about_group)

        layout.addStretch()
        return widget

    def save_gemini_api_key(self):
        """Save Gemini API Key"""
        api_key = self.api_key_input.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "⚠️ Warning", "Please enter an API key")
            return
        
        if not self.gemini_manager.is_api_key_valid(api_key):
            QMessageBox.warning(self, "❌ Invalid Key", "API key appears to be invalid. Please check and try again.")
            return
        
        if self.gemini_manager.save_config(api_key):
            QMessageBox.information(self, "✅ Success", "Gemini API key saved successfully!\n\nYou can now use Gemini AI features.")
            self.api_key_input.clear()
        else:
            QMessageBox.critical(self, "❌ Error", "Failed to save API key. Please check permissions.")

    def test_gemini_connection(self):
        """Test Gemini API connection"""
        if not self.gemini_manager.is_configured:
            QMessageBox.warning(self, "⚠️ Warning", "Gemini is not configured. Please save an API key first.")
            return
        
        # Show progress
        QMessageBox.information(self, "🧪 Testing", "Testing connection to Gemini API...")
        result = self.gemini_manager.test_connection()
        
        if result['success']:
            QMessageBox.information(
                self, 
                "✅ Connection Successful", 
                f"Gemini API is working!\n\nResponse:\n{result['response']}"
            )
        else:
            QMessageBox.critical(
                self, 
                "❌ Connection Failed", 
                f"Error: {result['message']}\n\n{result['error']}"
            )

    def remove_gemini_api_key(self):
        """Remove stored Gemini API Key"""
        reply = QMessageBox.question(
            self,
            "🗑️ Confirm Deletion",
            "Are you sure you want to remove the saved API key?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.gemini_manager.remove_api_key():
                QMessageBox.information(self, "✅ Success", "API key removed successfully.")
                self.api_key_input.clear()
            else:
                QMessageBox.critical(self, "❌ Error", "Failed to remove API key.")

    def open_link(self, url: str):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)

    def get_tab_stylesheet(self) -> str:
        """Get modern tab stylesheet"""
        return """
            QTabWidget {
                background: transparent;
                border: none;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                           stop:0 rgba(124,58,237,0.1),
                           stop:1 rgba(124,58,237,0.05));
                color: #CBD5E1;
                border: 1px solid rgba(124,58,237,0.2);
                border-bottom: 3px solid transparent;
                padding: 12px 20px;
                margin-right: 3px;
                border-radius: 8px 8px 0px 0px;
                font-weight: bold;
                font-size: 11pt;
            }
            QTabBar::tab:hover {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                           stop:0 rgba(124,58,237,0.2),
                           stop:1 rgba(124,58,237,0.1));
                color: #F0F4F8;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                           stop:0 rgba(124,58,237,0.3),
                           stop:1 rgba(6,182,212,0.1));
                color: #F0F4F8;
                border: 1px solid rgba(124,58,237,0.5);
                border-bottom: 3px solid #06B6D4;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """
