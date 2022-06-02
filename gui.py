# -*- coding: utf-8 -*-

import sys

import os
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog, QDialog, QFrame
from PyQt5.QtGui import QFont

# from camera_proc_csv import camera_csv_processor
# from gui_result_dialog import Ui_Dialog_CSV_Data_Result


class Ui_Dialog_Camera_CSV_Proc(QDialog):  # (object):

    last_work_dir = ""


    result_dialog = None
    test_result_dlg = None
    """
    def __init__(self, object):
        self.setupUi(object)
    """

    def setupUi(self, Dialog_Camera_CSV_Proc):
        Dialog_Camera_CSV_Proc.setObjectName("Dialog_Camera_CSV_Proc")
        Dialog_Camera_CSV_Proc.resize(676, 840)

        """ color test : file 01 """
        self.groupBox_01_color_test = QtWidgets.QGroupBox(Dialog_Camera_CSV_Proc)
        self.groupBox_01_color_test.setGeometry(QtCore.QRect(20, 20, 631, 421))
        self.groupBox_01_color_test.setObjectName("groupBox_01_color_test")

        self.widget_01_color_file_01 = QtWidgets.QWidget(self.groupBox_01_color_test)
        self.widget_01_color_file_01.setGeometry(QtCore.QRect(30, 20, 571, 71))
        self.widget_01_color_file_01.setObjectName("widget_01_color_file_01")

        self.toolButton_07_del_color_file_01 = QtWidgets.QToolButton(self.widget_01_color_file_01)
        self.toolButton_07_del_color_file_01.setGeometry(QtCore.QRect(480, 10, 71, 51))
        self.toolButton_07_del_color_file_01.setObjectName("toolButton_07_del_color_file_01")
        self.toolButton_07_del_color_file_01.clicked.connect(self.del_color_file_01)

        self.textEdit_01_color_file_01_path = QtWidgets.QTextEdit(self.widget_01_color_file_01)
        self.textEdit_01_color_file_01_path.setGeometry(QtCore.QRect(10, 10, 321, 51))
        self.textEdit_01_color_file_01_path.setObjectName("textEdit_01_color_file_01_path")
        self.textEdit_01_color_file_01_path.setDisabled(True)

        self.toolButton_01_add_color_file_01 = QtWidgets.QToolButton(self.widget_01_color_file_01)
        self.toolButton_01_add_color_file_01.setGeometry(QtCore.QRect(370, 10, 71, 51))
        self.toolButton_01_add_color_file_01.setObjectName("toolButton_01_add_color_file_01")
        self.toolButton_01_add_color_file_01.clicked.connect(self.add_color_file_01)




        self.pushButton_proc_data = QtWidgets.QPushButton(Dialog_Camera_CSV_Proc)
        self.pushButton_proc_data.setGeometry(QtCore.QRect(160, 730, 301, 51))
        self.pushButton_proc_data.setObjectName("pushButton_proc_data")
        self.pushButton_proc_data.clicked.connect(self.process_csv_data)

        self.retranslateUi(Dialog_Camera_CSV_Proc)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Camera_CSV_Proc)

    def retranslateUi(self, Dialog_Camera_CSV_Proc):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Camera_CSV_Proc.setWindowTitle(_translate("Dialog_Camera_CSV_Proc", "Causal Learn算法"))
        self.groupBox_01_color_test.setTitle(_translate("Dialog_Camera_CSV_Proc", "色彩测试"))
        self.toolButton_07_del_color_file_01.setText(_translate("Dialog_Camera_CSV_Proc", "删除"))
        self.toolButton_01_add_color_file_01.setText(_translate("Dialog_Camera_CSV_Proc", "添加"))

        self.pushButton_proc_data.setText(_translate("Dialog_Camera_CSV_Proc", "处理txt文件"))

    """ handle 'delete button clicked ' event """

    def del_color_file_01(self):
        print("del_color_file_01 button  clicked")
        self.textEdit_01_color_file_01_path.setDisabled(False)
        self.textEdit_01_color_file_01_path.clear()
        self.textEdit_01_color_file_01_path.setDisabled(True)
        pass



    def add_color_file_01(self):
        print("add_color_file_01 button  clicked")

        print("last work dir : " + self.last_work_dir)

        """ Add to handle the exception case that no new main GUI is open, the users
            delete the last work directory and then continue to add files. 
        """
        if os.path.exists(self.last_work_dir) is False:
            print("last data file path is deleted, change back to current work directory")
            self.last_work_dir = os.getcwd()

        file_name, file_type = QFileDialog.getOpenFileName(parent=self, caption="open color test file 01 ",
                                                           directory=self.last_work_dir, filter="TXT files(*.txt)")
        # print("After re-check, last work dir :   " + last_work_dir)
        print("The file you select is " + file_name)
        print("The file type is " + file_type)

        if file_name == "":
            """ handle the case that users open file explorer , but do not select any file.
                We will not use a counter to count how many files are added. Because users 
                may select the same add, delete button many times to add a file , delete a file,
                or change their file selection  
            """
            print("No file is added")
            return
        else:
            # assert isinstance(filename, object)
            self.last_work_dir = os.path.dirname(file_name)
            self.textEdit_01_color_file_01_path.setDisabled(False)
            self.textEdit_01_color_file_01_path.setText(file_name)

            """ Mark for future use : If the path is too long, textEdit can't hold and display
                the whole string. So we enable textEdit, to enable the scroll bar.
            """
            self.textEdit_01_color_file_01_path.setFont(QFont("Times", 10, QFont.Normal))
            self.textEdit_01_color_file_01_path.setDisabled(True)
            pass


    def process_csv_data(self):
        pass
    #     print("process_csv_data button  clicked")
    #     print("os path real path :  " + os.path.realpath(__file__))  # 当前文件的路径
    #
    #     csv_handler = camera_csv_processor()
    #     color_file_count = csv_handler.read_color_resut(self.color_test_file_list)
    #     shading_file_count = csv_handler.read_shading_result(self.shading_test_file_list)
    #     step_file_count = csv_handler.read_stepchart_result(self.step_test_file_list)
    #     error_str = ""
    #
    #     self.result_dialog = Ui_Dialog_CSV_Data_Result()
    #     self.result_dialog.set_color_test_file_count(color_file_count)
    #     self.result_dialog.set_shading_test_file_count(shading_file_count)
    #     self.result_dialog.set_step_test_file_count(step_file_count)
    #     self.test_result_dlg = QDialog()
    #
    #     if color_file_count == 0 and shading_file_count == 0 and step_file_count == 0:  # file_save_path is None:
    #         print(" No file is selected to process, do nothing")
    #         # self.result_dialog.setup_ui_notify_error(self.result_dialog.result_window)
    #         # self.result_dialog.result_window.show()
    #         error_str = "错误：没有添加任何文件"
    #         self.result_dialog.setup_ui_notify_error(self.test_result_dlg, error_str)
    #         self.test_result_dlg.show()
    #         return
    #
    #     """ If the added file is wrong type, no matter the content is incorrect or file type is incorrect,
    #         we treat it as a fatal error, and do not process remaining correct files.
    #         A notification dialog will prompt out and no csv file will be processed.
    #
    #         For example, users add "step test files" to "color test item", we treat it as a fatal error.
    #     """
    #     if color_file_count < 0 or shading_file_count < 0 or step_file_count < 0:  # file_save_path is None:
    #         print(" At least one wrong file is selected")
    #         # self.result_dialog.setup_ui_notify_error(self.result_dialog.result_window)
    #         # self.result_dialog.result_window.show()
    #         error_str = "错误：添加的文件格式不正确"
    #         self.result_dialog.setup_ui_notify_error(self.test_result_dlg, error_str)
    #         self.test_result_dlg.exec()
    #         # self.test_result_dlg.show()
    #         return
    #
    #     # else:
    #
    #     """ The code below is for "else" case : no fatal error occurs and
    #         at least one correct file is added, and no wrong file is added.
    #         ( file_list should not contain file path of wrong file. )
    #     """
    #     file_save_path = csv_handler.decide_file_save_path(self.color_test_file_list,
    #                                                        self.step_test_file_list, self.shading_test_file_list)
    #     print(" file save path is " + file_save_path)
    #     ret_val = csv_handler.write_result_csv(file_save_path)
    #     if ret_val == -10:
    #         error_str = "错误：result.csv文件已经被打开，无法写入数据"
    #         self.result_dialog.setup_ui_notify_error(self.test_result_dlg, error_str)
    #         self.test_result_dlg.exec()
    #         # self.test_result_dlg.show()
    #         return
    #     elif ret_val == -20:
    #         error_str = "错误：last_data_path.txt文件已经被打开，无法写入上一次工作路径"
    #         self.result_dialog.setup_ui_notify_error(self.test_result_dlg, error_str)
    #         self.test_result_dlg.exec()
    #         # self.test_result_dlg.show()
    #         return
    #
    #     """ We change the way to calculate file count and add error handler
    #         to handle the case that wrong file is added.
    #
    #     color_count = 0
    #     for file in self.color_test_file_list:
    #         if file is not None:
    #             color_count = color_count + 1
    #
    #     step_file_count = 0
    #     for file in self.step_test_file_list:
    #         if file is not None:
    #             step_file_count = step_file_count + 1
    #
    #     shading_file_count = 0
    #     for file in self.shading_test_file_list:
    #         if file is not None:
    #             shading_file_count = shading_file_count + 1
    #
    #     """
    #     self.result_dialog.set_result_csv_path(file_save_path)
    #     # self.result_dialog.setup_ui_show_open_file(self.result_dialog.result_window)
    #     # self.result_dialog.result_window.show()
    #     self.result_dialog.setup_ui_show_open_file(self.test_result_dlg)
    #     # self.test_result_dlg.show()
    #     self.test_result_dlg.exec()
    #
    #     pass

    def get_last_work_diretory(self):
        """
           Add this part to memory the last work directory.

           Due to confliction between backslash and escape character (with special character),
           when we save file path ( backslash included ) to a file (such as .txt file ),
           the system will change the path format to a Unix style, i.e, aaa/bbb, no matter what
           kind of OS we are using ( Windows, Linux, or Mac OS ).

           That is to say, backslash will be replaced with slash. But do not worry, the python
           can handle unix style path (using slash not backslash) very well in windows environment.

           If we do want to keep the original path with backslash, we can save the string (maybe one row)
           to a ".csv" file , or ".xls" (or ".xlsx") file, using functions like "writerow".

        """

        self.last_work_dir = os.getcwd()

        print("enter get_last_work_diretory() , last_work_dir = " + self.last_work_dir)

        last_path_config_file = os.getcwd() + os.path.sep + "last_data_path.txt"
        if os.path.exists(last_path_config_file):
            with open(last_path_config_file, mode="r") as fd_last_path:
                last_path_read = fd_last_path.read()
                print("read last work dir from last_data_path.txt  :  " + last_path_read)
                if last_path_read != "" and os.path.exists(last_path_read):
                    self.last_work_dir = last_path_read

        print("After read config , last_work_dir = " + self.last_work_dir)
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()



    main_ui = Ui_Dialog_Camera_CSV_Proc()
    main_ui.setupUi(main_window)
    main_window.show()


    sys.exit(app.exec_())

    pass
