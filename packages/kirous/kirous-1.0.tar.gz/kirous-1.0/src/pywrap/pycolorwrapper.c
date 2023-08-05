#include "pycolorwrapper.h"

// core includes
#include "../core/colors.h"

void pywrap_define_colors(PyObject* module) {
	PyObject_SetAttrString(module, "NONE", Py_BuildValue("i", NONE));
	PyObject_SetAttrString(module, "BLACK", Py_BuildValue("i", BLACK));
	PyObject_SetAttrString(module, "RED", Py_BuildValue("i", RED));
	PyObject_SetAttrString(module, "GREEN", Py_BuildValue("i", GREEN));
	PyObject_SetAttrString(module, "YELLOW", Py_BuildValue("i", YELLOW));
	PyObject_SetAttrString(module, "BLUE", Py_BuildValue("i", BLUE));
	PyObject_SetAttrString(module, "MAGENTA", Py_BuildValue("i", MAGENTA));
	PyObject_SetAttrString(module, "CYAN", Py_BuildValue("i", CYAN));
	PyObject_SetAttrString(module, "WHITE", Py_BuildValue("i", WHITE));
	PyObject_SetAttrString(module, "GRAY", Py_BuildValue("i", GRAY));
	PyObject_SetAttrString(module, "LIGHT_RED", Py_BuildValue("i", LIGHT_RED));
	PyObject_SetAttrString(module, "LIGHT_GREEN", Py_BuildValue("i", LIGHT_GREEN));
	PyObject_SetAttrString(module, "LIGHT_YELLOW", Py_BuildValue("i", LIGHT_YELLOW));
	PyObject_SetAttrString(module, "LIGHT_BLUE", Py_BuildValue("i", LIGHT_BLUE));
	PyObject_SetAttrString(module, "LIGHT_MAGENTA", Py_BuildValue("i", LIGHT_MAGENTA));
	PyObject_SetAttrString(module, "LIGHT_CYAN", Py_BuildValue("i", LIGHT_CYAN));
	PyObject_SetAttrString(module, "DARK_GRAY", Py_BuildValue("i", DARK_GRAY));
}
