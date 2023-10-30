
#include <stdio.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

#include <vpng.h>
#include "cpnglib.h"
#include "cpnglib_common.h"


int read_png_texts(
	const char *srcfile,
	int num_text,
	int max_text,
	int *text_compression,
	char *text_keywords,
	size_t *text_lengths,
	char *texts
) {
	// open file
	png_structp png;
	png_infop info;
  	FILE *fp;
  	if ((fp = _read_png(srcfile, &png, &info)) == NULL) {
		fprintf(stderr, "_read_png failed!\n");
    	return 0;
  	}

	// read texts
	if(texts != NULL) {
		png_textp textp;
		png_get_text(png, info, &textp, NULL);
		size_t start_length = 0;
		// fprintf(stderr, "num_text %d max_text %d\n", num_text, max_text);
		for(int i = 0; i < num_text; i++) {
			text_compression[i] = textp[i].compression;
			strcpy(text_keywords + i*79, textp[i].key);
			// fprintf(stderr, "%d %d\n", textp[i].text_length, textp[i].itxt_length);
			text_lengths[i] = (textp[i].compression < 1) ?
				textp[i].text_length : textp[i].itxt_length;
			if(text_lengths[i] > 0) {
				// for(j = 0; j < text_lengths[i]; j++)
				// 	texts[i*max_text+j] = textp[i].text[j];
				memcpy(texts+i*max_text, textp[i].text, text_lengths[i]);
				texts[i*max_text+text_lengths[i]] = 0;
			}
		}
	}

	// // read data
	// //png_read_png(png, info, PNG_TRANSFORM_IDENTITY, NULL);
	// png_read_image(png, rgbp);
	// png_read_end(png, NULL);

	// cleanup
	png_destroy_read_struct(&png, &info, NULL);
	fclose(fp);
	// delete [] rgbp;

	return 1;
}

#ifdef __cplusplus
}
#endif