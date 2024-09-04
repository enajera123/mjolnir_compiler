class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        value = self.symbols.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
