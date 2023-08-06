Large Print Splitter
====================

Takes an image, printed height or width (in mm) and page size then
splits image across multiple pages with alignment marks and generates a
PDF.

It is intended for printing projections exported as SVGs from Openscad.

For the image it supports anything that Pillow supports, as well as SVGs
thanks to CairoSVG.

PDF generation is done by ReportLab.

::

    $ lps -h
    usage: lps [-h] (--width WIDTH | --height HEIGHT) [--page_size PAGE_SIZE]
               [--overlap OVERLAP] [--svg_start_scale SVG_START_SCALE]
               image_file

    positional arguments:
      image_file            Image to parse

    optional arguments:
      -h, --help            show this help message and exit
      --width WIDTH         Width of image in millimeters
      --height HEIGHT       Height of image in millimeters
      --page_size PAGE_SIZE
                            Page size, e.g. a3, a4
      --overlap OVERLAP     Print overlap in mm
      --svg_start_scale SVG_START_SCALE
                            When using SVG, this is the largest scale factor to
                            attempt to generate an image

    $ lps --width 970 --page_size a3 --overlap 20 wrap.svg
    Loading Image
    Trying to generate raster image of svg at 3x scale
    The image will not fit on a single page
    Calculating crop list
    This will require 3 pages
    Chunking image
    Generating PDF

Licensed under `MIT License <LICENSE.md>`__
