#include "backend_serial.h"
#include "colors.h"
#include "keyboard.h"
#include "util.h"

#include <curses.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>

static int serial_fd;
static struct termios tty;
static struct termios tty_old;
static int16_t input_char;


/**
 * \param screen_w
 * \param screen_h
 * \param color_mode
 * \param kirous status code
 */
STATUS backend_serial_init(dim* screen_w, dim* screen_h, COLOR_MODE color_mode)
{
	*screen_w = 84;
	*screen_h = 48;
	
	serial_fd = open("/dev/ttyACM0", O_RDWR | O_NOCTTY);
	
	memset(&tty, 0, sizeof(tty));
	
	tty_old = tty;
	
	cfsetospeed(&tty, (speed_t) B115200);
	cfsetispeed(&tty, (speed_t) B115200);
	
	tty.c_cflag &= ~PARENB;
	tty.c_cflag &= ~CSTOPB;
	tty.c_cflag &= ~CSIZE;
	tty.c_cflag |= CS8;
	
	tty.c_cflag &= ~CRTSCTS;
	tty.c_cc[VMIN] = 5;
	tty.c_cc[VTIME] = 5;
	tty.c_cflag |= CREAD | CLOCAL;
	
	cfmakeraw(&tty);
	
	tcflush(serial_fd, TCIFLUSH);
	
	if (tcsetattr(serial_fd, TCSANOW, &tty) != 0) {
		perror("tcsetattr failed");
		return ERR_SERIAL;
	}
	
	return RETURN_OK;
}


/**
 * \param screen
 * \param bufmask
 * \param screen_w
 * \param screen_h
 * \return kirous status code
 */
STATUS backend_serial_pre_draw(COLOR_CODE** screen, int** bufmask, dim* screen_w, dim* screen_h)
{
	int bytes_written;
	unsigned char* data;
	unsigned char comm;
	STATUS status;
	
	if (*screen_h % 8 != 0) {
		return ERR_PARAM;
	}
	
	status = kirous_calloc((void**) &data, *screen_w * *screen_h / 8, sizeof(unsigned char));
	
	for (dim y = 0; y < *screen_h / 8; y++) {
		dim y8 = y * 8;
		for (dim x = 0; x < *screen_w; x++) {
			data[x + y * *screen_w] = 0;
			for (uint8_t i = 0; i < 8; i++) {
				COLOR_CODE pixel = (*screen)[x + (y8 + i) * *screen_w];
				int8_t binary_pixel;
				kirous_color_convert_binary(pixel, &binary_pixel);
				data[x + y * *screen_w] |= (binary_pixel << i);
			}
		}
	}
	
	bytes_written = write(serial_fd, data, *screen_w * *screen_h / 8);
	
	if (bytes_written == 0) {
		return ERR_SERIAL;
	}
	
	free(data);
	
	comm = 0;
	while (comm == 0) {
		read(serial_fd, &comm, 1);
	}
	
	switch (comm) {
		case 1:
			input_char = -1;
			break;
		case 2:
			input_char = KEY_UP;
			break;
		case 3:
			input_char = KEY_DOWN;
			break;
		case 4:
			input_char = KEY_RIGHT;
			break;
		case 5:
			input_char = KEY_LEFT;
			break;
		default:
			input_char = (int16_t) comm;
			break;
	}
	
	return status;
}


/**
 * \param x
 * \param y
 * \param fg
 * \param bg
 * \return kirous status code
 */
STATUS backend_serial_draw(dim x, dim y, COLOR_CODE fg, COLOR_CODE bg)
{
	return RETURN_OK;
}


STATUS backend_serial_post_draw(void)
{
	return RETURN_OK;
}


STATUS backend_serial_fatal(const char* message)
{
	return RETURN_OK;
}


/**
 * \return RETURN_OK
 */
STATUS backend_serial_end(void)
{
	switch (close(serial_fd)) {
		case 0:
			return RETURN_OK;
		default:
			return ERR_GENERAL;
	}
}


/**
 * \return input char (int)
 */
int16_t backend_serial_get_char(void)
{
	return input_char;
}


/**
 * \param x
 * \param y
 * \param text
 * \param fg
 * \param bg
 */
STATUS backend_serial_draw_string(dim x, dim y, const uint8_t* text, COLOR_CODE fg, COLOR_CODE bg)
{
	return RETURN_OK;
}
