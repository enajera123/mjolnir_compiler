from model.Program import Program

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
if __name__ == "__main__":
    text = open("code.mj", "r").read()
    print(text)
    results, error = Program.run("<stdin>", text)
    if error:
        print(error)
    else:
        for result in results:
            print(result)

