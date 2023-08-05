/**
 * screen.c
 */

// std
#include <stdlib.h>
#include <curses.h>
#include <locale.h>
#include <string.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include <stdint.h>

// core
#include "colors.h"
#include "screen.h"
#include "util.h"

// backends
#include "backend_curses.h"
#include "backend_dummy.h"
#include "backend_opengl.h"
#include "backend_serial.h"


typedef struct _string_queue
{
	dim x;
	dim y;
	uint8_t* string;
	COLOR_CODE bg;
	COLOR_CODE fg;
	struct _string_queue* next;
} string_queue;

static string_queue* string_buffer;


typedef struct _kirous_backend
{
	STATUS (*init)(dim* screen_w, dim* screen_h, COLOR_MODE color_mode);
	STATUS (*pre_draw)(COLOR_CODE** screen, int** bufmask, dim* screen_w, dim* screen_h);
	STATUS (*draw)(dim x, dim y, COLOR_CODE fg, COLOR_CODE bg);
	STATUS (*post_draw)(void);
	STATUS (*fatal)(const char* message);
	STATUS (*end)(void);
	int16_t (*get_char)(void);
	STATUS (*draw_string)(dim x, dim y, const uint8_t* text, COLOR_CODE fg, COLOR_CODE bg);
} kirous_backend;

static BACKEND_CODE kirous_backend_code;
static kirous_backend backend;

static COLOR_MODE kirous_color_mode;

// virtual screen buffer
static COLOR_CODE* kirous_screen;
// mask buffer
static int* kirous_bufmask;

// buffer dimensions
static dim kirous_screen_w;
static dim kirous_screen_h;


/**
 * Terminates the curses session and frees all resources.
 */
static void kirous_screen_end(void)
{
	string_queue* head;
	string_queue* tmp;
	
	backend.end();
	
	// free memory
	if (kirous_screen != nullptr) {
		kirous_free((void*) &kirous_screen);
		kirous_screen = nullptr;
	}
	
	if (kirous_bufmask != nullptr) {
		kirous_free((void*) &kirous_bufmask);
		kirous_bufmask = nullptr;
	}
	
	head = string_buffer;
	while (head != nullptr) {
		tmp = head;
		head = head->next;
		if (tmp != nullptr) {
			kirous_free((void*) &tmp);
			tmp = nullptr;
		}
	}
	
	string_buffer = nullptr;
}


static void signal_handler(int sig)
{
	kirous_screen_end();
	if (sig == SIGINT) {
		exit(EXIT_SUCCESS);
	}
	
	exit(EXIT_FAILURE);
}


/**
 * Initializes the curses session and creates all necessary buffer arrays,
 * that is the screen buffer, the mask buffer and the text buffer.
 * 
 * \param width screen buffer width
 * \param height screen buffer height
 * \return status code
 */
STATUS kirous_screen_init(BACKEND_CODE backend_code, COLOR_MODE color_mode)
{
	// enable unicode support to allow block characters
	setlocale(LC_ALL, "");
	
	kirous_init_exception_handling();
	
	kirous_backend_code = backend_code;
	kirous_color_mode = color_mode;
	
	switch (backend_code) {
		case BACKEND_OPENGL:
			backend = (kirous_backend) {
				backend_opengl_init,
				backend_opengl_pre_draw,
				backend_opengl_draw,
				backend_opengl_post_draw,
				backend_opengl_fatal,
				backend_opengl_end,
				backend_opengl_get_char,
				backend_opengl_draw_string
			};
			break;
		case BACKEND_DUMMY:
			backend = (kirous_backend) {
				backend_dummy_init,
				backend_dummy_pre_draw,
				backend_dummy_draw,
				backend_dummy_post_draw,
				backend_dummy_fatal,
				backend_dummy_end,
				backend_dummy_get_char,
				backend_dummy_draw_string
			};
			break;
		case BACKEND_SERIAL:
			backend = (kirous_backend) {
				backend_serial_init,
				backend_serial_pre_draw,
				backend_serial_draw,
				backend_serial_post_draw,
				backend_serial_fatal,
				backend_serial_end,
				backend_serial_get_char,
				backend_serial_draw_string
			};
			break;
		case BACKEND_CURSES:
		default:
			backend = (kirous_backend) {
				backend_curses_init,
				backend_curses_pre_draw,
				backend_curses_draw,
				backend_curses_post_draw,
				backend_curses_fatal,
				backend_curses_end,
				backend_curses_get_char,
				backend_curses_draw_string
			};
			break;
	}
	
	atexit(kirous_screen_end);
	signal(SIGINT, signal_handler);
	signal(SIGSEGV, signal_handler);
	
	backend.init(&kirous_screen_w, &kirous_screen_h, kirous_color_mode);
	
	// allocate memory for the buffers
	STATUS status = kirous_calloc((void**) &kirous_screen, kirous_screen_w * kirous_screen_h, sizeof(int));
	if (status != RETURN_OK) {
		return status;
	}
	
	status = kirous_calloc((void**) &kirous_bufmask, kirous_screen_w * kirous_screen_h, sizeof(int));
	if (status != RETURN_OK) {
		return status;
	}
	
	// prepare string queue
	status = kirous_malloc((void**) &string_buffer, sizeof(string_queue));
	if (status != RETURN_OK) {
		return status;
	}
	
	*string_buffer = (string_queue) { 0, 0, nullptr, 0, 0, nullptr };
	
	// clear the screen and mask buffers
	kirous_int_array_clear(&kirous_screen, BLACK, kirous_screen_w * kirous_screen_h);
	kirous_int_array_clear(&kirous_bufmask, 1, kirous_screen_w * kirous_screen_h);
	
	return RETURN_OK;
}


/**
 * \return screen width
 */
dim kirous_screen_get_w()
{
	return kirous_screen_w;
}


/**
 * \return screen height
 */
dim kirous_screen_get_h()
{
	return kirous_screen_h;
}


/**
 * Returns the selected pixel's value
 * 
 * \param x x coordinate
 * \param y y coordinate
 * \return pixel color at position (x, y) or negative status code
 */
COLOR_CODE kirous_screen_get(dim x, dim y)
{
	if (x >= 0 && y >= 0 && x < kirous_screen_w && y < kirous_screen_h) {
		return kirous_screen[x + y * kirous_screen_w];
	}
	
	return ERR_PARAM;
}


/**
 * Sets a pixel on the screen buffer.
 * 
 * \param x
 * \param y
 * \param color
 * \return status code
 */
STATUS kirous_screen_set(dim x, dim y, COLOR_CODE color)
{
	if (x >= 0 && y >= 0 && x < kirous_screen_w && y < kirous_screen_h) {
		uint32_t i = (uint32_t) x + (uint32_t) y * (uint32_t) kirous_screen_w;
		kirous_screen[i] = color;
		kirous_bufmask[i] = true;
		
		return RETURN_OK;
	}
	
	return WARN_NOP;
}


/**
 * Appends a string to the string buffer.
 * 
 * \param x
 * \param y
 * \param str nullptr-terminated string
 * \param bg background color
 * \param fg foreground color
 * \return status code
 */
STATUS kirous_screen_stradd(dim x, dim y, const char* str, COLOR_CODE bg, COLOR_CODE fg)
{
	if (x < 0 || y < 0) {
		return ERR_PARAM;
	}
	
	string_queue* tail;
	tail = string_buffer;
	while (tail->next != nullptr) {
		tail = tail->next;
	}

	uint8_t* token;
	uint8_t token_start = 0;
	uint8_t i = 0;
	uint8_t line = 0;
	do {
		for (; i < (uint8_t) strlen(str); i++) {
			if (str[i] == '\n') {
				break;
			}
		}
		token = (uint8_t*) strndup(str + token_start, i - token_start);
		
		if (kirous_malloc((void**) &(tail->next), sizeof(string_queue)) == RETURN_OK) {
			*(tail->next) = (string_queue) { x, y + line, (uint8_t*) strdup((char*) token), bg, fg, nullptr };
			tail = tail->next;
		} else {
			return ERR_MEM_ALLOC;
		}
		
		line++;
		i += 1;
		token_start = i;
	} while (token_start < strlen(str));
	
	return RETURN_OK;
}


/**
 * Writes the screen buffer to the terminal window.
 * 
 * \return status code
 */
STATUS kirous_screen_draw(void)
{
	dim x, y;
	uint32_t i_bg, i_fg;
	COLOR_CODE bg, fg;
	
	string_queue* head;
	string_queue* tmp;
	
	clock_t clock_start, clock_end;
	double delta_t;
	
	clock_start = clock();
	
	backend.pre_draw(&kirous_screen, &kirous_bufmask, &kirous_screen_w, &kirous_screen_h);
	
	if (kirous_backend_code != BACKEND_SERIAL) {
		for (y = 0; y < kirous_screen_h / 2; y++) {
			for (x = 0; x < kirous_screen_w; x++) {
				// draw two buffer rows at once by setting bg and fg colors
				// respectively
				i_bg = x + (y * 2) * kirous_screen_w;
				i_fg = x + (y * 2 + 1) * kirous_screen_w;
				
				if (kirous_bufmask[i_bg] || kirous_bufmask[i_fg] || kirous_backend_code == BACKEND_OPENGL) {
					bg = kirous_screen[i_bg];
					fg = kirous_screen[i_fg];
					kirous_bufmask[i_bg] = 0;
					kirous_bufmask[i_fg] = 0;
					
					backend.draw(x, y, fg, bg);
				}
			}
		}
	}
	
	// draw and clear string buffer
	head = string_buffer->next;
	
	while (head != nullptr) {
		tmp = head;
		
		if (head->string != nullptr) {
			
			backend.draw_string(head->x, head->y, head->string, head->fg, head->bg);
		}
		
		head = head->next;
		
		if (tmp != nullptr) {
			kirous_free((void*) &tmp);
		}
	}
	
	string_buffer->next = nullptr;
	
	backend.post_draw();
	
	clock_end = clock();
	delta_t = (double) (clock_end - clock_start) / (double) CLOCKS_PER_SEC;
	usleep((int) (MS_PER_FRAME - delta_t * 1000) * 1000);
	
	return RETURN_OK;
}

/**
 * Clears the character buffer.
 * Clears the screen buffer with a specified color.
 * 
 * \param color clear color
 * \return status code
 */
STATUS kirous_screen_clear(COLOR_CODE color)
{
	if (kirous_backend_code == BACKEND_CURSES) {
		if (kirous_screen_w != COLS || kirous_screen_h != LINES * 2) {
			return RETURN_OK;
		}
	}
	
	for (dim y = 0; y < kirous_screen_h; y++) {
		for (dim x = 0; x < kirous_screen_w; x++) {
			if (kirous_screen[x + y * kirous_screen_w] != color) {
				kirous_screen[x + y * kirous_screen_w] = color;
				kirous_bufmask[x + y * kirous_screen_w] = true;
			}
		}
	}
	
	return RETURN_OK;
}

/**
 * \param message error message
 */
void kirous_fatal(const char* message)
{
	backend.fatal(message);
	
	exit(EXIT_FAILURE);
}


/**
 * \return keyboard input, -1 if no input given
 */
int16_t kirous_getch()
{
	return backend.get_char();
}
