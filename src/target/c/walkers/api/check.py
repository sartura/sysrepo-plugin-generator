from .base import APIWalker


class CheckAPIWalker(APIWalker):
    def __init__(self, prefix, root_nodes, source_dir):
        super().__init__(prefix, root_nodes, source_dir, ['check'])
