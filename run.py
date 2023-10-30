
import numpy as np
from PIL import Image
import pnglib

# # === test palette ===
# x = np.array([
#     [[0], [0], [0]],
#     [[0], [1], [0]],
#     [[0], [0], [0]],
# ], dtype='uint8')
# palette = [
#     pnglib.Color(index=0, red=0, green=0, blue=0),
#     pnglib.Color(index=1, red=255, green=255, blue=255),
# ]
# # pnglib
# im = pnglib.from_spatial(
#     x,
#     png_color_type=pnglib.PNG_COLOR_TYPE_PALETTE,
#     palette=palette,
# )
# FNAME = 'output.png'
# im.write_spatial(FNAME)

# # compare
# x_ref = np.array(Image.open(FNAME))
# x_ref = np.expand_dims(x_ref, 2)
# print('palette', (x == x_ref).all())


# # === test writing ===
# FNAME = 'examples/lizard.png'
# x_orig = np.array(Image.open(FNAME))

# # pnglib
# im = pnglib.from_spatial(x_orig)
# im.write_spatial('output.png')
# # reference
# Image.fromarray(x_orig).save('output_ref.png')

# # compare
# x = np.array(Image.open('output.png'))
# x_ref = np.array(Image.open('output_ref.png'))
# print('writing', (x == x_ref).all())


# === test reading ===
FNAME = 'examples/lizard.png'
im = pnglib.read_spatial(FNAME)
x = im.spatial

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
rng = np.random.default_rng(12345)
x_g = np.array(Image.open(FNAME).convert('L'))[..., None]
x_wk = rng.random(x_g.shape) < (x_g/255)
# plt.imshow(x_wk * 255, cmap='gray')
# plt.show()

pnglib.from_spatial(
	x_wk, bit_depth=pnglib.PNG_BIT_DEPTH_1
).write_spatial('output.png')



# print(im.png_interlace)
# print(f'{im.texts=}')

# im.write_spatial('output.png')
# im2 = pnglib.read_spatial('output.png')
# print(im.texts)
# print(im2.texts)

# print(im.filter_type)
# print(im.compression_type)
# print(f'{im.hist=}')

# # reference
# x_ref = np.array(Image.open(FNAME))

# # compare
# print('reading', (x == x_ref).all())
