import sys
from PySide6.QtWidgets import QApplication
from soft_ai_code import SoftAICodeUI  # Updated import name

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SoftAICodeUI()
    window.show()
    sys.exit(app.exec())