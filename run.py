
import numpy as np
from PIL import Image
import pnglib

exit()

# === test writing ===
FNAME = 'examples/lizard.png'
x_orig = np.array(Image.open(FNAME))

# pnglib
im = pnglib.from_spatial(x_orig)
im.write_spatial('output.png')
# reference
Image.fromarray(x_orig).save('output_ref.png')

# compare
x = np.array(Image.open('output.png'))
x_ref = np.array(Image.open('output_ref.png'))
print('writing', (x == x_ref).all())

# exit()

# === test reading ===
FNAME = 'examples/lizard.png'

# pnglib
im = pnglib.read_spatial(FNAME)
x = im.spatial
# reference
x_ref = np.array(Image.open(FNAME))

# compare
print('reading', (x == x_ref).all())
