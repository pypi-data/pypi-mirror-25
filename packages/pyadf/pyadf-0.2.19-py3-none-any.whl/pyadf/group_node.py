from pyadf.inline_node_children_mixin import InlineNodeChildrenMixin

from pyadf.inline_nodes.marks.link import Link
from pyadf.inline_nodes.marks.textcolor import TextColor

class GroupNode(object):

    def __init__(self, parent=None):
        self.content = []
        self.parent = parent

    def to_doc(self):
        attrs = self.attrs()
        
        result = {
            'type': self.type,
            'content': [f.to_doc() for f in self.content]
        }

        if (attrs != None):
            result['attrs'] = attrs

        return result

    def attrs(self):
        return None

    def end(self):
        return self.parent

    # these marks apply to the last-used inline node
    def link(self, href, title=None):
        if (self.content == None or len(self.content) == 0):
            raise ValueError('Can\'t apply marks when there is no content to mark.')
        node = Link(href, title)
        self.content[-1].add_mark(node)
        return self

    def textcolor(self, color):
        if (self.content == None or len(self.content) == 0):
            raise ValueError('Can\'t apply marks when there is no content to mark.')
        node = TextColor(color)
        self.content[-1].add_mark(node)
        return self