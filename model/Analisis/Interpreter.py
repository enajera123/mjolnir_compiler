from typing import Union
from model.RuntimeResult import RuntimeResult
from model.Node import *
from utils.law import LAW
from model.Number import Number


class Interpreter:
    def visit(
        self,
        node: Union[NumberNode, UnaryOperatorNode, BinaryOperatorNode],
    ):
        method_name = f"{type(node).__name__}"
        visitor = getattr(self, method_name, self.default)
        return visitor(node)

    def default(
        self,
        node: Union[NumberNode, UnaryOperatorNode, BinaryOperatorNode],
    ):
        raise Exception(f"No {type(node).__name__} defined")

    def AccessVariableNode(self, node: AccessVariableNode):#Must be the same name as the class
        res = RuntimeResult()
        variable_name = node.variable_token.value
        value = LAW.SYMBOL_TABLE.get(variable_name)
        if value == None:
            return res.failure(
                RuntimeError(
                    node.start_position,
                    node.final_position,
                    f"Variable {variable_name} is not defined",
                )
            )
        return res.success(value)

    def AssignVariableNode(self, node: AssignVariableNode):
        res = RuntimeResult()
        variable_name = node.variable_name.value
        value = res.register(self.visit(node.value_node))
        if res.error:
            return res
        LAW.SYMBOL_TABLE.set(variable_name, value)
        return res.success(value)

    def NumberNode(
        self,
        node: NumberNode,
    ):
        return RuntimeResult().success(
            Number(node.token.value).set_position(
                node.start_position, node.final_position
            )
        )

    def BinaryOperatorNode(
        self,
        node: BinaryOperatorNode,
    ):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node))
        if res.error:
            return res
        if node.operator_token.type == LAW.SUM:
            result, error = left.sum(right)
        elif node.operator_token.type == LAW.SUB:
            result, error = left.sub(right)
        elif node.operator_token.type == LAW.MUL:
            result, error = left.mul(right)
        elif node.operator_token.type == LAW.DIV:
            result, error = left.div(right)
        if error:
            return res.failure(error)
        else:
            return res.success(
                result.set_position(node.start_position, node.final_position)
            )

    def UnaryOperatorNode(
        self,
        node: UnaryOperatorNode,
    ):
        res = RuntimeResult()
        number = res.register(self.visit(node.node))
        if res.error:
            return res
        error = None
        if node.operator_token.type == LAW.SUM:
            number, error = number.mul(Number(1))
        elif node.operator_token.type == LAW.SUB:
            number, error = number.multed_by(Number(-1))
        if error:
            return res.failure(error)
        else:
            return res.success(
                number.set_position(node.start_position, node.final_position)
            )
