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
    int *block_dims,
    int *image_dims,
    int *png_interlace,
    png_colorp *palette,
    int *num_palette,
    int *compression_type,
	int *filter_type,
	short *background, // 1B+4*2B
	double *gamma,
	png_uint_16p hist,
	double *cHRM
);

LIBRARY_API
int read_png_markers(
    const char *srcfile,
    unsigned char *markers
);

// ----------- RGB -------------
LIBRARY_API
int read_png_spatial(
    const char *srcfile,
    unsigned char *rgb
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
    int *png_color_type,
	int bit_depth,
	int png_interlace,
    png_colorp palette,
    int num_palette
    // int *jpeg_color_space,
    // int *num_components,
    // int dct_method,
    // int *samp_factor,
    // unsigned short *qt,
    // short quality,
    // short *quant_tbl_no,
    // short base_quant_tbl_idx,
    // short smoothing_factor,
    // int num_markers,
    // int *marker_types,
    // int *marker_lengths,
    // unsigned char *markers,
    // BITMASK flags
);

// int jpeg_lib_version(void) { return JPEG_LIB_VERSION; }
LIBRARY_API
int print_png_params(const char *srcfile);


#endif // CJPEGLIB_H