/**
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Tue 25 Mar 2014 12:57:21 CET
 *
 * @brief General directives for all modules in bob.learn.libsvm
 */

#ifndef BOB_LEARN_LIBSVM_CONFIG_H
#define BOB_LEARN_LIBSVM_CONFIG_H

/* Macros that define versions and important names */
#define BOB_LEARN_LIBSVM_API_VERSION 0x0200

#ifdef BOB_IMPORT_VERSION

  /***************************************
  * Here we define some functions that should be used to build version dictionaries in the version.cpp file
  * There will be a compiler warning, when these functions are not used, so use them!
  ***************************************/

  #include <Python.h>
  #include <boost/preprocessor/stringize.hpp>
  #include <svm.h>

  /**
   * Describes the libsvm version
   */
  static PyObject* get_libsvm_version() {
    boost::format s("%d.%d");
    s % (LIBSVM_VERSION / 100) % (LIBSVM_VERSION % 100);
    return Py_BuildValue("s", s.str().c_str());
  }

  /**
   * bob.learn.libsvm c/c++ api version
   */
  static PyObject* bob_learn_libsvm_version() {
    return Py_BuildValue("{ss}", "api", BOOST_PP_STRINGIZE(BOB_LEARN_LIBSVM_API_VERSION));
  }

#endif // BOB_IMPORT_VERSION

#endif /* BOB_LEARN_LIBSVM_CONFIG_H */
