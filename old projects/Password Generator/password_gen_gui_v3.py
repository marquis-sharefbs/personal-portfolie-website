# Create a standalone UI for the password generator
'''
Integrating GeneratePasswordDialog
'''
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QStackedWidget,
    QLabel
)
from PySide6.QtCore import Qt
import sys
from ui_saved_passwords import SavedPasswordsPage
from ui_generate_dialog import GeneratePasswordDialog
import vault_backend
from vault_backend import load_all_passwords
from vault_backend import load_or_create_key


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.backend = vault_backend
        self.cipher = load_or_create_key()
        
        self.setWindowTitle("Password Manager")
        self.setMinimumSize(900, 600)

        # Main Container
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItem("Generate Password")
        self.sidebar.addItem("Saved Passwords")
        self.sidebar.addItem("Search")
        self.sidebar.addItem("Settings")
        self.sidebar.addItem("Import")
        self.sidebar.addItem("Export")
        self.sidebar.addItem("Exit")
        self.sidebar.currentRowChanged.connect(self.switch_page)

        # Stacked pages
        self.pages = QStackedWidget()

        # Placeholder pages to be replaced
        self.page_generate = QWidget()
        self.page_saved = SavedPasswordsPage(backend=vault_backend, cipher=self.cipher)
        self.page_search = QLabel("Search Page")
        self.page_settings = QLabel("Settings Page")
        self.page_import = QLabel("Import Page")
        self.page_export = QLabel("Export Page")

        self.pages.addWidget(self.page_generate)
        self.pages.addWidget(self.page_saved)
        self.pages.addWidget(self.page_search)
        self.pages.addWidget(self.page_settings)
        self.pages.addWidget(self.page_import)
        self.pages.addWidget(self.page_export)

        # Add sidebar + pages to layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        self.setCentralWidget(main_widget)
    
    def switch_page(self, index):
        if index == 0: # generate password
            dialog = GeneratePasswordDialog(self.backend, self.cipher, self)
            if dialog.exec():
                self.page_saved.load_passwords() # automatically refresh table
            return # do NOT switch pages
        elif index == 6: # exit
            self.close()
            return
        # switch pages normally for other items
        self.pages.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())