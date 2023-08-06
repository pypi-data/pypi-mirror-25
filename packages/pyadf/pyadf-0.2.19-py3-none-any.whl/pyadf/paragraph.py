from pyadf.group_node import GroupNode
from pyadf.inline_node_children_mixin import InlineNodeChildrenMixin
from pyadf.inline_nodes.hardbreak import HardBreak

class Paragraph(GroupNode, InlineNodeChildrenMixin):

    def __init__(self, parent=None):
        self.type = 'paragraph'
        super(Paragraph, self).__init__(parent=parent)

    def hardbreak(self):
        self.content.append(HardBreak())
