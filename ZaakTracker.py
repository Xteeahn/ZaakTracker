from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTableWidget, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem, QHeaderView, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor
import os
import subprocess
import sqlite3

# Get the directory where the current script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Set the current working directory to the script's directory
os.chdir(script_directory)

app = QApplication([])

# Create the main window
window = QMainWindow()
window.setWindowTitle("Zaak Tracker")

# Create a menu bar
menu_bar = window.menuBar()
file_menu = menu_bar.addMenu("File")

# Create actions for the menu
exit_action = QAction("Exit", window)

# Add actions to the menu
file_menu.addAction(exit_action)

# Create a central widget with a layout
central_widget = QWidget()
layout = QVBoxLayout(central_widget)

# Create a table view for rows, columns, and cells
table = QTableWidget(19, 19)  # rows, columns

# Set the column headers
column_headers = [
    "Zaaknaam", "Aanvraag", "SIN", "Evidence number", "Make", "Model", "Uitgelezen", "Op Zakenserver",
    "Rapport", "Op-Map", "Op-Map Maken", "Transport", "Copy to Transport", "Overgedragen",
    "Transport 1", "Disk drive 1", "Transport 2", "Disk drive 2", "Comments"
]

# Column names in database
column_names = ["Zaaknaam", "Aanvraag", "SIN", "Evidence_number", "Make", "Model", "Uitgelezen", "Op_Zakenserver",
                "Rapport", "Op_Map", "Op_Map_Maken", "Transport", "Copy_to_Transport", "Overgedragen", 
                "Transport_1", "Disk_drive_1", "Transport_2", "Disk_drive_2", "Comments"]

# Define a mapping between table column names and database column names
column_name_mapping = {
    "Zaaknaam": "Zaaknaam",
    "Aanvraag": "Aanvraag",
    "SIN": "SIN",
    "Evidence number": "Evidence_number",
    "Make": "Make",
    "Model": "Model",
    "Uitgelezen": "Uitgelezen",
    "Op Zakenserver": "Op_Zakenserver",
    "Rapport": "Rapport",
    "Op-Map": "Op_Map",
    "Op-Map Maken": "Op_Map_Maken",
    "Transport": "Transport",
    "Copy to Transport": "Copy_to_Transport",
    "Overgedragen": "Overgedragen",
    "Transport 1": "Transport_1",
    "Disk drive 1": "Disk_drive_1",
    "Transport 2": "Transport_2",
    "Disk drive 2": "Disk_drive_2",
    "Comments": "Comments"
}
table.setHorizontalHeaderLabels(column_headers)

# Default file path
default_file_path = "Zaak_Tracker.db"

# Get the absolute path to the default file in the current working directory
default_file_path = os.path.abspath(default_file_path)

# Create a database connection
conn = sqlite3.connect(default_file_path)
cursor = conn.cursor()

progress_widgets = []
# Create a dictionary to map status values to colors
progress_status_colors = {0: "white", 1: "yellow", 2: "green", 3: "red"}

# Add widgets to the layout
layout.addWidget(table)

# Set the central widget
window.setCentralWidget(central_widget)

# Connect actions to functions
def exit_application():
    app.quit()

def execute_map_button():
    button = table.sender()
    if button:
        row = table.indexAt(button.pos()).row()
        zaaknaam = table.item(row, 0)
        aanvraag = table.item(row, 1)
        SIN = table.item(row, 2)

        if zaaknaam and aanvraag and SIN:
            command = f"python oplevermap.py {zaaknaam.text()} {aanvraag.text()} {SIN.text()}"
            r = subprocess.run(command, shell=True)
        else:
            print("Not all cells in columns 0, 1, and 2 have been filled in.") # does not actually work 

def execute_copy_button():
    button = table.sender()
    if button:
        row = table.indexAt(button.pos()).row()
        zaaknaam = table.item(row, 0)
        aanvraag = table.item(row, 1)
        SIN = table.item(row, 2)
        Disk_1 = table.item(row, 15)
        Disk_2 = table.item(row, 17)

        if zaaknaam and aanvraag and SIN:
            command = f"python transport.py {zaaknaam.text()} {aanvraag.text()} {SIN.text()} {Disk_1.text()} {Disk_2.text()}"
            r = subprocess.run(command, shell=True)
        else:
            print("Not all cells in columns 0, 1, and 2 have been filled in.") # does not actually work

       
def draw_buttons(): 
    # Create buttons for the "Copy to Transport" column
    copy_buttons = [QPushButton("Copy") for _ in range(table.rowCount())]
    for row, button in enumerate(copy_buttons):
        table.setCellWidget(row, 12, button)  # 13 is the index of the "Copy to Transport" column
    
    for copy_button in copy_buttons:
        copy_button.clicked.connect(execute_copy_button)

    # Create buttons for the "Op-Map Maken" column
    map_buttons = [QPushButton("Create") for _ in range(table.rowCount())]
    for row, button in enumerate(map_buttons):
        table.setCellWidget(row, 10, button)  # 10 is the index of the "Op-Map Maken" column
    
    for map_button in map_buttons:
        map_button.clicked.connect(execute_map_button)

def set_window_size():
    # Set column widths to fit content
    default_width = 100
    table.horizontalHeader().setDefaultSectionSize(default_width)

    # Set different widths for specific columns
    table.horizontalHeader().resizeSection(0, 200)  # Zaaknaam
    table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents) # Uitgelezen
    table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents) # Op Zakenserver
    table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents) # Rapport
    table.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents) # Op-Map
    table.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeToContents) # Transport
    table.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeToContents) # Overgedragen
    table.horizontalHeader().setSectionResizeMode(15, QHeaderView.ResizeToContents) # Disk Drive 1
    table.horizontalHeader().setSectionResizeMode(17, QHeaderView.ResizeToContents) # Disk Drive 2
    table.horizontalHeader().resizeSection(18, 300)  # Comments

    # Set the window size to fit the columns' total width
    window.setMinimumWidth(table.horizontalHeader().length() + 42)

    # Set the window height to match the number of rows
    window.setMinimumHeight(table.verticalHeader().length() + 100)

# Create a custom widget for the progress indicator
class ProgressIndicator(QWidget):
    def __init__(self, row, column, status=0):
        super(ProgressIndicator, self).__init__()
        self.row = row
        self.column = column
        self.status = status
        self.setMinimumSize(30, 30)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calculate the center position of the cell
        center_x = self.width() // 2
        center_y = self.height() // 2

        # Define the color based on the status
        color = progress_status_colors[int(self.status)]

        # Adjust the circle's position to the cell's center
        radius = min(center_x -6, center_y -6)
        painter.setBrush(QBrush(QColor(color)))
        painter.drawEllipse(center_x - radius, center_y - radius, 2 * radius, 2 * radius)

    def mousePressEvent(self, event):
        # Change the status and update the color when clicked
        self.status = (self.status + 1) % 4
        self.update()
        handle_progress_status_change(self.row, self.column)
        # load_data_from_db()

def create_progress_widgets():
    # Create progress widgets for all columns
    for row in range(table.rowCount()):
        row_widgets = []
        for col in range(table.columnCount()):
            # Create the ProgressIndicator widget
            if col in [6, 7, 8, 9, 11, 13]:
                progress_widget = ProgressIndicator(row, col)
                table.setCellWidget(row, col, progress_widget)
                row_widgets.append(progress_widget)
            else:
                row_widgets.append(None)  # Placeholder for non-status columns
        progress_widgets.append(row_widgets)

def load_data_from_db():
    try:
        cursor.execute("SELECT zaaknaam, Aanvraag, SIN, Evidence_number, Make, Model, Uitgelezen, Op_Zakenserver, Rapport, Op_Map, Op_Map_Maken, Transport, Copy_to_Transport, Overgedragen, Transport_1, Disk_drive_1, Transport_2, Disk_drive_2, Comments FROM zaak_tracker")
        data = cursor.fetchall()

        if data:
            # Clear the existing data in the table
            table.setRowCount(0)

            for row, row_data in enumerate(data):
                table.insertRow(row)
                for col, cell_data in enumerate(row_data):
                    if col not in [10, 12]:
                        if col in [6, 7, 8, 9, 11, 13]:
                            cell_data = int(cell_data)
                            progress_widget = ProgressIndicator(row, col, cell_data)
                            table.setCellWidget(row, col, progress_widget)
                        else:
                            item = QTableWidgetItem(str(cell_data))
                            table.setItem(row, col, item)

    except sqlite3.Error as e:
        print(f"Error reading data from the database: {str(e)}")

def reload_data():
    load_data_from_db()
    draw_buttons()

# Function to save the progress status to a database file
def save_progress(file_path):
    cursor.execute("DELETE FROM zaak_tracker")  # Clear the existing table

    for row in range(table.rowCount()):
        row_data = [None]  # Initialize the row data list with a placeholder for the ID column
        for col in range(table.columnCount()):
            if col in [10, 12]:
                # Handle specific values for columns 10 and 12
                cell_data = "create" if col == 10 else "copy"
            elif col in [6, 7, 8, 9, 11, 13]:
                # Handle progress indicator status
                progress_widget = table.cellWidget(row, col)
                cell_data = str(progress_widget.status)
            else:
                cell_item = table.item(row, col)
                cell_data = cell_item.text() if cell_item is not None else ""
            row_data.append(cell_data)
        cursor.execute("INSERT INTO zaak_tracker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       row_data)
    conn.commit()

# Function that saves data to the database when a cell is changed
def handle_cell_data_change(item):
    column_name = column_names[item.column()]  # Get the column name
    row = item.row()
    cell_data = item.text()

    if column_name != "ID":
        # Update the corresponding record in the database based on the column name and row
        cursor.execute(f"UPDATE zaak_tracker SET {column_name} = ? WHERE ID = ?", (cell_data, row + 1))
        conn.commit()


def handle_progress_status_change(row, column):
 # Check if the column corresponds to a status cell (e.g., 6, 7, 8, 9, 11, 13)
    if column in [6, 7, 8, 9, 11, 13]:
        # Get the corresponding database column name
        table_column_name = column_headers[column]
        database_column_name = column_name_mapping.get(table_column_name, table_column_name)
        
        # Get the status from the clicked cell
        progress_widget = table.cellWidget(row, column)
        status = progress_widget.status

        # Update the corresponding record in the database
        cursor.execute(f"UPDATE zaak_tracker SET {database_column_name} = ? WHERE ID = ?", (status, row + 1))
        conn.commit()


# Apply a custom style using CSS
style = """
QTableWidget {
    background-color: #f0f0f0;
}

QTableWidget QHeaderView::section {
    background-color: #d0d0d0;
    border: none;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px;
}

QPushButton:hover {
    background-color: #45a049;
}
"""

if __name__ == "__main__":
    set_window_size()
    create_progress_widgets()
    
    # Check if the default file exists before loading it
    if os.path.exists(default_file_path):
        load_data_from_db()
        draw_buttons()
    else:
        # Handle the case where the file does not exist
        print(f"File '{default_file_path}' does not exist.")

    table.itemChanged.connect(handle_cell_data_change)

    # Create a QTimer to reload data every X milliseconds (e.g., 5000 milliseconds or 5 seconds)
    data_reload_timer = QTimer()
    data_reload_timer.timeout.connect(reload_data)
    data_reload_timer.start(30000)  # Reload data every 30 seconds

    exit_action.triggered.connect(exit_application)
    
    # Set colours
    window.setStyleSheet(style)

    window.show()
    app.exec()
