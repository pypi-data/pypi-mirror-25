==========
imagedupes
==========
--------------------------------------------------------
Python 3 application for finding visually similar images
--------------------------------------------------------
usage: __init__.py [-h] [-a ALGORITHM] [-d DIRECTORY] [-l] [-o OPTIONS]
                   [-p PROGRAM] [-r] [-R] [-s HASH_SIZE]

Finds visually similar images and opens them in an image viewer, one group of
matches at a time. If no options are specified, it defaults to searching the
current working directory non-recursively using a perceptual image hash
algorithm with a hash size of 8, opens images in the system default image
handler (all at once), and does not follow symbolic links.

optional arguments:
  -h, --help            show this help message and exit
  -a ALGORITHM, --algorithm ALGORITHM
                        Specify a hash algorithm to use. Acceptable inputs:
                        'dhash' (horizontal difference hash),
                        'dhash_vertical', 'ahash' (average hash), 'phash'
                        (perceptual hash), 'phash_simple', 'whash_haar' (Haar
                        wavelet hash), 'whash_db4' (Daubechles wavelet hash).
                        Defaults to 'phash' if not specified.
  -d DIRECTORY, --directory DIRECTORY
                        Directory to search for images. Defaults to the
                        current working directory if not specified.
  -l, --links           Follow symbolic links. Defaults to off if not
                        specified.
  -o OPTIONS, --options OPTIONS
                        Option parameters to pass to the program opened by the
                        --program flag. Defaults to no options if not
                        specified.
  -p PROGRAM, --program PROGRAM
                        Program to open the matched images with. Defaults to
                        your system's default image handler if not specified.
  -r, --recursive       Search through directories recursively. Defaults to
                        off if not specified.
  -R, --raws            Process and hash raw image files. Note: Very slow.
                        Best to leave running overnight for large image sets.
                        Defaults to off if not specified.
  -s HASH_SIZE, --hash_size HASH_SIZE
                        Resolution of the hash; higher is more sensitive to
                        differences. Must be a power of 2 (2, 4, 8, 16...).
                        Defaults to 8 if not specified. Values lower than 8
                        may not work with some hash algorithms.
