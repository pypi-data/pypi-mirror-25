/**
 * error.c
 * 
 * \author eichkat3r
 */
#include "error.h"
#include "screen.h"

#include <stdlib.h>
#include <setjmp.h>
#include <string.h>


int __kirous_jmp_count = 1;


/**
 * Call this method before using any exception handling routine.
 */
void kirous_init_exception_handling(void)
{
	__kirous_default_exception_handler();
}

/**
 * Function used by macro KIROUS_THROW.
 * Jumps into the catch block if defined. If there is no catch block, the
 * default exception handler is called.
 * 
 * \param e Exception object
 * \param filename __FILE__ preprocessor directive
 * \param line __LINE__ preprocessor directive
 */
void __kirous_throw(Exception e, const char* filename, int32_t line)
{
	// TODO @eichkat3r initialize stack trace here
	if (__kirous_jmp_count >= 1024) {
		fprintf(stderr, "Jump buffer limit exceeded.\n");
		exit(EXIT_FAILURE);
	}
	
	__kirous_exception = e;
	longjmp(__kirous_jmp_buf[__kirous_jmp_count], __kirous_jmp_count);
}

/**
 * Default exception handler.
 */
void __kirous_default_exception_handler(void)
{
	int code;
	
	code = setjmp(__kirous_jmp_buf[__kirous_jmp_count]);
	if (code != 0) {
		printf("Uncaught exception occured: %d\n", code);
	}
}

