# Electron Configuration Calculator

A modern, easy-to-use desktop application built with Python for calculating and displaying the electron configurations of chemical elements.

## Features
- **Accurate Calculations**: Quickly find the electron configuration for elements across the periodic table.
- **Modern User Interface**: Built with `CustomTkinter` for a sleek, responsive, and customizable design.
- **Offline Data**: Operates completely offline using a localized element database.

## Project Structure
- `main.py`: The main entry point for running the application.
- `ui.py`: Contains the graphical user interface components and layouts.
- `config.py`: Core configuration settings and underlying calculation logic.
- `periodictable.py`: The localized database containing element information and properties.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MisoMaster11/electron-configuraton.git
   cd electron-configuraton
   ```

2. **Install dependencies:**
   Ensure you have Python installed. This project requires `customtkinter`. You can install it using pip:
   ```bash
   pip install customtkinter
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Built With
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern and customizable UI library
* **Tkinter** - The standard Python GUI framework

## License

The original source code of this project is licensed under the **MIT License** - see the `LICENSE` file for details. 

*Note: This project includes `periodictable.py` (Copyright © 2016, Cristian García), which is distributed under the **GNU Lesser General Public License (LGPL) v3**. The source code for this specific library file is bound by the LGPL, while the rest of the application remains under the MIT License.*
