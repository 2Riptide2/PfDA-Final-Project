from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QHBoxLayout
)

from services.trait_service import get_traits
from ui.trait_editor import TraitEditor


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Character Trait Library")

        layout = QVBoxLayout()

        # 🔍 SEARCH BAR
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search traits...")
        self.search_input.textChanged.connect(self.load_traits)
        layout.addWidget(self.search_input)

        # 🏷 TAG FILTER
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Filter by tags (comma separated)")
        self.tag_input.textChanged.connect(self.load_traits)
        layout.addWidget(self.tag_input)

        # 📋 TRAIT LIST
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # BUTTON ROW
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Trait")
        self.add_button.clicked.connect(self.open_add_editor)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.open_edit_editor)
        button_layout.addWidget(self.edit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.current_traits = []
        self.load_traits()

    def load_traits(self):
        search = self.search_input.text().strip()
        tags = [t.strip() for t in self.tag_input.text().split(",") if t.strip()]

        traits = get_traits(search_text=search, include_tags=tags)

        self.current_traits = traits

        self.list_widget.clear()
        for trait in traits:
            tag_list = [tt.tag.name for tt in trait.tags]
            self.list_widget.addItem(
                f"{trait.name} ({trait.category}) | Tags: {', '.join(tag_list)}"
            )

    def open_add_editor(self):
        self.editor = TraitEditor(refresh_callback=self.load_traits)
        self.editor.show()

    def open_edit_editor(self):
        selected_index = self.list_widget.currentRow()

        if selected_index < 0:
            return

        trait = self.current_traits[selected_index]

        self.editor = TraitEditor(
            refresh_callback=self.load_traits,
            trait=trait
        )
        self.editor.show()