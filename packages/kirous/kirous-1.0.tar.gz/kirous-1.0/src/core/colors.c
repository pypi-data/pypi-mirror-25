// system includes
#include <curses.h>

// core includes
#include "colors.h"
#include "error.h"


// color pair matrix
static COLOR_CODE kirous_pairs[16][16];


/**
 * Initialises color pairs and enables the curses color system.
 * 
 * \return status code
 */
STATUS kirous_colors_init(void)
{
	int pairnum = 1;
	COLOR_CODE bg, fg;
	
	if (start_color() != OK) {
		return ERR_CURSES;
	}
	
	for (bg = 0; bg < 16; bg++) {
		for (fg = 0; fg < 16; fg++) {
			kirous_pairs[bg][fg] = pairnum;
			init_pair(pairnum, fg, bg);
			pairnum += 1;
		}
	}
	
	return RETURN_OK;
}


/**
 * Used by curses backend to set pixel colors.
 * 
 * \param bg background color code
 * \param fg foreground color code
 * \return ERR_CURSES on error, RETURN_OK on success
 */
STATUS kirous_colors_use(COLOR_CODE bg, COLOR_CODE fg)
{
	if (attron(COLOR_PAIR(kirous_pairs[bg][fg])) == ERR) {
		return ERR_CURSES;
	}
	
	return RETURN_OK;
}


/**
 * Converts color codes to OpenGL color space.
 * 
 * \param color curses color
 * \param r return value for red channel in range [0.0..1.0]
 * \param g return value for green channel in range [0.0..1.0]
 * \param b return value for blue channel in range [0.0..1.0]
 * \return kirous error status code
 */
STATUS kirous_color_convert_gl(const COLOR_CODE color, float* r, float* g, float* b)
{
	// TODO @eichkat3r read these values from config
	switch (color) {
		case -1:
		case COLOR_BLACK:
			*r = 0x33; *g = 0x33; *b = 0x33; break;
		case COLOR_RED:
			*r = 0xff; *g = 0x65; *b = 0x65; break;
		case COLOR_GREEN:
			*r = 0x60; *g = 0xb4; *b = 0x8a; break;
		case COLOR_BLUE:
			*r = 0x3e; *g = 0x51; *b = 0x5a; break;
		case COLOR_YELLOW:
			*r = 0xad; *g = 0x89; *b = 0x2d; break;
		case COLOR_MAGENTA:
			*r = 0xce; *g = 0x5c; *b = 0x00; break;
		case COLOR_CYAN:
			*r = 0x22; *g = 0x55; *b = 0x66; break;
		case 7: // light gray
			*r = 0xba; *g = 0xbd; *b = 0xb6; break;
		case 8: // dark gray
			*r = 0x55; *g = 0x55; *b = 0x55; break;
		case 9: // red
			*r = 0xff; *g = 0x8d; *b = 0x8d; break;
		case 10: // green
			*r = 0x72; *g = 0xd5; *b = 0xa3; break;
		case 11: // yellow
			*r = 0xff; *g = 0xc1; *b = 0x23; break;
		case 12: // blue
			*r = 0x4c; *g = 0x64; *b = 0x71; break;
		case 13: // magenta
			*r = 0xf5; *g = 0x79; *b = 0x00; break;
		case 14: // cyan
			*r = 0x22; *g = 0xaa; *b = 0xbb; break;
		case 15: // white
			*r = 0xdd; *g = 0xdd; *b = 0xdd; break;
		default:
			return ERR_PARAM;
	}
	
	*r /= 255;
	*g /= 255;
	*b /= 255;
	
	return RETURN_OK;
}


/**
 * \param color
 * \param binary
 * \return kirous error status code
 */
STATUS kirous_color_convert_binary(const COLOR_CODE color, int8_t* binary)
{
	if (color < -1 || color >= 16) {
		return ERR_PARAM;
	}
	
	switch (color) {
		case BLACK:
		case RED:
		case GREEN:
		case YELLOW:
		case BLUE:
		case MAGENTA:
		case CYAN:
		case DARK_GRAY:
			*binary = 1;
			break;
		default:
			*binary = 0;
			break;
	}
	
	return RETURN_OK;
}
