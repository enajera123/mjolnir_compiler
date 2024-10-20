class SwitchNode:
    def __init__(self, switch_expr, cases, default_case, pos_start, pos_end):
        self.switch_expr = switch_expr
        self.cases = cases
        self.default_case = default_case
        self.pos_start = pos_start
        self.pos_end = pos_end
