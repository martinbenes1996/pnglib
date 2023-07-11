
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
	int *num_palette
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
	// png_get_filter_type
	// png_get_compression_type
	if(palette != NULL)
		png_get_PLTE(png, info, palette, num_palette);
	// https://gist.github.com/niw/5963798

	// palette

	// cleanup
	png_destroy_read_struct(&png, &info, NULL);
	fclose(fp);

	return 1;

	// // allocate
	// FILE *fp = NULL;
	// struct jpeg_decompress_struct cinfo;
	// struct jpeg_error_mgr jerr;

	// // sanitizing libjpeg errors
	// int status = 1;
	// try {

	// 	// read jpeg header
	// 	if((fp = _read_jpeg(srcfile, &cinfo, &jerr, FALSE)) == NULL) return 0;

	// 	// markers
	// 	if((marker_lengths != NULL) || (marker_types != NULL)) {
	// 		// setup
	// 		set_marker_handlers(&cinfo);
	// 		// read markers
	// 		(void) jpeg_read_header(&cinfo, TRUE);
	// 		// collect marker data
	// 		for(int i = 0; i < gpos; i++) {
	// 			marker_lengths[i] = gmarker_lengths[i];
	// 			marker_types[i] = gmarker_types[i];
	// 		}
	// 		unset_marker_handlers(&cinfo);
	// 	} else {
	// 		(void) jpeg_read_header(&cinfo, TRUE);
	// 	}

	// 	jpeg_calc_output_dimensions(&cinfo);

	// 	(void)jpeg_read_coefficients(&cinfo);

	// 	// copy to caller
	// 	if (block_dims != NULL) {
	// 		for (int i = 0; i < cinfo.num_components; i++) {
	// 			block_dims[2 * i] = cinfo.comp_info[i].height_in_blocks;
	// 			block_dims[2 * i + 1] = cinfo.comp_info[i].width_in_blocks;
	// 		}
	// 	}
	// 	if (image_dims != NULL) {
	// 		image_dims[0] = cinfo.output_height;
	// 		image_dims[1] = cinfo.output_width;
	// 	}
	// 	if (num_components != NULL) {
	// 		num_components[0] = cinfo.num_components;
	// 		num_components[1] = cinfo.out_color_components;
	// 		num_components[2] = cinfo.output_components;
	// 	}
	// 	if (jpeg_color_space != NULL) {
	// 		jpeg_color_space[0] = cinfo.out_color_space;
	// 		jpeg_color_space[1] = cinfo.jpeg_color_space;
	// 	}

	// 	if (samp_factor != NULL)
	// 		for (int comp = 0; comp < cinfo.num_components; comp++) {
	// 			*(samp_factor + comp * 2 + 0) = cinfo.comp_info[comp].v_samp_factor;
	// 			*(samp_factor + comp * 2 + 1) = cinfo.comp_info[comp].h_samp_factor;
	// 		}

	// 	if (flags != NULL) {
	// 		*(flags) = (((cinfo.progressive_mode) ? (-1) : 0) & PROGRESSIVE_MODE) | (*flags);
	// 	}

	// 	if(huffman_bits != NULL) {
	// 		for(int comp = 0; comp < 4; comp++) {
	// 			*(huffman_valid + (comp)) = cinfo.dc_huff_tbl_ptrs[comp] != NULL;
	// 			*(huffman_valid + (comp + 4)) = cinfo.ac_huff_tbl_ptrs[comp] != NULL;
	// 			// huffman tables - bits
	// 			int dc_max = 0, ac_max = 0;
	// 			for(int i = 0; i < 17; i++) {
	// 				if(cinfo.dc_huff_tbl_ptrs[comp] != NULL) {
	// 					*(huffman_bits + comp * 17 + i) = cinfo.dc_huff_tbl_ptrs[comp]->bits[i];
	// 					dc_max += cinfo.dc_huff_tbl_ptrs[comp]->bits[i];
	// 				}
	// 				if(cinfo.ac_huff_tbl_ptrs[comp] != NULL) {
	// 					*(huffman_bits + (comp + 4) * 17 + i) = cinfo.ac_huff_tbl_ptrs[comp]->bits[i];
	// 					ac_max += cinfo.ac_huff_tbl_ptrs[comp]->bits[i];
	// 				}
	// 			}
	// 			// hufman tables - values
	// 			for(int v = 0; v < 256; v++) {
	// 				if(cinfo.dc_huff_tbl_ptrs[comp] != NULL && v < dc_max)
	// 					*(huffman_values + comp * 256 + v) = cinfo.dc_huff_tbl_ptrs[comp]->huffval[v];
	// 				if(cinfo.ac_huff_tbl_ptrs[comp] != NULL && v < ac_max)
	// 					*(huffman_values + (4 + comp) * 256 + v) = cinfo.ac_huff_tbl_ptrs[comp]->huffval[v];
	// 			}
	// 		}
	// 	}

	// // error handling
	// } catch(...) {
	// 	status = 0;
	// }

	// // cleanup and return
	// jpeg_destroy_decompress(&cinfo);
	// if(fp != NULL)
	// 	fclose(fp);
	// return status;

    return 42;

}


int print_png_params(
	const char *srcfile
) {
    printf("Hello, World!\n");
    return 43;

	// // allocate
	// FILE *fp = NULL;
	// struct jpeg_decompress_struct cinfo;
	// struct jpeg_error_mgr jerr;

	// // sanitizing libjpeg errors
	// int status = 1;
	// try {

	// 	// read jpeg header
	// 	if ((fp = _read_jpeg(srcfile, &cinfo, &jerr, TRUE)) == NULL) return 0;
	// 	(void)jpeg_start_decompress(&cinfo);

	// 	printf("File %s details:\n", srcfile);
	// 	printf("  image_height             %d\n", cinfo.image_height);
	// 	printf("  image_width              %d\n", cinfo.image_width);
	// 	printf("  jpeg_color_space         %d\n", cinfo.jpeg_color_space);
	// 	printf("  out_color_space          %d\n", cinfo.out_color_space);
	// 	printf("  scale_num                %u\n", cinfo.scale_num);
	// 	printf("  scale_denom              %u\n", cinfo.scale_denom);
	// 	printf("  output_gamma             %f\n", cinfo.output_gamma);
	// 	printf("  buffered_image           %d\n", cinfo.buffered_image);
	// 	printf("  dct_method               %d\n", cinfo.dct_method);
	// 	printf("  do_fancy_upsampling      %d\n", cinfo.do_fancy_upsampling);
	// 	printf("  do_block_smoothing       %d\n", cinfo.do_block_smoothing);
	// 	printf("  quantize_colors          %d\n", cinfo.quantize_colors);
	// 	printf("  dither_mode              %d\n", cinfo.dither_mode);
	// 	printf("  two_pass_quantize        %d\n", cinfo.two_pass_quantize);
	// 	printf("  desired_number_of_colors %d\n", cinfo.desired_number_of_colors);
	// 	printf("  enable_1pass_quant       %d\n", cinfo.enable_1pass_quant);
	// 	printf("  enable_external_quant    %d\n", cinfo.enable_external_quant);
	// 	printf("  enable_2pass_quant       %d\n", cinfo.enable_2pass_quant);
	// 	printf("  output_width             %d\n", cinfo.output_width);
	// 	printf("  output_height            %d\n", cinfo.output_height);
	// 	printf("  out_color_components     %d\n", cinfo.out_color_components);
	// 	printf("  output_components        %d\n", cinfo.output_components);
	// 	printf("  actual_number_of_colors  %d\n", cinfo.actual_number_of_colors);
	// 	printf("  output_scanline          %d\n", cinfo.output_scanline);
	// 	printf("  input_scan_number        %d\n", cinfo.input_scan_number);
	// 	printf("  input_iMCU_row           %d\n", cinfo.input_iMCU_row);
	// 	printf("  output_scan_number       %d\n", cinfo.output_scan_number);
	// 	printf("  output_iMCU_row          %d\n", cinfo.output_iMCU_row);
	// 	printf("  data_precision           %d\n", cinfo.data_precision);
	// 	printf("  progressive_mode         %d\n", cinfo.progressive_mode);
	// 	printf("  arith_code               %d\n", cinfo.arith_code);

	// 	for (int comp = 0; comp < cinfo.out_color_components; comp++) {
	// 		printf("  comp_info[%d]\n", comp);
	// 		printf("    h_samp_factor          %d\n", cinfo.comp_info[comp].h_samp_factor);
	// 		printf("    v_samp_factor          %d\n", cinfo.comp_info[comp].v_samp_factor);
	// 		printf("    quant_tbl_no           %d\n", cinfo.comp_info[comp].quant_tbl_no);
	// 		printf("    dc_tbl_no              %d\n", cinfo.comp_info[comp].dc_tbl_no);
	// 		printf("    ac_tbl_no              %d\n", cinfo.comp_info[comp].ac_tbl_no);
	// 		printf("    width_in_blocks        %d\n", cinfo.comp_info[comp].width_in_blocks);
	// 		printf("    height_in_blocks       %d\n", cinfo.comp_info[comp].height_in_blocks);
	// 		printf("    downsampled_width      %d\n", cinfo.comp_info[comp].downsampled_width);
	// 		printf("    downsampled_height     %d\n", cinfo.comp_info[comp].downsampled_height);
	// 		printf("    component_needed       %d\n", cinfo.comp_info[comp].component_needed);
	// 		printf("    MCU_width              %d\n", cinfo.comp_info[comp].MCU_width);
	// 		printf("    MCU_height             %d\n", cinfo.comp_info[comp].MCU_height);
	// 		printf("    MCU_blocks             %d\n", cinfo.comp_info[comp].MCU_blocks);
	// 		printf("    MCU_sample_width       %d\n", cinfo.comp_info[comp].MCU_sample_width);
	// 		printf("    last_col_width         %d\n", cinfo.comp_info[comp].last_col_width);
	// 		printf("    last_row_height        %d\n", cinfo.comp_info[comp].last_row_height);
	// 	}

	// // error handling
	// } catch(...) {
	// 	status = 0;
	// }

	// // cleanup and return
	// jpeg_destroy_decompress(&cinfo);
	// if(fp != NULL)
	// 	fclose(fp);
	// return status;

}

#ifdef __cplusplus
}
#endif