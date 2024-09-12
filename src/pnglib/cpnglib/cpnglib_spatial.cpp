
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
	// int num_text,
	// int max_text,
	// int *text_compression,
	// char *text_keywords,
	// size_t *text_lengths,
	// char *texts
) {
	// open file
	png_structp png;
	png_infop info;
  	FILE *fp;
  	if ((fp = _read_png(srcfile, &png, &info)) == NULL) {
		fprintf(stderr, "_read_png failed!\n");
    	return 0;
  	}

	// // read texts
	// if(texts != NULL) {
	// 	png_textp textp;
	// 	png_get_text(png, info, &textp, NULL);
	// 	size_t start_length = 0;
	// 	// fprintf(stderr, "num_text %d max_text %d\n", num_text, max_text);
	// 	for(int i = 0; i < num_text; i++) {
	// 		text_compression[i] = textp[i].compression;
	// 		strcpy(text_keywords + i*79, textp[i].key);
	// 		// fprintf(stderr, "%d %d\n", textp[i].text_length, textp[i].itxt_length);
	// 		text_lengths[i] = (textp[i].compression < 1) ?
	// 			textp[i].text_length : textp[i].itxt_length;
	// 		if(text_lengths[i] > 0) {
	// 			// for(j = 0; j < text_lengths[i]; j++)
	// 			// 	texts[i*max_text+j] = textp[i].text[j];
	// 			memcpy(texts+i*max_text, textp[i].text, text_lengths[i]);
	// 			texts[i*max_text+text_lengths[i]] = 0;
	// 		}
	// 	}
	// }

	// read dimensions
	int height, width;
	height = (int)png_get_image_height(png, info);
	width = (int)png_get_image_width(png, info);
	// get channels
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

	// set output format
	int height = image_dims[0];
	int width = image_dims[1];
  	png_set_IHDR(
    	png,
    	info,
    	width, height,
    	bit_depth,
    	png_color_type,
    	png_interlace,
    	PNG_COMPRESSION_TYPE_DEFAULT,
    	PNG_FILTER_TYPE_DEFAULT
  	);

	//
	if (bit_depth < 8)
        png_set_packing(png_ptr);

	// add palette
	if(palette != NULL)
		png_set_PLTE(png, info, palette, num_palette);

	// text
	png_textp textp = NULL;
	// fprintf(stderr, "texts %p\n", texts);
	if(texts != NULL) {
		// png
		textp = new png_text[num_text];
		size_t start_length = 0;
		for(int i = 0; i < num_text; i++) {
			textp[i].compression = text_compression[i];
			textp[i].key = text_keywords + i*79;
			// textp[i].text_length =
			textp[i].itxt_length = 0;
			// textp[i].text_length = text_lengths[i];
			// if(textp[i].compression < 1)
			// 	textp[i].text_length = text_lengths[i];
			// else
			// 	textp[i].itxt_length = text_lengths[i];
			textp[i].lang = textp[i].lang_key = NULL;
			// textp[i].text = NULL;
			textp[i].text = texts + start_length;
			start_length += text_lengths[i];
			// fprintf(
			// 	stderr,
			// 	"png_set_text: i %d compression %d length %lu %lu key %s\n",
			// 	i, text_compression[i],
			// 	textp[i].text_length, textp[i].itxt_length,
			// 	textp[i].key
			// );
		}
		png_set_text(png, info, textp, num_text);
	}

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
	delete [] textp;
	delete [] rgbp;

	return 1;
}


#ifdef __cplusplus
}
#endif