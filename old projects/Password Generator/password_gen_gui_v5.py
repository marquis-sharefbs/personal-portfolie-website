# Create a standalone UI for the password generator
'''
Integrating SettingsPage, Update to access settings JSON file
'''
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QStackedWidget,
    QLabel
)
from PySide6.QtCore import Qt
import sys
import json
import os
from ui_saved_passwords import SavedPasswordsPage
from ui_generate_dialog_v2 import GeneratePasswordDialog
from ui_settings_page import SettingsPage
from ui_search_page import SearchPage
import vault_backend
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
        self.page_saved = SavedPasswordsPage(backend=self.backend, cipher=self.cipher)
        self.page_search = SearchPage(backend=self.backend, cipher=self.cipher)
        self.page_settings = SettingsPage()
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
            
            settings = self.load_settings()
            dialog = GeneratePasswordDialog(self.backend, self.cipher, settings, self)
            if dialog.exec():
                self.page_saved.load_passwords() # automatically refresh table
            
            return # do NOT switch pages
        
        elif index == 6: # exit
            
            self.close()
            return
        
        # switch pages normally for other items
        self.pages.setCurrentIndex(index)

    # Access json file
    def load_settings(self):
        if not os.path.exists("settings.json"):
            return {
                "default_length": 12,
                "lowercase": True,
                "uppercase": True,
                "numbers": True,
                "symbols": True
            }
        return json.load(open("settings.json"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())