from model.Node.ForNode import ForNode
from model.Node.PrintNode import PrintNode
from model.Node.WhileNode import WhileNode
from utils.law import LAW
from model.Error.InvalidSyntaxError import InvalidSyntaxError
from model.Node.BinaryOperatorNode import BinaryOperatorNode
from model.Node.ListNode import ListNode
from model.Node.AccessVariableNode import AccessVariableNode
from model.Node.NumberNode import NumberNode
from model.Node.StringNode import StringNode
from model.Node.AssignVariableNode import AssignVariableNode
from model.Node.UnaryOperatorNode import UnaryOperatorNode
from model.Node.IfNode import IfNode


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
        elif token.equals(LAW.RW, "IF"):
            expression = result.register(self.if_statement())
            if result.error:
                return result
            return result.success(expression)
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
                self.comparison_expresion,
                (LAW.EQ, LAW.NEQ, LAW.LT, LAW.GT, LAW.LTE, LAW.GTE),
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

    def var_expression(self, res):
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

    def expression(self):
        res = RunResult()
        if self.current_token.equals(LAW.RW, "VAR"):
            return self.var_expression(res)
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

        while self.current_token.type == LAW.END_LINE:
            res.register(self.advance())

        line = res.register(self.line())
        if res.error:
            return res
        lines.append(line)

        while (
            self.current_token.type == LAW.END_LINE
            or self.current_token.type != LAW.RCB
        ):
            while self.current_token.type == LAW.END_LINE:
                res.register(self.advance())

            if self.current_token.type == LAW.RCB:
                break

            if self.current_token.type == LAW.END_OF_FILE:
                return res.success(
                    ListNode(lines, start_position, self.current_token.final_position)
                )

            line = res.register(self.line())
            if res.error:
                return res
            lines.append(line)

        return res.success(
            ListNode(lines, start_position, self.current_token.final_position)
        )

    def line(self):
        res = RunResult()
        initial_position = self.current_token.start_position
        if self.current_token.equals(LAW.RW, "FOR"):
            return res.register(self.for_expression())
        elif self.current_token.equals(LAW.RW, "PRINT"):
            return res.register(self.print_statement())
        elif self.current_token.equals(LAW.RW, "WHILE"):
            return res.register(self.while_expression())

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

        if not self.current_token.equals(LAW.RW, "FOR"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected 'FOR'",
                )
            )

        res.register(self.advance())

        # Leer variable de control
        if self.current_token.type != LAW.IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected variable identifier",
                )
            )
        var_name = self.current_token
        res.register(self.advance())

        if self.current_token.type != LAW.EQUALS:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected '='",
                )
            )
        res.register(self.advance())

        start_value = res.register(self.expression())
        if res.error:
            return res

        if not self.current_token.equals(LAW.RW, "TO"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected 'TO'",
                )
            )
        res.register(self.advance())

        end_value = res.register(self.expression())
        if res.error:
            return res

        step_value = None
        if self.current_token.equals(LAW.RW, "STEP"):
            res.register(self.advance())
            step_value = res.register(self.expression())
            if res.error:
                return res

        if self.current_token.type != LAW.LCB:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected '{'",
                )
            )
        res.register(self.advance())

        body = res.register(self.lines())
        if res.error:
            return res

        if self.current_token.type != LAW.RCB:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected '}'",
                )
            )
        res.register(self.advance())

        return res.success(
            ForNode(
                var_name,
                start_value,
                end_value,
                step_value,
                body,
                var_name.start_position,
                body.final_position,
            )
        )

    def if_statement(self):
        res = RunResult()
        cases = []
        else_cases = None
        if not self.current_token.equals(LAW.RW, "IF"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    f"Expected 'IF' expression",
                )
            )
        self.advance()
        condition = res.register(self.expression())
        if res.error:
            return res
        if not self.current_token.equals(LAW.RW, "THEN"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Expected 'THEN'",
                )
            )
        self.advance()
        if_condition = res.register(self.expression())
        if res.error:return res
        cases.append((condition, if_condition))
        while self.current_token.equals(LAW.RW, "ELIF"):
            self.advance()
            if_condition = res.register(self.expression())
            if res.error:
                return res
            if not self.current_token.equals(LAW.RW, "THEN"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start_position,
                        self.current_token.final_position,
                        f"Expected 'THEN' expression",
                    )
                )
            self.advance()
            if_condition = res.register(self.expression())
            if res.error:
                return res
            cases.append((condition, if_condition))
        if self.current_token.equals(LAW.RW, "ELSE"):
            self.advance()
            else_cases = res.register(self.expression())
            if res.error:
                return res
        return res.success(IfNode(cases, else_cases))

    def print_statement(self):
        res = RunResult()

        if not self.current_token.equals(LAW.RW, "PRINT"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected 'PRINT'",
                )
            )

        res.register(self.advance())

        value = res.register(self.expression())
        if res.error:
            return res

        return res.success(PrintNode(value))

    def while_expression(self):
        res = RunResult()

        if not self.current_token.equals(LAW.RW, "WHILE"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected 'WHILE'",
                )
            )

        res.register(self.advance())

        if self.current_token.type != LAW.LP:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected '(' after 'WHILE'",
                )
            )
        res.register(self.advance())

        condition = res.register(self.expression())
        if res.error:
            return res

        if self.current_token.type != LAW.RP:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected ')' after condition",
                )
            )
        res.register(self.advance())

        if self.current_token.type != LAW.LCB:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected '{' after condition",
                )
            )
        res.register(self.advance())

        body = res.register(self.lines())
        print(body)
        if res.error:
            return res

        if self.current_token.type != LAW.RCB:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    "Expected '}' after body",
                )
            )
        res.register(self.advance())

        return res.success(
            WhileNode(condition, body, condition.start_position, body.final_position)
        )


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
