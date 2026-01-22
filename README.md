# JPEG Encoder/Decoder User Guide

## 1. Quick Installation

### 1.1 Install Dependencies

```bash
conda env create -f environment.yml
conda activate jpeg-env
```

### 1.2 Build (Choose one of 3 options)

**For both encode & decode:**

```bash
python setup.py build_ext --inplace
```

**For decode only (fastest):**

```bash
python setup_decoder.py build_ext --inplace
```

**For encode only:**

```bash
python setup_encoder.py build_ext --inplace
```

---

## 2. Quick Start

### 2.1 Run Encode + Decode Automatically

Single command:

```bash
python main.py
```

Output:
- `out.jpg` - Compressed JPEG image
- `rec.png` - Reconstructed image from JPEG

---

## 3. Advanced Usage (Create Custom Script)

### 3.1 Encode Image to JPEG

Create file `encode_example.py` and copy code below:

```python
from encoder import encode
from PIL import Image
import numpy as np

# Step 1: Load image from file
img = Image.open("input.jpg")

# Step 2: Convert to YCbCr and split channels
y, cb, cr = img.convert('YCbCr').split()

# Step 3: Encode to JPEG
result = encode(
    y_channel=np.array(y),
    cb_channel=np.array(cb),
    cr_channel=np.array(cr),
    img_width=img.width,
    img_height=img.height
)

# Step 4: Save JPEG to file
with open("output.jpg", "wb") as f:
    f.write(result.jpeg_bitstream)

print(f"Done! File size: {len(result.jpeg_bitstream)} bytes")
```

---

### 3.2 Decode JPEG to Image

Create file `decode_example.py` and copy code below:

```python
from decoder import decode
from util import EncodingResult
from PIL import Image
import numpy as np

# Step 1: Load JPEG file
with open("image.jpg", "rb") as f:
    jpeg_data = f.read()

# Step 2: Create EncodingResult object
result = EncodingResult()
result.jpeg_bitstream = jpeg_data

# Step 3: Decode JPEG
ycbcr = decode(result, "jpeg")

# Step 4: Convert YCbCr to RGB
ycbcr_img = Image.fromarray(ycbcr.astype('uint8'), 'YCbCr')
rgb_img = ycbcr_img.convert('RGB')

# Step 5: Save reconstructed image
rgb_img.save("reconstructed.png")

print("Done! Image saved to: reconstructed.png")
```

---

## 4. Advanced Customization

### 4.1 Adjust JPEG Quality

Add `quality` parameter to encode:

```python
result = encode(
    ...,
    quality=85  # 1-100 (higher = better quality + larger file)
)
```

---

## 5. Performance Analysis

### 5.1 Analyze Encode/Decode Time

To profile the implementation:

```bash
python profile_run.py
```

This will:
- Run encode & decode once
- Display top 40 functions by execution time
- Open interactive visualization in browser (if snakeviz is installed)

### 5.2 Comparison with Pillow

This encoder/decoder uses Cython to optimize bottleneck functions:

| Tool | Time | Notes |
|------|------|-------|
| Pillow (PIL.Image) | ~45 sec | Pure Python implementation |
| This Project (Cython) | ~14 sec | Huffman decode optimized |
| **Speedup** | **3.2x** | DCT + RLE + Huffman optimized |

---

## 6. Technical Documentation

For detailed algorithm explanation and mathematical formulas (DCT, Quantization, Huffman...):
👉 [JPEG_THEORY.md](JPEG_THEORY.md)
