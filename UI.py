import sys
import design
import Trainer
from PyQt5 import QtWidgets


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    tr = Trainer.Trainer()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.calc)
        self.tr.write_to_files()
        self.tr.draw_plot()

    def calc(self):
        #tr = Trainer.Trainer()
        #tr.write_to_files()
        #tr.draw_plot()
        if self.textEdit.toPlainText() != '':
            spam, ham = self.tr.calc_pos(self.textEdit.toPlainText())
            if spam > ham:
                self.lineEdit.setText('spam')
            elif spam < ham:
                self.lineEdit.setText('ham')
            else:
                self.lineEdit.setText('spam/ham')
        return


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()


if __name__ == '__main__':
    main()