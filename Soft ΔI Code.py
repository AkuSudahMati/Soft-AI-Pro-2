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
    QColor
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
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QSize, QRect

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
        """Setup welcome screen layout with optimized spacing"""
        home_layout = QVBoxLayout(self.home_page)
        home_layout.setSpacing(12)
        home_layout.setContentsMargins(20, 15, 20, 15)

        # Create welcome container with refined gradient
        welcome_container = QFrame()
        welcome_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(28, 41, 90, 0.94),
                    stop:0.5 rgba(35, 50, 100, 0.96),
                    stop:1 rgba(46, 64, 120, 0.94)
                );
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)
        
        welcome_layout = QVBoxLayout(welcome_container)
        welcome_layout.setSpacing(15)
        welcome_layout.setContentsMargins(25, 20, 25, 20)
        
        # Title section with optimized styling
        title_container = QFrame()
        title_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
        """)
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(15, 12, 15, 12)
        
        welcome_text = QLabel("✨ Selamat Datang di Soft ΔI Pro ✨")
        welcome_text.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Segoe UI';
                letter-spacing: 0.5px;
            }
        """)
        welcome_text.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(welcome_text)
        
        # Content section
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Description section (left)
        desc_container = QFrame()
        desc_container.setFixedWidth(int(self.width * 0.45))
        desc_layout = QVBoxLayout(desc_container)
        desc_layout.setContentsMargins(15, 15, 15, 15)
        
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
                color: #F8F9FA;
                font-size: 15px;
                font-family: 'Inter', 'Poppins', 'Segoe UI';
                font-weight: 400;
                letter-spacing: 0.4px;
                line-height: 165%;
                background: rgba(0, 0, 0, 0.25);
                padding: 30px 35px;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            QLabel:hover {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
            }
        """)

        # Add shadow effect for depth
        desc_shadow = QGraphicsDropShadowEffect()
        desc_shadow.setBlurRadius(20)
        desc_shadow.setXOffset(0)
        desc_shadow.setYOffset(6)
        desc_shadow.setColor(QColor(0, 0, 0, 50))
        desc_text.setGraphicsEffect(desc_shadow)

        # Container for description with gradient border
        desc_container = QFrame()
        desc_container.setFixedWidth(int(self.width * 0.45))
        desc_container.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 16px;
                padding: 2px;
                border: 1px solid transparent;
                background-image: linear-gradient(
                    rgba(0, 0, 0, 0.2),
                    rgba(0, 0, 0, 0.2)
                ),
                linear-gradient(
                    135deg,
                    rgba(79, 195, 247, 0.4),
                    rgba(129, 199, 132, 0.4),
                    rgba(255, 183, 77, 0.4)
                );
                background-origin: border-box;
                background-clip: content-box, border-box;
            }
        """)
        
        desc_layout = QVBoxLayout(desc_container)
        desc_layout.setContentsMargins(15, 15, 15, 15)
        desc_layout.addWidget(desc_text)
        
        # Make text selectable but read-only
        desc_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        desc_text.setWordWrap(True)
        desc_text.setAlignment(Qt.AlignJustify)
        content_layout.addWidget(desc_container)
        
        # Features section with proper icon handling
        features_container = self.setup_feature_cards()
        content_layout.addWidget(features_container)
        
        # Final assembly
        welcome_layout.addWidget(title_container)
        welcome_layout.addLayout(content_layout)
        home_layout.addWidget(welcome_container)
        
    def init_paths(self):
        """Initialize all required paths"""
        try:
            # Base paths
            self.base_path = Path(r"C:\Users\dragon\Downloads\Soft AI Pro")
            self.asset_path = self.base_path / "assets"
            
            # Create icon directories
            icon_path = self.asset_path / "icons" / "features"
            icon_path.mkdir(parents=True, exist_ok=True)
            
            # Verify icons exist
            required_icons = ["rocket.png", "ai.png", "cloud.png"]
            for icon in required_icons:
                icon_file = icon_path / icon
                if not icon_file.exists():
                    print(f"Missing icon: {icon}")
                    print(f"Please place icon at: {icon_file}")
    
        except Exception as e:
            print(f"Error initializing paths: {e}")
            sys.exit(1)

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
                background: #000022;
                border-radius: 15px;
                margin: 5px;
            }
        """)

        copyright_frame.setFixedHeight(int(self.height * 0.15))  # Changed height to self.height
        
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
                background: #000000;
                border: 2px solid #333333;
                border-radius: 15px;
            }
        """)
        logo_frame.setFixedWidth(frame_width)
        logo_frame.setFixedHeight(int(self.height * 0.30))  # Changed height to self.height
        
        menu_frame.setStyleSheet("""
            QFrame {
                background: #000000;
                border: 2px solid #333333;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        menu_frame.setFixedWidth(frame_width)
        menu_frame.setFixedHeight(int(self.height * 0.60))  # Changed height to self.height
    
        # Create layouts for frames
        logo_layout = QVBoxLayout(logo_frame)
        menu_layout = QVBoxLayout(menu_frame)
    
        # Logo layout setup
        logo_layout.setSpacing(5)
        logo_layout.setContentsMargins(15, 10, 15, 10)
        
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
        logo_pixmap = QPixmap(str(self.logo_path))
        logo_size = int(frame_width * 0.4)
        scaled_logo = logo_pixmap.scaled(
            logo_size, logo_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        logo_label.setPixmap(scaled_logo)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)

        # Menu layout setup
        menu_layout.setSpacing(8)  # Reduced spacing between buttons
        menu_layout.setContentsMargins(10, 15, 10, 15)  # Adjusted margins

        # Create menu buttons
        for item in self.menu_items:
            btn = self.create_menu_button(item)
            menu_layout.addWidget(btn)
            if item != self.menu_items[-1]:
                menu_layout.addSpacing(5)  # Reduced spacing between buttons

        # Add frames to left panel with proper proportions
        left_panel.addWidget(logo_frame)
        left_panel.addWidget(menu_frame)
        left_panel.setStretch(0, 30)  # Logo frame takes 30%
        left_panel.setStretch(1, 60)  # Menu frame takes 60%

        # Add left panel to main layout
        main_layout.addLayout(left_panel, 0, 0)
        main_layout.setColumnStretch(0, 1)  # Left panel takes 20% of width

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
        background = QPixmap(r"C:\Users\dragon\Downloads\Soft AI Pro\assets\background.jpg")
        palette.setBrush(QPalette.Window, 
            background.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        )
        self.setPalette(palette)

        # Update main widget background to be semi-transparent
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(26, 35, 126, 0.9),
                    stop:0.4 rgba(13, 71, 161, 0.9),
                    stop:1 rgba(1, 87, 155, 0.9)
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

        def setup_frame_background(frame, opacity=0.85):
            """Setup background untuk setiap frame"""
            try:
                bg_path = self.asset_path / "background.jpg"
                if not bg_path.exists():
                    raise FileNotFoundError(f"Background not found: {bg_path}")

                frame.setAutoFillBackground(True)
                palette = frame.palette()
                bg_pixmap = QPixmap(str(bg_path))
                
                # Scale background sesuai ukuran frame
                scaled_bg = bg_pixmap.scaled(
                    frame.size(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
                
                # Set background dengan opacity
                frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: rgba(0, 0, 0, {opacity});
                        border-radius: 15px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }}
                """)
                
                palette.setBrush(QPalette.Window, scaled_bg)
                frame.setPalette(palette)
                
            except Exception as e:
                print(f"Error setting frame background: {e}")
                # Fallback style
                frame.setStyleSheet("""
                    QFrame {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #1a237e,
                            stop:0.4 #0d47a1,
                            stop:1 #01579b
                        );
                        border-radius: 15px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }
                """)

        # Apply background ke semua frame
        setup_frame_background(logo_frame, 0.8)  # Logo frame lebih transparan
        setup_frame_background(menu_frame, 0.9)   # Menu frame lebih solid
        setup_frame_background(copyright_frame, 0.85)  # Copyright frame balance

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
        """Create styled menu button"""
        btn = QPushButton()
        btn.setFixedHeight(50)  # Reduced height for better proportions
        btn.setFixedWidth(int(self.width * 0.22))  # Slightly reduced width
        
        # Create horizontal layout with better spacing
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 5, 20, 5)  # Adjusted margins
        
        # Load and set icon with consistent sizing
        icon_label = QLabel()
        icon_path = self.asset_path / item["icon"]
        if icon_path.exists():
            icon_pixmap = QPixmap(str(icon_path))
            if not icon_pixmap.isNull():
                scaled_icon = icon_pixmap.scaled(
                    24, 24,  # Smaller icon size
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                icon_label.setPixmap(scaled_icon)
                icon_label.setFixedSize(24, 24)  # Fixed icon container size
    
        layout.addWidget(icon_label)
        
        # Add text with refined styling
        text_label = QLabel(item["text"])
        text_label.setStyleSheet(f"""
            color: {item["colors"]["text"]};
            font-family: 'Segoe UI';
            font-size: 13pt;
            font-weight: 600;
            padding-left: 8px;
        """)
        layout.addWidget(text_label)
        layout.addStretch()
        
        # Enhanced button styling with gradients
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {item["colors"]["start"]},
                    stop:1 {item["colors"]["end"]}
                );
                border: none;
                border-radius: 0px;
                padding: 8px;
                margin: 3px 10px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {item["colors"]["hover"]},
                    stop:1 {item["colors"]["end"]}
                );
            }}
            QPushButton:pressed {{
                background: {item["colors"]["start"]};
                margin: 5px 12px;
            }}
        """)
        
        btn.setLayout(layout)
        btn.setCursor(Qt.PointingHandCursor)  # Add hand cursor on hover
        btn.clicked.connect(lambda: self.switch_page(item["text"]))
        
        return btn

    def switch_page(self, button_text):
        """Switch to appropriate page based on button text"""
        if button_text == "Project Baru":
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
        # Create home page
        self.home_page = QWidget()
        self.setup_home_page()
        
        # Create other pages
        self.project_page = ProjectPage()
        self.archive_page = ArchivePage()
        self.docs_page = DocsPage()
        self.cloud_page = CloudPage()
        self.settings_page = SettingsPage()
        
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
        
        # Check each icon
        missing = []
        for folder, icons in icon_paths.items():
            for icon in icons:
                path = self.asset_path / 'icons' / folder / icon
                if not path.exists():
                    missing.append(f"{folder}/{icon}")
    
        if missing:
            print("\nMissing icons:")
            for icon in missing:
                print(f"- {icon}")
            print(f"\nPlease add PNG icons to: {self.asset_path}/icons/features/")
            print("Icon specifications:")
            print("- Format: PNG with transparency")
            print("- Size: 28x28 pixels")
            print("- Color: White or light colored")

    def setup_feature_cards(self):
        """Setup feature cards with refined design"""
        features_container = QFrame()
        features_container.setFixedWidth(int(self.width * 0.3))
        features_container.setFixedHeight(int(self.height * 0.45))
        features_container.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 35, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        features_layout = QVBoxLayout(features_container)
        features_layout.setSpacing(8)  # Reduced spacing between cards
        features_layout.setContentsMargins(12, 12, 12, 12)

        feature_cards = [
            {
                "icon": "features/rocket.png",
                "title": "Cepat & Efisien",
                "desc": "Accelerated Development Process",
                "color": "#9A83FF",
                "gradient": "rgba(154, 131, 255, 0.1)"
            },
            {
                "icon": "features/ai.png",
                "title": "AI Powered", 
                "desc": "Smart Code Assistance",
                "color": "#A3FFA8",
                "gradient": "rgba(163, 255, 168, 0.1)"
            },
            {
                "icon": "features/cloud.png",
                "title": "Real-time Sync",
                "desc": "Cloud Integration & Backup",
                "color": "#7AD9FF",
                "gradient": "rgba(122, 217, 255, 0.1)"
            }
        ]

        for card in feature_cards:
            card_frame = QFrame()
            card_frame.setFixedHeight(75)  # Slightly reduced height
            card_frame.setStyleSheet(f"""
                QFrame {{
                    background: {card['gradient']};
                    border-left: 3px solid {card['color']};
                    border-top: 1px solid rgba(255, 255, 255, 0.05);
                    border-right: 1px solid rgba(255, 255, 255, 0.05);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                }}
                QFrame:hover {{
                    background: rgba(255, 255, 255, 0.08);
                    border-left: 3px solid {card['color']};
                    border-top: 1px solid {card['color']};
                    border-right: 1px solid {card['color']};
                    border-bottom: 1px solid {card['color']};
                }}
            """)
            
            card_layout = QHBoxLayout(card_frame)
            card_layout.setSpacing(12)
            card_layout.setContentsMargins(15, 8, 15, 8)

            # Icon container with refined styling
            icon_container = QFrame()
            icon_container.setFixedSize(45, 45)
            icon_container.setStyleSheet(f"""
                QFrame {{
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }}
            """)

            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(8, 8, 8, 8)
            icon_layout.setSpacing(0)

            # Icon
            icon_label = QLabel()
            icon_path = self.asset_path / "icons" / card["icon"]
            if icon_path.exists():
                icon_pixmap = QPixmap(str(icon_path))
                if not icon_pixmap.isNull():
                    scaled_icon = icon_pixmap.scaled(
                        28, 28,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    icon_label.setPixmap(scaled_icon)
                    icon_label.setAlignment(Qt.AlignCenter)

            icon_layout.addWidget(icon_label)

            # Text section with better spacing
            text_container = QVBoxLayout()
            text_container.setSpacing(4)

            title_label = QLabel(card["title"])
            title_label.setStyleSheet(f"""
                QLabel {{
                    color: {card['color']};
                    font-size: 13px;
                    font-weight: bold;
                    font-family: 'Poppins', 'Segoe UI';
                    letter-spacing: 0.3px;
                }}
            """)

            desc_label = QLabel(card["desc"])
            desc_label.setStyleSheet("""
                QLabel {
                    color: #CCCCCC;
                    font-size: 11px;
                    font-family: 'Inter', 'Segoe UI';
                    letter-spacing: 0.2px;
                }
            """)
            desc_label.setWordWrap(True)

            text_container.addWidget(title_label)
            text_container.addWidget(desc_label)

            # Layout assembly with proper spacing
            card_layout.addWidget(icon_container)
            card_layout.addLayout(text_container, stretch=1)
            
            features_layout.addWidget(card_frame)

        features_layout.addStretch()
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
        
        # Create main window
        window = SoftAICodeUI()
        
        # Check required files
        required_files = {
            "background.jpg": window.bg_path,
            "SoftAI_Logo.png": window.logo_path
        }
        
        missing_files = []
        for name, path in required_files.items():
            if not path.exists():
                missing_files.append(name)
                
        if missing_files:
            print("Missing required files:")
            for file in missing_files:
                print(f"- {file}")
            print(f"\nPlease place files in: {window.asset_path}")
            
        # Show window and start event loop
        window.show()
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)