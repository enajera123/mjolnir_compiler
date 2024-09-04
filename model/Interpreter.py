from model.RuntimeResult import RuntimeResult
from utils.law import LAW
from model.Number import Number


class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
            Number(node.token.value).set_position(node.start_position, node.final_position)
        )

    def visit_BinaryOperatorNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res
        if node.operator_token.type == LAW.SUM:
            result, error = left.added_to(right)
        elif node.operator_token.type == LAW.SUB:
            result, error = left.subbed_by(right)
        elif node.operator_token.type == LAW.MUL:
            result, error = left.multed_by(right)
        elif node.operator_token.type == LAW.DIV:
            result, error = left.dived_by(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_position(node.start_position, node.final_position))

    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res
        error = None
        if node.operator_token.type == LAW.SUM:
            number, error = number.multed_by(Number(1))
        elif node.operator_token.type == LAW.SUB:
            number, error = number.multed_by(Number(-1))
        if error:
            return res.failure(error)
        else:
            return res.success(number.set_position(node.start_position, node.pos_end))
