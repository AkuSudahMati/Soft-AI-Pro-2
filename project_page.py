from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton,
                            QFrame, QMessageBox)
from PySide6.QtCore import Qt, Signal
import sys
from pathlib import Path

# Add parent directory to path untuk import dari root
sys.path.insert(0, str(Path(__file__).parent.parent))

class ProjectPage(QWidget):
    wizard_requested = Signal()  # Signal untuk request membuka wizard
    
    def __init__(self):
        super().__init__()
        self.step1_dialog = None
        self.step2_dialog = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header dengan gradient modern yang menakjubkan
        header = QLabel("🚀 Buat Project Baru")
        header.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 40px;
                font-weight: bold;
                font-family: 'Poppins', 'Segoe UI';
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF6B6B,
                    stop:0.5 #4ECDC4,
                    stop:1 #45B7D1
                );
                padding: 30px 40px;
                border-radius: 20px;
                letter-spacing: 1px;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Info text dengan styling yang lebih menarik
        info = QLabel("⚙️ Ikuti langkah-langkah di bawah untuk memulai wizard pembuatan project")
        info.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.85);
                font-size: 14px;
                padding: 15px 20px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 200, 255, 0.2),
                    stop:1 rgba(100, 200, 255, 0.1)
                );
                border-left: 4px solid #4FC3F7;
                border-radius: 8px;
                font-weight: 600;
            }
        """)
        layout.addWidget(info)
        
        # Main content container dengan styling modern
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(40, 70, 150, 0.5),
                    stop:1 rgba(50, 80, 160, 0.5)
                );
                border-radius: 20px;
                border: 2px solid rgba(100, 180, 255, 0.4);
                padding: 30px;
            }
        """)
        content_layout = QVBoxLayout(content)
        
        # Instructions dengan formatting yang lebih baik
        instructions = QLabel(
            "<div style='line-height: 200%;'>"
            "<p style='margin-bottom: 20px;'><strong style='font-size: 18px; color: #FFD700;'>📋 Langkah-langkah Membuat Project Baru</strong></p>"
            
            "<p style='margin-bottom: 15px;'>"
            "<span style='color: #4FC3F7; font-weight: 700; font-size: 16px;'>Step 1:</span> "
            "<span style='color: #E0E0FF;'>Isi informasi dasar project dan pilih fitur-fitur yang ingin digunakan</span>"
            "</p>"
            
            "<p style='margin-bottom: 15px;'>"
            "<span style='color: #81C784; font-weight: 700; font-size: 16px;'>Step 2:</span> "
            "<span style='color: #E0E0FF;'>Upload minimal 10 halaman design Figma UI/UX untuk analisis</span>"
            "</p>"
            
            "<p style='margin-bottom: 15px;'>"
            "<span style='color: #FFB74D; font-weight: 700; font-size: 16px;'>Step 3:</span> "
            "<span style='color: #E0E0FF;'>Desain komponen UI menggunakan drag & drop interface</span>"
            "</p>"
            
            "<p style='margin-bottom: 20px;'>"
            "<span style='color: #9A83FF; font-weight: 700; font-size: 16px;'>Step 4:</span> "
            "<span style='color: #E0E0FF;'>Konfigurasi API dan database untuk backend project Anda</span>"
            "</p>"
            
            "<p style='text-align: center; margin-top: 25px;'>"
            "<span style='color: #FFB74D; font-weight: bold; font-size: 14px;'>✨ Klik tombol di bawah untuk memulai wizard ✨</span>"
            "</p>"
            "</div>"
        )
        instructions.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                line-height: 1.8;
                padding: 25px;
                background: rgba(30, 50, 120, 0.3);
                border-radius: 15px;
                border: 2px solid rgba(100, 180, 255, 0.2);
            }
        """)
        content_layout.addWidget(instructions)
        
        content_layout.addStretch()
        
        # Create Project Button dengan styling menakjubkan
        create_btn = QPushButton("🚀 Mulai Wizard - Buat Project Baru")
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4CAF50,
                    stop:0.5 #45a049,
                    stop:1 #388E3C
                );
                color: white;
                padding: 22px 50px;
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Poppins', 'Segoe UI';
                letter-spacing: 0.5px;
                min-width: 350px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #45a049,
                    stop:0.5 #388E3C,
                    stop:1 #2E7D32
                );
                border: 3px solid rgba(255, 255, 255, 0.5);
                padding: 21px 50px;
            }
            QPushButton:pressed {
                background: #2E7D32;
                padding: 24px 50px;
                border: 3px solid rgba(255, 255, 255, 0.2);
            }
        """)
        create_btn.clicked.connect(self.open_step1_dialog)
        
        content_layout.addWidget(create_btn, alignment=Qt.AlignCenter)
        layout.addWidget(content)
    
    def open_step1_dialog(self):
        """Membuka Step 1 Dialog untuk input informasi project"""
        try:
            from step1_dialog import Step1Dialog
            
            self.step1_dialog = Step1Dialog(parent=self)
            self.step1_dialog.project_created.connect(self.on_project_created)
            
            result = self.step1_dialog.exec()
            print(f"✅ Step 1 Dialog ditutup dengan result: {result}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuka Step 1: {str(e)}")
            print(f"❌ Error: {e}")
    
    def on_project_created(self, project_data):
        """Handler ketika project berhasil dibuat di Step 1"""
        try:
            # Setelah Step 1 selesai, buka Step 2 untuk Figma Design
            self.open_step2_dialog(project_data.get('project_id'))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saat melanjutkan: {str(e)}")
            print(f"❌ Error: {e}")
    
    def open_step2_dialog(self, project_id):
        """Membuka Step 2 Dialog untuk input Figma design pages"""
        try:
            from step2_dialog import Step2Dialog
            
            self.step2_dialog = Step2Dialog(parent=self, project_id=project_id)
            self.step2_dialog.design_completed.connect(self.on_design_completed)
            
            result = self.step2_dialog.exec()
            print(f"✅ Step 2 Dialog ditutup dengan result: {result}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuka Step 2: {str(e)}")
            print(f"❌ Error: {e}")
    
    def on_design_completed(self, design_data):
        """Handler ketika design berhasil disimpan di Step 2"""
        try:
            # Setelah desain selesai, otomatis lanjut ke Step 3 (komponen)
            project_id = design_data.get('project_id')
            self.open_step3_dialog(project_id, design_data.get('pages', []))
        except Exception as e:
            QMessageBox.information(
                self,
                "Project Dibuat",
                f"🎉 Project dengan {design_data.get('pages_count')} halaman design telah berhasil dibuat!\n\n"
                f"Project ID: {design_data.get('project_id')}\n\n"
                "Anda dapat melanjutkan ke step 3 dan 4 di halaman berikutnya."
            )

    def open_step3_dialog(self, project_id, pages=None):
        """Membuka Step 3 Dialog untuk desain komponen UI"""
        try:
            from step3_dialog import Step3Dialog

            self.step3_dialog = Step3Dialog(parent=self, project_id=project_id)
            self.step3_dialog.components_completed.connect(self.on_components_completed)

            result = self.step3_dialog.exec()
            print(f"✅ Step 3 Dialog ditutup dengan result: {result}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuka Step 3: {str(e)}")
            print(f"❌ Error: {e}")

    def on_components_completed(self, components_data):
        """Handler ketika komponen berhasil disimpan pada Step 3"""
        try:
            project_id = components_data.get('project_id')
            # Simpan komponen ke project_data
            self.project_data['components'] = components_data.get('components', [])
            # Lanjut ke Step 4
            self.open_step4_dialog(project_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saat melanjutkan: {str(e)}")
            print(f"❌ Error: {e}")

    def open_step4_dialog(self, project_id):
        """Membuka Step 4 Dialog untuk konfigurasi API & Database"""
        try:
            from step4_dialog import Step4Dialog

            self.step4_dialog = Step4Dialog(parent=self, project_id=project_id)
            self.step4_dialog.finished_setup.connect(self.on_finished_setup)

            result = self.step4_dialog.exec()
            print(f"✅ Step 4 Dialog ditutup dengan result: {result}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuka Step 4: {str(e)}")
            print(f"❌ Error: {e}")

    def on_finished_setup(self, setup_data):
        """Handler setelah Step 4 selesai - finalisasi project"""
        QMessageBox.information(
            self,
            "Wizard Selesai",
            "🎉 Setup project selesai. Anda dapat melihat detail project di daftar project."
        )


