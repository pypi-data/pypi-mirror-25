/**
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Tue 01 Oct 2013 15:37:07 CEST
 *
 * @brief Pure python bindings for Blitz Arrays
 */

#define BOB_BLITZ_MODULE
#include <bob.blitz/capi.h>
#include <bob.extension/documentation.h>
#include <structmember.h>

auto array_doc = bob::extension::ClassDoc(
  BOB_EXT_MODULE_PREFIX ".array",
  "A pythonic representation of an N-dimensional ``blitz::Array<T,N>``",
  "Objects of this class hold a pointer to C++ ``blitz::Array<T,N>``. "
  "The C++ data type ``T`` is mapped to a :py:class:`numpy.dtype` object, while the extents and number of dimensions ``N`` are mapped to a shape, similar to what is done for :py:class:`numpy.ndarray` objects.\n\n"
  "Objects of this class can be wrapped in :py:class:`numpy.ndarray` quite efficiently, so that flexible numpy-like operations are possible on its contents. "
  "You can also deploy objects of this class wherever :py:class:`numpy.ndarray`'s may be input."
).add_constructor(
  bob::extension::FunctionDoc(
    "array",
    "Constructs a new :py:class:`bob.blitz.array`",
    "The implementation current supports a maximum of 4 dimensions. "
    "Building an array with more dimensions will raise a :py:exc:`TypeError`. "
    "There are no explicit limits for the size in each dimension, except for the machine's maximum address size.\n\n"
    "The following numpy data types are supported by this library:\n\n"
    " * :py:class:`numpy.bool_`\n"
    " * :py:class:`numpy.int8`\n"
    " * :py:class:`numpy.int16`\n"
    " * :py:class:`numpy.int32`\n"
    " * :py:class:`numpy.int64`\n"
    " * :py:class:`numpy.uint8`\n"
    " * :py:class:`numpy.uint16`\n"
    " * :py:class:`numpy.uint32`\n"
    " * :py:class:`numpy.uint64`\n"
    " * :py:class:`numpy.float32`\n"
    " * :py:class:`numpy.float64`\n"
    " * :py:class:`numpy.float128` (if this architecture suppports it)\n"
    " * :py:class:`numpy.complex64`\n"
    " * :py:class:`numpy.complex128`\n"
    " * :py:class:`numpy.complex256` (if this architecture suppports it)\n",
    true
  )
  .add_prototype("shape, dtype", "")
  .add_parameter("shape", "iterable", "An iterable, indicating the shape of the array to be constructed")
  .add_parameter("dtype", ":py:class:`numpy.dtype` or ``dtype`` convertible object", "The data type of the object to be created")
);

/**
 * Formal initialization of an Array object
 */
static int PyBlitzArray_init(PyBlitzArrayObject* self, PyObject *args,
    PyObject* kwds) {

  /* Parses input arguments in a single shot */
  static const char* const_kwlist[] = {"shape", "dtype", 0};
  static char** kwlist = const_cast<char**>(const_kwlist);

  PyBlitzArrayObject shape;
  PyBlitzArrayObject* shape_p = &shape;
  int type_num = NPY_NOTYPE;

  if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "O&O&", kwlist,
        &PyBlitzArray_IndexConverter, &shape_p,
        &PyBlitzArray_TypenumConverter, &type_num)
      )
    return -1; ///< FAILURE

  /* Checks if none of the shape positions are zero */
  for (Py_ssize_t i=0; i<shape.ndim; ++i) {
    if (shape.shape[i] == 0) {
      PyErr_Format(PyExc_ValueError, "shape values should not be 0, but one was found at position %" PY_FORMAT_SIZE_T "d of input sequence", i);
      return -1; ///< FAILURE
    }
  }

  return PyBlitzArray_SimpleInit(self, type_num, shape.ndim, shape.shape);

}

/**
 * Methods for Sequence operation
 */
static Py_ssize_t PyBlitzArray_len (PyBlitzArrayObject* self) {
  Py_ssize_t retval = 1;
  for (Py_ssize_t i=0; i<self->ndim; ++i) retval *= self->shape[i];
  return retval;
}

static PyObject* PyBlitzArray_getitem(PyBlitzArrayObject* self,
    PyObject* item) {

  if (PyBob_NumberCheck(item)) {

    if (self->ndim != 1) {
      PyErr_Format(PyExc_TypeError, "expected tuple for accessing %" PY_FORMAT_SIZE_T "dD array", self->ndim);
      return 0;
    }

    // if you get to this point, the user has passed single number
    Py_ssize_t k = PyNumber_AsSsize_t(item, PyExc_IndexError);
    return PyBlitzArray_GetItem(self, &k);

  }

  if (PySequence_Check(item)) {

    if (self->ndim != PySequence_Fast_GET_SIZE(item)) {
      PyErr_Format(PyExc_TypeError, "expected tuple of size %" PY_FORMAT_SIZE_T "d for accessing %" PY_FORMAT_SIZE_T "dD array", self->ndim, self->ndim);
      return 0;
    }

    // if you get to this point, then the input tuple has the same size
    PyBlitzArrayObject shape;
    PyBlitzArrayObject* shape_p = &shape;
    if (!PyBlitzArray_IndexConverter(item, &shape_p)) return 0;
    return PyBlitzArray_GetItem(self, shape.shape);

  }

  PyErr_Format(PyExc_TypeError, "%s(@%" PY_FORMAT_SIZE_T "d,'%s') indexing requires a single integers (for 1D arrays) or sequences, for any rank size", Py_TYPE(self)->tp_name, self->ndim, PyBlitzArray_TypenumAsString(self->type_num));
  return 0;
}

static int PyBlitzArray_setitem(PyBlitzArrayObject* self, PyObject* item,
    PyObject* value) {

  if (PyBob_NumberCheck(item)) {

    if (self->ndim != 1) {
      PyErr_Format(PyExc_TypeError, "expected sequence for accessing %s(@%" PY_FORMAT_SIZE_T "d,'%s'", Py_TYPE(self)->tp_name, self->ndim, PyBlitzArray_TypenumAsString(self->type_num));
      return -1;
    }

    // if you get to this point, the user has passed single number
    Py_ssize_t k = PyNumber_AsSsize_t(item, PyExc_IndexError);
    return PyBlitzArray_SetItem(self, &k, value);

  }

  if (PySequence_Check(item)) {

    if (self->ndim != PySequence_Fast_GET_SIZE(item)) {
      PyErr_Format(PyExc_TypeError, "expected sequence of size %" PY_FORMAT_SIZE_T "d for accessing %s(@%" PY_FORMAT_SIZE_T "d,'%s')", PySequence_Fast_GET_SIZE(item), Py_TYPE(self)->tp_name, self->ndim, PyBlitzArray_TypenumAsString(self->type_num));
      return -1;
    }

    // if you get to this point, then the input tuple has the same size
    PyBlitzArrayObject shape;
    PyBlitzArrayObject* shape_p = &shape;
    if (!PyBlitzArray_IndexConverter(item, &shape_p)) return 0;
    return PyBlitzArray_SetItem(self, shape.shape, value);

  }

  PyErr_Format(PyExc_TypeError, "%s(@%" PY_FORMAT_SIZE_T "d,'%s') assignment requires a single integers (for 1D arrays) or sequences, for any rank size", Py_TYPE(self)->tp_name, self->ndim, PyBlitzArray_TypenumAsString(self->type_num));
  return -1;
}

static PyMappingMethods PyBlitzArray_mapping = {
    (lenfunc)PyBlitzArray_len,
    (binaryfunc)PyBlitzArray_getitem,
    (objobjargproc)PyBlitzArray_setitem,
};


auto as_ndarray = bob::extension::FunctionDoc(
  "as_ndarray",
  ":py:class:`numpy.ndarray` accessor",
  "This function wraps this array as a :py:class:`numpy.ndarray`. "
  "If ``dtype`` is given and the current data type is not the same, then forces the creation of a copy conforming to the require data type, if possible.",
  true
)
.add_prototype("[dtype]", "array")
.add_parameter("dtype", ":py:class:`numpy.dtype` or dtype convertible object", "[optional] The data type of the array to create")
.add_return("array", ":py:class:`numpy.ndarray`", "This array converted to a :py:class`numpy.ndarray`")
;
auto __array__ = as_ndarray.clone("__array__");
static PyObject* PyBlitzArray_AsNumpyArrayPrivate(PyBlitzArrayObject* self,
    PyObject* args, PyObject* kwds) {

  /* Parses input arguments in a single shot */
  static const char* const_kwlist[] = {"dtype", 0};
  static char** kwlist = const_cast<char**>(const_kwlist);

  PyArray_Descr* dtype = 0;

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&", kwlist,
        &PyArray_DescrConverter2, &dtype)) return 0;

  return PyBlitzArray_AsNumpyArray(self, dtype);

}


auto cast = bob::extension::FunctionDoc(
  "cast",
  "Casts an existing array into a (possibly) different data type, without changing its shape",
  "If the data type matches the current array's data type, then a new view to the same array is returned. "
  "Otherwise, a new array is allocated and returned.",
  true
)
.add_prototype("dtype", "array")
.add_parameter("dtype", ":py:class:`numpy.dtype` or dtype convertible object", "The data type to convert this array into")
.add_return("array", ":py:class:`bob.blitz.array`", "This array converted to the given data type")
;
static PyObject* PyBlitzArray_SelfCast(PyBlitzArrayObject* self, PyObject* args, PyObject* kwds) {

  /* Parses input arguments in a single shot */
  static const char* const_kwlist[] = {"dtype", 0};
  static char** kwlist = const_cast<char**>(const_kwlist);

  int type_num = NPY_NOTYPE;

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "O&", kwlist,
        &PyBlitzArray_TypenumConverter, &type_num)) return 0;

  return PyBlitzArray_Cast(self, type_num);

}

static PyMethodDef PyBlitzArray_methods[] = {
    {
      as_ndarray.name(),
      (PyCFunction)PyBlitzArray_AsNumpyArrayPrivate,
      METH_VARARGS|METH_KEYWORDS,
      as_ndarray.doc()
    },
    {
      __array__.name(),
      (PyCFunction)PyBlitzArray_AsNumpyArrayPrivate,
      METH_VARARGS|METH_KEYWORDS,
      __array__.doc()
    },
    {
      cast.name(),
      (PyCFunction)PyBlitzArray_SelfCast,
      METH_VARARGS|METH_KEYWORDS,
      cast.doc()
    },
    {0}  /* Sentinel */
};

/* Property API */
auto shape = bob::extension::VariableDoc(
  "shape",
  "tuple",
  "A tuple indicating the shape of this array (in **elements**)"
);

auto stride = bob::extension::VariableDoc(
  "stride",
  "tuple",
  "A tuple indicating the strides of this array (in **bytes**)"
);

auto dtype = bob::extension::VariableDoc(
  "dtype",
  ":py:class:`numpy.dtype`",
  "The data type for every element in this array"
);

auto writeable = bob::extension::VariableDoc(
  "writeable",
  "bool",
  "A flag, indicating if this array is writeable"
);

auto base = bob::extension::VariableDoc(
  "base",
  "object",
  "If the memory of this array is borrowed from some other object, this is it"
);

static PyGetSetDef PyBlitzArray_getseters[] = {
    {
      dtype.name(),
      (getter)PyBlitzArray_PyDTYPE,
      0,
      dtype.doc(),
      0,
    },
    {
      shape.name(),
      (getter)PyBlitzArray_PySHAPE,
      0,
      shape.doc(),
      0,
    },
    {
      stride.name(),
      (getter)PyBlitzArray_PySTRIDE,
      0,
      stride.doc(),
      0,
    },
    {
      writeable.name(),
      (getter)PyBlitzArray_PyWRITEABLE,
      0,
      writeable.doc(),
      0,
    },
    {
      base.name(),
      (getter)PyBlitzArray_PyBASE,
      0,
      base.doc(),
      0,
    },
    {0}  /* Sentinel */
};

/* Stringification */
static PyObject* PyBlitzArray_str(PyBlitzArrayObject* o) {
  PyObject* nd = PyBlitzArray_AsNumpyArray(o, 0);
  if (!nd) {
    PyErr_Print();
    PyErr_SetString(PyExc_RuntimeError, "could not convert array into numpy ndarray for str() method call");
    return 0;
  }
  PyObject* retval = PyObject_Str(nd);
  Py_DECREF(nd);
  return retval;
}

/* Representation */
static PyObject* PyBlitzArray_repr(PyBlitzArrayObject* o) {
  switch (o->ndim) {
    case 1:
      return
        PyString_FromFormat
          ("%s(%" PY_FORMAT_SIZE_T "d,'%s')",
          Py_TYPE(o)->tp_name,
          o->shape[0],
          PyBlitzArray_TypenumAsString(o->type_num)
          );
    case 2:
      return
        PyString_FromFormat
          ("%s((%" PY_FORMAT_SIZE_T "d,%" PY_FORMAT_SIZE_T "d),'%s')",
          Py_TYPE(o)->tp_name,
          o->shape[0],
          o->shape[1],
          PyBlitzArray_TypenumAsString(o->type_num)
          );
    case 3:
      return
        PyString_FromFormat
          ("%s((%" PY_FORMAT_SIZE_T "d,%" PY_FORMAT_SIZE_T "d,%" PY_FORMAT_SIZE_T "d),'%s')",
          Py_TYPE(o)->tp_name,
          o->shape[0],
          o->shape[1],
          o->shape[2],
          PyBlitzArray_TypenumAsString(o->type_num)
          );
    case 4:
      return
        PyString_FromFormat
          ("%s((%" PY_FORMAT_SIZE_T "d,%" PY_FORMAT_SIZE_T "d,%" PY_FORMAT_SIZE_T "d,%" PY_FORMAT_SIZE_T "d),'%s')",
          Py_TYPE(o)->tp_name,
          o->shape[0],
          o->shape[1],
          o->shape[2],
          o->shape[3],
          PyBlitzArray_TypenumAsString(o->type_num)
          );
    default:
      return
        PyString_FromFormat
          ("[unsupported] %s(@%" PY_FORMAT_SIZE_T "d,'%s') %" PY_FORMAT_SIZE_T "d elements>",
          Py_TYPE(o)->tp_name,
          o->ndim,
          PyBlitzArray_TypenumAsString(o->type_num),
          PyBlitzArray_len(o)
          );
  }
}

/* Members */
static PyMemberDef PyBlitzArray_members[] = {
    {0}  /* Sentinel */
};

PyTypeObject PyBlitzArray_Type = {
    PyVarObject_HEAD_INIT(0, 0)
    0
};

bool init_BlitzArray(PyObject* module)
{

  // initialize the Gabor wavelet type struct
  PyBlitzArray_Type.tp_name = array_doc.name();
  PyBlitzArray_Type.tp_basicsize = sizeof(PyBlitzArrayObject);
  PyBlitzArray_Type.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
  PyBlitzArray_Type.tp_doc = array_doc.doc();

  // set the functions
  PyBlitzArray_Type.tp_new = PyBlitzArray_New;
  PyBlitzArray_Type.tp_init = reinterpret_cast<initproc>(PyBlitzArray_init);
  PyBlitzArray_Type.tp_dealloc = reinterpret_cast<destructor>(PyBlitzArray_Delete);
  PyBlitzArray_Type.tp_methods = PyBlitzArray_methods;
  PyBlitzArray_Type.tp_members = PyBlitzArray_members;
  PyBlitzArray_Type.tp_getset = PyBlitzArray_getseters;

  PyBlitzArray_Type.tp_str = reinterpret_cast<reprfunc>(PyBlitzArray_str);
  PyBlitzArray_Type.tp_repr = reinterpret_cast<reprfunc>(PyBlitzArray_repr);
  PyBlitzArray_Type.tp_as_mapping = &PyBlitzArray_mapping;


  // check that everyting is fine
  if (PyType_Ready(&PyBlitzArray_Type) < 0)
    return false;

  // add the type to the module
  Py_INCREF(&PyBlitzArray_Type);
  return PyModule_AddObject(module, "array", (PyObject*)&PyBlitzArray_Type) >= 0;
}
