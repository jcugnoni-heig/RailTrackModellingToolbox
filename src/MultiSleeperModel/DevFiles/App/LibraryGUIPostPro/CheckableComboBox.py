from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # template for managing checked states
        self.setModel(QStandardItemModel(self))

        # optional: make the combo box “editable” to display the summary in the field
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("Select...")

        # connection to manage the click in the view (before the pop-up closes)
        self.view().pressed.connect(self.handle_item_pressed)

    def add_items(self, items):
        """Add a list of channels as checkable items."""
        self.model().clear()
        for text in items:
            item = QStandardItem(text)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            item.setCheckState(Qt.Checked)
            self.model().appendRow(item)

    def handle_item_pressed(self, index):
        """Reverses the checked/unchecked state and updates the display."""
        item = self.model().itemFromIndex(index)
        if item is None:
            return
        new_state = Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked
        item.setCheckState(new_state)
        self.update_display()

    def checked_items(self):
        """Returns the list of checked items."""
        result = []
        for i in range(self.model().rowCount()):
            it = self.model().item(i)
            if it.checkState() == Qt.Checked:
                result.append(it.text())
        return result

    def update_display(self):
        """Displays the selection in the combo box (or '(none)')"""
        checked = self.checked_items()
        text = ", ".join(checked) if checked else "(none)"
        self.lineEdit().setText(text)