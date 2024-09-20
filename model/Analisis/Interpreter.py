from typing import Union

from model.Node.AccessVariableNode import AccessVariableNode
from model.Node.AssignVariableNode import AssignVariableNode
from model.Node.BinaryOperatorNode import BinaryOperatorNode
from model.Node.ForNode import ForNode
from model.Node.ListNode import ListNode
from model.Node.PrintNode import PrintNode
from model.Node.StringNode import StringNode
from model.String import String
from model.Node.NumberNode import NumberNode
from model.Node.UnaryOperatorNode import UnaryOperatorNode
from model.RuntimeResult import RuntimeResult
from model.Node import *
from utils.law import LAW
from model.Number import Number


class Interpreter:
    def run(
        self,
        node: Union[NumberNode, UnaryOperatorNode, BinaryOperatorNode],
    ):
        method_name = f"{type(node).__name__}"
        method = getattr(self, method_name, self.default)
        return method(node)

    def default(
        self,
        node: Union[NumberNode, UnaryOperatorNode, BinaryOperatorNode],
    ):
        raise Exception(f"No {type(node).__name__} defined")

    def ListNode(self, node: ListNode):
        res = RuntimeResult()
        elements = []
        for element in node.elements:
            value = res.register(self.run(element))
            if res.error:
                return res
            elements.append(value)
        return res.success(elements)

    def AccessVariableNode(
        self, node: AccessVariableNode
    ):  # Must be the same name as the class
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
        value = res.register(self.run(node.value_node))
        if res.error:
            return res
        LAW.SYMBOL_TABLE.set(variable_name, value)
        return res.success(value)

    def StringNode(self, node: StringNode):
        return RuntimeResult().success(
            String(node.token.value).set_position(
                node.start_position, node.final_position
            )
        )

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
        left = res.register(self.run(node.left_node))
        if res.error:
            return res
        right = res.register(self.run(node.right_node))
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
        elif node.operator_token.type == LAW.EQ:
            result, error = left.equals(right)
        elif node.operator_token.type == LAW.NEQ:
            result, error = left.not_equals(right)
        elif node.operator_token.type == LAW.GT:
            result, error = left.greater_than(right)
        elif node.operator_token.type == LAW.GTE:
            result, error = left.greater_than_equals(right)
        elif node.operator_token.type == LAW.LT:
            result, error = left.less_than(right)
        elif node.operator_token.type == LAW.LTE:
            result, error = left.less_than_equals(right)
        elif node.operator_token.equals(LAW.KEY, "AND"):
            result, error = left.and_expression(right)
        elif node.operator_token.equals(LAW.KEY, "OR"):
            result, error = left.or_expression(right)
        if error:
            return res.failure(error)
        else:
            return res.success(
                result.set_position(node.start_position, node.final_position)
            )

    def ForNode(self, node: ForNode):
        res = RuntimeResult()

        start_value = res.register(self.run(node.start_value))
        if res.error:
            return res
        end_value = res.register(self.run(node.end_value))
        if res.error:
            return res
        step_value = res.register(self.run(node.step_value)) if node.step_value else Number(1)

        i = start_value
        # Usar los valores booleanos para la comparación
        while True:
            condition_met, error = i.less_than(end_value) if step_value.greater_than(Number(0))[0] else i.greater_than(
                end_value)
            if error or not condition_met:
                break

            # Ejecutar el cuerpo del ciclo
            res.register(self.run(node.body_node))
            if res.error:
                return res

            # Actualizar la variable de control
            i, error = i.sum(step_value)
            if error:
                return res.failure(error)

        return res.success(None)

    def PrintNode(self, node: PrintNode):
        value = self.run(node.value).value  # Ejecuta la expresión y obtiene el valor
        print(value)  # Imprime el valor en la consola
        return RuntimeResult().success(None)  # Devuelve un resultado exitoso

    def UnaryOperatorNode(
        self,
        node: UnaryOperatorNode,
    ):
        res = RuntimeResult()
        number = res.register(self.run(node.node))
        if res.error:
            return res
        error = None
        if node.operator_token.type == LAW.SUM:
            number, error = number.mul(Number(1))
        elif node.operator_token.type == LAW.SUB:
            number, error = number.multed_by(Number(-1))
        elif node.operator_token.equals(LAW.KEY, "NOT"):
            number, error = number.not_expression()
        if error:
            return res.failure(error)
        else:
            return res.success(
                number.set_position(node.start_position, node.final_position)
            )
