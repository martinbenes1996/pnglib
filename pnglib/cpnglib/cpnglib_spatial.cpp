
#include <stdio.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

// this is envelope for jpeglib.h
// trying to avoid naming the same as system library
#include "vpng.h"
#include "cpnglib.h"
#include "cpnglib_common.h"

/**
 * @brief Helper for indexing pixel row base[h].
 *
 * @param base Base pointer.
 * @param h Height.
 * @param Hmax Height of image.
 * @param Wmax Width of image.
 * @param channels Channels of image.
 * @return void* Pointer to base[h].
 */
png_byte *_px_row_offset(
	png_byte *base,
	int h,
	int Hmax,
	int Wmax,
	int channels
) {
	return base + channels * Wmax * h;
}

int read_png_spatial(
	const char *srcfile,
	unsigned char *rgb
	// unsigned char *colormap, // colormap used
	// unsigned char *in_colormap, // colormap to use
	// int out_color_space,
	// int dither_mode,
	// int dct_method,
	// BITMASK flags
) {
	// open file
	png_structp png;
	png_infop info;
  	FILE *fp;
  	if ((fp = _read_png(srcfile, &png, &info)) == NULL) {
		fprintf(stderr, "_read_png failed!\n");
    	return 0;
  	}

	// read dimensions
	int height, width;
	height = (int)png_get_image_height(png, info);
	width = (int)png_get_image_width(png, info);
	// get channels
	// png_byte channels = png->channels;
	png_byte channels = png_get_channels(png, info);

	// allocate pointer array
	unsigned char **rgbp = new unsigned char*[height];
	for(int h = 0; h < height; h++) {
		rgbp[h] = _px_row_offset(rgb, h, height, width, channels);
	}

	// read data
	//png_read_png(png, info, PNG_TRANSFORM_IDENTITY, NULL);
	png_read_image(png, rgbp);
	png_read_end(png, NULL);

	// cleanup
	png_destroy_read_struct(&png, &info, NULL);
	fclose(fp);
	delete [] rgbp;

	return 1;
}

int write_png_spatial(
	const char *dstfile,
	unsigned char *rgb,
	int *image_dims,
    int *png_color_type,
	int bit_depth,
	int png_interlace,
    png_colorp palette,
    int num_palette
) {
    // open file
	png_structp png;
	png_infop info;
	FILE *fp;
  	if ((fp = fopen(dstfile, "wb")) == NULL) {
		fprintf(stderr, "failed to open\n");
    	return 0;
  	}
	if(!(png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL))) {
		fprintf(stderr, "failed to create png write struct\n");
		fclose(fp);
		return 0;
	}
	if(!(info = png_create_info_struct(png))) {
		fprintf(stderr, "failed to create png info struct\n");
		png_destroy_read_struct(&png, NULL, NULL);
		fclose(fp);
		return 0;
	}
    if (setjmp(png_jmpbuf(png))) {
		fprintf(stderr, "failed to set up png error handling\n");
		png_destroy_read_struct(&png, &info, NULL);
		fclose(fp);
        return 0;
    }
	png_init_io(png, fp);

	if(palette != NULL)
		png_set_PLTE(png, info, palette, num_palette);

	// set output format
	int height = image_dims[0];
	int width = image_dims[1];
  	png_set_IHDR(
    	png,
    	info,
    	width, height,
    	bit_depth,
    	png_color_type[0],
    	png_interlace,
    	PNG_COMPRESSION_TYPE_DEFAULT,
    	PNG_FILTER_TYPE_DEFAULT
  	);
  	png_write_info(png, info);

	// allocate pointer array
	png_byte channels = png_get_channels(png, info);
	unsigned char **rgbp = new unsigned char*[height];
    for(int h = 0; h < height; h++) {
		rgbp[h] = _px_row_offset(rgb, h, height, width, channels);
    }

	// write data
	png_write_image(png, rgbp);
  	png_write_end(png, NULL);

	// cleanup
	png_destroy_write_struct(&png, &info);
	fclose(fp);
	delete [] rgbp;

	return 1;
}


#ifdef __cplusplus
}
#endif