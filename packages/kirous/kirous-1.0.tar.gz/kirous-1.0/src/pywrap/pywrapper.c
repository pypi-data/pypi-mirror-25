// wrapper imports
#include "pywrapper.h"
#include "pyscreenwrapper.h"
#include "pycolorwrapper.h"
#include "pykeyboardwrapper.h"

// core includes
#include "../core/colors.h"
#include "../core/keyboard.h"
#include "../core/screen.h"


/**
 * 
 */
static PyMethodDef kirous_methods[] = {
	// screen functions
	{"screen_init", (PyCFunction) pywrap_screen_init, METH_VARARGS, NULL},
	{"screen_get_size", (PyCFunction) pywrap_screen_get_size, METH_NOARGS, NULL},
	{"screen_set", (PyCFunction) pywrap_screen_set, METH_VARARGS, NULL},
	{"screen_stradd", (PyCFunction) pywrap_screen_stradd, METH_VARARGS, NULL},
	{"screen_draw", (PyCFunction) pywrap_screen_draw, METH_NOARGS, NULL},
	{"screen_clear", (PyCFunction) pywrap_screen_clear, METH_VARARGS, NULL},
	{"fatal", (PyCFunction) pywrap_fatal, METH_VARARGS, NULL},
	// keyboard functions
	{"getch", (PyCFunction) pywrap_getch, METH_NOARGS, NULL},
	// sentinel
	{NULL, NULL, 0, NULL}
};


/**
 * 
 */
static struct PyModuleDef module_definition = {
	PyModuleDef_HEAD_INIT,
	"kirous",
	NULL,
	sizeof(module_state),
	kirous_methods,
	NULL,
	NULL,
	NULL,
	NULL
};


/**
 * \return
 */
PyMODINIT_FUNC PyInit_kirous(void) {
	PyObject* module;
	
	module = PyModule_Create(&module_definition);
	
	if(module == NULL) {
		return NULL;
	}
	
	PyObject_SetAttrString(module, "BACKEND_CURSES", Py_BuildValue("i", BACKEND_CURSES));
	PyObject_SetAttrString(module, "BACKEND_DUMMY", Py_BuildValue("i", BACKEND_DUMMY));
	PyObject_SetAttrString(module, "BACKEND_OPENGL", Py_BuildValue("i", BACKEND_OPENGL));
	PyObject_SetAttrString(module, "BACKEND_SERIAL", Py_BuildValue("i", BACKEND_SERIAL));
	
	PyObject_SetAttrString(module, "COLOR_MODE_BINARY", Py_BuildValue("i", COLOR_MODE_BINARY));
	PyObject_SetAttrString(module, "COLOR_MODE_16", Py_BuildValue("i", COLOR_MODE_16));
	
	pywrap_define_colors(module);
	pywrap_define_keys(module);
	
	return module;
}
