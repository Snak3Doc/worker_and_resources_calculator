# main.py --
import sys
import os

if getattr(sys, 'frozen', False):
    txt_path = os.path.join(sys._MEIPASS, "data.txt")
else:
    txt_path = "data.txt"

#workers * mech_speed

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QApplication, 
    QLineEdit, QTextEdit, QPushButton,
    QLabel, QGroupBox, QHBoxLayout, 
    QVBoxLayout)

from tools import calc_mine_output, calc_factory_output


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup()
        self.event_handlers()

    def closeEvent(self, event):
        self.auto_save(event)
        event.accept()

    def setup(self):
        ### Setup Window ###
        self.setWindowTitle("Workers & Resources Calculator")
        self.setGeometry(100, 100, 600, 700)

        ### Setup UI ###
        ## Functions UI ##
        # Mine Widgets
        self.lbl_mine_ore_purity = QLabel("Source Purity", self)
        self.lbl_mine_prod_workers = QLabel("Prod/p Worker", self)
        self.lbl_mine_max_workers = QLabel("Max Workers", self)
        self.lbl_mine_num_workers = QLabel("Actual Workers", self)

        self.txt_mine_ore_purity = QLineEdit(self)
        self.txt_mine_prod_workers = QLineEdit(self)
        self.txt_mine_max_workers = QLineEdit(self)
        self.txt_mine_num_workers = QLineEdit(self)

        self.btn_mine_calc = QPushButton("Run", self)

        # Factory/Plant Widgets
        self.lbl_factory_max_output = QLabel("Max Output", self)
        self.lbl_factory_max_inputs = QLabel("Max Inputs", self)
        self.lbl_factory_max_workers = QLabel("Max Workers", self)
        self.lbl_factory_num_workers = QLabel("Actual Workers", self)

        self.txt_factory_max_output = QLineEdit(self)
        self.txt_factory_max_inputs = QLineEdit(self, placeholderText="Seperate with comas")
        self.txt_factory_max_workers = QLineEdit(self)
        self.txt_factory_num_workers = QLineEdit(self)

        self.btn_factory_calc = QPushButton("Run", self)

        # Mine Layouts
        self.lyt_func_mine_lbl = QHBoxLayout()
        self.lyt_func_mine_txt = QHBoxLayout()

        # Factory/Plant Layouts
        self.lyt_func_factory_lbl = QHBoxLayout()
        self.lyt_func_factory_txt = QHBoxLayout()

        # Mine Setup
        self.lyt_func_mine_lbl.addWidget(self.lbl_mine_ore_purity)
        self.lyt_func_mine_lbl.addWidget(self.lbl_mine_prod_workers)
        self.lyt_func_mine_lbl.addWidget(self.lbl_mine_max_workers)
        self.lyt_func_mine_lbl.addWidget(self.lbl_mine_num_workers)

        self.lyt_func_mine_txt.addWidget(self.txt_mine_ore_purity)
        self.lyt_func_mine_txt.addWidget(self.txt_mine_prod_workers)
        self.lyt_func_mine_txt.addWidget(self.txt_mine_max_workers)
        self.lyt_func_mine_txt.addWidget(self.txt_mine_num_workers)
        self.lyt_func_mine_txt.addWidget(self.btn_mine_calc)

        # Factory/Plant Setup
        self.lyt_func_factory_lbl.addWidget(self.lbl_factory_max_output)
        self.lyt_func_factory_lbl.addWidget(self.lbl_factory_max_inputs)
        self.lyt_func_factory_lbl.addWidget(self.lbl_factory_max_workers)
        self.lyt_func_factory_lbl.addWidget(self.lbl_factory_num_workers)

        self.lyt_func_factory_txt.addWidget(self.txt_factory_max_output)
        self.lyt_func_factory_txt.addWidget(self.txt_factory_max_inputs)
        self.lyt_func_factory_txt.addWidget(self.txt_factory_max_workers)
        self.lyt_func_factory_txt.addWidget(self.txt_factory_num_workers)
        self.lyt_func_factory_txt.addWidget(self.btn_factory_calc)

        ## Terminal UI ##
        # Widgets
        self.txt_terminal = QTextEdit(self)
        #!self.txt_terminal.setText()

        # Layouts
        self.lyt_terminal_main = QVBoxLayout()

        # Setup
        self.lyt_terminal_main.addWidget(self.txt_terminal)

        ## Main Win UI ##
        # Widgets
        centeral_widget = QWidget()

        # Layouts
        self.lyt_main = QVBoxLayout()

        # Setup
        self.lyt_main.addLayout(self.lyt_func_mine_lbl)
        self.lyt_main.addLayout(self.lyt_func_mine_txt)
        self.lyt_main.addLayout(self.lyt_func_factory_lbl)
        self.lyt_main.addLayout(self.lyt_func_factory_txt)

        self.lyt_main.addLayout(self.lyt_terminal_main)

        centeral_widget.setLayout(self.lyt_main)

        self.setCentralWidget(centeral_widget)

    def event_handlers(self):
        self.btn_mine_calc.clicked.connect(self.get_mine_calc_data)
        self.btn_factory_calc.clicked.connect(self.get_factory_calc_data)

    def write_txt(self):
        with open("data.txt", 'w') as file:
            temp_data = self.txt_terminal.toPlainText()
            file.write(temp_data)

    def read_txt(self):
        with open("data.txt", 'r') as file:
            temp_data = file.read()
            self.txt_terminal.setText(temp_data)

    def auto_save(self, event):
            self.write_txt()


    def get_mine_calc_data(self):
        source_purity = int(self.txt_mine_ore_purity.text())
        max_prod = float(self.txt_mine_prod_workers.text())
        max_workers = int(self.txt_mine_max_workers.text())
        num_workers = self.txt_mine_num_workers.text()
        if num_workers:
            num_workers = int(num_workers)
        else:
            num_workers = None
        data = calc_mine_output(source_purity, max_prod, max_workers, num_workers)
        self.txt_terminal.append(f"Type: {data[0]}\nWorkers: {data[1]}\nOutput: {data[2]}t\n")

    def get_factory_calc_data(self):
        max_output = int(self.txt_factory_max_output.text())
        max_inputs = self.txt_factory_max_inputs.text().split(',')
        max_inputs = list(map(int, max_inputs))
        max_workers = int(self.txt_factory_max_workers.text())
        num_workers = self.txt_factory_num_workers.text()
        if num_workers:
            num_workers = int(num_workers)
        else:
            num_workers = None
        data = calc_factory_output(max_output, max_inputs, max_workers, num_workers)
        self.txt_terminal.append(f"Type: {data[0]}\nWorkers: {data[1]}\nOutput: {data[2]}t\nInputs: {'t, '.join(map(str, data[3]))}t\nUtilization: {data[4]}%\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    mw = MainWindow()
    mw.read_txt()
    mw.show()
    sys.exit(app.exec())






