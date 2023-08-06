==========
imagedupes
==========
--------------------------------------------------------
Python 3 application for finding visually similar images
--------------------------------------------------------
usage: imagedupes [-h] [-a ALGORITHM] [-d DIRECTORY] [-D DATABASE] [-l]
                   [-o OPTIONS] [-p PROGRAM] [-r] [-R] [-s HASH_SIZE]

Finds visually similar images and opens them in an image viewer, one group of
matches at a time. If no options are specified, it defaults to searching the
current working directory non-recursively using a perceptual image hash
algorithm with a hash size of 8, opens images in the system default image
handler (all members of a group of matches at once), and does not follow
symbolic links or use a persistent database.

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
  -D DATABASE, --database DATABASE
                        Use a database to cache hash results and speed up hash
                        comparisons. Argument should be the path to which you
                        want to save or read from the database. Warning:
                        runnning the program multiple times with the same
                        database but a different hash algorithm (or different
                        hash size) will lead to missed matches. Defaults to no
                        database if not specified.
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
  -R, --raws            Process and hash raw image files. Note: Very slow. You
                        might want to leave it running overnight for large
                        image sets. Using the --database option in tandem is
                        highly recommended. Defaults to off if not specified.
  -s HASH_SIZE, --hash_size HASH_SIZE
                        Resolution of the hash; higher is more sensitive to
                        differences. Some hash algorithms require that it be a
                        power of 2 (2, 4, 8, 16...) so using a power of two is
                        recommended. Defaults to 8 if not specified. Values
                        lower than 8 may not work with some hash algorithms.
