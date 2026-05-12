from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)

from services.trait_service import create_trait, update_trait, get_trait_tags


class TraitEditor(QWidget):
    def __init__(self, refresh_callback=None, trait=None):
        super().__init__()

        self.setWindowTitle("Trait Editor")
        self.refresh_callback = refresh_callback
        self.trait = trait  # None = create mode

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.tags_input = QLineEdit()
        self.description_input = QTextEdit()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_trait)

        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_input)

        layout.addWidget(QLabel("Tags (comma separated)"))
        layout.addWidget(self.tags_input)

        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.description_input)

        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # 🔥 LOAD EXISTING DATA IF EDITING
        if self.trait:
            self.load_trait_data()

    def load_trait_data(self):
        self.name_input.setText(self.trait.name)
        self.category_input.setText(self.trait.category)
        self.description_input.setText(self.trait.description or "")

        tags = get_trait_tags(self.trait)
        self.tags_input.setText(", ".join(tags))

    def save_trait(self):
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        description = self.description_input.toPlainText().strip()
        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]

        if not name or not category:
            QMessageBox.warning(self, "Error", "Name and Category are required.")
            return

        if self.trait:
            update_trait(self.trait.id, name, category, description, tags)
        else:
            create_trait(name, category, description, tags)

        QMessageBox.information(self, "Success", "Saved!")

        if self.refresh_callback:
            self.refresh_callback()

        self.close()