
import self as self
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import difflib
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher

import sys
import platform
import os
from os import path

from pyqt5_plugins.examplebuttonplugin import QtGui

# AUTO-LIVE
FROM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))
FROM_TRUECLASS, _ = loadUiType(path.join(path.dirname(__file__), "trueMain.ui"))

counter = 0


def calculate_similarity_ratio(text1, text2):
    diff = difflib.SequenceMatcher(None, text1, text2)
    similarity_ratio = diff.ratio()
    return similarity_ratio

# APP TRUEMAIN
class MainWindow(QMainWindow, FROM_TRUECLASS):
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
    #TITLE + ICON##################################################################
        self.setWindowTitle("Plagiat Scanner")
        self.setWindowIcon(QtGui.QIcon('scanner.png'))
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)
    #BUTTON TO PAGE################################################################
        self.home_btn_2.clicked.connect(self.showHome)
        self.compare_btn_2.clicked.connect(self.showCompare)
        self.online_btn_2.clicked.connect(self.showOnline)
        self.maybe_btn_2.clicked.connect(self.showWhat)
        self.setting_btn_2.clicked.connect(self.showSettings)
    #IMPORT DOCUMENT###############################################################
        self.import_btn1.clicked.connect(self.import_file)
        self.import_btn2.clicked.connect(self.import_file2)
        self.import_btn1_2.clicked.connect(self.import_file3)
    #DELETE########################################################################
        self.delete_btn1.clicked.connect(self.delete_text)
        self.delete_btn2.clicked.connect(self.delete_text1)
        self.delete_btn1_2.clicked.connect(self.delete_text1_2)
########################################################################################################################
        self.scan_btn_3.clicked.connect(self.detect_plagiarism)
########################################################################################################################
        self.scan_btn_2.clicked.connect(self.detect_plagiarism2)
    def showHome(self):
        self.stackedWidget.setCurrentIndex(0)
    def showCompare(self):
        self.stackedWidget.setCurrentIndex(1)
    def showOnline(self):
        self.stackedWidget.setCurrentIndex(2)
    def showWhat(self):
        self.stackedWidget.setCurrentIndex(3)
    def showSettings(self):
        self.stackedWidget.setCurrentIndex(4)
########################################################################################################################
    def import_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)')

        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
                self.pte1.setPlainText(text)
                self.statusBar().showMessage(f'File "{file_name}" imported successfully.')
                QTimer.singleShot(3000, self.clear_status_bar)
    def import_file2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)')

        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
                self.pte2.setPlainText(text)
                self.statusBar().showMessage(f'File "{file_name}" imported successfully.')
                QTimer.singleShot(3000, self.clear_status_bar)
    def import_file3(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)')

        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
                self.pte1_2.setPlainText(text)
                self.statusBar().showMessage(f'File "{file_name}" imported successfully.')
                QTimer.singleShot(3000, self.clear_status_bar)
########################################################################################################################
    def delete_text(self):
        self.pte1.clear()
        self.statusBar().showMessage('Text deleted successfully.')
        QTimer.singleShot(3000, self.clear_status_bar)
    def delete_text1(self):
        self.pte2.clear()
        self.statusBar().showMessage('Text deleted successfully.')
        QTimer.singleShot(3000, self.clear_status_bar)
    def delete_text1_2(self):
        self.pte1_2.clear()
        self.statusBar().showMessage('Text deleted successfully.')
        QTimer.singleShot(3000, self.clear_status_bar)
########################################################################################################################
    def clear_status_bar(self):
        self.statusBar().clearMessage()
########################################################################################################################

    def detect_plagiarism(self):
        text1 = self.pte1.toPlainText()
        text2 = self.pte2.toPlainText()

        if text1 and text2:
            similarity_ratio = calculate_similarity_ratio(text1, text2)
            self.highlight_similarity(text1, text2)
            self.result_label.setText('Similarity: {:.2f}%'.format(similarity_ratio * 100))
        else:
            self.result_label.setText('Entrez les deux textes.!')

    def highlight_similarity(self, text1, text2):
        self.pte1.clear()
        self.pte2.clear()

        diff = difflib.SequenceMatcher(None, text1, text2)
        opcodes = diff.get_opcodes()

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                self.pte1.insertHtml('<span style="background-color: #bfccb5;">{}</span>'.format(text1[i1:i2]))
                self.pte2.insertHtml('<span style="background-color: #bfccb5;">{}</span>'.format(text2[j1:j2]))
            elif tag == 'replace':
                self.pte1.insertHtml('<span >{}</span>'.format(text1[i1:i2]))
                self.pte2.insertHtml('<span >{}</span>'.format(text2[j1:j2]))

            elif tag == 'insert':
                self.pte2.insertHtml('<span >{}</span>'.format(text2[j1:j2]))
########################################################################################################################
    def detect_plagiarism2(self):
        input_text = self.pte1_2.toPlainText()

        if input_text:
            plagiarism_percentages = self.calculate_plagiarism_percentages(input_text)
            self.display_results(plagiarism_percentages)
            #self.pte1_2.insertHtml('<span style="background-color: #bfccb5;">{}</span>'.format(input_text))
            self.pte1_2.selectAll()  # Select all the text in the QTextEdit widget
            self.pte1_2.setTextBackgroundColor(QColor('#bfccb5'))

        else:
            self.result_label2.setText('Please enter the text to check for plagiarism.')

    def calculate_plagiarism_percentages(self, input_text):
        online_sources = [
            'https://fr.wikipedia.org/wiki/Python_(langage)',
            #'https://www.wikipedia.org',  # Wikipedia
            #'https://www.infoplease.com/',
            #'https://www.britannica.com/',
            #'https://www.theguardian.com',
        ]

        plagiarism_percentages = []
        for source_url in online_sources:
            online_text = self.fetch_online_text(source_url)

            if online_text:
                preprocessed_input_text = self.preprocess_text(input_text)
                preprocessed_online_text = self.preprocess_text(online_text)

                plagiarism_percentage = self.calculate_similarity(preprocessed_input_text, preprocessed_online_text)
                plagiarism_percentages.append((source_url, plagiarism_percentage))

        return plagiarism_percentages

    def fetch_online_text(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            online_text = soup.get_text()
            return online_text
        else:
            return ''

    def preprocess_text(self, text):
        processed_text = text.lower()
        return processed_text

    def calculate_similarity(self, input_text, online_text):
        similarity_percentage = 0.0  # Placeholder, replace with the actual calculation
        return similarity_percentage

    def display_results(self, plagiarism_percentages):
        self.result_label2.clear()

        result_text = ""
        for source_url, plagiarism_percentage in plagiarism_percentages:
            result = f'{source_url}: Plagiarism Percentage: 100%\n'
            result_text += result

        self.result_label2.setText(result_text)


# SPLASH MAIN
class MainApp(QMainWindow, FROM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # REMOVE X- BAR TITLE
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # START PROGRESSBAR
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(40)

        self.label_description.setText("<strong>Bienvenue</strong> sur l'application")
        # TEXTS CHANGES
        QTimer.singleShot\
            (2500, lambda: self.label_description.setText("Le vérificateur de <strong>PLAGIAT</strong> le plus fiable"))

        # QTimer.singleShot(4000, lambda: self.label_description.setText
        # ("Logiciel <strong>anti-plagiat</strong>gratuit"))

        self.label_loading.setText("Chargement...")
        # TEXTS CHANGES
        QTimer.singleShot(1500, lambda: self.label_loading.setText("Chargement de données"))
        QTimer.singleShot(3000, lambda: self.label_loading.setText("Chargement d'interface"))
        QTimer.singleShot(5100, lambda: self.label_loading.setText("Chargement Terminé"))

    def progress(self):
        global counter
        # PROGRESSBAR ++
        self.progressBar.setValue(counter)

        # CLOSE MAIN AND OPEN TRUEMAIN
        if counter > 100:
            # STOP TIMER
            self.timer.stop()
            # OPEN TRUEMAIN
            self.main = MainWindow()
            self.main.show()
            # CLOSE MAIN
            self.close()

        # COUNTER++
        counter += 1
def main():

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
