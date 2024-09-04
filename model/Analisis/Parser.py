from utils.law import LAW
from model.Error.InvalidSyntaxError import InvalidSyntaxError
from model.Node.BinaryOperatorNode import BinaryOperatorNode
from model.Node.AccessVariableNode import AccessVariableNode
from model.Node.NumberNode import NumberNode
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
        result = ParseResult()
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
        result = ParseResult()
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

    def expression(self):
        res = ParseResult()
        if self.current_token.equals(LAW.RW,"VAR"):
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
        return self.binary_operation(self.term, (LAW.SUM, LAW.SUB))
        

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != LAW.END_OF_FILE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start_position,
                    self.current_token.final_position,
                    f"Expected '+', '-', '*', or '/' Got {self.current_token.type}",
                )
            )
        return res


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
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
