![logo](https://github.com/user-attachments/assets/41ca9d19-638d-458d-aaf0-55850c06ac52)


**PhoneBooker Pro** is a modern and user-friendly phonebook management application designed to help you organize, edit, and convert your contact lists effortlessly. Built using Python and PyQt6, this application offers sleek styling, intuitive controls, and powerful features for seamless contact management.

## Features

- **Contact Management:**
  - Add, edit, and delete contacts with ease.
  - Group contacts into categories like Work, Friends, Family, etc.
  - Search and filter contacts with advanced options, including fuzzy matching.

- **File Formats:**
  - Import and export contacts in XML and VCF formats.
  - Convert phonebooks between XML and VCF formats.

- **Modern Interface:**
  - Clean, responsive UI with support for dark and light themes.
  - Customizable styling for buttons, tables, and inputs.

- **Advanced Tools:**
  - Case-sensitive and exact match search options.
  - CSV import with duplicate detection.
  - Alphabetical sorting of contacts by name.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8+
- Required Python packages:

  ```bash
  pip install PyQt6 thefuzz
  ```

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/lolitemaultes/PhoneBooker-Pro.git
   cd PhoneBooker-pro
   ```

2. Run the application:

   ```bash
   python "PhoneBooker Pro.py"
   ```

### Running as an Executable

To create an executable for distribution, use PyInstaller:
```bash
pyinstaller --onefile --windowed "PhoneBooker Pro.py"
```

The generated executable will be available in the `dist` folder.

## Usage

### Starting the Application
On launch, the app displays a startup menu:
- **Edit Phonebook:** Manage your contacts in an interactive table view.
- **Convert Phonebook:** Convert XML to VCF or vice versa.

### Contact Operations
- Double-click a contact to edit it.
- Use the action buttons to add, delete, or save contacts.

### File Operations
- Import contacts from a CSV file or load an XML file.
- Export your phonebook as an XML or VCF file.

## Screenshots

![Screenshot from 2024-11-30 16-16-43](https://github.com/user-attachments/assets/1a7efede-c8c8-44fb-8244-662ddfdf524c)
![Screenshot from 2024-11-30 16-17-33](https://github.com/user-attachments/assets/a8feb997-dbe9-4342-ac7a-f6dedcdef594)
![Screenshot from 2024-11-30 16-17-09](https://github.com/user-attachments/assets/6507d2ad-3764-4c1b-97af-5279a7c7b195)

## Roadmap

Planned features:
- Additional export formats.
- Integration with cloud-based contact storage.
- Real-time syncing with mobile devices.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
