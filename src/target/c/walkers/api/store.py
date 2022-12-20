from base import APIWalker


class StoreAPIWalker(APIWalker):
    def __init__(self, prefix, root_nodes, source_dir):
        super.__init__(prefix, root_nodes, source_dir, ['store'])
