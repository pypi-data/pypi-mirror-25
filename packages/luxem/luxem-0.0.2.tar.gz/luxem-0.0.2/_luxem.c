#include <Python.h>

#include "c/luxem_rawread.h"
#include "c/luxem_rawwrite.h"

#include <assert.h>

#if PY_MAJOR_VERSION >= 3
#define WRAP_STRING_FROM(pointer, size) PyUnicode_FromStringAndSize(pointer, size)
#define WRAP_STRING_TO(o, pointer, size) do { *pointer = PyUnicode_AsUTF8AndSize(o, (Py_ssize_t *)size); } while (0)
#define WRAP_STRING_CHECK(o) PyUnicode_Check(o)
#define WRAP_BYTES_FROM(pointer, size) PyBytes_FromStringAndSize(pointer, size)
#define WRAP_BYTES_TO(o, pointer, size) PyBytes_AsStringAndSize(o, pointer, (Py_ssize_t *)size)
#define WRAP_BYTES_CHECK(o) PyBytes_Check(o)
#define WRAP_INT_FROM_SIZET(o) PyLong_FromSize_t(o)
#define WRAP_FILE_CHECK(o) compat_file_check(o)
#define WRAP_FILE_INC(o) do {} while (0)
#define WRAP_FILE_DEC(o) do {} while (0)
#define WRAP_FILE_TO(o, mode) compat_file_file(o, mode)

static luxem_bool_t compat_file_check(PyObject *o)
{
	_Py_IDENTIFIER(fileno);
	return PyLong_Check(o) || _PyObject_HasAttrId(o, &PyId_fileno);
}

static FILE* compat_file_file(PyObject *o, char const *mode)
{
	int fd = PyObject_AsFileDescriptor(o);
	if (fd == -1) return NULL;
	FILE* out = fdopen(fd, mode);
	if (out == NULL)
		PyErr_SetString(PyExc_TypeError, "Could not access file.");
	return out;
}

#else
#define WRAP_STRING_FROM(pointer, size) PyString_FromStringAndSize(pointer, size)
#define WRAP_STRING_TO(o, pointer, size) PyString_AsStringAndSize(o, pointer, size)
#define WRAP_STRING_CHECK(o) PyString_Check(o)
#define WRAP_BYTES_FROM(pointer, size) PyString_FromStringAndSize(pointer, size)
#define WRAP_BYTES_TO(o, pointer, size) PyString_AsStringAndSize(o, pointer, size)
#define WRAP_BYTES_CHECK(o) PyString_Check(o)
#define WRAP_INT_FROM_SIZET(o) PyInt_FromSize_t(o)
#define WRAP_FILE_CHECK(o) PyFile_Check(o)
#define WRAP_FILE_INC(o) PyFile_IncUseCount((PyFileObject *)o)
#define WRAP_FILE_DEC(o) PyFile_DecUseCount((PyFileObject *)o)
#define WRAP_FILE_TO(o, mode) PyFile_AsFile(o)
#endif

/* ************************************************************************** */

static char const exception_marker;

/* Reader */
/**********/

typedef struct {
	PyObject_HEAD
	struct luxem_rawread_context_t *context;
	PyObject *object_begin;
	PyObject *object_end;
	PyObject *array_begin;
	PyObject *array_end;
	PyObject *key;
	PyObject *type;
	PyObject *primitive;
	PyThreadState *thread_state;
} Reader;

#define TRANSLATE_VOID_CALLBACK(name) \
static luxem_bool_t translate_rawread_##name(struct luxem_rawread_context_t *context, Reader *user_data) \
{ \
	PyObject *arguments = Py_BuildValue("()"); \
	if (!arguments) return luxem_false; \
	{ \
		PyObject *result = PyEval_CallObject(user_data->name, arguments); \
		Py_DECREF(arguments); \
		if (!result) \
		{ \
			luxem_rawread_get_error(context)->pointer = &exception_marker; \
			luxem_rawread_get_error(context)->length = 0; \
			return luxem_false; \
		} \
		Py_DECREF(result); \
	} \
	return luxem_true; \
}

TRANSLATE_VOID_CALLBACK(object_begin)
TRANSLATE_VOID_CALLBACK(object_end)
TRANSLATE_VOID_CALLBACK(array_begin)
TRANSLATE_VOID_CALLBACK(array_end)

#define TRANSLATE_STRING_CALLBACK(name) \
static luxem_bool_t translate_rawread_##name(struct luxem_rawread_context_t *context, Reader *user_data, struct luxem_string_t const *string) \
{ \
	PyObject *prearguments = WRAP_STRING_FROM(string->pointer == 0 ? (char *) 1 : string->pointer, string->length); \
	PyObject *arguments = Py_BuildValue("(O)", prearguments); \
	Py_DECREF(prearguments); \
	if (!arguments) return luxem_false; \
	{ \
		PyObject *result = PyEval_CallObject(user_data->name, arguments); \
		Py_DECREF(arguments); \
		if (!result) \
		{ \
			luxem_rawread_get_error(context)->pointer = &exception_marker; \
			luxem_rawread_get_error(context)->length = 0; \
			return luxem_false; \
		} \
		Py_DECREF(result); \
	} \
	return luxem_true; \
}

TRANSLATE_STRING_CALLBACK(key)
TRANSLATE_STRING_CALLBACK(type)
TRANSLATE_STRING_CALLBACK(primitive)

static PyObject *Reader_new(PyTypeObject *type, PyObject *positional_args, PyObject *named_args)
{
	Reader *self = (Reader *)type->tp_alloc(type, 0);

	if (self != NULL)
	{
		self->context = luxem_rawread_construct();
		if (!self->context)
		{
			Py_DECREF(self);
			return NULL;
		}

		{
			struct luxem_rawread_callbacks_t *callbacks = luxem_rawread_callbacks(self->context);
			callbacks->user_data = self;
			callbacks->object_begin = (luxem_rawread_void_callback_t)translate_rawread_object_begin;
			callbacks->object_end = (luxem_rawread_void_callback_t)translate_rawread_object_end;
			callbacks->array_begin = (luxem_rawread_void_callback_t)translate_rawread_array_begin;
			callbacks->array_end = (luxem_rawread_void_callback_t)translate_rawread_array_end;
			callbacks->key = (luxem_rawread_string_callback_t)translate_rawread_key;
			callbacks->type = (luxem_rawread_string_callback_t)translate_rawread_type;
			callbacks->primitive = (luxem_rawread_string_callback_t)translate_rawread_primitive;
		}

		self->object_begin = NULL;
		self->object_end = NULL;
		self->array_begin = NULL;
		self->array_end = NULL;
		self->key = NULL;
		self->type = NULL;
		self->primitive = NULL;
		self->thread_state = NULL;
	}

	return (PyObject *)self;
}

static int Reader_init(Reader *self, PyObject *positional_args, PyObject *named_args)
{
	static char *named_args_list[] =
	{
		"object_begin",
		"object_end",
		"array_begin",
		"array_end",
		"key",
		"type",
		"primitive",
		NULL
	};

	if (!PyArg_ParseTupleAndKeywords(
		positional_args,
		named_args,
		"OOOOOOO",
		named_args_list,
		&self->object_begin,
		&self->object_end,
		&self->array_begin,
		&self->array_end,
		&self->key,
		&self->type,
		&self->primitive))
		return -1;

	Py_INCREF(self->object_begin);
	Py_INCREF(self->object_end);
	Py_INCREF(self->array_begin);
	Py_INCREF(self->array_end);
	Py_INCREF(self->key);
	Py_INCREF(self->type);
	Py_INCREF(self->primitive);

	return 0;
}

static void Reader_dealloc(Reader *self)
{
	luxem_rawread_destroy(self->context);
	Py_XDECREF(self->object_begin);
	Py_XDECREF(self->object_end);
	Py_XDECREF(self->array_begin);
	Py_XDECREF(self->array_end);
	Py_XDECREF(self->key);
	Py_XDECREF(self->type);
	Py_XDECREF(self->primitive);
	Py_TYPE(self)->tp_free((PyObject*)self);
}

void format_context_error(struct luxem_rawread_context_t *context)
{
	if (luxem_rawread_get_error(context)->pointer != &exception_marker)
	{
		assert(luxem_rawread_get_error(context)->length > 0);
		{
			struct luxem_string_t const *error = luxem_rawread_get_error(context);
			char const *error_format = "%.*s [offset %lu]";
			int formatted_error_size = snprintf(NULL, 0, error_format, error->length, error->pointer, luxem_rawread_get_position(context));
			assert(formatted_error_size >= 0);
			if (formatted_error_size < 0)
			{
				PyErr_SetString(PyExc_ValueError, "Encountered an exception, then encountered an error while trying to format the exception.");
			}
			else
			{
				formatted_error_size += 1; /* Was returning one too small */
				{
					char *formatted_error = malloc(formatted_error_size);
					snprintf(formatted_error, formatted_error_size, error_format, error->length, error->pointer, luxem_rawread_get_position(context));
					PyErr_SetString(PyExc_ValueError, formatted_error);
					free(formatted_error);
				}
			}
		}
	}
	else
	{
		/* Pass through python exception */
		assert(luxem_rawread_get_error(context)->length == 0);
	}
}

void feed_unlock_gil(struct luxem_rawread_context_t *context, Reader *self)
{
	assert(!self->thread_state);
	self->thread_state = PyEval_SaveThread();
}

void feed_lock_gil(struct luxem_rawread_context_t *context, Reader *self)
{
	assert(self->thread_state);
	PyEval_RestoreThread(self->thread_state);
	self->thread_state = NULL;
}

static PyObject *Reader_feed(Reader *self, PyObject *positional_args, PyObject *named_args)
{
	PyObject *data;
	luxem_bool_t finish = luxem_true;

	static char *named_args_list[] =
	{
		"data",
		"finish",
		NULL
	};

	if (!PyArg_ParseTupleAndKeywords(
		positional_args,
		named_args,
		"O|b",
		named_args_list,
		&data,
		&finish))
		return NULL;

	if (WRAP_BYTES_CHECK(data))
	{
		struct luxem_string_t string;
		size_t eaten = 0;
		WRAP_BYTES_TO(data, (char **)&string.pointer, &string.length);

		if (!luxem_rawread_feed(self->context, &string, &eaten, finish))
		{
			format_context_error(self->context);
			return NULL;
		}

		return WRAP_INT_FROM_SIZET(eaten);
	}
	else if (WRAP_FILE_CHECK(data))
	{
		luxem_bool_t success;
		FILE *file = WRAP_FILE_TO(data, "r");
		WRAP_FILE_INC(data);
		success = luxem_rawread_feed_file(self->context, file, feed_unlock_gil, feed_lock_gil);
		WRAP_FILE_DEC(data);
		if (!success)
		{
			format_context_error(self->context);
			return NULL;
		}

		Py_INCREF(Py_None);
		return Py_None;
	}
	else
	{
		PyErr_SetString(PyExc_TypeError, "luxem.RawReader.feed requires a single bytes or binary file argument.");
		return NULL;
	}
}

static PyMethodDef Reader_methods[] =
{
	{
		"feed",
		(PyCFunction)Reader_feed,
		METH_VARARGS | METH_KEYWORDS,
		"Stream from bytes or binary file argument."
	},
	{NULL}
};

static PyTypeObject ReaderType = {PyObject_HEAD_INIT(NULL) 0};

static luxem_bool_t ReaderType_init(void)
{
	ReaderType.tp_name = "luxem.RawReader";
	ReaderType.tp_basicsize = sizeof(Reader);
	ReaderType.tp_dealloc = (destructor)Reader_dealloc;
	ReaderType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	ReaderType.tp_doc = "Decodes luxem data";
	ReaderType.tp_methods = Reader_methods;
	ReaderType.tp_init = (initproc)Reader_init;
	ReaderType.tp_new = Reader_new;
	return PyType_Ready(&ReaderType) >= 0;
}

/* ************************************************************************** */

/* luxem writer */
/****************/

typedef struct {
	PyObject_HEAD
	struct luxem_rawwrite_context_t *context;
	PyObject *target;
	FILE *file;
} Writer;

static luxem_bool_t translate_rawwrite_write(struct luxem_rawwrite_context_t *context, Writer *user_data, struct luxem_string_t const *string)
{
#if PY_MAJOR_VERSION >= 3
	PyObject *arguments = Py_BuildValue("(y#)", string->pointer, string->length);
#else
	PyObject *arguments = Py_BuildValue("(s#)", string->pointer, string->length);
#endif
	if (!arguments) return luxem_false;
	{
		PyObject *result = PyEval_CallObject(user_data->target, arguments);
		Py_DECREF(arguments);
		if (!result)
		{
			luxem_rawwrite_get_error(context)->pointer = &exception_marker;
			luxem_rawwrite_get_error(context)->length = 0;
			return luxem_false;
		}
		Py_DECREF(result);
	}
	return luxem_true;
}

static PyObject *Writer_new(PyTypeObject *type, PyObject *positional_args, PyObject *named_args)
{
	Writer *self = (Writer *)type->tp_alloc(type, 0);

	if (self != NULL)
	{
		self->context = luxem_rawwrite_construct();
		if (!self->context)
		{
			Py_DECREF(self);
			return NULL;
		}

		self->target = NULL;
		self->file = NULL;
	}

	return (PyObject *)self;
}

static int Writer_init(Writer *self, PyObject *positional_args, PyObject *named_args)
{
	luxem_bool_t pretty = luxem_false, use_spaces = luxem_false;
	int indent_multiple = 1;

	static char *named_args_list[] =
	{
		"target",
		"pretty",
		"use_spaces",
		"indent_multiple",
		NULL
	};

	if (!PyArg_ParseTupleAndKeywords(
		positional_args,
		named_args,
		"|Obbi",
		named_args_list,
		&self->target,
		&pretty,
		&use_spaces,
		&indent_multiple))
		return -1;

	if (self->target)
	{
		Py_INCREF(self->target);
		if (WRAP_FILE_CHECK(self->target))
		{
			self->file = WRAP_FILE_TO(self->target, "w");
			if (self->file == NULL) return -1;
			WRAP_FILE_INC(self->file);
			luxem_rawwrite_set_file_out(self->context, self->file);
		}
		else
			luxem_rawwrite_set_write_callback(self->context, (luxem_rawwrite_write_callback_t)translate_rawwrite_write, self);
	}
	else luxem_rawwrite_set_buffer_out(self->context);

	if (pretty)
		luxem_rawwrite_set_pretty(self->context, use_spaces ? ' ' : '\t', indent_multiple);

	return 0;
}

static void Writer_dealloc(Writer *self)
{
	luxem_rawwrite_destroy(self->context);
	if (self->file != NULL)
	{
		fflush(self->file);
		WRAP_FILE_DEC(self->file);
	}
	Py_XDECREF(self->target);
	Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *translate_void_method(Writer *self, luxem_bool_t (*method)(struct luxem_rawwrite_context_t *))
{
	if (!method(self->context))
	{
		if (luxem_rawwrite_get_error(self->context)->pointer != &exception_marker)
		{
			struct luxem_string_t const *error = luxem_rawwrite_get_error(self->context);
			assert(error->length > 0);
			PyErr_SetObject(PyExc_ValueError, WRAP_STRING_FROM(error->pointer, error->length));
		}
		else
		{
			/* Pass through python exception */
			assert(luxem_rawwrite_get_error(self->context)->length == 0);
		}
		return NULL;
	}

	Py_INCREF((PyObject *)self);
	return (PyObject *)self;
}

static PyObject *Writer_object_begin(Writer *self) { return translate_void_method(self, luxem_rawwrite_object_begin); }
static PyObject *Writer_object_end(Writer *self) { return translate_void_method(self, luxem_rawwrite_object_end); }
static PyObject *Writer_array_begin(Writer *self) { return translate_void_method(self, luxem_rawwrite_array_begin); }
static PyObject *Writer_array_end(Writer *self) { return translate_void_method(self, luxem_rawwrite_array_end); }

static PyObject *translate_string_method(Writer *self, PyObject *positional_args, luxem_bool_t (*method)(struct luxem_rawwrite_context_t *, struct luxem_string_t const *), char const *badargs)
{
	PyObject *argument;

	if (!PyArg_ParseTuple(
		positional_args,
		"O",
		&argument))
		return NULL;

	if (WRAP_STRING_CHECK(argument))
	{
		struct luxem_string_t string;
		WRAP_STRING_TO(argument, (char **)&string.pointer, &string.length);

		if (!method(self->context, &string))
		{
			if (luxem_rawwrite_get_error(self->context)->pointer != &exception_marker)
			{
				struct luxem_string_t const *error = luxem_rawwrite_get_error(self->context);
				assert(error->length > 0);
				PyErr_SetObject(PyExc_ValueError, WRAP_STRING_FROM(error->pointer, error->length));
			}
			else
			{
				/* Pass through python exception */
				assert(luxem_rawwrite_get_error(self->context)->length == 0);
			}
			return NULL;
		}
	}
	else
	{
		PyErr_SetString(PyExc_TypeError, badargs);
		return NULL;
	}

	Py_INCREF((PyObject *)self);
	return (PyObject *)self;
}

static PyObject *Writer_key(Writer *self, PyObject *positional_args)
	{ return translate_string_method(self, positional_args, luxem_rawwrite_key, "luxem.RawWriter.key requires a single string argument."); }
static PyObject *Writer_type(Writer *self, PyObject *positional_args)
	{ return translate_string_method(self, positional_args, luxem_rawwrite_type, "luxem.RawWriter.type requires a single string argument."); }
static PyObject *Writer_primitive(Writer *self, PyObject *positional_args)
	{ return translate_string_method(self, positional_args, luxem_rawwrite_primitive, "luxem.RawWriter.primitive requires a single string argument."); }

static PyObject *Writer_dump(Writer *self)
{
	if (self->target)
	{
		PyErr_SetString(PyExc_TypeError, "luxem.RawWriter.dump can only be used if not using a custom serialize callback for serializing to file.");
		return NULL;
	}
	else
	{
		struct luxem_string_t *rendered = luxem_rawwrite_buffer_render(self->context);
		if (!rendered)
		{
				struct luxem_string_t const *error = luxem_rawwrite_get_error(self->context);
				assert(error->length > 0);
				PyErr_SetObject(PyExc_ValueError, WRAP_STRING_FROM(error->pointer, error->length));
				return NULL;
		}

		PyObject *out = WRAP_BYTES_FROM(rendered->pointer, rendered->length);
		free(rendered);
		return out;
	}
}

static PyMethodDef Writer_methods[] =
{
	{"object_begin", (PyCFunction)Writer_object_begin, METH_NOARGS, "Start a new object."},
	{"object_end", (PyCFunction)Writer_object_end, METH_NOARGS, "End current object."},
	{"array_begin", (PyCFunction)Writer_array_begin, METH_NOARGS, "Start a new array."},
	{"array_end", (PyCFunction)Writer_array_end, METH_NOARGS, "End current array."},
	{"key", (PyCFunction)Writer_key, METH_VARARGS, "Write a key."},
	{"type", (PyCFunction)Writer_type, METH_VARARGS, "Write a type."},
	{"primitive", (PyCFunction)Writer_primitive, METH_VARARGS, "Write a primitive."},
	{"dump", (PyCFunction)Writer_dump, METH_NOARGS, "If serializing to a buffer, returns all rendered data so far."},
	{NULL}
};

static PyTypeObject WriterType = {PyObject_HEAD_INIT(NULL) 0};

static luxem_bool_t WriterType_init(void)
{
	WriterType.tp_name = "luxem.RawWriter";
	WriterType.tp_basicsize = sizeof(Writer);
	WriterType.tp_dealloc = (destructor)Writer_dealloc;
	WriterType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	WriterType.tp_doc = "Encodes luxem data";
	WriterType.tp_methods = Writer_methods;
	WriterType.tp_init = (initproc)Writer_init;
	WriterType.tp_new = Writer_new;
	return PyType_Ready(&WriterType) >= 0;
}

/* ************************************************************************** */

/* luxem module + module entry point */
/*************************************/

static PyObject *translate_to_from_ascii16(PyObject *self, PyObject *positional_args, struct luxem_string_t const *(*function)(struct luxem_string_t const *, struct luxem_string_t *))
{
	PyObject *argument;
	if (!PyArg_ParseTuple(
		positional_args,
		"O",
		&argument))
		return NULL;

	if (WRAP_STRING_CHECK(argument))
	{
		struct luxem_string_t string;
		struct luxem_string_t error;
		struct luxem_string_t const *out;
		PyObject *out_string;
		WRAP_STRING_TO(argument, (char **)&string.pointer, &string.length);
		out = function(&string, &error);
		if (!out)
		{
			PyErr_SetObject(PyExc_ValueError, WRAP_STRING_FROM(error.pointer, error.length));
			return NULL;
		}
		out_string = WRAP_STRING_FROM(out->pointer, out->length);
		free((void *)out);
		return out_string;
	}
	else
	{
		PyErr_SetString(PyExc_TypeError, "A single string argument is required.");
		return NULL;
	}
}

static PyObject *translate_to_ascii16(PyObject *self, PyObject *positional_args)
	{ return translate_to_from_ascii16(self, positional_args, luxem_to_ascii16); }

static PyObject *translate_from_ascii16(PyObject *self, PyObject *positional_args)
	{ return translate_to_from_ascii16(self, positional_args, luxem_from_ascii16); }

static PyMethodDef luxem_methods[] =
{
	{"to_ascii16", (PyCFunction)translate_to_ascii16, METH_VARARGS, "Encode ascii16."},
	{"from_ascii16", (PyCFunction)translate_from_ascii16, METH_VARARGS, "Decode ascii16."},
	{NULL}
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef =
{
	PyModuleDef_HEAD_INIT,
	"_luxem",
	NULL,
	0,
	luxem_methods,
	NULL,
	NULL,
	NULL,
	NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit__luxem(void)

#else
#define INITERROR return

void
init_luxem(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
	if (!ReaderType_init()) return NULL;
	if (!WriterType_init()) return NULL;
	PyObject *module = PyModule_Create(&moduledef);
#else
	if (!ReaderType_init()) return;
	if (!WriterType_init()) return;
	PyObject *module = Py_InitModule3("_luxem", luxem_methods, "luxem C API internal-use module.");
#endif

	if (module == NULL)
		INITERROR;

	Py_INCREF(&ReaderType);
	PyModule_AddObject(module, "Reader", (PyObject *)&ReaderType);
	PyModule_AddObject(module, "Writer", (PyObject *)&WriterType);

#if PY_MAJOR_VERSION >= 3
	return module;
#endif
}
