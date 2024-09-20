from model.Node.ForNode import ForNode
from model.Node.PrintNode import PrintNode
from utils.law import LAW
from model.Error.InvalidSyntaxError import InvalidSyntaxError
from model.Node.BinaryOperatorNode import BinaryOperatorNode
from model.Node.ListNode import ListNode
from model.Node.AccessVariableNode import AccessVariableNode
from model.Node.NumberNode import NumberNode
from model.Node.StringNode import StringNode
from model.Node.AssignVariableNode import AssignVariableNode
from model.Node.UnaryOperatorNode import UnaryOperatorNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(
        self,
    ):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self):
        result = RunResult()
        token = self.current_token
        if token.type in (LAW.SUM, LAW.SUB):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOperatorNode(token, factor))
        elif token.type == LAW.IDENTIFIER:
            result.register(self.advance())
            return result.success(AccessVariableNode(token))
        elif token.type == LAW.STRING:
            result.register(self.advance())
            return result.success(StringNode(token))
        elif token.type in (LAW.NUMBER, LAW.DECIMAL):
            result.register(self.advance())
            return result.success(NumberNode(token))
        elif token.type == LAW.LP:
            result.register(self.advance())
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type == LAW.RP:
                result.register(self.advance())
                return result.success(expression)
            else:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.start_position,
                        self.current_token.final_position,
                        f"Expected ')' Got {self.current_token.type}",
                    )
                )
        return result.failure(
            InvalidSyntaxError(
                token.start_position,
                token.final_position,
                f"Expected int or float, Got {token.type}",
            )
        )

    def term(self):
        return self.binary_operation(self.factor, (LAW.MUL, LAW.DIV))

    def binary_operation(self, function, operations):
        result = RunResult()
        left = result.register(function())
        if result.error:
            return result
        while self.current_token.type in operations:
            operator_token = self.current_token
            result.register(self.advance())
            right = result.register(function())
            if result.error:
                return result
            left = BinaryOperatorNode(left, operator_token, right)
        return result.success(left)

    def compare_expression(self):
        res = RunResult()
        if self.current_token.equals(LAW.KEY, "NOT"):
            operator_token = self.current_token
            self.advance()
            node = res.register(self.compare_expression())
            if res.error:
                return res
            return res.success(UnaryOperatorNode(operator_token, node))
        node = res.register(
            self.binary_operation(
                self.comparison_expresion, (LAW.EQ, LAW.NEQ, LAW.LT, LAW.GT, LAW.LTE, LAW.GTE)
            )
        )

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected int, float, identifier, '+', '-', '(' or 'NOT'",
                )
            )
        return res.success(node)

    def comparison_expresion(self):
        return self.binary_operation(self.term, (LAW.SUM, LAW.SUB))

    def expression(self):
        res = RunResult()
        if self.current_token.equals(LAW.RW, "VAR"):
            res.register(self.advance())
            if self.current_token.type != LAW.IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start_position,
                        self.current_token.final_position,
                        f"Expected identifier Got {self.current_token.type}",
                    )
                )
            var_name = self.current_token
            res.register(self.advance())
            if self.current_token.type != LAW.EQUALS:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start_position,
                        self.current_token.final_position,
                        f"Expected '=' Got {self.current_token.type}",
                    )
                )
            res.register(self.advance())
            value = res.register(self.expression())
            if res.error:
                return res
            return res.success(AssignVariableNode(var_name, value))
        node = res.register(
            self.binary_operation(
                self.compare_expression, ((LAW.KEY, "AND"), (LAW.KEY, "OR"))
            )
        )
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected 'VAR', int, float, identifier, '+', '-', '(' or 'NOT'",
                )
            )
        return res.success(node)

    def lines(self):
        res = RunResult()
        lines = []
        start_position = self.current_token.start_position

        # Saltar líneas vacías o innecesarias al principio del bloque
        while self.current_token.type == LAW.END_LINE:
            res.register(self.advance())

        # Procesar la primera línea del bloque
        line = res.register(self.line())
        if res.error:
            return res
        lines.append(line)

        # Continuar procesando las siguientes líneas hasta encontrar 'END_OF_FILE' o '}'
        while self.current_token.type == LAW.END_LINE or self.current_token.type != LAW.RCB:
            # Saltar cualquier nueva línea o ';'
            while self.current_token.type == LAW.END_LINE:
                res.register(self.advance())

            # Si encontramos '}', terminamos de procesar el bloque
            if self.current_token.type == LAW.RCB:
                break

            # Si encontramos 'END_OF_FILE' (o 'END'), terminamos el archivo
            if self.current_token.type == LAW.END_OF_FILE:
                return res.success(ListNode(lines, start_position, self.current_token.final_position))

            # Procesar la siguiente línea
            line = res.register(self.line())
            if res.error:
                return res
            lines.append(line)

        return res.success(ListNode(lines, start_position, self.current_token.final_position))

    def line(self):
        res = RunResult()
        initial_position = self.current_token.start_position

        # Manejar las palabras reservadas primero
        if self.current_token.equals(LAW.RW, "FOR"):
            return res.register(self.for_expression())
        elif self.current_token.equals(LAW.RW, "PRINT"):
            return res.register(self.print_statement())

        # Si no es una palabra reservada, procesar como una expresión
        expression = res.register(self.expression())
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    f"Expected expression, Got {self.current_token.type}",
                )
            )
        return res.success(expression)

    def run(self):
        res = self.lines()
        if not res.error and self.current_token.type != LAW.END_OF_FILE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    f"Expected '+', '-', '*', or '/' Got {self.current_token.type}",
                )
            )
        return res

    def for_expression(self):
        res = RunResult()

        # Asegurarse de que el token actual es 'FOR'
        if not self.current_token.equals(LAW.RW, "FOR"):
            return res.failure(
                InvalidSyntaxError(self.current_token.start_position, self.current_token.final_position,
                                   "Expected 'FOR'")
            )

        res.register(self.advance())  # Avanzar después de 'FOR'

        # Leer variable de control
        if self.current_token.type != LAW.IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(self.current_token.start_position, self.current_token.final_position,
                                   "Expected variable identifier")
            )
        var_name = self.current_token
        res.register(self.advance())

        # Asegurarse de que el próximo token sea un '='
        if self.current_token.type != LAW.EQUALS:
            return res.failure(
                InvalidSyntaxError(self.current_token.start_position, self.current_token.final_position, "Expected '='")
            )
        res.register(self.advance())

        # Valor inicial de la variable de control
        start_value = res.register(self.expression())
        if res.error:
            return res

        # Asegurarse de que el próximo token sea 'TO'
        if not self.current_token.equals(LAW.RW, "TO"):
            return res.failure(
                InvalidSyntaxError(self.current_token.start_position, self.current_token.final_position,
                                   "Expected 'TO'")
            )
        res.register(self.advance())

        # Valor final
        end_value = res.register(self.expression())
        if res.error:
            return res

        # Leer el 'STEP' si existe
        step_value = None
        if self.current_token.equals(LAW.RW, "STEP"):
            res.register(self.advance())
            step_value = res.register(self.expression())
            if res.error:
                return res

        # Asegúrate de que se abre el bloque con '{'
        if self.current_token.type != LAW.LCB:
            return res.failure(
                InvalidSyntaxError(self.current_token.start_position, self.current_token.final_position, "Expected '{'")
            )
        res.register(self.advance())

        # Leer el cuerpo del ciclo
        body = res.register(self.lines())
        if res.error:
            return res

        # Asegúrate de que se cierra el bloque con '}'
        if self.current_token.type != LAW.RCB:
            return res.failure(
                InvalidSyntaxError(self.current_token.start_position, self.current_token.final_position, "Expected '}'")
            )
        res.register(self.advance())  # Avanzar después de encontrar '}'

        return res.success(
            ForNode(var_name, start_value, end_value, step_value, body, var_name.start_position, body.final_position))

    def print_statement(self):
        res = RunResult()

        if not self.current_token.equals(LAW.RW, "PRINT"):
            return res.failure(
                InvalidSyntaxError(self.current_token.start_position, self.current_token.final_position,
                                   "Expected 'PRINT'")
            )

        res.register(self.advance())  # Avanzar después de 'PRINT'

        value = res.register(self.expression())
        if res.error:
            return res

        return res.success(PrintNode(value))  # Retorna un nodo PrintNode
class RunResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, RunResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
