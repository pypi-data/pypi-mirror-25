/**
 * Curses unicode backend.
 */

#include "backend_curses.h"
#include "colors.h"
#include "util.h"

#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <ncurses.h>
#include <wchar.h>
#include <string.h>
#include <stdio.h>


static wchar_t* UPPER_HALF_BLOCK;
static wchar_t* LOWER_HALF_BLOCK;
static wchar_t* FULL_BLOCK;


static char* old_TERM;


/**
 * Brings terminal into raw mode. Sets the screen dimensions
 * to the terminal's width and height.
 * 
 * \param screen_w
 * \param screen_h
 * \return RETURN_OK, always
 */
STATUS backend_curses_init(dim* screen_w, dim* screen_h, COLOR_MODE color_mode)
{
	old_TERM = getenv("TERM");
	
	if (color_mode == COLOR_MODE_16) {
		setenv("TERM", "xterm-256color", 1);
	}
	
	UPPER_HALF_BLOCK = L"\u2580";
	LOWER_HALF_BLOCK = L"\u2584";
	FULL_BLOCK = L"\u2588";
	
	// initialize curses session
	initscr();
	raw();
	kirous_colors_init();
	timeout(0);
	noecho();
	curs_set(0);
	keypad(stdscr, 1);
	
	*screen_w = COLS;
	*screen_h = LINES * 2;
	
	return RETURN_OK;
}


/**
 * Resizes kirous screen buffer if terminal size has changed.
 * 
 * \param screen kirous screen buffer
 * \param bufmask kirous mask buffer
 * \param screen_w kirous screen width
 * \param screen_h kirous screen height
 * \param kirous status code
 */
STATUS backend_curses_pre_draw(COLOR_CODE** screen, int** bufmask, dim* screen_w, dim* screen_h)
{
	STATUS status;
	
	// resize screen buffer if terminal size changed
	if (*screen_w != COLS || *screen_h != LINES * 2) {
		status = kirous_recalloc((void**) screen, COLS * LINES * 2, sizeof(COLOR_CODE));
		if (status != RETURN_OK) {
			return status;
		}
		
		status = kirous_recalloc((void**) bufmask, COLS * LINES * 2, sizeof(int));
		if (status != RETURN_OK) {
			return status;
		}
		
		*screen_w = COLS;
		*screen_h = LINES * 2;
		
		kirous_int_array_clear(screen, BLACK, *screen_w * *screen_h);
		kirous_int_array_clear(bufmask, 1, *screen_w * *screen_h);
	}
	
	return RETURN_OK;
}

/**
 * \param x block x position
 * \param y block y position
 * \param fg foreground color
 * \param bg background color
 * \return kirous status code
 */
STATUS backend_curses_draw(dim x, dim y, COLOR_CODE fg, COLOR_CODE bg)
{
	// in case the terminal window was resized
	// (resizes are handled in pre_draw)
	if (x >= COLS || y >= LINES) {
		return RETURN_OK;
	}
	
	// save amount of allocated color pairs by
	// switching between lower and upper half blocks
	if (bg == fg) {
		kirous_colors_use(0, fg);
		mvwaddwstr(stdscr, y, x, FULL_BLOCK);
	} else if (bg > fg) {
		kirous_colors_use(fg, bg);
		mvwaddwstr(stdscr, y, x, UPPER_HALF_BLOCK);
	} else {
		kirous_colors_use(bg, fg);
		mvwaddwstr(stdscr, y, x, LOWER_HALF_BLOCK);
	}
	
	return RETURN_OK;
}


/**
 * Not implemented.
 * 
 * \return RETURN_OK, always
 */
STATUS backend_curses_post_draw()
{
	return RETURN_OK;
}


/**
 * Calls backend_curses_end and prints error to stderr.
 * 
 * \param message Error message string.
 * \return RETURN_OK, always
 */
STATUS backend_curses_fatal(const char* message)
{
	backend_curses_end();
	fprintf(stderr, "%s\n", message);
	
	return RETURN_OK;
}


/**
 * Restores TERM environment variable and cooked mode terminal
 * settings.
 * 
 * \return RETURN_OK, always
 */
STATUS backend_curses_end()
{
	setenv("TERM", old_TERM, 1);
	echo();
	nocbreak();
	endwin();
	
	return RETURN_OK;
}


/**
 * Reads keyboard input and returns character.
 * 
 * \return curses key code
 */
int16_t backend_curses_get_char()
{
	int16_t c = getch();
	
	return c;
}


/**
 * Draws a string in the curses (text) coordinate system.
 * 
 * \param x x coordinate
 * \param y y coordinate
 * \param text string to draw
 * \param fg foreground color
 * \param bg background color
 * \return kirous status code
 */
STATUS backend_curses_draw_string(dim x, dim y, const uint8_t* text, COLOR_CODE fg, COLOR_CODE bg)
{
	kirous_colors_use(bg, fg);
	mvaddstr(y, x, (char*) text);
	
	return RETURN_OK;
}
