/**
 * @author Manuel Guenther <manuel.guenther@idiap.ch>
 * @date Thu 21 May 12:31:49 CEST 2015
 *
 * @brief Functionality to provide version information in the python bindings
 */

#ifndef BOB_BLITZ_CONFIG_H
#define BOB_BLITZ_CONFIG_H

/* Define API version */
#define BOB_BLITZ_API_VERSION 0x0202


#ifdef BOB_IMPORT_VERSION

  /***************************************
  * Here we define some functions that should be used to build version dictionaries in the version.cpp file
  * There will be a compiler warning, when these functions are not used, so use them!
  ***************************************/

  #include <bob.blitz/cleanup.h>
  #include <boost/preprocessor/stringize.hpp>
  #include <boost/version.hpp>
  #include <boost/format.hpp>
  #include <blitz/blitz.h>
  #include <string>
  #include <cstdlib>

  /**
   * Python version with which we compiled the extensions
   */
  static PyObject* python_version() {
    boost::format f("%s.%s.%s");
    f % BOOST_PP_STRINGIZE(PY_MAJOR_VERSION);
    f % BOOST_PP_STRINGIZE(PY_MINOR_VERSION);
    f % BOOST_PP_STRINGIZE(PY_MICRO_VERSION);
    return Py_BuildValue("s", f.str().c_str());
  }

  /**
   * Describes the version of Blitz++ library
   */
  static PyObject* blitz_version() {
    return Py_BuildValue("s", BZ_VERSION);
  }

  /**
   * Describes the version of Boost libraries installed
   */
  static PyObject* boost_version() {
    boost::format f("%d.%d.%d");
    f % (BOOST_VERSION / 100000);
    f % (BOOST_VERSION / 100 % 1000);
    f % (BOOST_VERSION % 100);
    return Py_BuildValue("s", f.str().c_str());
  }

  /**
   * Describes the compiler version
   */
  static PyObject* compiler_version() {
  # if defined(__GNUC__) && !defined(__llvm__)
    boost::format f("%s.%s.%s");
    f % BOOST_PP_STRINGIZE(__GNUC__);
    f % BOOST_PP_STRINGIZE(__GNUC_MINOR__);
    f % BOOST_PP_STRINGIZE(__GNUC_PATCHLEVEL__);
    return Py_BuildValue("{ssss}", "name", "gcc", "version", f.str().c_str());
  # elif defined(__llvm__) && !defined(__clang__)
    return Py_BuildValue("{ssss}", "name", "llvm-gcc", "version", __VERSION__);
  # elif defined(__clang__)
    return Py_BuildValue("{ssss}", "name", "clang", "version", __clang_version__);
  # else
    return Py_BuildValue("{ssss}", "name", "unsupported", "version", "unknown");
  # endif
  }

  /**
   * Numpy version
   */
  static PyObject* numpy_version() {
    return Py_BuildValue("{ssss}", "abi", BOOST_PP_STRINGIZE(NPY_VERSION),
        "api", BOOST_PP_STRINGIZE(NPY_API_VERSION));
  }

  /**
   * bob.blitz c/c++ api version
   */
  static PyObject* bob_blitz_version() {
    return Py_BuildValue("{ss}", "api", BOOST_PP_STRINGIZE(BOB_BLITZ_API_VERSION));
  }

  inline int dict_steal(PyObject* d, const char* key, PyObject* value) {
    if (!value) return 0;
    int retval = PyDict_SetItemString(d, key, value);
    Py_DECREF(value);
    return !retval;
  }

#endif // BOB_IMPORT_VERSION

#endif // BOB_BLITZ_CONFIG_H
