"""
Author: Huy Hiep Nguyen
Copyright (c) 2026 Huy Hiep Nguyen
"""
from pathlib import Path

import numpy as np
from PIL import Image
from logging import DEBUG

# Import application modules
from util import parse_arguments, ycbcr_to_rgb, rgb_to_ycbcr, logger
from util.write_bitstream import write_bitstream_to_file
from encoder import encode
from decoder import decode


def main() -> int:
    """
    Main entry point for the JPEG encoder application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_arguments()

    if args.verbose:
        logger.setLevel(DEBUG)
        for handler in logger.handlers:
            handler.setLevel(DEBUG)

    if not Path(args.input).is_file():
        logger.error(f"Input file '{args.input}' does not exist.")
        return 1

    with Image.open(args.input) as im:
        im_rgb = im.convert("RGB")
        pixel_array = np.array(im_rgb, dtype=np.uint8)
        img_width = im_rgb.width
        img_height = im_rgb.height

    logger.debug(f"Image {args.input} loaded - Width: {img_width}px, Height: {img_height}px")

    # Convert from RGB to YCbCr
    ycbcr_array = rgb_to_ycbcr(pixel_array)

    # Split into separate Y, Cb, Cr channels
    y_channel = ycbcr_array[:, :, 0]
    cb_channel = ycbcr_array[:, :, 1]
    cr_channel = ycbcr_array[:, :, 2]

    # Run the encoding pipeline
    encoding_result = encode(
        y_channel,
        cb_channel,
        cr_channel,
        img_width,
        img_height,
        args.last_encoding_stage,
        args.verbose)

    # Write JPEG file if we have a complete bitstream
    if encoding_result.jpeg_bitstream is not None:
        write_bitstream_to_file(encoding_result.jpeg_bitstream, args.output)

    # If decoding is enabled, decode and save the image
    if not args.no_decode:
        # Decode to YCbCr array
        ycbcr_array = decode(encoding_result, args.last_encoding_stage)

        # Convert YCbCr to RGB and create PIL Image
        decoded_image_rgb = ycbcr_to_rgb(ycbcr_array)
        decoded_image = Image.fromarray(decoded_image_rgb)
        decoded_image.save(args.reconstructed)
        logger.info(f"Decoded image saved as {args.reconstructed}")

    return 0


if __name__ == "__main__":
    main()
