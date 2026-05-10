# ui/main_window.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QApplication
)
from services.trait_service import get_traits
from ui.trait_editor import TraitEditor
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Character Trait Library")
        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.refresh_button = QPushButton("Refresh Traits")
        self.refresh_button.clicked.connect(self.load_traits)
        self.layout.addWidget(self.refresh_button)

        self.add_button = QPushButton("Add Trait")
        self.add_button.clicked.connect(self.open_trait_editor)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

        # 🔥 THIS WAS MISSING
        self.load_traits()

    def load_traits(self):
        self.list_widget.clear()
        traits = get_traits()

        for trait in traits:
            self.list_widget.addItem(f"{trait.name} ({trait.category})")

    def open_trait_editor(self):
        self.editor = TraitEditor(refresh_callback=self.load_traits)
        self.editor.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())