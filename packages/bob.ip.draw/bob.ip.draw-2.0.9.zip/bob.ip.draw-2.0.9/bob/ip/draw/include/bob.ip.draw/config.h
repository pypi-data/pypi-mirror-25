/**
 * @author Manuel Guenther <manuel.guenther@idiap.ch>
 * @date Wed Aug 20 12:52:04 CEST 2014
 *
 * @brief General directives for all modules in bob.ip.draw
 */

#ifndef BOB_IP_DRAW_CONFIG_H
#define BOB_IP_DRAW_CONFIG_H

/* Macros that define versions and important names */
#define BOB_IP_DRAW_API_VERSION 0x0200

#ifdef BOB_IMPORT_VERSION

  /***************************************
  * Here we define some functions that should be used to build version dictionaries in the version.cpp file
  * There will be a compiler warning, when these functions are not used, so use them!
  ***************************************/

  #include <Python.h>
  #include <boost/preprocessor/stringize.hpp>

  /**
   * bob.ip.draw c/c++ api version
   */
  static PyObject* bob_ip_draw_version() {
    return Py_BuildValue("{ss}", "api", BOOST_PP_STRINGIZE(BOB_IP_DRAW_API_VERSION));
  }

#endif // BOB_IMPORT_VERSION

#endif /* BOB_IP_DRAW_CONFIG_H */
