class VarAssignNode:
    def __init__(self, var_name_tok, value_node, access_nodes=None):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.access_nodes = access_nodes or []

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end if self.access_nodes else self.var_name_tok.pos_end
