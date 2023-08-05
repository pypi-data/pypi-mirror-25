import _luxem
from luxem.struct import Typed


class Reader(_luxem.Reader):
    def __init__(self):
        self._stack = [(None, None, [])]
        self._current_key = 0
        self._current_type = None

        super(Reader, self).__init__(
            object_begin=self._object_begin,
            object_end=self._pop,
            array_begin=self._array_begin,
            array_end=self._pop,
            key=self._key,
            type=self._type,
            primitive=self._primitive,
        )

    def _push(self, new_key, value):
        key = self._current_key
        self._current_key = new_key
        type = self._current_type
        self._current_type = None
        self._stack.append((key, type, value))

    def _finish(self, value):
        top = self._stack[-1][2]
        if isinstance(top, list):
            if self._current_type is not None:
                value = Typed(self._current_type, value)
                self._current_type = None
            top.append(value)
            self._current_key += 1
        else:
            if self._current_type is not None:
                value = Typed(self._current_type, value)
                self._current_type = None
            top[self._current_key] = value
            self._current_key = None

    def _object_begin(self):
        self._push(None, {})

    def _array_begin(self):
        self._push(0, [])

    def _pop(self):
        self._current_key, self._current_type, value = self._stack.pop()
        self._finish(value)

    def _key(self, data):
        self._current_key = data

    def _type(self, data):
        self._current_type = data

    def _primitive(self, data):
        self._finish(data)


def load(source):
    r = Reader()
    r.feed(source)
    return r._stack[0][2]
