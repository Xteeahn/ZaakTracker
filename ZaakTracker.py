import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QTableWidget, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidgetItem
import csv

app = QApplication([])

# Create the main window
window = QMainWindow()
window.setWindowTitle("Excel-Like GUI")

# Create a menu bar
menu_bar = window.menuBar()
file_menu = menu_bar.addMenu("File")

# Create actions for the menu
exit_action = QAction("Exit", window)
save_action = QAction("Save as CSV", window)
load_action = QAction("Load CSV", window)

# Add actions to the menu
file_menu.addAction(exit_action)
file_menu.addAction(save_action)
file_menu.addAction(load_action)

# Create a central widget with a layout
central_widget = QWidget()
layout = QVBoxLayout(central_widget)

# Create a table view for rows, columns, and cells
table = QTableWidget(20, 20)  # 20 rows, 20 columns

# Set the column headers
column_headers = [
    "Zaaknaam", "Aanvraag", "SIN", "Evidence number", "Make", "Model", "Uitgelezen", "Op Zakenserver",
    "Rapport", "Op-Map", "Op-Map Maken", "Hash", "Transport", "Copy to Transport", "Overgedragen",
    "Transport 1", "Disk drive 1", "Transport 2", "Disk drive 2", "Comments"
]

table.setHorizontalHeaderLabels(column_headers)

# Create buttons
button = QPushButton("Save as CSV")

# Add widgets to the layout
layout.addWidget(table)
layout.addWidget(button)

# Set the central widget
window.setCentralWidget(central_widget)

# Connect actions to functions
def exit_application():
    app.quit()

def save_to_csv():
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(None, "Save as CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

    if file_path:
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write the column headers
            csv_writer.writerow(column_headers)
            # Write the data from the table
            for row in range(table.rowCount()):
                row_data = [table.item(row, col).text() for col in range(table.columnCount())]
                csv_writer.writerow(row_data)

def load_csv():
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(None, "Load CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

    if file_path:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            if header != column_headers:
                # Handle mismatched headers
                print("Header mismatch. File not loaded.")
            else:
                for row, row_data in enumerate(csv_reader):
                    for col, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(cell_data)
                        table.setItem(row, col, item)

button.clicked.connect(save_to_csv)
exit_action.triggered.connect(exit_application)
load_action.triggered.connect(load_csv)

# Set column widths to fit content
table.resizeColumnsToContents()

# Set the window size to fit the columns' total width
window.setMinimumWidth(table.horizontalHeader().length())

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

window.setStyleSheet(style)

# Set the window height to match the number of rows
window.setMinimumHeight(table.verticalHeader().length())

window.show()
app.exec()
