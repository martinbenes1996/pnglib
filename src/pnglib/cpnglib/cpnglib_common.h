#ifndef CPNGLIB_COMMON_H
#define CPNGLIB_COMMON_H

#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

// this is envelope for png.h
// trying to avoid naming the same as system library
#include "vpng.h"
#include "cpnglib.h"
// #include "cjpeglib_common_flags.h"
// #include "cjpeglib_common_markers.h"

// // declaration to avoid errors
// long jround_up (long a, long b);

FILE *_read_png(
	const char *filename,
    png_structp *png,
	png_infop *info
);

// /**
//  * @brief Custom error handler, mapping libjpeg error on C++ exception.
//  * @author licy183
//  *
//  * @param cinfo
//  */
// void my_custom_error_exit(
// 	j_common_ptr cinfo
// );
// #define jpeg_std_error(jerr) ( \
//   (jpeg_std_error(jerr)), \
//   ((jerr)->error_exit = my_custom_error_exit), \
//   (jerr))

int print_png_params(
	const char *srcfile
);

#ifdef __cplusplus
}
#endif

#endif // CPNGLIB_COMMON_H