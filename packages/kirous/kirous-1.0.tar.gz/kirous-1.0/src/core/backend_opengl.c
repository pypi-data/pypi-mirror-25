/**
 * X11+OpenGL backend.
 */

#ifdef OPENGL_SUPPORT

#include "backend_opengl.h"
#include "colors.h"
#include "util.h"

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <ncurses.h>
#include <time.h>
#include <string.h>

#include <X11/X.h>
#include <X11/Xlib.h>
#include <GL/gl.h>
#include <GL/glx.h>


#define DEFAULT_WIDTH 640
#define DEFAULT_HEIGHT 480
#define BLOCK_SIZE 7


static Display* display;
static Window root;
static XVisualInfo* visual;
static GLint attributes[] = { GLX_RGBA, GLX_DEPTH_SIZE, 24, GLX_DOUBLEBUFFER, None };
static Colormap colormap;
static XSetWindowAttributes xsetwa;
static Window window;
static GLXContext context;
static XWindowAttributes xwa;
static XEvent event;

static GLuint font_base;
static XFontStruct* font;
static unsigned int first, last;

static int32_t input_char;


/**
 * 
 */
STATUS backend_opengl_init(dim* screen_w, dim* screen_h, COLOR_MODE color_mode)
{
	display = XOpenDisplay(NULL);
	
	if (display == NULL) {
		return ERR_GENERAL;
	}
	
	root = DefaultRootWindow(display);
	
	visual = glXChooseVisual(display, 0, attributes);
	
	colormap = XCreateColormap(display, root, visual->visual, AllocNone);
	xsetwa.colormap = colormap;
	xsetwa.event_mask = ExposureMask | KeyPressMask | StructureNotifyMask;
	window = XCreateWindow(display, root, 0, 0, DEFAULT_WIDTH, DEFAULT_HEIGHT, 0, visual->depth,
							InputOutput, visual->visual, CWColormap | CWEventMask, &xsetwa);
	XMapWindow(display, window);
	XStoreName(display, window, "kirous GL Test");
	
	context = glXCreateContext(display, visual, NULL, GL_TRUE);
	glXMakeCurrent(display, window, context);
	
	char fontname[4];
	snprintf(fontname, 4, "%dx*", BLOCK_SIZE);
	font = XLoadQueryFont(display, fontname);
	
	if (!font) {
		font = XLoadQueryFont(display, "fixed");
	}
	
	first = font->min_char_or_byte2;
	last = font->max_char_or_byte2;
	
	font_base = glGenLists(last + 1);
	if (font_base == 0) {
		exit (1);
	}
	
	glXUseXFont(font->fid, first, last - first + 1, font_base + first);
	
	*screen_w = DEFAULT_WIDTH / BLOCK_SIZE;
	*screen_h = DEFAULT_HEIGHT / BLOCK_SIZE;
	
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0.0f, (float) DEFAULT_WIDTH, (float) DEFAULT_HEIGHT, 0.0f, 0.0f, 1.0f);
	glViewport(0, 0, DEFAULT_WIDTH, DEFAULT_HEIGHT);
	
	input_char = 0;
	
	return RETURN_OK;
}


/**
 * 
 */
STATUS backend_opengl_pre_draw(COLOR_CODE** screen, int** bufmask, dim* screen_w, dim* screen_h)
{
	int status;
	
	while(XPending(display)) {
		XNextEvent(display, &event);
		
		switch(event.type) {
			case Expose:
				XGetWindowAttributes(display, window, &xwa);
				glMatrixMode(GL_PROJECTION);
				glLoadIdentity();
				glOrtho(0.0f, (float) xwa.width, (float) xwa.height, 0.0f, 0.0f, 1.0f);
				glViewport(0, 0, xwa.width, xwa.height);
				break;
			
			case KeyPress:
				input_char = XLookupKeysym(&(event.xkey), 0);
				break;
			
			case ConfigureNotify:
				if(event.xconfigure.width / BLOCK_SIZE != *screen_w ||
					event.xconfigure.height / BLOCK_SIZE != *screen_h) {
					*screen_w = event.xconfigure.width / BLOCK_SIZE;
					*screen_h = event.xconfigure.height / BLOCK_SIZE;
					
					status = kirous_recalloc((void**) screen, *screen_w * *screen_h, sizeof(int));
					if (status != RETURN_OK) {
						return status;
					}
					
					status = kirous_recalloc((void**) bufmask, *screen_w * *screen_h, sizeof(int));
					if (status != RETURN_OK) {
						return status;
					}
				}
				break;
			
			case DestroyNotify:
				exit(0);
		}
	}
	
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	
	return RETURN_OK;
}


/**
 * 
 */
STATUS backend_opengl_draw(dim x, dim y, COLOR_CODE fg, COLOR_CODE bg)
{
	float r, g, b;
	
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	
	kirous_color_convert_gl(bg, &r, &g, &b);
	glBegin(GL_QUADS);
		glColor3f(r, g, b);
		glVertex3i(x * BLOCK_SIZE, y * BLOCK_SIZE * 2, 0);
		glVertex3i((x + 1) * BLOCK_SIZE, y * BLOCK_SIZE * 2, 0);
		glVertex3i((x + 1) * BLOCK_SIZE, y * BLOCK_SIZE * 2 + BLOCK_SIZE, 0);
		glVertex3i(x * BLOCK_SIZE, y * BLOCK_SIZE * 2 + BLOCK_SIZE, 0);
	glEnd();
	
	kirous_color_convert_gl(fg, &r, &g, &b);
	glBegin(GL_QUADS);
		glColor3f(r, g, b);
		glVertex3i(x * BLOCK_SIZE, y * BLOCK_SIZE * 2 + BLOCK_SIZE, 0);
		glVertex3i((x + 1) * BLOCK_SIZE, y * BLOCK_SIZE * 2 + BLOCK_SIZE, 0);
		glVertex3i((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE * 2, 0);
		glVertex3i(x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE * 2, 0);
	glEnd();
	
	return RETURN_OK;
}


/**
 * 
 */
STATUS backend_opengl_post_draw()
{
	glXSwapBuffers(display, window);
	
	return RETURN_OK;
}


/**
 * 
 */
STATUS backend_opengl_fatal(const char* message)
{
	fprintf(stderr, "%s\n", message);
	
	return RETURN_OK;
}


/**
 * 
 */
STATUS backend_opengl_end()
{
	return RETURN_OK;
}


/**
 * 
 */
int16_t backend_opengl_get_char()
{
	int16_t ret;
	
	switch (input_char) {
		case XK_Up: ret = KEY_UP; break;
		case XK_Down: ret = KEY_DOWN; break;
		case XK_Left: ret = KEY_LEFT; break;
		case XK_Right: ret = KEY_RIGHT; break;
		case XK_Tab: ret = '\t'; break;
		case XK_Return: ret = '\n'; break;
		default: ret = (int16_t) input_char; break;
	}
	
	input_char = -1;
	
	return ret;
}


/**
 * 
 */
STATUS backend_opengl_draw_string(dim x, dim y, const uint8_t* text, COLOR_CODE fg, COLOR_CODE bg)
{
	uint8_t text_y;
	uint8_t text_w;
	float r, g, b;
	
	text_y = (font->ascent + font->descent);
	text_w = (uint8_t) strlen((char*) text);
	
	// draw bg
	kirous_color_convert_gl(bg, &r, &g, &b);
	glBegin(GL_QUADS);
		glColor3f(r, g, b);
		glVertex3i(x * BLOCK_SIZE, y * BLOCK_SIZE * 2, 0);
		glVertex3i((x + text_w) * BLOCK_SIZE, y * BLOCK_SIZE * 2, 0);
		glVertex3i((x + text_w) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE * 2, 0);
		glVertex3i(x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE * 2, 0);
	glEnd();
	
	// draw text
	kirous_color_convert_gl(fg, &r, &g, &b);
	glColor3f(r, g, b);
	glRasterPos2i(x * BLOCK_SIZE, y * BLOCK_SIZE * 2 + text_y);
	glListBase(font_base);
	glCallLists(text_w, GL_UNSIGNED_BYTE, (unsigned char*) text);
	
	glFlush();
	
	return RETURN_OK;
}

#endif
