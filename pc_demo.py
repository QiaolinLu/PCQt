from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.cit import gsq, fisherz, mv_fisherz, kci, chisq
import numpy as np
import os
import sys

class Peter_Clark_Test(QWidget):


    global gsq, fisherz, mv_fisherz, kci, chisq

    NumButtons = ['plot1','plot2', 'plot3']

    def __init__(self):


        super(Peter_Clark_Test, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.last_work_dir = ""
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 1000, 800)
        self.center()
        self.setWindowTitle('Peter Clark Algorithm')

        grid = QGridLayout()
        self.setLayout(grid)


        InputLayout = QVBoxLayout()
        self.verticalGroupBox = QGroupBox()
        layout = QVBoxLayout()
        """
        PC 算法 计算
        """
        self.button = QPushButton("PC")
        layout.addWidget(self.button)
        self.button.clicked.connect(lambda: self.PC_algorithm(
            input_data = np.loadtxt(self.textEdit_file_path.toPlainText(), skiprows=1),
            alpha = float(self.alpha.currentText()),
            indep_test = self.indepedence_test_method.currentText(),
            uc_rule = int(self.uc_rule.currentText()),
            uc_priority= int(self.uc_priority.currentText()),
            mvpc = self.mvpc.currentText(),
            graph_model=self.graph_model.currentText()

        ))

        self.alpha_label = QLabel("alpha")
        layout.addWidget(self.alpha_label)
        self.alpha = QComboBox()
        self.alpha.addItems(['0.05', '0.01', '0.10'])
        layout.addWidget(self.alpha)

        self.indepedence_test_method = QLabel("indep_test")
        layout.addWidget(self.indepedence_test_method)
        self.indepedence_test_method = QComboBox()
        self.indepedence_test_method.addItems(['fisherz', 'chisq', 'gsq', 'kci', 'mv_fisherz'])
        layout.addWidget(self.indepedence_test_method)

        self.uc_rule_label = QLabel("uc_rule")
        layout.addWidget(self.uc_rule_label)
        self.uc_rule = QComboBox()
        self.uc_rule.addItems(['0', '1', '2'])
        layout.addWidget(self.uc_rule)

        self.uc_priority_label = QLabel("uc_priority")
        layout.addWidget(self.uc_priority_label)
        self.uc_priority = QComboBox()
        self.uc_priority.addItems(['2', '-1', '0', '1', '3', '4'])
        layout.addWidget(self.uc_priority)

        self.mvpc_label = QLabel("mvpc")
        layout.addWidget(self.uc_priority_label)
        self.mvpc = QComboBox()
        self.mvpc.addItems(['False', 'True'])
        layout.addWidget(self.mvpc)

        self.graph_model_label = QLabel("视图模式")
        layout.addWidget(self.graph_model_label)
        self.graph_model = QComboBox()
        self.graph_model.addItems(['networkx', 'pydot'])
        layout.addWidget(self.graph_model)

        self.add_file_label = QLabel("添加文件")
        layout.addWidget(self.add_file_label)
        self.input_data_button = QPushButton()
        self.input_data_button.setText("输入")
        layout.addWidget(self.input_data_button)
        self.input_data_button.clicked.connect(self.add_file)

        self.del_file_label = QLabel("删除文件")
        layout.addWidget(self.del_file_label)
        self.del_data_button = QPushButton()
        self.del_data_button.setText("删除")
        layout.addWidget(self.del_data_button)
        self.del_data_button.clicked.connect(self.del_file)

        self.textEdit_file_path = QTextEdit()
        self.textEdit_file_path.setObjectName("textEdit_file_path")
        self.textEdit_file_path.setDisabled(True)
        layout.addWidget(self.textEdit_file_path)

        layout.setSpacing(10)
        self.verticalGroupBox.setLayout(layout)
        InputLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)
        grid.addLayout(InputLayout, 0, 0)

        self.show()





    def add_file(self):
        print("add_file button clicked")
        print("last work dir: "+ self.last_work_dir)
        if os.path.exists(self.last_work_dir) is False:
            print("last data file path is deleted, change back to current work directory")
            self.last_work_dir = os.getcwd()
        file_name, file_type = QFileDialog.getOpenFileName(parent=self, caption="open color test file 01 ",
                                                           directory=self.last_work_dir, filter="TXT files(*.txt)")
        # print("After re-check, last work dir :   " + last_work_dir)
        print("The file you select is " + file_name)
        print("The file type is " + file_type)

        if file_name == "":
            print("No file is added")
            return
        else:
            self.last_work_dir = os.path.dirname(file_name)
            self.textEdit_file_path.setDisabled(False)
            self.textEdit_file_path.setText(file_name)
            self.textEdit_file_path.setFont(QFont("Times", 10, QFont.Normal))
            self.textEdit_file_path.setDisabled(True)
            pass

    def del_file(self):
        print("del_file button clicked")
        self.textEdit_file_path.setDisabled(False)
        self.textEdit_file_path.clear()
        self.textEdit_file_path.setDisabled(True)
        pass

    def PC_algorithm(self, input_data, alpha, indep_test, uc_rule, uc_priority,mvpc, graph_model):

        if indep_test == "fisherz":
            indep_test = fisherz
        elif indep_test == "kci":
            indep_test = kci
        elif indep_test == "chisq":
            indep_test = chisq
        elif indep_test == "mv_fisherz":
            indep_test = mv_fisherz
        elif indep_test == "gsq":
            indep_test = gsq

        if mvpc == "False":
            mvpc = False
        else:
            mvpc = True
        cg = pc(input_data, alpha, indep_test, True, uc_rule, uc_priority, mvpc)

        if graph_model == "networkx":
            print(graph_model)
            cg.to_nx_graph()
            cg.draw_nx_graph(skel=False)
            self.canvas.draw_idle()
        else:
            cg.draw_pydot_graph()
            self.canvas.draw_idle()




    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = Peter_Clark_Test()
    screen.show()
    sys.exit(app.exec_())