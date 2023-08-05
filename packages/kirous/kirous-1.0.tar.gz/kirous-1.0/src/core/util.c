#include "util.h"

#include <stdlib.h>
#include <string.h>

/**
 * Error checked malloc.
 * 
 * \param ptr pointer for which memory is allocated
 * \param size
 * \return ERR_MEM_ALLOC on failure
 */
STATUS kirous_malloc(void** ptr, size_t size)
{
	// use calloc to initialize with zero
	*ptr = calloc(1, size);
	
	if (*ptr == nullptr) {
		return ERR_MEM_ALLOC;
	}
	
	return RETURN_OK;
}


/**
 * Error checked calloc.
 * 
 * \param ptr
 * \param nmemb units to allocate
 * \param size size of one unit (in bytes)
 * \return ERR_MEM_ALLOC on failure
 */
STATUS kirous_calloc(void** ptr, size_t nmemb, size_t size)
{
	*ptr = calloc(nmemb, size);
	
	if (*ptr == nullptr) {
		return ERR_MEM_ALLOC;
	}
	
	return RETURN_OK;
}


/**
 * Error checked realloc.
 * 
 * \param ptr
 * \param size
 * \return ERR_MEM_ALLOC on failure
 */
STATUS kirous_realloc(void** ptr, size_t size)
{
	*ptr = realloc(*ptr, size);
	
	if (*ptr == nullptr) {
		return ERR_MEM_ALLOC;
	}
	
	return RETURN_OK;
}


/**
 * Reallocates memory for an array.
 * 
 * \param ptr
 * \param nmemb number of units to reallocate
 * \param size unit size (in bytes)
 * \return ERR_MEM_ALLOC on failure
 */
STATUS kirous_recalloc(void** ptr, size_t nmemb, size_t size)
{
	*ptr = realloc(*ptr, size * nmemb);
	
	if (*ptr == nullptr) {
		return ERR_MEM_ALLOC;
	}
	
	// set to zero
	*ptr = memset(*ptr, 0, size * nmemb);
	
	return RETURN_OK;
}


/**
 * Error checked free function.
 * 
 * \param ptr pointer to memory to be free'd
 * \return WARN_NOP if freeing has failed
 */
STATUS kirous_free(void** ptr) {
	if (*ptr != nullptr) {
		free(*ptr);
		*ptr = nullptr;
		
		return RETURN_OK;
	}
	
	return WARN_NOP;
}


// TODO create error checked memset
/**
 */
STATUS kirous_int_array_clear(int** ptr, int content, size_t nmemb)
{
	unsigned int i;
	
	if (ptr == nullptr) {
		return ERR_MEM_ACCESS;
	}
	
	for (i = 0; i < nmemb; i++) {
		(*ptr)[i] = content;
	}
	
	return RETURN_OK;
}
