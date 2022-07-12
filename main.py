import sys

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QListWidget, QHBoxLayout, QLabel, QComboBox, QListWidgetItem
import qtawesome as qta


class DropDownList(QWidget):
    def __init__(self, parent=None, item=None):
        super(DropDownList, self).__init__(parent)

        self.item = item
        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem(f"No {self.item}")

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def addElement(self):
        self.cb.addItem(f"{self.item} {self.cb.count()}")
        self.cb.setCurrentIndex(self.cb.count()-1)


class HorizontalElements(QWidget):
    def __init__(self, parent=None, item=None):
        super(HorizontalElements, self).__init__(parent)

        self.dlist = DropDownList(item=item)

        self.button = QPushButton(self)
        self.button.setIcon(qta.icon("msc.add"))
        self.button.clicked.connect(self.dlist.addElement)
        self.button.setFixedSize(self.button.iconSize().width() + 5, self.button.iconSize().height() + 5)

        self.window = QWidget()
        self.layout = QHBoxLayout()

        self.label = QLabel(self)
        self.label.setText(f"{item}:")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dlist)
        self.layout.addWidget(self.button)
        self.window.setLayout(self.layout)


class ListBox(QWidget):
    def __init__(self, parent=None, newItem=None, itemName=None, extension=None, icon=None):
        super(ListBox, self).__init__(parent)

        self.newItem = newItem
        self.itemName = itemName
        self.extension = extension
        self.icon = icon

        self.widget = QListWidget()
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(f"{newItem}", self)
        self.button.clicked.connect(self.onClicked)
        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.button)

    def onClicked(self):
        item = QListWidgetItem()
        item.setText(f"{self.itemName}_{self.widget.count()}{self.extension if self.extension else ''}")
        if self.icon:
            item.setIcon(qta.icon(self.icon))
        self.widget.addItem(item)


class LeftSide(QWidget):
    def __init__(self, parent=None):
        super(LeftSide, self).__init__(parent)

        self.window = QWidget()
        self.layout = QVBoxLayout()

        self.projects = HorizontalElements(item="Project")
        self.categories = HorizontalElements(item="Category")
        self.tasks = ListBox(newItem="New task", itemName="task", icon="fa.file-image-o")

        self.layout.addWidget(self.projects.window)
        self.layout.addWidget(self.categories.window)
        self.layout.addWidget(self.tasks)
        self.window.setLayout(self.layout)


class RightSide(QWidget):
    def __init__(self, parent=None):
        super(RightSide, self).__init__(parent)

        self.window = QWidget()
        self.layout = QVBoxLayout()

        self.files = ListBox(newItem="Publish file", itemName="file1", extension=".ma", icon="fa.file-text")
        self.layout.addWidget(self.files)
        self.window.setLayout(self.layout)


class Window(QWidget):

    def __init__(self, title=None):
        super().__init__()

        layout = QHBoxLayout()
        layout.addWidget(LeftSide().window)
        layout.addWidget(RightSide().window)

        self.window().setWindowTitle(title)
        self.window().setLayout(layout)

        self.setGeometry(300, 300, 660, 660)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Window(title="Maya AssetManager")
    form.show()
    sys.exit(app.exec_())