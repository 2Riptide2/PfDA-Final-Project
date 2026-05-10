# ui/trait_editor.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)

from services.trait_service import create_trait


class TraitEditor(QWidget):
    def __init__(self, refresh_callback=None):
        super().__init__()

        self.setWindowTitle("Add Trait")
        self.refresh_callback = refresh_callback

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Trait Name")

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category (e.g. personality)")

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Tags (comma separated)")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")

        self.save_button = QPushButton("Save Trait")
        self.save_button.clicked.connect(self.save_trait)

        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_input)

        layout.addWidget(QLabel("Tags"))
        layout.addWidget(self.tags_input)

        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.description_input)

        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_trait(self):
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        description = self.description_input.toPlainText().strip()
        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]

        if not name or not category:
            QMessageBox.warning(self, "Error", "Name and Category are required.")
            return

        create_trait(name, category, description, tags)

        QMessageBox.information(self, "Success", "Trait added!")

        if self.refresh_callback:
            self.refresh_callback()

        self.close()