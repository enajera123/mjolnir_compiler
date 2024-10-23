class VarAccessNode:
    def __init__(self, var_name_tok, access_nodes=None):
        self.var_name_tok = var_name_tok
        self.access_nodes = access_nodes or []

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end
        if self.access_nodes:
            self.pos_end = self.access_nodes[-1].pos_end

    def __repr__(self):
        return f'(Var: {self.var_name_tok}, Access: {self.access_nodes})'