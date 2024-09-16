from model.Number import Number


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        # Asign null,false,true values like constants, so always it exits in the table
        self.set("NULL", Number(0))
        self.set("FALSE", Number(0))
        self.set("TRUE", Number(1))

    def get(self, name):
        value = self.symbols.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
