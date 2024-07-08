import sys
import re
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QTextEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox, 
                             QInputDialog, QSizePolicy)

class RegexCompiler(QWidget):
    def __init__(self):
        super().__init__()
        self.json_file = 'regex_history.json'
        self.initUI()
        self.load_history()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Regex Compiler')
        self.setGeometry(100, 100, 900, 500)  # Adjusted window size

        # Main Layout
        main_layout = QHBoxLayout()

        # Left Layout for history
        left_layout = QVBoxLayout()

        # History Tree Widget
        self.history_tree = QTreeWidget()
        self.history_tree.setHeaderLabels(['Regex Pattern', 'Example'])
        self.history_tree.setColumnWidth(0, 200)
        self.history_tree.itemClicked.connect(self.load_from_history)
        left_layout.addWidget(QLabel('History'))
        left_layout.addWidget(self.history_tree)

        # Right Layout for input and output
        right_layout = QVBoxLayout()

        # Input Form Layout
        form_layout = QVBoxLayout()

        # Regex Pattern Input
        self.regex_input = QLineEdit()
        self.regex_input.setText(r'\b\w+\b')  # Example regex pattern
        self.regex_input.textChanged.connect(self.check_input)
        form_layout.addWidget(QLabel('Regex Pattern:'))
        form_layout.addWidget(self.regex_input)

        # Example String Input
        self.example_input = QLineEdit()
        self.example_input.setText('This is an example string with several words.')  # Example string
        self.example_input.textChanged.connect(self.check_input)
        form_layout.addWidget(QLabel('Example String:'))
        form_layout.addWidget(self.example_input)

        # Explanation Input and Edit Text Box
        explanation_layout = QVBoxLayout()
        explanation_label = QLabel('Explanation:')
        explanation_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.explanation_input = QTextEdit()
        self.explanation_input.setPlaceholderText('Enter explanation...')
        self.explanation_input.setMaximumHeight(120)  # Limit height to 120 pixels
        self.explanation_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        explanation_layout.addWidget(explanation_label)
        explanation_layout.addWidget(self.explanation_input)
        form_layout.addLayout(explanation_layout)

        right_layout.addLayout(form_layout)

        # Output Console
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        right_layout.addWidget(self.output_console)

        # Compile Button
        self.compile_button = QPushButton('Compile')
        self.compile_button.setEnabled(True)  # Enable the button as fields are pre-filled
        self.compile_button.clicked.connect(self.compile_regex)
        right_layout.addWidget(self.compile_button)

        # Add left and right layouts to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def check_input(self):
        if self.regex_input.text() and self.example_input.text():
            self.compile_button.setEnabled(True)
        else:
            self.compile_button.setEnabled(False)

    def compile_regex(self):
        pattern = self.regex_input.text()
        example = self.example_input.text()
        explanation = self.explanation_input.toPlainText()
        self.output_console.clear()

        # Save the pattern, example, and explanation to history if not already present
        if pattern and example:
            history = self.load_history_from_file()
            entry = {'pattern': pattern, 'example': example, 'explanation': explanation}
            if entry not in history:
                history.append(entry)
                self.save_history_to_file(history)

        try:
            compiled_pattern = re.compile(pattern)
            matches = compiled_pattern.findall(example)

            if matches:
                self.output_console.append("Matches found:\n")
                for match in matches:
                    self.output_console.append(str(match))
            else:
                self.output_console.append("No matches found.")

        except re.error as err:
            self.output_console.append(f"Regex error: {str(err)}")
            QMessageBox.critical(self, "Regex Error", str(err), QMessageBox.Ok)

    def load_from_history(self, item):
        pattern = item.text(0)
        example = item.text(1)
        self.regex_input.setText(pattern)
        self.example_input.setText(example)
        self.explanation_input.clear()  # Clear any previous explanations

    def save_history_to_file(self, history):
        with open(self.json_file, 'w') as f:
            json.dump(history, f, indent=4)

    def load_history_from_file(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                return json.load(f)
        return []

    def load_history(self):
        history = self.load_history_from_file()
        for entry in history:
            self.add_to_history_tree(entry['pattern'], entry['example'])

    def add_to_history_tree(self, pattern, example):
        root = QTreeWidgetItem(self.history_tree)
        root.setText(0, pattern)
        root.setText(1, example)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    compiler = RegexCompiler()
    compiler.show()
    sys.exit(app.exec_())
