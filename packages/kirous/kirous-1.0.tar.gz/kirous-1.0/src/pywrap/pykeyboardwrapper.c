// wrapper includes
#include "pykeyboardwrapper.h"

// core includes
#include "../core/keyboard.h"

// system includes
#include <curses.h>


void pywrap_define_keys(PyObject* module) {
	PyObject_SetAttrString(module, "KEY_ESCAPE", Py_BuildValue("i", KEY_ESCAPE));
	PyObject_SetAttrString(module, "KEY_RETURN", Py_BuildValue("i", KEY_RETURN));
	PyObject_SetAttrString(module, "KEY_SPACE", Py_BuildValue("i", KEY_SPACE));
	PyObject_SetAttrString(module, "KEY_UP", Py_BuildValue("i", KEY_UP));
	PyObject_SetAttrString(module, "KEY_DOWN", Py_BuildValue("i", KEY_DOWN));
	PyObject_SetAttrString(module, "KEY_LEFT", Py_BuildValue("i", KEY_LEFT));
	PyObject_SetAttrString(module, "KEY_RIGHT", Py_BuildValue("i", KEY_RIGHT));
}

