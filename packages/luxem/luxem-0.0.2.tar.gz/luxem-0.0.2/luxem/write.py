import _luxem
from luxem.struct import Typed


class _ArrayElement(object):
    def __init__(self, item):
        self.item_iter = iter(item)

    def step(self, writer, stack):
        try:
            next_child = next(self.item_iter)
            writer._process(stack, next_child)
            return True
        except StopIteration:
            writer.array_end()
            return False


class _ObjectElement(object):
    def step(self, writer, stack):
        try:
            next_child = next(self.item_iter)
            writer.key(next_child[0])
            writer._process(stack, next_child[1])
            return True
        except StopIteration:
            writer.object_end()
            return False


if hasattr(dict, 'iteritems'):
    def init(self, item):
        self.item_iter = item.iteritems()
    _ObjectElement.__init__ = init
else:
    def init(self, item):
        self.item_iter = iter(item.items())
    _ObjectElement.__init__ = init


class Writer(_luxem.Writer):
    def _process(self, stack, item):
        if isinstance(item, dict):
            self.object_begin()
            stack.append(_ObjectElement(item))
        elif isinstance(item, list):
            self.array_begin()
            stack.append(_ArrayElement(item))
        elif isinstance(item, Typed):
            self.type(item.name)
            self._process(stack, item.value)
        else:
            self.primitive(str(item))

    def element(self, data):
        stack = []
        self._process(stack, data)
        while stack:
            while stack[-1].step(self, stack):
                pass
            stack.pop()
        return self


def dump(dest, value, **kwargs):
    Writer(target=dest, **kwargs).element(value)


def dumps(value, **kwargs):
    w = Writer(**kwargs)
    w.element(value)
    return w.dump()
