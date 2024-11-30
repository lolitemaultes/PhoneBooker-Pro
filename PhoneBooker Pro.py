import sys
import xml.etree.ElementTree as ET
import csv
import re
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                            QLineEdit, QComboBox, QCheckBox, QDialog, QFormLayout,
                            QMessageBox, QLabel, QStackedWidget, QDialogButtonBox, QFileDialog,
                            QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
from thefuzz import fuzz

def parse_complex_name(name):
    # Remove any parentheses and their contents
    name = re.sub(r'\([^)]*\)', '', name)
    
    # Split the name into parts
    parts = [part.strip() for part in name.split()]
    
    # If we have multiple parts and they look like nickname + full name
    if len(parts) >= 2:
        first_part = parts[0].lower()
        second_part = parts[1].lower()
        
        # Define nickname mappings where key is nickname and value is list of possible formal names
        common_nicknames = {
            'kate': ['kathryn', 'katherine', 'kathleen'],
            'kathy': ['kathryn', 'katherine'],
            'katie': ['katherine', 'kathryn'],
            'beth': ['elizabeth'],
            'liz': ['elizabeth'],
            'lizzy': ['elizabeth'],
            'betty': ['elizabeth'],
            'meg': ['margaret'],
            'maggie': ['margaret'],
            'peggy': ['margaret'],
            'abby': ['abigail'],
            'gabby': ['gabriella'],
            'maddie': ['madeline'],
            'madi': ['madeleine'],
            'alex': ['alexandra', 'alexandria'],
            'sandy': ['sandra'],
            'becky': ['rebecca'],
            'vicky': ['victoria'],
            'val': ['valerie'],
            'sue': ['susan'],
            'susie': ['susan'],
            'tom': ['thomas'],
            'sam': ['samuel'],
            'mike': ['michael'],
            'mick': ['michael'],
            'jim': ['james'],
            'jimmy': ['james'],
            'bob': ['robert'],
            'rob': ['robert'],
            'dick': ['richard'],
            'rick': ['richard'],
            'bill': ['william'],
            'will': ['william'],
            'matt': ['matthew'],
            'chris': ['christopher'],
            'tony': ['anthony'],
            'don': ['donald'],
            'ed': ['edward'],
            'ted': ['edward'],
            'joe': ['joseph'],
            'pete': ['peter'],
            'dan': ['daniel'],
            'danny': ['daniel'],
            'nick': ['nicholas'],
            'dave': ['david'],
            'steve': ['stephen', 'steven'],
            'andy': ['andrew'],
            'drew': ['andrew'],
            'fred': ['frederick'],
            'ben': ['benjamin'],
            'charlie': ['charles'],
            'chuck': ['charles'],
        }
        
        # Check if first part is a nickname and second part is its formal name
        should_remove_first = (
            (first_part in common_nicknames and second_part in common_nicknames[first_part]) or
            (len(first_part) >= 2 and first_part in second_part)
        )
        
        if should_remove_first:
            parts = parts[1:]
    
    # Capitalize each part
    parts = [part.capitalize() for part in parts]
    
    # Determine first and last name
    if len(parts) > 2:
        # If there are more than two parts, assume the last part is the last name
        first_name = ' '.join(parts[:-1])
        last_name = parts[-1]
    elif len(parts) == 2:
        # If there are two parts, assume first part is first name and second part is last name
        first_name, last_name = parts
    elif len(parts) == 1:
        first_name = parts[0]
        last_name = ""
    else:
        first_name = ""
        last_name = ""
    
    return first_name.strip(), last_name.strip()

def get_phone_type(phone_number):
    if phone_number.startswith("61"):
        return "Home"
    elif phone_number.startswith("2"):
        return "Home"
    else:
        return "Mobile"

def format_phone_number(phone_number):
    if phone_number.startswith("61"):
        return phone_number[2:]
    elif phone_number.startswith("2"):
        return phone_number[1:]
    else:
        return phone_number

class ThemeManager:
    """Enhanced theme management for modern, sleek styling"""
    
    @staticmethod
    def get_theme(is_dark_mode=False):
        if is_dark_mode:
            return {
                'bg_color': "#1e1e1e",
                'text_color': "#ffffff",
                'accent_color': "#782FD4",      # Purple from logo
                'secondary_color': "#9ED42F",    # Lime from logo
                'hover_color': "#9E2FD4",       # Lighter purple
                'active_color': "#561FBA",      # Darker purple
                'secondary_bg': "#2d2d2d",
                'border_color': "#404040",
                'success_color': "#43A047",
                'error_color': "#D32F2F",
                'warning_color': "#F57C00",
                'disabled_color': "#9e9e9e",
                'white': "#ffffff",
                'light_gray': "#f5f5f5",
                'medium_gray': "#757575",
                'dark_gray': "#212529"
            }
        else:
            return {
                'bg_color': "#f5f5f5",
                'text_color': "#212529",
                'accent_color': "#782FD4",      # Purple from logo
                'secondary_color': "#9ED42F",    # Lime from logo
                'hover_color': "#9E2FD4",       # Lighter purple
                'active_color': "#561FBA",      # Darker purple
                'secondary_bg': "#ffffff",
                'border_color': "#dcdcdc",
                'success_color': "#66BB6A",
                'error_color': "#EF5350",
                'warning_color': "#FFA726",
                'disabled_color': "#757575",
                'white': "#ffffff",
                'light_gray': "#f5f5f5",
                'medium_gray': "#757575",
                'dark_gray': "#212529"
            }

    @staticmethod
    def get_stylesheet(colors):
        return f"""
            /* Main Window */
            QMainWindow, QDialog {{
                background-color: {colors['bg_color']};
                color: {colors['text_color']};
            }}
            
            /* Labels */
            QLabel {{
                color: {colors['text_color']};
                font-size: 14px;
            }}
            
            QLabel[heading="true"] {{
                font-size: 24px;
                font-weight: bold;
                color: {colors['accent_color']};
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {colors['accent_color']};
                color: {colors['white']};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }}
            
            QPushButton:hover {{
                background-color: {colors['hover_color']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['active_color']};
                padding: 11px 19px 9px 21px;
            }}
            
            QPushButton:disabled {{
                background-color: {colors['disabled_color']};
                color: {colors['light_gray']};
            }}
            
            QPushButton.secondary {{
                background-color: transparent;
                color: {colors['accent_color']};
                border: 2px solid {colors['accent_color']};
            }}
            
            QPushButton.secondary:hover {{
                background-color: {colors['accent_color']};
                color: {colors['white']};
            }}
            
            /* Table Widget */
            QTableWidget {{
                background-color: {colors['secondary_bg']};
                border: 1px solid {colors['border_color']};
                border-radius: 10px;
                padding: 5px;
                gridline-color: {colors['border_color']};
            }}
            
            QTableWidget::item {{
                padding: 8px;
                border-radius: 4px;
            }}
            
            QTableWidget::item:selected {{
                background-color: {colors['accent_color']};
                color: {colors['white']};
            }}
            
            QHeaderView::section {{
                background-color: {colors['accent_color']};
                color: {colors['white']};
                padding: 12px;
                border: none;
                font-weight: bold;
            }}
            
            /* Input Fields */
            QLineEdit {{
                background-color: {colors['secondary_bg']};
                border: 2px solid {colors['border_color']};
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: {colors['accent_color']};
                color: {colors['text_color']};
            }}
            
            QLineEdit:focus {{
                border-color: {colors['accent_color']};
            }}
            
            /* Combo Box */
            QComboBox {{
                background-color: {colors['secondary_bg']};
                border: 2px solid {colors['border_color']};
                border-radius: 8px;
                padding: 10px;
                min-width: 150px;
                color: {colors['text_color']};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {colors['secondary_bg']};
                border: 2px solid {colors['border_color']};
                border-radius: 8px;
                selection-background-color: {colors['accent_color']};
                color: {colors['text_color']};
            }}
            
            /* Checkboxes */
            QCheckBox {{
                spacing: 8px;
                color: {colors['text_color']};
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {colors['border_color']};
                border-radius: 4px;
                background-color: {colors['secondary_bg']};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {colors['accent_color']};
                border-color: {colors['accent_color']};
            }}
            
            /* Scroll Bars */
            QScrollBar:vertical {{
                background-color: {colors['secondary_bg']};
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {colors['accent_color']};
                min-height: 30px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {colors['hover_color']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            /* Modern Button specific styling */
            QPushButton[class="ModernButton"] {{
                background-color: {colors['accent_color']};
                color: {colors['white']};
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
                min-height: 50px;
            }}
            
            QPushButton[class="ModernButton"]:hover {{
                background-color: {colors['hover_color']};
            }}
        """
        
class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(250, 60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Arial", 12, QFont.Weight.Bold))

class Contact:
    def __init__(self, first_name, last_name, phone_type, phone_number, groups, company=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_type = phone_type
        self.phone_number = phone_number
        self.groups = groups
        self.company = company

    @classmethod
    def from_csv_row(cls, name, phone_number):
        first_name, last_name = parse_complex_name(name)
        phone_type = get_phone_type(phone_number)
        phone_number = format_phone_number(phone_number)
        return cls(first_name, last_name, phone_type, phone_number, ["Work"], "")

class ContactDialog(QDialog):
    def __init__(self, groups, phone_types, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contact Details")
        self.groups = groups
        self.phone_types = phone_types
        self.setup_ui()
        
        # Apply theme
        app = QApplication.instance()
        is_dark = app.palette().color(QPalette.ColorRole.Window).lightness() < 128
        colors = ThemeManager.get_theme(is_dark)
        self.setStyleSheet(ThemeManager.get_stylesheet(colors))

    def setup_ui(self):
        layout = QFormLayout(self)
        
        self.first_name = QLineEdit(self)
        self.last_name = QLineEdit(self)
        self.phone_type = QComboBox(self)
        self.phone_type.addItems(self.phone_types)
        self.phone_number = QLineEdit(self)
        self.company = QLineEdit(self)
        
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Phone Type:", self.phone_type)
        layout.addRow("Phone Number:", self.phone_number)
        layout.addRow("Company:", self.company)
        
        self.group_checkboxes = []
        group_layout = QVBoxLayout()
        for group in self.groups:
            checkbox = QCheckBox(group)
            self.group_checkboxes.append(checkbox)
            group_layout.addWidget(checkbox)
        
        layout.addRow("Groups:", group_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 2px solid #c0c0c0;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox {
                spacing: 5px;
            }
            QPushButton {
                padding: 5px 15px;
                background-color: #f0f0f0;
                border: 2px solid #c0c0c0;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

    def get_contact(self):
        groups = [cb.text() for cb in self.group_checkboxes if cb.isChecked()]
        return Contact(
            self.first_name.text(),
            self.last_name.text(),
            self.phone_type.currentText(),
            self.phone_number.text(),
            groups,
            self.company.text()
        )

class PhonebookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle("PhoneBooker Pro")
        self.setGeometry(100, 100, 1000, 800)
        
        # Initialize core attributes
        self.contacts = []
        self.groups = ["Blocklist", "Allowlist", "Work", "Friends", "Family", "Blacklist", "Whitelist"]
        self.phone_types = ["Home", "Work", "Mobile"]
        
        # Detect system theme
        self.is_dark_mode = self.is_system_dark_mode()
        self.colors = ThemeManager.get_theme(self.is_dark_mode)
        self.setStyleSheet(ThemeManager.get_stylesheet(self.colors))
        
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.setup_startup_menu()
        self.setup_edit_view()
        self.setup_convert_view()
        
        # Handle initial file
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            self.show_edit_view()
            self.load_phonebook(sys.argv[1])

    def is_system_dark_mode(self):
        app = QApplication.instance()
        return app.palette().color(QPalette.ColorRole.Window).lightness() < 128

    def apply_theme(self):
        if self.is_dark_mode:
            # Dark mode colors
            bg_color = "#1e1e1e"
            text_color = "#9ED42F"
            accent_color = "#782FD4"
            secondary_bg = "#2d2d2d"
            border_color = "#404040"
            hover_color = "#9ED42F"
        else:
            # Light mode colors
            bg_color = "#f5f5f5"
            text_color = "#782FD4"
            accent_color = "#2c3e50"
            secondary_bg = "#ffffff"
            border_color = "#dcdcdc"
            hover_color = "#34495e"

        # Apply the theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QLabel {{
                color: {text_color};
            }}
            
            QTableWidget {{
                background-color: {secondary_bg};
                border: 1px solid {border_color};
                border-radius: 8px;
                gridline-color: {border_color};
                color: {text_color};
            }}
            
            QTableWidget::item {{
                padding: 5px;
            }}
            
            QHeaderView::section {{
                background-color: {accent_color};
                color: white;
                padding: 8px;
                border: none;
            }}
            
            QLineEdit {{
                padding: 8px;
                border: 2px solid {border_color};
                border-radius: 6px;
                background-color: {secondary_bg};
                color: {text_color};
            }}
            
            QComboBox {{
                padding: 8px;
                border: 2px solid {border_color};
                border-radius: 6px;
                background-color: {secondary_bg};
                color: {text_color};
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {secondary_bg};
                color: {text_color};
                selection-background-color: {accent_color};
                selection-color: white;
            }}
            
            QCheckBox {{
                spacing: 8px;
                color: {text_color};
            }}
            
            QPushButton.ModernButton {{
                background-color: {accent_color};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }}
            
            QPushButton.ModernButton:hover {{
                background-color: {hover_color};
            }}
            
            QPushButton.ModernButton:pressed {{
                background-color: {accent_color};
            }}
            
            QDialog {{
                background-color: {bg_color};
                color: {text_color};
            }}
        """)

    def setup_startup_menu(self):
        startup_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Logo handling with multiple fallback paths
        logo_label = QLabel()
        logo_paths = [
            'logo.png',  # Current directory
            '/resources/logo.png',  # Resources directory
            os.path.join(os.path.dirname(__file__), 'logo.png'),  # Script directory
            os.path.join(os.path.dirname(__file__), 'resources', 'logo.png'),  # Script's resources directory
            os.path.join(sys._MEIPASS, 'logo.png') if hasattr(sys, '_MEIPASS') else None,  # PyInstaller bundle
        ]
        
        logo_loaded = False
        for path in logo_paths:
            if path and os.path.isfile(path):
                try:
                    logo_pixmap = QPixmap(path)
                    if not logo_pixmap.isNull():
                        # Successfully loaded the logo
                        scaled_pixmap = logo_pixmap.scaled(
                            800, 400, 
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        logo_label.setPixmap(scaled_pixmap)
                        logo_loaded = True
                        break
                except Exception as e:
                    print(f"Failed to load logo from {path}: {str(e)}")
        
        if not logo_loaded:
            # Fallback to text-based logo
            app_name = QLabel("PhoneBooker Pro")
            app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            app_name.setStyleSheet("""
                QLabel {
                    font-size: 48px;
                    font-weight: bold;
                    color: #782FD4;
                    padding: 40px;
                }
            """)
            layout.addWidget(app_name)
        else:
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        # Create buttons and set their class for styling
        edit_button = ModernButton("Edit Phonebook")
        convert_button = ModernButton("Convert Phonebook")
        quit_button = ModernButton("Quit")
        
        for button in [edit_button, convert_button, quit_button]:
            button.setProperty("class", "ModernButton")
        
        edit_button.clicked.connect(self.show_edit_view)
        convert_button.clicked.connect(self.show_convert_view)
        quit_button.clicked.connect(self.close)
        
        button_layout.addWidget(edit_button)
        button_layout.addWidget(convert_button)
        button_container.setLayout(button_layout)
        
        layout.addWidget(button_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(quit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        startup_widget.setLayout(layout)
        self.central_widget.addWidget(startup_widget)

    def setup_edit_view(self):
        edit_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Search Section with Title
        search_section = QWidget()
        search_layout = QVBoxLayout(search_section)
        search_layout.setSpacing(15)
        
        # Title for the section
        title_label = QLabel("Search Contacts")
        title_label.setProperty("heading", True)
        search_layout.addWidget(title_label)
        
        # Search controls container
        search_controls = QWidget()
        search_controls_layout = QHBoxLayout(search_controls)
        search_controls_layout.setSpacing(10)
        
        # Enhanced search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search contacts...")
        self.search_bar.setMinimumHeight(40)
        self.search_bar.textChanged.connect(self.filter_contacts)
        
        # Enhanced search type dropdown
        self.search_type = QComboBox()
        self.search_type.addItems(["All Fields", "Name Only", "Phone Only", "Company Only", "Groups Only"])
        self.search_type.setMinimumHeight(40)
        self.search_type.currentTextChanged.connect(self.filter_contacts)
        
        # Add search controls to their layout
        search_controls_layout.addWidget(self.search_bar, stretch=4)
        search_controls_layout.addWidget(self.search_type, stretch=1)
        
        search_layout.addWidget(search_controls)
        
        # Advanced search options in a separate container
        advanced_options = QWidget()
        advanced_layout = QHBoxLayout(advanced_options)
        advanced_layout.setSpacing(20)
        
        self.case_sensitive = QCheckBox("Case Sensitive")
        self.exact_match = QCheckBox("Exact Match")
        self.case_sensitive.stateChanged.connect(self.filter_contacts)
        self.exact_match.stateChanged.connect(self.filter_contacts)
        
        advanced_layout.addWidget(self.case_sensitive)
        advanced_layout.addWidget(self.exact_match)
        advanced_layout.addStretch()
        
        search_layout.addWidget(advanced_options)
        
        # Add complete search section to main layout
        main_layout.addWidget(search_section)
        
        # Contacts Table Section
        table_section = QWidget()
        table_layout = QVBoxLayout(table_section)
        table_layout.setSpacing(15)
        
        # Title for the table section
        contacts_title = QLabel("Contact List")
        contacts_title.setProperty("heading", True)
        table_layout.addWidget(contacts_title)
        
        # Enhanced table widget
        self.contacts_table = QTableWidget()
        self.contacts_table.setColumnCount(6)
        self.contacts_table.setHorizontalHeaderLabels([
            "First Name", "Last Name", "Phone Type", 
            "Phone Number", "Groups", "Company"
        ])
        
        # Set table properties
        self.contacts_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.contacts_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.contacts_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.contacts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.contacts_table.setAlternatingRowColors(True)
        self.contacts_table.verticalHeader().setVisible(False)
        self.contacts_table.setShowGrid(True)
        self.contacts_table.itemDoubleClicked.connect(self.edit_contact)
        
        table_layout.addWidget(self.contacts_table)
        
        # Add table section to main layout
        main_layout.addWidget(table_section)
        
        # Action Buttons Section
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(10)
        
        # Create action buttons
        buttons = [
            ("Add Contact", self.add_contact),
            ("Delete Contact", self.delete_contact),
            ("Save", self.save_phonebook),
            ("Load", lambda: self.load_phonebook()),
            ("Import CSV", self.import_csv),
            ("Back to Menu", self.show_startup_menu)
        ]
        
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setMinimumWidth(120)
            btn.setMinimumHeight(40)
            btn.clicked.connect(callback)
            button_layout.addWidget(btn)
        
        # Add button container to main layout
        main_layout.addWidget(button_container)
        
        edit_widget.setLayout(main_layout)
        self.central_widget.addWidget(edit_widget)

    def setup_convert_view(self):
        convert_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Fix the title styling to match theme
        title_label = QLabel("Convert Phonebook")
        title_label.setProperty("heading", True)  # This will use our themed heading style
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Conversion buttons
        xml_to_vcf_button = ModernButton("Convert XML to VCF")
        vcf_to_xml_button = ModernButton("Convert VCF to XML")
        back_button = ModernButton("Back to Menu")
        
        xml_to_vcf_button.clicked.connect(lambda: self.convert_phonebook("xml", "vcf"))
        vcf_to_xml_button.clicked.connect(lambda: self.convert_phonebook("vcf", "xml"))
        back_button.clicked.connect(self.show_startup_menu)
        
        layout.addWidget(xml_to_vcf_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(vcf_to_xml_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)  # Add some extra space before the back button
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        convert_widget.setLayout(layout)
        self.central_widget.addWidget(convert_widget)

    def show_startup_menu(self):
        self.central_widget.setCurrentIndex(0)

    def show_edit_view(self):
        self.central_widget.setCurrentIndex(1)

    def show_convert_view(self):
        self.central_widget.setCurrentIndex(2)

    def add_contact(self):
        dialog = ContactDialog(self.groups, self.phone_types, self)
        if dialog.exec():
            new_contact = dialog.get_contact()
            self.contacts.append(new_contact)
            self.refresh_contacts_table()

    def edit_contact(self, item):
        row = item.row()
        contact = self.contacts[row]
        dialog = ContactDialog(self.groups, self.phone_types, self)
        dialog.first_name.setText(contact.first_name)
        dialog.last_name.setText(contact.last_name)
        dialog.phone_type.setCurrentText(contact.phone_type)
        dialog.phone_number.setText(contact.phone_number)
        dialog.company.setText(contact.company)
        for cb in dialog.group_checkboxes:
            cb.setChecked(cb.text() in contact.groups)
        
        if dialog.exec():
            updated_contact = dialog.get_contact()
            self.contacts[row] = updated_contact
            self.refresh_contacts_table()

    def delete_contact(self):
        current_row = self.contacts_table.currentRow()
        if current_row > -1:
            del self.contacts[current_row]
            self.refresh_contacts_table()

    def filter_contacts(self):
        search_text = self.search_bar.text()
        search_type = self.search_type.currentText()
        case_sensitive = self.case_sensitive.isChecked()
        exact_match = self.exact_match.isChecked()
        
        if not case_sensitive:
            search_text = search_text.lower()
        
        # Minimum similarity ratio for fuzzy matching
        SIMILARITY_THRESHOLD = 75  # Adjust this value to make matching more/less strict
        
        for row in range(self.contacts_table.rowCount()):
            show = False
            
            if search_type == "All Fields":
                fields_to_search = range(self.contacts_table.columnCount())
            elif search_type == "Name Only":
                fields_to_search = [0, 1]  # First Name and Last Name columns
            elif search_type == "Phone Only":
                fields_to_search = [3]  # Phone Number column
            elif search_type == "Company Only":
                fields_to_search = [5]  # Company column
            elif search_type == "Groups Only":
                fields_to_search = [4]  # Groups column
            
            # Special handling for name search with fuzzy matching
            if search_type == "Name Only":
                full_name = f"{self.contacts_table.item(row, 0).text()} {self.contacts_table.item(row, 1).text()}"
                if not case_sensitive:
                    full_name = full_name.lower()
                
                if exact_match:
                    show = full_name == search_text
                else:
                    # Use token_set_ratio for better partial matching
                    ratio = fuzz.token_set_ratio(search_text, full_name)
                    show = ratio >= SIMILARITY_THRESHOLD
            else:
                for col in fields_to_search:
                    item = self.contacts_table.item(row, col)
                    if item:
                        text = item.text()
                        if not case_sensitive:
                            text = text.lower()
                        
                        if exact_match:
                            if text == search_text:
                                show = True
                                break
                        else:
                            # Use different fuzzy matching strategies depending on field type
                            if col == 3:  # Phone number
                                # For phone numbers, use simpler partial matching
                                show = search_text in text
                            else:
                                # For other fields, use token_set_ratio
                                ratio = fuzz.token_set_ratio(search_text, text)
                                if ratio >= SIMILARITY_THRESHOLD:
                                    show = True
                                    break
            
            self.contacts_table.setRowHidden(row, not show)

    def refresh_contacts_table(self):
        self.contacts.sort(key=lambda x: (x.last_name.lower() if x.last_name else '', x.first_name.lower() if x.first_name else ''))
        self.contacts_table.setRowCount(0)
        for contact in self.contacts:
            row_position = self.contacts_table.rowCount()
            self.contacts_table.insertRow(row_position)
            self.contacts_table.setItem(row_position, 0, QTableWidgetItem(contact.first_name))
            self.contacts_table.setItem(row_position, 1, QTableWidgetItem(contact.last_name))
            self.contacts_table.setItem(row_position, 2, QTableWidgetItem(contact.phone_type))
            self.contacts_table.setItem(row_position, 3, QTableWidgetItem(contact.phone_number))
            self.contacts_table.setItem(row_position, 4, QTableWidgetItem(", ".join(contact.groups)))
            self.contacts_table.setItem(row_position, 5, QTableWidgetItem(contact.company))

    def save_phonebook(self):
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "Save Phonebook", "", 
            "XML Files (*.xml);;VCF Files (*.vcf)"
        )
        if filename:
            try:
                print(f"Attempting to save to: {filename}")  # Debug print
                print(f"Number of contacts to save: {len(self.contacts)}")  # Debug print
                
                if not filename.endswith(('.xml', '.vcf')):
                    if selected_filter == "XML Files (*.xml)":
                        filename += '.xml'
                    else:
                        filename += '.vcf'
                
                if filename.endswith('.xml'):
                    print("Saving as XML")  # Debug print
                    self.save_as_xml(filename)
                elif filename.endswith('.vcf'):
                    print("Saving as VCF")  # Debug print
                    self.save_as_vcf(filename)
                
                # Verify file was created
                if os.path.exists(filename):
                    print(f"File successfully created at: {filename}")  # Debug print
                    QMessageBox.information(self, "Success", f"Phonebook saved successfully to:\n{filename}")
                else:
                    print(f"File was not created at: {filename}")  # Debug print
                    raise Exception("File was not created")
                    
            except Exception as e:
                print(f"Error during save: {str(e)}")  # Debug print
                QMessageBox.critical(self, "Error", f"Error saving phonebook:\n{str(e)}\nAttempted to save to: {filename}")

    def save_as_xml(self, filename):
        try:
            root = ET.Element("AddressBook")
            
            # Save groups
            for i, group in enumerate(self.groups, start=4):
                pbgroup = ET.SubElement(root, "pbgroup")
                ET.SubElement(pbgroup, "id").text = str(i)
                ET.SubElement(pbgroup, "name").text = group
            
            # Save contacts
            for contact in self.contacts:
                contact_elem = ET.SubElement(root, "Contact")
                ET.SubElement(contact_elem, "FirstName").text = contact.first_name
                ET.SubElement(contact_elem, "LastName").text = contact.last_name
                
                phone = ET.SubElement(contact_elem, "Phone")
                phone.set("type", contact.phone_type)
                ET.SubElement(phone, "phonenumber").text = contact.phone_number
                
                for group in contact.groups:
                    group_id = str(self.groups.index(group) + 4)
                    ET.SubElement(contact_elem, "Group").text = group_id
                
                ET.SubElement(contact_elem, "Company").text = contact.company
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Write the file with explicit open
            with open(filename, 'wb') as f:
                tree = ET.ElementTree(root)
                tree.write(f, encoding="UTF-8", xml_declaration=True)
            
            print(f"XML file written to: {filename}")  # Debug print
            
        except Exception as e:
            print(f"Error in save_as_xml: {str(e)}")  # Debug print
            raise

    def save_as_vcf(self, filename):
        with open(filename, 'w', encoding='utf-8') as vcf_file:
            for contact in self.contacts:
                vcf_file.write("BEGIN:VCARD\n")
                vcf_file.write("VERSION:3.0\n")
                vcf_file.write(f"N:{contact.last_name};{contact.first_name};;;\n")
                vcf_file.write(f"FN:{contact.first_name} {contact.last_name}\n")
                vcf_file.write(f"TEL;TYPE={contact.phone_type}:{contact.phone_number}\n")
                if contact.company:
                    vcf_file.write(f"ORG:{contact.company}\n")
                if contact.groups:
                    vcf_file.write(f"CATEGORIES:{','.join(contact.groups)}\n")
                vcf_file.write("END:VCARD\n\n")

    def load_phonebook(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Load Phonebook", "", "XML Files (*.xml)")
        if filename:
            try:
                tree = ET.parse(filename)
                root = tree.getroot()
                
                self.contacts = []
                
                for contact_elem in root.findall("Contact"):
                    first_name = contact_elem.find("FirstName").text if contact_elem.find("FirstName") is not None else ""
                    last_name = contact_elem.find("LastName").text if contact_elem.find("LastName") is not None else ""
                    
                    phone = contact_elem.find("Phone")
                    phone_type = phone.get("type") if phone is not None else "Mobile"
                    phone_number = phone.find("phonenumber").text if phone is not None and phone.find("phonenumber") is not None else ""
                    
                    groups = []
                    for group_elem in contact_elem.findall("Group"):
                        group_id = int(group_elem.text)
                        if 4 <= group_id < len(self.groups) + 4:
                            groups.append(self.groups[group_id - 4])
                    
                    company = contact_elem.find("Company").text if contact_elem.find("Company") is not None else ""
                    
                    contact = Contact(first_name, last_name, phone_type, phone_number, groups, company)
                    self.contacts.append(contact)
                
                self.refresh_contacts_table()
                QMessageBox.information(self, "Success", "Phonebook loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading phonebook: {str(e)}")

    def is_duplicate_contact(self, phone_number):
        """Check if a contact with the given phone number already exists."""
        formatted_number = format_phone_number(phone_number)
        return any(contact.phone_number == formatted_number for contact in self.contacts)

    def import_csv(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Import CSV File", "", "CSV Files (*.csv)")
        if filename:
            try:
                duplicates_count = 0
                added_count = 0
                
                with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    next(csv_reader)  # Skip the header row
                    for row in csv_reader:
                        if len(row) >= 4:  # Ensure the row has at least 4 columns
                            name = row[3]  # Column D (index 3) contains the name
                            phone_number = row[2]  # Column C (index 2) contains the phone number
                            
                            # Check for duplicate before adding
                            if not self.is_duplicate_contact(phone_number):
                                new_contact = Contact.from_csv_row(name, phone_number)
                                self.contacts.append(new_contact)
                                added_count += 1
                            else:
                                duplicates_count += 1
                
                self.refresh_contacts_table()
                
                # Show summary message
                message = f"CSV import completed:\n\n" \
                         f"• {added_count} contacts added\n" \
                         f"• {duplicates_count} duplicates skipped"
                QMessageBox.information(self, "Import Summary", message)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred during CSV import: {str(e)}")

    def convert_phonebook(self, source_format, target_format):
        input_filename, _ = QFileDialog.getOpenFileName(
            self, f"Select {source_format.upper()} File", "", 
            f"{source_format.upper()} Files (*.{source_format})"
        )
        if not input_filename:
            return

        output_filename, _ = QFileDialog.getSaveFileName(
            self, f"Save {target_format.upper()} File", "", 
            f"{target_format.upper()} Files (*.{target_format})"
        )
        if not output_filename:
            return

        try:
            if source_format == "xml" and target_format == "vcf":
                self.convert_xml_to_vcf(input_filename, output_filename)
            elif source_format == "vcf" and target_format == "xml":
                self.convert_vcf_to_xml(input_filename, output_filename)
            
            QMessageBox.information(self, "Success", 
                f"Phonebook converted from {source_format.upper()} to {target_format.upper()} successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during conversion: {str(e)}")

    def convert_xml_to_vcf(self):
        input_filename, _ = QFileDialog.getOpenFileName(self, "Select XML File", "", "XML Files (*.xml)")
        if not input_filename:
            return

        output_filename, _ = QFileDialog.getSaveFileName(self, "Save VCF File", "", "VCF Files (*.vcf)")
        if not output_filename:
            return

        try:
            tree = ET.parse(input_filename)
            root = tree.getroot()

            with open(output_filename, 'w', encoding='utf-8') as vcf_file:
                for contact in root.findall("Contact"):
                    vcf_file.write("BEGIN:VCARD\n")
                    vcf_file.write("VERSION:3.0\n")
                
                    first_name = contact.find("FirstName").text if contact.find("FirstName") is not None else ""
                    last_name = contact.find("LastName").text if contact.find("LastName") is not None else ""
                    vcf_file.write(f"N:{last_name};{first_name};;;\n")
                    vcf_file.write(f"FN:{first_name} {last_name}\n")
                
                    phone = contact.find("Phone")
                    if phone is not None:
                        phone_type = phone.get("type", "").upper()
                        phone_number = phone.find("phonenumber").text if phone.find("phonenumber") is not None else ""
                        vcf_file.write(f"TEL;TYPE={phone_type}:{phone_number}\n")
                
                    company = contact.find("Company")
                    if company is not None and company.text:
                        vcf_file.write(f"ORG:{company.text}\n")
                
                    for group in contact.findall("Group"):
                        group_id = int(group.text)
                        if 4 <= group_id < len(self.groups) + 4:
                            vcf_file.write(f"CATEGORIES:{self.groups[group_id - 4]}\n")
                
                    vcf_file.write("END:VCARD\n\n")

            QMessageBox.information(self, "Success", "Phonebook converted to VCF successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during conversion: {str(e)}")
            
    def convert_vcf_to_xml(self, input_file, output_file):
        root = ET.Element("AddressBook")
        current_contact = None
        
        with open(input_file, 'r', encoding='utf-8') as vcf:
            for line in vcf:
                line = line.strip()
                if line == "BEGIN:VCARD":
                    current_contact = ET.SubElement(root, "Contact")
                elif line == "END:VCARD":
                    current_contact = None
                elif current_contact is not None:
                    if line.startswith("N:"):
                        parts = line[2:].split(';')
                        if len(parts) >= 2:
                            ET.SubElement(current_contact, "LastName").text = parts[0]
                            ET.SubElement(current_contact, "FirstName").text = parts[1]
                    elif line.startswith("TEL;"):
                        phone = ET.SubElement(current_contact, "Phone")
                        if "TYPE=" in line:
                            phone_type = line.split("TYPE=")[1].split(':')[0]
                            phone.set("type", phone_type)
                        phone_number = line.split(":")[-1]
                        ET.SubElement(phone, "phonenumber").text = phone_number
                    elif line.startswith("ORG:"):
                        ET.SubElement(current_contact, "Company").text = line[4:]
                    elif line.startswith("CATEGORIES:"):
                        group_name = line[11:]
                        if group_name in self.groups:
                            group_id = str(self.groups.index(group_name) + 4)
                            ET.SubElement(current_contact, "Group").text = group_id

        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="UTF-8", xml_declaration=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhonebookApp()
    window.show()
    sys.exit(app.exec())
