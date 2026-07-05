import sys
import os
from typing import Dict, List, Optional, Union
from pathlib import Path
from PySide6.QtGui import (
    QFontDatabase, 
    QFont, 
    QPixmap, 
    QPalette, 
    QIcon, 
    QColor,
    QLinearGradient,
    QCursor,
    QPainter
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QStackedWidget,
    QGridLayout,
    QSizePolicy,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEasingCurve, QTimer

try:
    from ui_theme import get_global_styles, load_fonts
except Exception:
    # ui_theme may not be available during some operations; fail gracefully
    def get_global_styles():
        return ""
    def load_fonts(path=None):
        return


# Small animated button with subtle hover icon scaling
class AnimatedButton(QPushButton):
    """Simple animated button that scales its icon slightly on hover.

    Keeps behavior minimal and robust so it won't break if icon is missing.
    """
    def __init__(self, *args, icon_size: int = 28, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_icon_size = QSize(icon_size, icon_size)
        try:
            self.setIconSize(self._default_icon_size)
        except Exception:
            pass

    def enterEvent(self, event):
        try:
            sz = self.iconSize()
            self.setIconSize(QSize(int(sz.width() * 1.18), int(sz.height() * 1.18)))
        except Exception:
            pass
        return super().enterEvent(event)

    def leaveEvent(self, event):
        try:
            self.setIconSize(self._default_icon_size)
        except Exception:
            pass
        return super().leaveEvent(event)

# Import all page classes
from pages.project_page import ProjectPage
from pages.archive_page import ArchivePage
from pages.docs_page import DocsPage
from pages.cloud_page import CloudPage
from pages.settings_page import SettingsPage

class SoftAICodeUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        # Type-annotated class attributes
        self.width: int = 0
        self.height: int = 0
        self.screen_width: int = 0 
        self.screen_height: int = 0
        self.base_size: int = 0
        self.icon_size: int = 0
        self.button_icon_size: int = 0
        self.padding: int = 0
        
        # Path attributes
        self.base_path: Path = Path()
        self.asset_path: Path = Path()
        self.font_path: Path = Path()
        self.bg_path: Path = Path()
        self.logo_path: Path = Path()
        
        # Widget attributes
        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.home_page: QWidget = QWidget()
        self.project_page: ProjectPage
        self.archive_page: ArchivePage
        self.docs_page: DocsPage
        self.cloud_page: CloudPage
        self.settings_page: SettingsPage
        
        # Font dictionary
        self.fonts: Dict[str, QFont] = {}
        
        # Menu items
        self.menu_items: List[Dict[str, any]] = []
        
        # Initialize components
        self.init_paths()
        self.verify_icons()  # Add this line
        self.setup_window_size()
        self.init_menu_items()
        self.load_background()
        self.setup_pages()
        self.init_ui()

    def setup_home_page(self):
        """Setup halaman home dengan nuansa UI/UX premium, modern, dan lengkap."""
        home_layout = QVBoxLayout(self.home_page)
        home_layout.setSpacing(18)
        home_layout.setContentsMargins(24, 24, 24, 24)

        welcome_container = QFrame()
        welcome_container.setObjectName("welcomeHome")
        welcome_container.setStyleSheet("""
            QFrame#welcomeHome {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(19, 38, 92, 0.98),
                    stop:0.35 rgba(28, 58, 122, 0.97),
                    stop:0.7 rgba(45, 86, 160, 0.96),
                    stop:1 rgba(24, 48, 103, 0.98)
                );
                border-radius: 24px;
                border: 1px solid rgba(130, 220, 255, 0.32);
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 90))
        welcome_container.setGraphicsEffect(shadow)

        welcome_layout = QVBoxLayout(welcome_container)
        welcome_layout.setSpacing(18)
        welcome_layout.setContentsMargins(26, 24, 26, 24)

        header_row = QHBoxLayout()
        header_row.setSpacing(20)

        title_area = QVBoxLayout()
        title_area.setSpacing(8)

        main_title = QLabel("✨ Selamat Datang di Soft ΔI Pro ✨")
        main_title.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 30px;
                font-weight: 800;
                font-family: 'Poppins', 'Segoe UI';
                letter-spacing: 1px;
            }
        """)
        main_title.setAlignment(Qt.AlignLeft)

        subtitle = QLabel(
            "Platform AI modern yang membantu tim mengelola proyek, merancang alur kerja, dan mengeksekusi ide menjadi solusi digital yang matang."
        )
        subtitle.setStyleSheet("""
            QLabel {
                color: #DDEEFF;
                font-size: 14px;
                font-family: 'Segoe UI';
                line-height: 160%;
            }
        """)
        subtitle.setWordWrap(True)

        title_area.addWidget(main_title)
        title_area.addWidget(subtitle)

        badge = QFrame()
        badge.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.12);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.22);
            }
        """)
        badge_layout = QVBoxLayout(badge)
        badge_layout.setContentsMargins(14, 12, 14, 12)
        badge_title = QLabel("UI/UX Premium")
        badge_title.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: 700;")
        badge_desc = QLabel("AI Assisted • Design System")
        badge_desc.setStyleSheet("color: #BEDFEE; font-size: 12px;")
        badge_layout.addWidget(badge_title)
        badge_layout.addWidget(badge_desc)
        badge.setFixedWidth(int(self.width * 0.22))

        header_row.addLayout(title_area, 1)
        header_row.addWidget(badge, alignment=Qt.AlignTop)
        welcome_layout.addLayout(header_row)

        action_row = QHBoxLayout()
        action_row.setSpacing(12)
        for label, target_widget in [
            ("Mulai Project", self.project_page),
            ("Lihat Dokumentasi", self.docs_page),
            ("Jelajahi Cloud", self.cloud_page),
        ]:
            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(42)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255,255,255,0.18), stop:1 rgba(255,255,255,0.08));
                    color: #FFFFFF;
                    border: 1px solid rgba(255,255,255,0.24);
                    border-radius: 12px;
                    padding-left: 16px;
                    padding-right: 16px;
                    font-weight: 700;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255,255,255,0.28), stop:1 rgba(255,255,255,0.14));
                    border: 1px solid rgba(255,255,255,0.38);
                }
            """)
            btn.clicked.connect(lambda checked=False, widget=target_widget: self.stacked_widget.setCurrentWidget(widget))
            action_row.addWidget(btn)

        welcome_layout.addLayout(action_row)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        stats_cards = [
            ("Project Aktif", "12", "#4FC3F7"),
            ("AI Workflow", "98%", "#81C784"),
            ("Waktu Efektif", "+40%", "#FFB74D"),
        ]
        for title, value, accent in stats_cards:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: rgba(255, 255, 255, 0.10);
                    border-radius: 16px;
                    border: 1px solid rgba(255,255,255,0.14);
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(14, 12, 14, 12)
            card_title = QLabel(title)
            card_title.setStyleSheet("color: #EAF6FF; font-size: 12px;")
            card_value = QLabel(value)
            card_value.setStyleSheet(f"color: {accent}; font-size: 24px; font-weight: 800;")
            card_layout.addWidget(card_title)
            card_layout.addWidget(card_value)
            stats_row.addWidget(card)

        welcome_layout.addLayout(stats_row)

        content_area = QHBoxLayout()
        content_area.setSpacing(16)

        info_panel = QFrame()
        info_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.14);
            }
        """)
        info_layout = QVBoxLayout(info_panel)
        info_layout.setContentsMargins(18, 16, 18, 16)
        info_layout.setSpacing(10)

        info_title = QLabel("Kenapa tim menyukai Soft ΔI Pro")
        info_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        info_layout.addWidget(info_title)

        bullets = [
            "• Alur kerja terstruktur dari ide sampai eksekusi.",
            "• UI modern yang nyaman dipakai dalam durasi panjang.",
            "• Integrasi AI membantu mempercepat pengembangan.",
            "• Sinkronisasi project dan dokumentasi dalam satu tempat.",
        ]
        for item in bullets:
            bullet = QLabel(item)
            bullet.setStyleSheet("color: #DDEEFF; font-size: 13px;")
            bullet.setWordWrap(True)
            info_layout.addWidget(bullet)

        info_layout.addStretch()

        features_container = self.setup_feature_cards()
        content_area.addWidget(info_panel, 1)
        content_area.addWidget(features_container)
        welcome_layout.addLayout(content_area)

        footer_note = QLabel("Didesain untuk tetap cepat, bersih, dan elegan — cocok untuk project personal maupun tim profesional.")
        footer_note.setStyleSheet("color: #CFE7FF; font-size: 12px; font-style: italic;")
        footer_note.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(footer_note)

        home_layout.addWidget(welcome_container)
        
    def init_paths(self):
        """Initialize all required paths"""
        try:
            # Base paths - use current script directory
            self.base_path = Path(__file__).parent.absolute()
            self.asset_path = self.base_path
            self.font_path = self.base_path
            self.bg_path = self.base_path / "background.jpg"
            self.logo_path = self.base_path / "SoftAI_Logo.png"
            
            # Create icon directories if needed
            icon_path = self.asset_path / "icons" / "features"
            icon_path.mkdir(parents=True, exist_ok=True)
            
            print(f"Base path: {self.base_path}")
            print(f"Background path: {self.bg_path}")
            print(f"Logo path: {self.logo_path}")
    
        except Exception as e:
            print(f"Error initializing paths: {e}")
            # Set fallback paths
            self.base_path = Path.cwd()
            self.asset_path = self.base_path
            self.font_path = self.base_path
            self.bg_path = self.base_path / "background.jpg"
            self.logo_path = self.base_path / "SoftAI_Logo.png"

    def load_background(self):
        """Load and setup background image"""
        try:
            # Check if background exists
            if not self.bg_path.exists():
                raise FileNotFoundError(f"Background not found at: {self.bg_path}")

            # Load background image
            background = QPixmap(str(self.bg_path))
            if background.isNull():
                raise ValueError("Failed to load background image")

            # Set background with proper scaling
            self.setAutoFillBackground(True)
            palette = self.palette()
            scaled_bg = background.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            palette.setBrush(QPalette.Window, scaled_bg)
            self.setPalette(palette)

            # Add semi-transparent overlay
            self.setStyleSheet("""
                QWidget#mainWindow {
                    background-color: rgba(0, 0, 0, 0.5);
                }
            """)
            self.setObjectName("mainWindow")

        except Exception as e:
            print(f"Error loading background: {e}")
            self.use_fallback_background()
            
    def setup_window_size(self):
        """Initialize window size and screen dimensions"""
        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # Calculate window size (80% of screen size)
        self.width = int(self.screen_width * 0.8)
        self.height = int(self.screen_height * 0.8)
        
        # Center window
        x = (self.screen_width - self.width) // 2
        y = (self.screen_height - self.height) // 2
        
        self.setGeometry(x, y, self.width, self.height)
        
        # Calculate base sizes
        self.base_size = min(self.width, self.height) // 50
        self.icon_size = min(self.width, self.height) // 25
        self.button_icon_size = min(self.width, self.height) // 35
        self.padding = self.base_size

    def init_ui(self):
        # Create main layout first
        main_layout = QGridLayout(self)
        main_layout.setSpacing(self.padding)
        main_layout.setContentsMargins(self.padding, self.padding, 
                                     self.padding, self.padding)

        # Calculate sizes
        frame_width = int(self.width * 0.25)  # 25% of window width
        
       # Create left panel layout first
        left_panel = QVBoxLayout()  # Add this line
        left_panel.setSpacing(10)
        
        # Create all frames
        logo_frame = QFrame()
        menu_frame = QFrame()
        copyright_frame = QFrame()
        
        # Copyright frame (15%)
        copyright_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(25, 35, 80, 0.9),
                    stop:1 rgba(30, 50, 100, 0.9)
                );
                border: 2px solid rgba(100, 180, 255, 0.3);
                border-radius: 15px;
                margin: 5px;
            }
        """)

        copyright_frame.setFixedHeight(int(self.height * 0.15))
        
        # Add shadow to copyright frame
        copyright_shadow = QGraphicsDropShadowEffect()
        copyright_shadow.setBlurRadius(20)
        copyright_shadow.setXOffset(0)
        copyright_shadow.setYOffset(5)
        copyright_shadow.setColor(QColor(0, 0, 0, 70))
        copyright_frame.setGraphicsEffect(copyright_shadow)
        
        copyright_layout = QVBoxLayout(copyright_frame)
        copyright_text = QLabel("Copyright © 2027 • Senja Intan Permata")
        copyright_text.setStyleSheet("""
            QLabel {
                color: #808080;
                font-size: 12pt;
            }
        """)
        copyright_text.setAlignment(Qt.AlignCenter)
        copyright_layout.addWidget(copyright_text)

        # Set frame styles and sizes
        logo_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(30, 50, 100, 0.9),
                    stop:0.5 rgba(40, 70, 130, 0.9),
                    stop:1 rgba(50, 80, 150, 0.9)
                );
                border: 2px solid rgba(100, 180, 255, 0.4);
                border-radius: 20px;
            }
        """)
        logo_frame.setFixedWidth(frame_width)
        logo_frame.setFixedHeight(int(self.height * 0.30))  # Changed height to self.height
        
        menu_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 50, 100, 0.85),
                    stop:0.5 rgba(35, 60, 115, 0.85),
                    stop:1 rgba(25, 45, 95, 0.85)
                );
                border: 2px solid rgba(100, 180, 255, 0.4);
                border-radius: 20px;
                padding: 10px;
            }
        """)
        menu_frame.setFixedWidth(frame_width)
        menu_frame.setFixedHeight(int(self.height * 0.60))  # Changed height to self.height
        
        # Add shadow effects to frames
        logo_shadow = QGraphicsDropShadowEffect()
        logo_shadow.setBlurRadius(30)
        logo_shadow.setXOffset(0)
        logo_shadow.setYOffset(10)
        logo_shadow.setColor(QColor(0, 0, 0, 80))
        logo_frame.setGraphicsEffect(logo_shadow)
        
        menu_shadow = QGraphicsDropShadowEffect()
        menu_shadow.setBlurRadius(30)
        menu_shadow.setXOffset(0)
        menu_shadow.setYOffset(10)
        menu_shadow.setColor(QColor(0, 0, 0, 80))
        menu_frame.setGraphicsEffect(menu_shadow)
    
        # Create layouts for frames
        logo_layout = QVBoxLayout(logo_frame)
        menu_layout = QVBoxLayout(menu_frame)
    
        # Logo layout setup
        logo_layout.setSpacing(6)
        logo_layout.setContentsMargins(15, 12, 15, 12)
        
        # Software name
        name_label = QLabel("Soft ΔI Pro")
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Segoe UI';
                font-size: 24pt;
                font-weight: bold;
            }
        """)
        name_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(name_label)

        # Logo image
        logo_label = QLabel()
        if self.logo_path.exists():
            logo_pixmap = QPixmap(str(self.logo_path))
            logo_size = int(frame_width * 0.40)
            scaled_logo = logo_pixmap.scaled(
                logo_size, logo_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            logo_label.setPixmap(scaled_logo)
        else:
            logo_label.setText("🧠")
            logo_label.setStyleSheet("color: white; font-size: 42px;")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)

        status_label = QLabel("AI Workspace • Ready")
        status_label.setStyleSheet("color: #CFE8FF; font-size: 10pt; font-style: italic;")
        status_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(status_label)

        # Menu layout setup
        menu_layout.setSpacing(8)
        menu_layout.setContentsMargins(10, 12, 10, 12)

        menu_title = QLabel("Navigasi Halaman")
        menu_title.setStyleSheet("color: #DDEFFF; font-size: 11pt; font-weight: 700;")
        menu_layout.addWidget(menu_title)

        # Create menu buttons
        for item in self.menu_items:
            btn = self.create_menu_button(item)
            menu_layout.addWidget(btn)
            if item != self.menu_items[-1]:
                menu_layout.addSpacing(4)
        menu_layout.addStretch()

        # Add frames to left panel with proper proportions
        left_panel.addWidget(logo_frame)
        left_panel.addWidget(menu_frame)
        left_panel.setStretch(0, 30)  # Logo frame takes 30%
        left_panel.setStretch(1, 60)  # Menu frame takes 60%

        # Create home button
        home_btn = QPushButton()
        home_btn.setFixedSize(40, 40)  # Set fixed size for the icon button
        home_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                margin: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.15);
                margin: 12px;
            }
        """)
        
        # Load home icon
        home_icon = QPixmap(str(self.asset_path / "home.png"))
        if not home_icon.isNull():
            scaled_icon = home_icon.scaled(
                24, 24,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            home_btn.setIcon(QIcon(scaled_icon))
            home_btn.setIconSize(scaled_icon.size())
        
        # Connect home button click
        home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        
        # Create container for home button (top-right alignment)
        home_container = QHBoxLayout()
        home_container.addStretch()
        home_container.addWidget(home_btn)
        
        # Modify right panel layout to include home button
        right_panel = QVBoxLayout()
        right_panel.addLayout(home_container)  # Add home button at top
        right_panel.addWidget(self.stacked_widget, 85)
        right_panel.addWidget(copyright_frame, 15)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 0, 0)    # Left panel
        main_layout.addLayout(right_panel, 0, 1)   # Right panel
        
        # Set column stretches
        main_layout.setColumnStretch(0, 1)   # Left column (20%)
        main_layout.setColumnStretch(1, 4)   # Right column (80%)

        # Set background image
        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap(str(self.bg_path))
        if not background.isNull():
            scaled_bg = background.scaled(
                QSize(self.width, self.height),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            palette.setBrush(QPalette.Window, scaled_bg)
        self.setPalette(palette)

        # Update main widget background to be semi-transparent
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 32, 70, 0.95),
                    stop:0.3 rgba(25, 45, 100, 0.95),
                    stop:0.6 rgba(35, 55, 120, 0.95),
                    stop:1 rgba(10, 25, 60, 0.95)
                );
            }
        """)

        # Font Setup
        self.fonts = {
            'title': QFont('Poppins', int(self.base_size * 3.2), QFont.Bold),
            'menu': QFont('Poppins', int(self.base_size * 1.4), QFont.Medium),
            'welcome': QFont('Open Sans', int(self.base_size * 2.8), QFont.Bold),
            'description': QFont('Quicksand', int(self.base_size * 1.3)),
            'copyright': QFont('Montserrat', int(self.base_size * 1.1), QFont.Light)
        }

        # Debug code to check background path
        print(f"Checking background path: {self.bg_path}")
        print(f"File exists: {self.bg_path.exists()}")
        print("SoftAICodeUI initialization completed successfully")

    def init_layouts(self):
        # Create frames
        self.logo_frame = QFrame()
        self.menu_frame = QFrame()
        self.welcome_frame = QFrame()
        
        # Set size policies
        self.logo_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.menu_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.welcome_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Apply backgrounds
        self.setup_frame_background(self.logo_frame, 0.8)
        self.setup_frame_background(self.menu_frame, 0.9)
        self.setup_frame_background(self.welcome_frame, 0.85)

    def load_image(self, path: Union[str, Path]) -> Optional[QPixmap]:
        """Load image with type checking and error handling"""
        try:
            path = Path(path) if isinstance(path, str) else path
            if not path.exists():
                print(f"Warning: Image not found at {path}")
                return None
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                return None
            return pixmap
        except Exception as e:
            print(f"Error loading image: {e}")
            return None


    def use_fallback_background(self):
        """Fallback background if image fails to load"""
        try:
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1a237e,
                        stop:0.4 #0d47a1,
                        stop:1 #01579b
                    );
                }
            """)
        except Exception as e:
            print(f"Error setting fallback background: {e}")

    # Function to create styled button with icons
    def create_menu_button(self, item):
        """Create styled menu button sederhana (icon + text)."""
        btn = QPushButton(item["text"])
        btn.setFixedHeight(54)
        btn.setFixedWidth(int(self.width * 0.22))

        # Set icon jika tersedia
        icon_path = self.asset_path / item["icon"]
        if icon_path.exists():
            pix = QPixmap(str(icon_path))
            if not pix.isNull():
                icon = QIcon(pix.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                btn.setIcon(icon)
                btn.setIconSize(QSize(28, 28))

        # Styling tombol
        btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 18px;
                color: {item['colors']['text']};
                font-family: 'Poppins', 'Segoe UI';
                font-weight: 700;
                font-size: 13pt;
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {item['colors']['start']}, stop:1 {item['colors']['end']});
                border-radius: 12px;
                border: 2px solid rgba(255,255,255,0.12);
            }}
            QPushButton:hover {{ border: 2px solid rgba(255,255,255,0.4); }}
            QPushButton:pressed {{ padding-left: 20px; }}
        """)

        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: self.switch_page(item["text"]))

        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(14)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 60))
        btn.setGraphicsEffect(shadow)

        return btn

    def switch_page(self, button_text):
        """Switch to appropriate page based on button text"""
        if button_text == "Beranda":
            self.stacked_widget.setCurrentWidget(self.home_page)
        elif button_text == "Project Baru":
            self.stacked_widget.setCurrentWidget(self.project_page)
        elif button_text == "Arsip Project":
            self.stacked_widget.setCurrentWidget(self.archive_page)
        elif button_text == "Dokumentasi":
            self.stacked_widget.setCurrentWidget(self.docs_page)
        elif button_text == "Cloud Integrated":
            self.stacked_widget.setCurrentWidget(self.cloud_page)
        elif button_text == "Pengaturan":
            self.stacked_widget.setCurrentWidget(self.settings_page)
        else:
            self.stacked_widget.setCurrentWidget(self.home_page)
        
        # Create home page with attractive design
        home_layout = QVBoxLayout(self.home_page)
        home_layout.setSpacing(30)
        home_layout.setContentsMargins(40, 40, 40, 40)

        # Create welcome container with gradient background
        welcome_container = QFrame()
        welcome_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(41, 53, 86, 0.9),
                    stop:0.5 rgba(55, 65, 105, 0.9),
                    stop:1 rgba(69, 77, 124, 0.9)
                );
                border-radius: 25px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        welcome_layout = QVBoxLayout(welcome_container)
        welcome_layout.setSpacing(30)
        welcome_layout.setContentsMargins(30, 40, 30, 40)
        
        # Animated welcome text with emoji and effects
        welcome_text = QLabel("✨ Selamat Datang di Soft ΔI Pro ✨")
        welcome_text.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 42px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 15px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        welcome_text.setAlignment(Qt.AlignCenter)
        
        # Modern description text with better formatting
        desc_text = QLabel(
            "<div style='line-height: 165%;'>"
            "<p style='margin-bottom: 20px;'>"
            "Selamat datang di platform inovatif yang mengintegrasikan "
            "<span style='color: #4FC3F7; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>"
            "Artificial Intelligence</span> dalam pengembangan Software.</p>"
            
            "<p style='margin-bottom: 20px;'>"
            "Dengan fitur AI canggih, kami mempercepat proses development Anda menjadi lebih "
            "<span style='color: #81C784; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>"
            "efisien</span> dan "
            "<span style='color: #81C784; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>"
            "produktif</span>.</p>"
            
            "<p>Platform ini menyediakan berbagai fitur AI yang "
            "<span style='color: #FFB74D; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>"
            "powerful</span> untuk optimasi kode dan pengembangan aplikasi.</p>"
            "</div>"
        )
        desc_text.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                font-size: 18px;
                font-family: 'Segoe UI';
                background: rgba(0, 0, 0, 0.2);
                padding: 25px;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        desc_text.setWordWrap(True)
        desc_text.setAlignment(Qt.AlignCenter)
        
        # Add elements to welcome layout
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addWidget(desc_text)
        
        # Add welcome container to home layout
        home_layout.addWidget(welcome_container, 1)
        
    def init_menu_items(self):
        """Initialize menu items with vibrant colors"""
        self.menu_items = [
            {
                "text": "Beranda",
                "colors": {
                    "start": "#4F46E5",
                    "end": "#7C3AED",
                    "hover": "#A78BFA",
                    "text": "#FFFFFF"
                },
                "icon": "home.png"
            },
            {
                "text": "Project Baru",
                "colors": {
                    "start": "#FF6B6B",  # Soft red
                    "end": "#4ECDC4",    # Turquoise
                    "hover": "#FFE66D",   # Bright yellow
                    "text": "#FFFFFF"
                },
                "icon": "new_project.png"
            },
            {
                "text": "Arsip Project",
                "colors": {
                    "start": "#FFD93D",  # Golden yellow
                    "end": "#6C5CE7",    # Purple
                    "hover": "#A8E6CF",  # Mint green
                    "text": "#FFFFFF"
                },
                "icon": "archive.png"
            },
            {
                "text": "Dokumentasi",
                "colors": {
                    "start": "#00B4D8",  # Bright blue
                    "end": "#FF7096",    # Pink
                    "hover": "#FFE162",   # Light yellow
                    "text": "#FFFFFF"
                },
                "icon": "docs.png"
            },
            {
                "text": "Cloud Integrated",
                "colors": {
                    "start": "#48BF91",  # Ocean green
                    "end": "#4361EE",    # Royal blue
                    "hover": "#FF9F1C",  # Orange
                    "text": "#FFFFFF"
                },
                "icon": "cloud.png"
            },
            {
                "text": "Pengaturan",
                "colors": {
                    "start": "#06D6A0",  # Mint
                    "end": "#BB8FCE",    # Light purple
                    "hover": "#45B7D1",  # Sky blue
                    "text": "#FFFFFF"
                },
                "icon": "settings.png"
            }
        ]

    def setup_pages(self):
        """Initialize and setup all pages"""
        # Create other pages first so navigation actions can target them safely
        self.project_page = ProjectPage()
        self.archive_page = ArchivePage()
        self.docs_page = DocsPage()
        self.cloud_page = CloudPage()
        self.settings_page = SettingsPage()

        # Create home page
        self.home_page = QWidget()
        self.setup_home_page()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.project_page)
        self.stacked_widget.addWidget(self.archive_page)
        self.stacked_widget.addWidget(self.docs_page)
        self.stacked_widget.addWidget(self.cloud_page)
        self.stacked_widget.addWidget(self.settings_page)
        
        # Set home page as default
        self.stacked_widget.setCurrentWidget(self.home_page)

    def load_custom_fonts(self):
        """Load custom fonts from the fonts directory"""
        try:
            font_dir = self.base_path / "fonts"
            font_dir.mkdir(exist_ok=True)
            
            # Define required fonts and their files
            required_fonts = {
                "Poppins": ["Poppins-Regular.ttf", "Poppins-Medium.ttf", "Poppins-Bold.ttf"],
                "Roboto": ["Roboto-Regular.ttf", "Roboto-Medium.ttf", "Roboto-Bold.ttf"],
                "Open Sans": ["OpenSans-Regular.ttf", "OpenSans-Bold.ttf"],
                "Quicksand": ["Quicksand-Regular.ttf", "Quicksand-Medium.ttf"],
                "Montserrat": ["Montserrat-Regular.ttf", "Montserrat-Light.ttf"]
            }
            
            # Load each font
            for font_family, font_files in required_fonts.items():
                for font_file in font_files:
                    font_path = font_dir / font_file
                    if font_path.exists():
                        font_id = QFontDatabase.addApplicationFont(str(font_path))
                        if font_id < 0:
                            print(f"Failed to load font: {font_file}")
                    else:
                        print(f"Missing font file: {font_file}")
                        
            # Set fallback fonts if needed
            self.fonts = {
                'title': QFont('Poppins', int(self.base_size * 3.2), QFont.Bold),
                'menu': QFont('Poppins', int(self.base_size * 1.4), QFont.Medium),
                'welcome': QFont('Open Sans', int(self.base_size * 2.8), QFont.Bold),
                'description': QFont('Quicksand', int(self.base_size * 1.3)),
                'copyright': QFont('Montserrat', int(self.base_size * 1.1), QFont.Light)
            }
                        
        except Exception as e:
            print(f"Error loading fonts: {e}")
            # Use system fonts as fallback
            self.fonts = {
                'title': QFont('Segoe UI', int(self.base_size * 3.2), QFont.Bold),
                'menu': QFont('Segoe UI', int(self.base_size * 1.4), QFont.Medium),
                'welcome': QFont('Segoe UI', int(self.base_size * 2.8), QFont.Bold),
                'description': QFont('Segoe UI', int(self.base_size * 1.3)),
                'copyright': QFont('Segoe UI', int(self.base_size * 1.1), QFont.Light)
            }                    

    def verify_icons(self):
        """Verify all required icons exist"""
        icon_paths = {
            'features': ['rocket.png', 'ai.png', 'cloud.png']
        }
        
        # Create features directory if it doesn't exist
        features_dir = self.asset_path / 'icons' / 'features'
        features_dir.mkdir(parents=True, exist_ok=True)
        # Check each icon and create simple placeholder if missing
        missing = []
        for folder, icons in icon_paths.items():
            for icon in icons:
                path = self.asset_path / 'icons' / folder / icon
                if not path.exists():
                    missing.append(path)

        if missing:
            print("\nMissing icons detected. Creating placeholder icons:")
            for p in missing:
                try:
                    size = 64
                    pix = QPixmap(size, size)
                    pix.fill(Qt.transparent)
                    painter = QPainter(pix)
                    painter.setRenderHint(QPainter.Antialiasing)
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QColor(255, 255, 255))
                    painter.drawEllipse(6, 6, size-12, size-12)
                    painter.end()
                    scaled = pix.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    p.parent.mkdir(parents=True, exist_ok=True)
                    scaled.save(str(p), "PNG")
                    print(f"- Created: {p}")
                except Exception as e:
                    print(f"Failed to create placeholder for {p}: {e}")

    def setup_feature_cards(self):
        """Setup feature cards dengan desain yang lebih menakjubkan"""
        features_container = QFrame()
        features_container.setFixedWidth(int(self.width * 0.35))
        features_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(50, 80, 150, 0.4),
                    stop:1 rgba(70, 100, 170, 0.4)
                );
                border-radius: 18px;
                border: 2px solid rgba(100, 180, 255, 0.3);
            }
        """)

        features_layout = QVBoxLayout(features_container)
        features_layout.setSpacing(15)
        features_layout.setContentsMargins(18, 18, 18, 18)

        feature_cards = [
            {
                "icon": "features/rocket.png",
                "title": "⚡ Cepat & Efisien",
                "desc": "Kecepatan tinggi dalam development",
                "color": "#9A83FF",
                "gradient": "rgba(154, 131, 255, 0.25)",
                "accent": "rgba(154, 131, 255, 0.5)"
            },
            {
                "icon": "features/ai.png",
                "title": "🤖 AI Powered", 
                "desc": "Asisten kode cerdas dengan AI",
                "color": "#A3FFA8",
                "gradient": "rgba(163, 255, 168, 0.25)",
                "accent": "rgba(163, 255, 168, 0.5)"
            },
            {
                "icon": "features/cloud.png",
                "title": "☁️ Cloud Sync",
                "desc": "Sinkronisasi real-time di cloud",
                "color": "#7AD9FF",
                "gradient": "rgba(122, 217, 255, 0.25)",
                "accent": "rgba(122, 217, 255, 0.5)"
            }
        ]

        for i, card in enumerate(feature_cards):
            card_frame = QFrame()
            card_frame.setFixedHeight(90)
            card_frame.setStyleSheet(f"""
                QFrame {{
                    background: {card['gradient']};
                    border-radius: 15px;
                    border: 2px solid {card['color']};
                }}
            """)
            
            card_layout = QHBoxLayout(card_frame)
            card_layout.setSpacing(15)
            card_layout.setContentsMargins(18, 12, 18, 12)

            # Icon container dengan styling lebih menarik
            icon_container = QFrame()
            icon_container.setFixedSize(60, 60)
            icon_container.setStyleSheet(f"""
                QFrame {{
                    background: {card['accent']};
                    border-radius: 12px;
                    border: 2px solid {card['color']};
                }}
            """)

            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(10, 10, 10, 10)

            # Icon
            icon_label = QLabel()
            icon_path = self.asset_path / "icons" / card["icon"]
            if icon_path.exists():
                icon_pixmap = QPixmap(str(icon_path))
                if not icon_pixmap.isNull():
                    scaled_icon = icon_pixmap.scaled(
                        40, 40,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    icon_label.setPixmap(scaled_icon)
                    icon_label.setAlignment(Qt.AlignCenter)
            else:
                icon_label.setText("📦")
                icon_label.setStyleSheet(f"color: {card['color']}; font-size: 32px;")
                icon_label.setAlignment(Qt.AlignCenter)

            icon_layout.addWidget(icon_label)

            # Text section dengan spacing optimal
            text_container = QVBoxLayout()
            text_container.setSpacing(5)
            text_container.setContentsMargins(0, 0, 0, 0)

            title_label = QLabel(card["title"])
            title_label.setStyleSheet(f"""
                QLabel {{
                    color: #FFFFFF;
                    font-size: 14px;
                    font-weight: 800;
                    font-family: 'Poppins', 'Segoe UI';
                    letter-spacing: 0.5px;
                }}
            """)

            desc_label = QLabel(card["desc"])
            desc_label.setStyleSheet(f"""
                QLabel {{
                    color: #E0E0FF;
                    font-size: 12px;
                    font-family: 'Segoe UI';
                    letter-spacing: 0.3px;
                }}
            """)
            desc_label.setWordWrap(True)

            text_container.addWidget(title_label)
            text_container.addWidget(desc_label)
            text_container.addStretch()

            # Layout assembly
            card_layout.addWidget(icon_container)
            card_layout.addLayout(text_container, stretch=1)
            
            features_layout.addWidget(card_frame)

            # Opacity animation (micro animation saat tampil)
            try:
                opacity_effect = QGraphicsOpacityEffect(card_frame)
                opacity_effect.setOpacity(0.0)
                card_frame.setGraphicsEffect(opacity_effect)
                anim = QPropertyAnimation(opacity_effect, b"opacity")
                anim.setDuration(420)
                anim.setStartValue(0.0)
                anim.setEndValue(1.0)
                anim.setEasingCurve(QEasingCurve.OutCubic)
                if not hasattr(self, '_feature_anims'):
                    self._feature_anims = []
                self._feature_anims.append(anim)
                QTimer.singleShot(140 * i, anim.start)
            except Exception:
                pass

        features_layout.addStretch()
        
        # Add shadow effect ke container
        container_shadow = QGraphicsDropShadowEffect()
        container_shadow.setBlurRadius(20)
        container_shadow.setXOffset(0)
        container_shadow.setYOffset(8)
        container_shadow.setColor(QColor(0, 0, 0, 80))
        features_container.setGraphicsEffect(container_shadow)
        
        return features_container
        

class SoftAIError(Exception):
    """Base exception for Soft AI Pro"""
    pass

class ResourceNotFoundError(SoftAIError):
    """Raised when a required resource is missing"""
    pass

class FontLoadError(SoftAIError):
    """Raised when font loading fails"""
    pass

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        # Set default font
        app.setFont(QFont("Segoe UI", 10))

        # Create main window and load fonts
        window = SoftAICodeUI()
        try:
            window.load_custom_fonts()
        except Exception:
            pass

        # Load bundled fonts (if present) and apply global theme
        try:
            load_fonts(window.base_path / 'fonts')
        except Exception:
            pass
        try:
            app.setStyleSheet(get_global_styles())
        except Exception:
            # Fallback minimal stylesheet
            app.setStyleSheet("""
                QWidget { color: #E8F0FF; font-family: 'Segoe UI'; }
                QPushButton { border: none; }
            """)

        # Check required files
        required_files = {
            "background.jpg": window.bg_path,
            "SoftAI_Logo.png": window.logo_path
        }
        missing_files = [name for name, path in required_files.items() if not path.exists()]
        if missing_files:
            print("Missing required files:")
            for file in missing_files:
                print(f"- {file}")
            print(f"\nPlease place files in: {window.asset_path}")

        # Fade-in animation for nicer startup
        window.setWindowOpacity(0.0)
        window.show()
        anim = QPropertyAnimation(window, b"windowOpacity")
        anim.setDuration(600)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        window._fade_anim = anim
        anim.start()

        sys.exit(app.exec())

    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)