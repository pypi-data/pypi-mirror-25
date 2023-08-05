#include "pyscreenwrapper.h"

#include <stdio.h>
#include <string.h>

// core includes
#include "../core/screen.h"



PyObject* pywrap_screen_init(PyObject* self, PyObject* args)
{
	BACKEND_CODE backend_code;
	COLOR_MODE color_mode;
	
	int status;
	
	if(!PyArg_ParseTuple(args, "ii", &backend_code, &color_mode)) {
		backend_code = BACKEND_CURSES;
		color_mode = COLOR_MODE_16;
	}
	
	status = kirous_screen_init(backend_code, color_mode);
	return Py_BuildValue("i", status);
}


PyObject* pywrap_screen_get_size(PyObject* self)
{
	return Py_BuildValue("(ii)", kirous_screen_get_w(), kirous_screen_get_h());
}


PyObject* pywrap_screen_set(PyObject* self, PyObject* args)
{
	int x;
	int y;
	int color;
	
	int status;
	
	if (!PyArg_ParseTuple(args, "iii", &x, &y, &color)) {
		return NULL;
	}
	
	status = kirous_screen_set(x, y, color);
	return Py_BuildValue("i", status);
}


PyObject* pywrap_screen_stradd(PyObject* self, PyObject* args)
{
	int x;
	int y;
	const char* str;
	int bg;
	int fg;
	
	int status;
	
	if (!PyArg_ParseTuple(args, "iisii", &x, &y, &str, &bg, &fg)) {
		return NULL;
	}
	
	status = kirous_screen_stradd(x, y, strdup(str), bg, fg);
	return Py_BuildValue("i", status);
}


PyObject* pywrap_screen_draw(PyObject* self)
{
	int status;
	
	status = kirous_screen_draw();
	return Py_BuildValue("i", status);
}


PyObject* pywrap_screen_clear(PyObject* self, PyObject* args)
{
	int color;
	
	int status;
	
	if (!PyArg_ParseTuple(args, "i", &color)) {
		return NULL;
	}
	
	status = kirous_screen_clear(color);
	return Py_BuildValue("i", status);
}


PyObject* pywrap_fatal(PyObject* self, PyObject* args)
{
	const char* message;
	
	if (!PyArg_ParseTuple(args, "s", &message)) {
		return NULL;
	}
	
	kirous_fatal(message);
	return Py_BuildValue("i", RETURN_OK);
}


PyObject* pywrap_getch(PyObject* self)
{
	int c;
	
	c = kirous_getch();
	
	return Py_BuildValue("i", c);
}
