/**
 * Dummy backend implementation for debugging purposes.
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "backend_dummy.h"


/**
 * Sets screen width and height to dummy values and prints
 * a status message to stdout.
 * 
 * \param screen_w set to 100
 * \param screen_h set to 100
 * \return RETURN_OK, always
 */
STATUS backend_dummy_init(dim* screen_w, dim* screen_h, COLOR_MODE color_mode)
{
	*screen_w = 100;
	*screen_h = 100;
	printf("Color Mode: %d\n", color_mode);
	
	return RETURN_OK;
}


/**
 * Not implemented.
 * 
 * \param screen
 * \param bufmask
 * \param screen_w
 * \param screen_h
 * \return RETURN_OK, always
 */
STATUS backend_dummy_pre_draw(COLOR_CODE** screen, int** bufmask, dim* screen_w, dim* screen_h)
{
	return RETURN_OK;
}


/**
 * Not implemented.
 * 
 * \param x
 * \param y
 * \param fg
 * \param bg
 * \return RETURN_OK, always
 */
STATUS backend_dummy_draw(dim x, dim y, COLOR_CODE fg, COLOR_CODE bg)
{
	return RETURN_OK;
}


/**
 * Not implemented.
 * 
 * \return RETURN_OK, always
 */
STATUS backend_dummy_post_draw(void)
{
	return RETURN_OK;
}


/**
 * Prints the error message to stderr and exits
 * with EXIT_FAILURE code.
 * 
 * \return nothing, premature exit
 */
STATUS backend_dummy_fatal(const char* message)
{
	fprintf(stderr, "%s\n", message);
	exit(EXIT_FAILURE);
}


/**
 * Prints a status message to stdout.
 * 
 * \return RETURN_OK, always
 */
STATUS backend_dummy_end(void)
{
	printf("[backend_dummy_end]\n");
	
	return RETURN_OK;
}


/**
 * \return -1, always
 */
int16_t backend_dummy_get_char(void)
{
	return -1;
}


/**
 * \param x
 * \param y
 * \param text
 * \param fg
 * \param bg
 * \return RETURN_OK, always
 */
STATUS backend_dummy_draw_string(dim x, dim y, const uint8_t* text, COLOR_CODE fg, COLOR_CODE bg)
{
	return RETURN_OK;
}
