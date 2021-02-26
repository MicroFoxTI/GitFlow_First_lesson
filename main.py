import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox


class EditThisCoffee(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.parent = parent
        self.ok_btn.clicked.connect(self.new_result)

    def show(self):
        super().show()
        self.name_ed.setText('')
        self.type_ed.setText('')
        self.degre_ed.setText('')
        self.descr_ed.setText('')
        self.price_ed.setText('')
        self.packing_ed.setText('')
        self.grinded_status.setCurrentIndex(0)

    def new_result(self):
        self.parent.cur.execute(f'INSERT INTO coffee VALUES ((SELECT MAX(id) FROM coffee)+1, "{self.name_ed.text()}",'
                                + f' "{self.type_ed.text()}", {self.degre_ed.text()},'
                                + f' "{str(self.grinded_status.currentText()).capitalize()}", "{self.descr_ed.text()}",'
                                + f' {self.price_ed.text()}, {self.packing_ed.text()})')
        self.parent.con.commit()
        self.parent.view_result()
        self.hide()


class EditThisCoffee2(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.parent = parent
        self.ok_btn.clicked.connect(self.new_result)

    def show(self):
        super().show()
        self.name_ed.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 1).text())
        self.type_ed.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 2).text())
        self.degre_ed.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 3).text())
        self.descr_ed.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 5).text())
        self.price_ed.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 6).text())
        self.packing_ed.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 7).text())
        self.grinded_status.setCurrentIndex(
            int(not bool(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 4).text())))

    def new_result(self):
        self.parent.cur.execute(f'UPDATE coffee SET name="{self.name_ed.text()}", type="{self.type_ed.text()}", '
                                + f'degree_of_roast={self.degre_ed.text()},'
                                + f' grind="{str(self.grinded_status.currentText()).capitalize()}",'
                                + f' description="{self.descr_ed.text()}",'
                                + f' price={self.price_ed.text()}, packaging={self.packing_ed.text()}'
                                + f' WHERE id=' +
                                self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 0).text())
        self.parent.con.commit()
        self.parent.view_result()
        self.hide()


class LookAtMyCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.tableWidget.setColumnCount(len(self.cur.execute("SELECT * FROM coffee").fetchone()))
        self.tableWidget.setHorizontalHeaderLabels([description[0] for description in self.cur.description])
        self.view_result()

        self.new_file = EditThisCoffee(self)
        self.editor = EditThisCoffee2(self)
        self.create_btn.clicked.connect(lambda: self.new_file.show())
        self.edit_btn.clicked.connect(self.open_editor)

    def view_result(self):
        res = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def open_editor(self):
        if self.tableWidget.currentRow() != -1:
            self.editor.show()
        else:
            QMessageBox.question(self, '', "Выберите элемент для изменения", QMessageBox.Ok)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LookAtMyCoffee()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
