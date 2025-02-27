# Cosmos Image Format (CIF)

**Cosmos Image Format (CIF)** is a high-efficiency image compression format designed for the transmission of photos in space missions. It reduces image data size while preserving quality, enabling faster and more reliable communication of images from space to Earth.

**Cosmos Image Format (CIF)** — формат сжатия изображений, предназначенный для передачи фотографий в космических миссиях. Он снижает размер данных изображений, сохраняя их качество, что позволяет ускорить и улучшить передачу изображений из космоса на Землю.

## Features

- High-efficiency compression for space missions
- Supports lossless compression
- Ideal for image data transmission in space

## Installation

To install, use pip:

```
pip install -r requirements.txt
```

## Usage

1. Compress images to CIF format:
   ```python
   from cosmos_image_format import CIFCompressor
   compressor = CIFCompressor()
   compressed_data = compressor.compress('path_to_image')
   with open('output.cif', 'wb') as f:
       f.write(compressed_data)
   ```

2. Decompress CIF images:
   ```python
   from cosmos_image_format import CIFDecompressor
   decompressor = CIFDecompressor()
   image = decompressor.decompress('output.cif')
   image.show()
   ```
