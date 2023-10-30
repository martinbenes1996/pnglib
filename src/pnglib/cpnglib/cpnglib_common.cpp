
#include <stdio.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

#include <vpng.h>

// #include "cjpeglib_common.h"

// extern int gpos;
// extern int gmarker_types[MAX_MARKER];
// extern int gmarker_lengths[MAX_MARKER];
// extern unsigned char * gmarker_data[MAX_MARKER];

// void my_custom_error_exit(
// 	j_common_ptr cinfo
// ) {
// 	// Write the message
// 	(*cinfo->err->output_message)(cinfo);

// 	// Let the memory manager delete any temp files before we die
// 	jpeg_destroy(cinfo);

// 	// Throw an "exception" using C++
// 	throw 0;
// }

FILE * _read_png(
	const char *filename,
	png_structp *png,
	png_infop *info
) {
	// open file
	FILE *fp;
  	if ((fp = fopen(filename, "rb")) == NULL) {
		fprintf(stderr, "failed to open\n");
		return NULL;
	}

	// check file size
	fseek(fp, 0L, SEEK_END);
	size_t fsize = ftell(fp);
	fseek(fp, 0L, SEEK_SET);
	if(fsize == 0) {
		return NULL;
	}

	// zero the structures
	memset(png, 0x00, sizeof(png_structp));
	memset(info, 0x00, sizeof(png_infop));

	if(!(*png = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL))) {
		fprintf(stderr, "failed to create png read struct\n");
		fclose(fp);
		return NULL;
	}
	if(!(*info = png_create_info_struct(*png))) {
		fprintf(stderr, "failed to create png info struct\n");
		png_destroy_read_struct(png, NULL, NULL);
		fclose(fp);
		return NULL;
	}
    if (setjmp(png_jmpbuf(*png))) {
		fprintf(stderr, "failed to set up png error handling\n");
		png_destroy_read_struct(png, info, NULL);
		fclose(fp);
        return NULL;
    }
	png_init_io(*png, fp);
	png_read_info(*png, *info);

	return fp;
}


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
) {
	// open file
	png_structp png;
	png_infop info;
  	FILE *fp;
  	if ((fp = _read_png(srcfile, &png, &info)) == NULL) {
		fprintf(stderr, "_read_png failed!\n");
    	return 0;
  	}

	// copy to caller
	if(image_dims != NULL) {
		image_dims[0] = (int)png_get_image_height(png, info);
		image_dims[1] = (int)png_get_image_width(png, info);
	}

	if(bit_depth != NULL)
		bit_depth[0] = png_get_bit_depth(png, info);

	if(png_color_type != NULL)
		png_color_type[0] = png_get_color_type(png, info);

	if(num_components != NULL)
		num_components[0] = png_get_channels(png, info);

	if(png_interlace != NULL)
		png_interlace[0] = png_get_interlace_type(png, info);

	if(compression_type != NULL)
		compression_type[0] = png_get_compression_type(png, info);

	// png_color_8 sig;
	// memset(&sig, 0, sizeof(png_color_8));
	// png_color_8p sigp = &sig;
	// png_get_sBIT(png, info, &sigp);

	if((num_text != NULL) || (max_text != NULL)) {
		png_textp textp;
		int no_text;
		png_get_text(png, info, &textp, &no_text);
		if(num_text != NULL)
			num_text[0] = no_text;
		if(max_text != NULL) {
			max_text[0] = 0;
			for(int i = 0; i < no_text; i++) {
				int text_length = (textp[i].compression < 1) ?
					textp[i].text_length : textp[i].itxt_length;
				if(text_length > max_text[0])
					max_text[0] = text_length;
			}
		}
	}
	if(filter_type != NULL)
		filter_type[0] = png_get_filter_type(png, info);

	if(background != NULL) {
		png_color_16_struct bkg[1];
		memset(bkg, 0x00, sizeof(png_color_16_struct));
		if(png_get_bKGD(png, info, (png_color_16p *)&bkg) == 0) {
			background[0] = -1;
		} else {
			background[0] = bkg[0].index;
			background[1] = bkg[0].red;
			background[2] = bkg[0].green;
			background[3] = bkg[0].blue;
			background[4] = bkg[0].gray;
		}
	}
	if(gamma != NULL) {
		if(png_get_gAMA(png, info, gamma) == 0)
			gamma[0] = -1;
	}
	if(hist != NULL) {
		if(png_get_hIST(png, info, &hist) == 0)
			hist[0] = -1;
	}
	if(palette != NULL)
		png_get_PLTE(png, info, palette, num_palette);

	// https://gist.github.com/niw/5963798
	if(cHRM != NULL) {
		if(png_get_cHRM(png, info,
						cHRM+0, cHRM+1, cHRM+2, cHRM+3,
						cHRM+4, cHRM+5, cHRM+6, cHRM+7) == 0)
			cHRM[0] = -1;
	}

	// cleanup
	png_destroy_read_struct(&png, &info, NULL);
	fclose(fp);

	return 1;
}


int print_png_params(
	const char *srcfile
) {
    printf("Hello, World!\n");
    return 42;

}

#ifdef __cplusplus
}
#endif