from model.Lexer import Lexer

# import sys
# from PyQt5.QtWidgets import QApplication
# from controllers.main_controller import main_view
# # =======================
# # Main
# # =======================

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = main_view()
#     main.show()
#     sys.exit(app.exec_())
while True:
    text = input("mjolnir > ")
    result, error = Lexer.run("<stdin>", text)
    if error:
        print(error)
    else:
        print(result)
