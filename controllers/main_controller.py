from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextCharFormat, QColor, QSyntaxHighlighter
from PyQt5.QtCore import QEventLoop, QRegExp
from main import run
import sys
import os
from models.StreamRedirector import StreamRedirector
from models.Analysis.Lexer import Lexer
from models.Analysis.Parser import Parser
from models.Constants import KEYWORDS

SYMBOLS = [
    "NIFLHEIM", "LOKI_FALSE", "THOR_TRUE", "MIDGARD_PI", "SAGA",
    "RAGNAR", "RAGNAR_INT", "BALDUR", "IS_TYR", "IS_SKALD",
    "YGGDRASIL_GROW", "FENRIR_BITE", "JORMUNGAND_SIZE", "ODIN_WISDOM"
]

class KeywordHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("orange"))

        symbol_format = QTextCharFormat()
        symbol_format.setForeground(QColor("cyan"))

        for keyword in KEYWORDS:
            pattern = QRegExp(rf'\b{keyword}\b')
            self.highlighting_rules.append((pattern, keyword_format))

        for symbol in SYMBOLS:
            pattern = QRegExp(rf'\b{symbol}\b')
            self.highlighting_rules.append((pattern, symbol_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)

class main_view(QMainWindow):
    def __init__(self):
        self.plain_text = ""
        self.current_file_path = None  # Ruta del archivo actual
        super(main_view, self).__init__()
        uic.loadUi("views/main.ui", self)
        self.initialize_events()
        self.redirect_stdout()
        self.input_buffer = ""
        self.input_field.setVisible(False)
        self.btn_execute.setEnabled(False)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.3)
        self.btn_execute.setGraphicsEffect(opacity_effect)
        self.highlighter = KeywordHighlighter(self.txt_input.document())

    def initialize_events(self):
        # Conectar botones
        self.btn_compile.clicked.connect(self.handler_clicked_btn_compile)
        self.btn_execute.clicked.connect(self.handler_clicked_btn_execute)
        self.txt_input.textChanged.connect(self.handler_text_input)
        self.input_field.returnPressed.connect(self.send_input)

        self.actionAbrir.triggered.connect(self.open_file)
        self.actionGuardar.triggered.connect(self.save_file)
        self.actionGuardar_como.triggered.connect(self.save_file_as)
        self.actionNuevo.triggered.connect(self.new_file)

        self.actionOperaciones_aritm_ticas.triggered.connect(
            lambda: self.load_example("../test/ejemplo_operaciones_aritmeticas.mj"))
        self.actionRetorno_en_funciones.triggered.connect(
            lambda: self.load_example("../test/ejemplo_retorno_en_funciones.mj"))
        self.actionFunci_n_con_m_ltiples_argumentos.triggered.connect(
            lambda: self.load_example("../test/ejemplo_funcion_multiple_args.mj"))
        self.actionFunciones_sin_retorno.triggered.connect(
            lambda: self.load_example("../test/ejemplo_funcion_sin_retorno.mj"))
        self.actionInt.triggered.connect(lambda: self.load_example("../test/ejemplo_int.mj"))
        self.actionString.triggered.connect(lambda: self.load_example("../test/ejemplo_string.mj"))
        self.actionFloat.triggered.connect(lambda: self.load_example("../test/ejemplo_float.mj"))
        self.actionMatriz_2.triggered.connect(lambda: self.load_example("../test/ejemplo_matriz.mj"))
        self.actionFor.triggered.connect(lambda: self.load_example("../test/ejemplo_for.mj"))
        self.actionWhile.triggered.connect(lambda: self.load_example("../test/ejemplo_while.mj"))
        self.actionIf.triggered.connect(lambda: self.load_example("../test/ejemplo_if.mj"))
        self.actionSwitch_2.triggered.connect(lambda: self.load_example("../test/ejemplo_switch.mj"))
        self.actionRune_2.triggered.connect(lambda: self.load_example("../test/ejemplo_rune.mj"))
        self.actionListas.triggered.connect(lambda: self.load_example("../test/ejemplo_listas.mj"))
        self.actionGuardar.setEnabled(False)

    def load_example(self, filename):
        """Carga el ejemplo de un archivo de texto y lo inserta en el campo de texto."""
        try:
            filepath = os.path.join("examples", filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            self.txt_input.setPlainText(content)
            QMessageBox.information(self, "Ejemplo cargado", f"Ejemplo de '{filename}' cargado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el ejemplo: {e}")

    def new_file(self):
        self.txt_input.clear()
        self.current_file_path = None
        self.actionGuardar.setEnabled(False)
        QMessageBox.information(self, "Nuevo archivo", "Se ha creado un nuevo archivo.")

    def save_file(self):
        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w') as file:
                    file.write(self.txt_input.toPlainText())
                QMessageBox.information(self, "Éxito", "Archivo guardado exitosamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo como", "", "Archivos Mjolnir (*.mj);;Todos los archivos (*)", options=options
        )
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.txt_input.toPlainText())
                self.current_file_path = file_path
                self.actionGuardar.setEnabled(True)
                QMessageBox.information(self, "Éxito", "Archivo guardado exitosamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", "", "Archivos Mjolnir (*.mj);;Todos los archivos (*)", options=options
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.txt_input.setPlainText(content)
                self.current_file_path = file_path
                self.actionGuardar.setEnabled(True)
                QMessageBox.information(self, "Éxito", "Archivo cargado exitosamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo: {e}")

    def handler_clicked_btn_compile(self):
        print("compile button clicked")
        self.txt_output.setPlainText("")
        self.compile()

    def handler_clicked_btn_execute(self):
        self.txt_output.setPlainText("")
        results, error = run("<valhalla>", self.plain_text)
        if error:
            self.txt_output.setPlainText(repr(error))
            return

    def handler_text_input(self):
        self.plain_text = self.txt_input.toPlainText()
        self.btn_execute.setEnabled(False)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.3)
        self.btn_execute.setGraphicsEffect(opacity_effect)

    def handler_clicked_btn_compile(self):
        print("compile button clicked")
        self.txt_output.setPlainText("")
        self.compile()

    def handler_clicked_btn_execute(self):
        self.txt_output.setPlainText("")
        results, error = run("<valhalla>", self.plain_text)
        if error:
            self.txt_output.setPlainText(repr(error))
            return

    def handler_text_input(self):
        self.plain_text = self.txt_input.toPlainText()
        self.btn_execute.setEnabled(False)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.3)
        self.btn_execute.setGraphicsEffect(opacity_effect)

    def redirect_stdout(self):
        self.stdout_redirector = StreamRedirector()
        self.stdout_redirector.stdout.connect(self.append_text)
        self.stdout_redirector.stdin.connect(self.wait_for_input)
        sys.stdout = self.stdout_redirector
        sys.stdin = self

    def wait_for_input(self):
        self.input_field.setVisible(True)
        self.loop = QEventLoop()
        self.loop.exec_()

    def send_input(self):
        input_text = self.input_field.text()
        if input_text:
            self.input_buffer = input_text
            self.input_field.clear()
            if self.loop.isRunning():
                self.loop.exit()
        self.input_field.setVisible(False)

    def readline(self):
        self.input_buffer = None
        self.wait_for_input()
        return self.input_buffer

    def append_text(self, text):
        self.txt_output.append(text.strip())

    def compile(self):
        text = self.plain_text
        lexer = Lexer("<valhalla>", text)
        tokens, error = lexer.make_tokens()
        if error:
            print(repr(error))
            return
        parser = Parser(tokens=tokens)
        tree = parser.parse()
        if tree.error:
            print(repr(tree.error))
            return
        print("Code compiled successfully")
        self.btn_execute.setEnabled(True)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(1)
        self.btn_execute.setGraphicsEffect(opacity_effect)
