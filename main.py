from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
import sys
from win32api import GetSystemMetrics
from teachers import teachers
from functools import partial
from datetime import datetime
import ctypes

myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
# Following line of code allows the application to have an icon.
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)

# from c++ qt documentation
Keep_Anchor = 1
StartOfBlock = 4
EndOfBlock = 15

teacher_set = set({})
for teacher in teachers:
    teacher_set.add(teacher)

# The date format: day (e.g. 1) month (e.g. Nov) Year (e.g. 2021)
date_format = "%d %b %Y"

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        # leave xpos and ypos as 0 because following line centers the window.
        self.setGeometry(0, 0, WIDTH // 3, HEIGHT // 2)

        # Setting the tile and icon of the window.
        self.setWindowTitle("Selborne College Teacher Substitution System")
        self.setWindowIcon(QtGui.QIcon('images/selborne.ico'))

        self.initUI()
        self.center()

        self.absent_teachers = []
        self.present_teachers = []
        for teacher in teachers:
            self.present_teachers.append(teacher)

        self.teachers_substituting = {}
        self.setTeacherRecords()
        with open("previous_teacher_records.txt", "r") as f:
            lines = f.readlines()
            self.previous_records_date = lines[0].strip()

    def setTeacherRecords(self):
        with open("teacher_records.txt", "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                pos_colon = line.find(':')
                teacher = line[:pos_colon]
                times_substituted = int(line[pos_colon+1:])
                self.teachers_substituting[teacher] = [0, 0]
                self.teachers_substituting[teacher][1] = times_substituted
        for teacher in self.teachers_substituting.keys():
            self.teachers_substituting[teacher][0] = 0

    def initUI(self):
        grid = QGridLayout()
        grid.setColumnStretch(0, self.width() // 4)
        grid.setColumnStretch(1, self.width() // 2)
        grid.setColumnStretch(2, self.width() // 4)
        grid.setRowMinimumHeight(1, 30)
        grid.setRowMinimumHeight(4, 30)
        grid.setRowStretch(2, self.height() // 30)
        grid.setRowStretch(3, self.height() // 30)
        grid.setRowStretch(4, self.height() // 10)
        grid.setRowMinimumHeight(7, 50)

        grid.setRowMinimumHeight(6, 190)
        self.setLayout(grid)

        grid_layout = ['image', 'entry', '',
                       '', 'add', '',
                       '', 'abs_teachers', '',
                       '', '', 'remove',
                       '', 'daycbx', ''
                       '', 'output_btn', '',
                       '', 'output', '',
                       'reset', '', 'select',
                       'view', '', 'clear',
                       'revert',  '', 'close'
                       ]

        self.labelImage = QtWidgets.QLabel(self)
        pixmap = QPixmap("images/SelborneLogo.jpg")
        pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4)
        self.labelImage.setPixmap(pixmap)
        grid.addWidget(self.labelImage, 0, 0, 3, 1)
        self.labelImage.resize(100, 100)

        self.entry = QtWidgets.QLineEdit(self)
        self.entry.setPlaceholderText("Enter code (e.g. HMN)")
        grid.addWidget(self.entry, 0, 1, 1, 1)

        self.btnAdd = QtWidgets.QPushButton(self)
        self.btnAdd.setText("Add Teacher")
        self.btnAdd.setMinimumHeight(30)
        self.btnAdd.clicked.connect(self.add_teacher)
        grid.addWidget(self.btnAdd, 1, 1, 1, 1)

        self.list = QtWidgets.QListWidget(self)
        grid.addWidget(self.list, 2, 1, 2, 1)

        self.btnRemove = QtWidgets.QPushButton(self)
        self.btnRemove.setText("Remove Selected\nTeacher")
        self.btnRemove.clicked.connect(self.remove)
        grid.addWidget(self.btnRemove, 3, 2, 1, 1)

        self.daycbx = QtWidgets.QComboBox(self)
        self.daycbx.addItems(["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"])
        grid.addWidget(self.daycbx, 4, 1, 1, 1)

        self.btnOutput = QtWidgets.QPushButton(self)
        self.btnOutput.setText("Find Replacements")
        self.btnOutput.clicked.connect(self.output)
        self.btnOutput.setMinimumHeight(30)
        grid.addWidget(self.btnOutput, 5, 1, 1, 1)

        self.text_output = QtWidgets.QListWidget(self)
        grid.addWidget(self.text_output, 6, 1, 4, 1)

        self.btnSelect = QtWidgets.QPushButton(self)
        self.btnSelect.setText("Select Teachers")
        self.btnSelect.clicked.connect(self.save)
        self.btnSelect.setMinimumHeight(45)
        grid.addWidget(self.btnSelect, 7, 2, 1, 1)

        self.btnReset = QtWidgets.QPushButton(self)
        self.btnReset.setText("Reset Substitution\nRecords")
        self.btnReset.clicked.connect(self.reset)
        self.btnReset.setMinimumHeight(45)
        grid.addWidget(self.btnReset, 7, 0, 1, 1)

        self.btnClear = QtWidgets.QPushButton(self)
        self.btnClear.setText("Clear All")
        self.btnClear.clicked.connect(self.clear)
        self.btnClear.setMinimumHeight(45)
        grid.addWidget(self.btnClear, 8, 2, 1, 1)

        self.btnViewRecords = QtWidgets.QPushButton(self)
        self.btnViewRecords.setText("View Substitution\nRecords")
        self.btnViewRecords.clicked.connect(self.viewRecords)
        self.btnViewRecords.setMinimumHeight(45)
        grid.addWidget(self.btnViewRecords, 8, 0, 1, 1)

        self.btnRevert = QtWidgets.QPushButton(self)
        self.btnRevert.setText("Revert to Previous\nRecords")
        self.btnRevert.clicked.connect(self.revert)
        self.btnRevert.setMinimumHeight(45)
        grid.addWidget(self.btnRevert, 9, 0, 1, 1)

        self.btnClose = QtWidgets.QPushButton(self)
        self.btnClose.setText("Close")
        self.btnClose.clicked.connect(self.closeProgram)
        self.btnClose.setMinimumHeight(45)
        grid.addWidget(self.btnClose, 9, 2, 1, 1)

    def reset(self):
        self.resetDialog = QtWidgets.QMessageBox()
        self.resetDialog.setIcon(QtWidgets.QMessageBox.Question)
        self.resetDialog.setWindowTitle("Reset Substitution Records?")
        self.resetDialog.setText("Are you sure you want to reset the substitution records?")
        self.resetDialog.setInformativeText("You can only revert changes once.")
        self.resetDialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        retval = self.resetDialog.exec_()
        if retval == QtWidgets.QMessageBox.Yes:
            with open("teacher_records.txt", "r") as f1:
                with open("previous_teacher_records.txt", "w") as f2:
                    lines = f1.readlines()
                    date = lines[0].strip()
                    print(date, file=f2)
                    for line in lines[1:]:
                        print(line.strip(), file=f2)
            with open("teacher_records.txt", "w") as f:

                date_today = datetime.date(datetime.now()).strftime(date_format)
                print(date_today, file=f)
                for teacher in self.teachers_substituting.keys():
                    print(teacher + ":" + '0', file=f)

        self.setTeacherRecords()
        self.output()

    def viewRecords(self):
        self.viewDialog = QtWidgets.QMessageBox()
        self.viewDialog.setIcon(QtWidgets.QMessageBox.Information)
        self.viewDialog.setWindowTitle("View Records")
        self.viewDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        text = ""
        with open("teacher_records.txt", "r") as f:
            lines = f.readlines()
            text += lines[0].strip() + '\n\n'
            count = 0
            for line in lines[1:]:
                count += 1
                code, record = line.strip().split(':')
                text += code + ': ' + record
                if count % 2 == 0:
                     text += '\t' + '|' + '   '
                else:
                    text += '\n'
        self.viewDialog.setText(text)

        self.viewDialog.exec_()

    def revert(self):
        if self.btnRevertInfoDialog() == QtWidgets.QMessageBox.Yes:
            with open("previous_teacher_records.txt", "r") as f1:
                with open("teacher_records.txt", "w") as f2:
                    for line in f1:
                        print(line.strip(), file=f2)

        self.setTeacherRecords()
        self.output()

    def save(self):
        if self.btnSaveInfoDialog() == QtWidgets.QMessageBox.Yes:
            if self.text_output.count() > 0:
                with open("teacher_records.txt", "r") as f1:
                    with open("previous_teacher_records.txt", "w") as f2:
                        for line in f1:
                            print(line.strip(), file=f2)
                with open("teacher_records.txt", "w") as f:
                    date_format = "%d %b %Y"
                    date_today = datetime.date(datetime.now()).strftime(date_format)
                    print(date_today, file=f)
                    for teacher in self.teachers_substituting.keys():
                        total = self.teachers_substituting[teacher][0] + self.teachers_substituting[teacher][1]
                        print(teacher + ":" + str(total), file=f)
            else:
                self.nothingSelectedDialog()
        self.setTeacherRecords()
        self.output(save=True)

    def nothingSelectedDialog(self):
        self.dialog = QtWidgets.QMessageBox()
        self.dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.dialog.setText("No teachers to select.")
        self.dialog.setWindowTitle("No Teachers to Select")
        self.dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.dialog.exec_()

    def btnRevertInfoDialog(self):
        self.revertDialog = QtWidgets.QMessageBox()
        self.revertDialog.setIcon(QtWidgets.QMessageBox.Question)
        self.revertDialog.setWindowTitle("Revert Changes?")
        self.revertDialog.setText("Are you sure you want to revert to the previous teacher records " + "(" +
                                  self.previous_records_date + ")" + "?")
        self.revertDialog.setInformativeText("Changes can only be reverted once.")
        self.revertDialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        retval = self.revertDialog.exec_()
        return retval

    def btnSaveInfoDialog(self):
        self.saveDialog = QtWidgets.QMessageBox()
        self.saveDialog.setIcon(QtWidgets.QMessageBox.Question)
        self.saveDialog.setText("Are you sure you want to select these teachers?")
        self.saveDialog.setInformativeText("Changes can only be reversed once.")
        self.saveDialog.setWindowTitle("Select Teachers?")
        self.saveDialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        retval = self.saveDialog.exec_()
        return retval

    def center(self):
        # frameGeometry() is a PyQt5.QtCore.QRect object which contains a tuple of 4 values:
        # xpos, ypos, width, height
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def remove(self):
        if self.list.currentRow() != -1:
            teacher = self.list.takeItem(self.list.currentRow())
            if teacher.text() in self.absent_teachers:
                self.absent_teachers.remove(teacher.text())
                self.present_teachers.append(teacher.text())
        else:
            self.btnRemoveErrorDialog()

    def btnRemoveErrorDialog(self):
        self.error_msg = QtWidgets.QMessageBox()
        self.error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_msg.setText("Sorry, couldn't find anything to remove.")
        self.error_msg.setWindowTitle("Nothing to Remove")
        self.error_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.error_msg.exec_()

    def btnOutputErrorDialog(self):
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_dialog.setText("Sorry, can't output anything because nothing was selected.")
        self.error_dialog.setWindowTitle("Nothing to Output")
        self.error_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.error_dialog.exec_()

    def add_teacher(self):
        absent_teacher = self.entry.text().upper()

        if absent_teacher not in self.present_teachers:
            if absent_teacher == '':
                self.btnAddErrorDialog(True)
            else:
                self.btnAddErrorDialog()
            self.entry.clear()
            self.entry.setFocus()
        elif absent_teacher not in self.absent_teachers:
            self.list.addItem(absent_teacher)
            self.absent_teachers.append(absent_teacher)
            self.present_teachers.remove(absent_teacher)
            self.entry.clear()

    def btnAddErrorDialog(self, nothing_entered=False):
        self.error_msg = QtWidgets.QMessageBox()
        self.error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        if nothing_entered:
            self.error_msg.setText("Nothing entered.")
        else:
            self.error_msg.setText("Sorry, couldn't find the teacher you were looking for.")
        self.error_msg.setInformativeText("Please try again.")
        self.error_msg.setWindowTitle("Invalid Input")
        self.error_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.error_msg.exec_()

    def btnCloseInformationDialog(self):
        self.information_msg = QtWidgets.QMessageBox()
        self.information_msg.setIcon(QtWidgets.QMessageBox.Question)
        self.information_msg.setText("Are you sure you want to exit the program?")
        self.information_msg.setWindowTitle("Exit Program?")
        self.information_msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        retval = self.information_msg.exec_()
        return retval

    def output(self, save=False):
        if self.list.count() > 0:
            for teacher in self.teachers_substituting.keys():
                self.teachers_substituting[teacher][0] = 0
            self.text_output.clear()
            self.absent_teachers.sort()
            self.present_teachers.sort()

            # outputs date on first line
            self.text_output.addItem(str(datetime.date(datetime.now()).strftime(date_format)))

            days = ["day1", "day2", "day3", "day4", "day5"]
            day = days[self.daycbx.currentIndex()]
            self.text_output.addItem(self.daycbx.currentText())
            self.text_output.addItem('')

            counter = 0
            for abs_teacher in self.absent_teachers:
                counter += 1
                self.text_output.addItem(abs_teacher + " :")
                for period in teachers[abs_teacher][day]:
                    self.text_output.addItem(period + ':')
                    teachers_for_current_period = []
                    if day == "day1" and period == "1":
                        self.text_output.addItem('\t'.replace('\t', ' ' * 6) + "Assembly")
                    else:

                        for present_teacher in self.present_teachers:
                            if teachers[abs_teacher][day][period]["availability"] == "unav" and \
                                    teachers[present_teacher][day][period]["availability"] == "free":
                                teachers_for_current_period.append(present_teacher)

                        teachers_for_current_period.sort()

                        if teachers_for_current_period:
                            self.text_output.addItem('\t'.replace('\t', ' ' * 6) + "Teacher(s):")
                            list_item = QtWidgets.QListWidgetItem()
                            cbx = QtWidgets.QComboBox()
                            for teacher in teachers_for_current_period:
                                content = teacher + '(' + str(self.teachers_substituting[teacher][1]) + ')'
                                cbx.addItem(content)

                            pos_bracket = cbx.currentText().find('(')
                            cbx.activated[str].connect(partial(self.ComboChange, lastitem=cbx.currentText()[:pos_bracket]))

                            self.teachers_substituting[cbx.currentText()[:pos_bracket]][0] += 1
                            self.text_output.addItem(list_item)
                            self.text_output.setItemWidget(list_item, cbx)
                            self.text_output.addItem('\t'.replace('\t', ' ' * 6) + "Class:")
                            self.text_output.addItem(
                                '\t'.replace('\t', ' ' * 17) + teachers[abs_teacher][day][period]["class"])

                        elif teachers[abs_teacher][day][period]["availability"] == "meeting":
                            self.text_output.addItem('\t'.replace('\t', ' ' * 6) + "Meeting")

                        elif teachers[abs_teacher][day][period]["availability"] == "free" or \
                                teachers[abs_teacher][day][period]["availability"] == "upres":
                            self.text_output.addItem('\t'.replace('\t', ' ' * 6) + "No Lesson")

                        else:
                            self.text_output.addItem('\t'.replace('\t', ' ' * 6) + "No Teachers Available")
                if counter < len(self.absent_teachers):
                    self.text_output.addItem('-'*40)
        elif save == False:
            self.btnOutputErrorDialog()

    def ComboChange(self, newitem, lastitem):
        cbx = self.sender()
        if cbx.property("lastitem") != None:
            lastitem = cbx.property("lastitem")

        pos_bracket_lastitem = lastitem.find('(')
        pos_bracket_newitem = newitem.find('(')

        if pos_bracket_lastitem == -1:
            if self.teachers_substituting[lastitem][0] > 0:
                self.teachers_substituting[lastitem][0] -= 1
        else:
            if self.teachers_substituting[lastitem[:pos_bracket_lastitem]][0] > 0:
                self.teachers_substituting[lastitem[:pos_bracket_lastitem]][0] -= 1

        self.teachers_substituting[newitem[:pos_bracket_newitem]][0] += 1

        cbx.setProperty("lastitem", newitem)

    def clear(self):
        self.entry.clear()
        self.list.clear()
        self.present_teachers.extend(self.absent_teachers)
        self.absent_teachers.clear()
        self.text_output.clear()
        self.setTeacherRecords()

    def closeProgram(self):
        if self.btnCloseInformationDialog() == QtWidgets.QMessageBox.Ok:
            sys.exit()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.setWindowIcon(QtGui.QIcon('Images/SelborneLogo.ico'))

    app.setStyleSheet(open("style.css").read())

    win.show()
    sys.exit(app.exec_())


window()
