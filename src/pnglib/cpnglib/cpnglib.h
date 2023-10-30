#ifndef CPNGLIB_H
#define CPNGLIB_H

#ifdef _WIN32
#define LIBRARY_API extern "C" __declspec(dllexport)
#else
#define LIBRARY_API extern "C"
#endif


// #include "cpnglib_common_flags.h"
#include "vpng.h"

// ---------- Meta -------------
LIBRARY_API
int read_png_info(
	const char *srcfile,
	int *image_dims,
	int *num_components,
	int *bit_depth,
	int *png_color_type,
	int *png_interlace,
	png_colorp *palette,
	int *num_palette,
	int *compression_type,
	int *num_text,
    size_t *max_text,
	int *filter_type,
	short *background,
	double *gamma,
	png_uint_16p hist,
	double *cHRM
);


LIBRARY_API
int read_png_texts(
	const char *srcfile,
	int num_text,
	int max_text,
	int *text_compression,
	char *text_keywords,
	size_t *text_lengths,
	char *texts
);

// ----------- RGB -------------
LIBRARY_API
int read_png_spatial(
    const char *srcfile,
    unsigned char *rgb//,
	// int num_text,
    // int max_text,
    // int *text_compression,
	// char *text_keywords,
    // size_t *text_lengths,
	// char *texts

    // unsigned char *colormap,    // colormap used
    // unsigned char *in_colormap, // colormap to use
    // int out_color_space,
    // int dither_mode,
    // int dct_method,
    // BITMASK flags
);

LIBRARY_API
int write_png_spatial(
    const char *dstfile,
    unsigned char *rgb,
	int *image_dims,
    int png_color_type,
	int bit_depth,
	int png_interlace,
    png_colorp palette,
    int num_palette,
	int num_text,
	int *text_compression,
	char *text_keywords,
	size_t *text_lengths,
	char *texts

    // int *samp_factor,
    // unsigned short *qt,
    // short quality,
    // short *quant_tbl_no,
    // short base_quant_tbl_idx,
    // short smoothing_factor,
    // BITMASK flags
);

// int jpeg_lib_version(void) { return JPEG_LIB_VERSION; }
LIBRARY_API
int print_png_params(const char *srcfile);


#endif // CJPEGLIB_H