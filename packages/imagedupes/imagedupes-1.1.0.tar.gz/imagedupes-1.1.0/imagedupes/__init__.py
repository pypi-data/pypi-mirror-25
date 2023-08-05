#!/usr/bin/python3

def createArgumentParser():

    from argparse import ArgumentParser

    __args = None
    __parser = None

    __parser = ArgumentParser(description="Finds visually similar images and opens them in an image viewer, one group of matches at a time. If no options are specified, it defaults to searching the current working directory non-recursively using a perceptual image hash algorithm with a hash size of 8, opens images in the system default image handler (all at once), and does not follow symbolic links.")
    __parser.add_argument("-a", "--algorithm", type=str, help="Specify a hash algorithm to use. Acceptable inputs:\n'dhash' (horizontal difference hash),\n'dhash_vertical',\n'ahash' (average hash),\n'phash' (perceptual hash),\n'phash_simple',\n'whash_haar' (Haar wavelet hash),\n'whash_db4' (Daubechles wavelet hash). Defaults to 'phash' if not specified.")
    __parser.add_argument("-d", "--directory", type=str, help="Directory to search for images. Defaults to the current working directory if not specified.")
    __parser.add_argument("-l", "--links", action="store_true", help="Follow symbolic links. Defaults to off if not specified.")
    __parser.add_argument("-o", "--options", type=str, help="Option parameters to pass to the program opened by the --program flag. Defaults to no options if not specified.")
    __parser.add_argument("-p", "--program", type=str, help="Program to open the matched images with. Defaults to your system's default image handler if not specified.")
    __parser.add_argument("-r", "--recursive", action="store_true", help="Search through directories recursively. Defaults to off if not specified.")
    __parser.add_argument("-R", "--raws", action="store_true", help="Process and hash raw image files. Note: Very slow. Best to leave running overnight for large image sets. Defaults to off if not specified.")
    __parser.add_argument("-s", "--hash_size", type=int, help="Resolution of the hash; higher is more sensitive to differences. Must be a power of 2 (2, 4, 8, 16...). Defaults to 8 if not specified. Values lower than 8 may not work with some hash algorithms.")
    __args = __parser.parse_args()
    return __args

def checkHashAlgorithmChoice(__hashAlgorithmString):

    from sys import exit

    __acceptableChoicesList = None

    __acceptableChoicesList = ['dhash', 'dhash_vertical', 'ahash', 'phash', 'phash_simple', 'whash_haar', 'whash_db4']
    if __hashAlgorithmString not in __acceptableChoicesList:
        print("Error: please choose a valid hash algorithm. Use the -h command line flag for help.")
        exit()

def getImagePaths(__directoryPath, __recursiveBoolean, __followLinksBoolean, __rawsBoolean, __hashAlgorithmString):
    "Creates a list of image paths within a given directory"

    import os

    __filePathList = []

    if __hashAlgorithmString is not None:
        checkHashAlgorithmChoice(__hashAlgorithmString)
    print("Searching for duplicate images...")
    if __directoryPath is not None:
        if __recursiveBoolean == True:
            if __rawsBoolean == True:
                for __root, __dirs, __files in os.walk(__directoryPath, followlinks=__followLinksBoolean):
                    for __file in __files:
                        if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                        or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                        or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                        or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                        or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                        or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm")\
                        or str(__file).lower().endswith(".crw") or str(__file).lower().endswith(".cr2")\
                        or str(__file).lower().endswith(".nef") or str(__file).lower().endswith(".dng")\
                        or str(__file).lower().endswith(".raf") or str(__file).lower().endswith(".dcr")\
                        or str(__file).lower().endswith(".mos") or str(__file).lower().endswith(".kdc"):
                            __filePathList.append(os.path.join(__root, __file))
            else:
                for __root, __dirs, __files in os.walk(__directoryPath, followlinks=__followLinksBoolean):
                    for __file in __files:
                        if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                        or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                        or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                        or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                        or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                        or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm"):
                            __filePathList.append(os.path.join(__root, __file))
        else:
            if __rawsBoolean == True:
                for __file in os.listdir(__directoryPath):
                    if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                    or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                    or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                    or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                    or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                    or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm")\
                    or str(__file).lower().endswith(".crw") or str(__file).lower().endswith(".cr2")\
                    or str(__file).lower().endswith(".nef") or str(__file).lower().endswith(".dng")\
                    or str(__file).lower().endswith(".raf") or str(__file).lower().endswith(".dcr")\
                    or str(__file).lower().endswith(".mos") or str(__file).lower().endswith(".kdc"):
                        __filePathList.append(os.path.join(__directoryPath, __file))
            else:
                for __file in os.listdir(__directoryPath):
                    if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                    or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                    or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                    or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                    or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                    or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm"):
                        __filePathList.append(os.path.join(__directoryPath, __file))
    else:
        if __recursiveBoolean == True:
            if __rawsBoolean == True:
                for __root, __dirs, __files in os.walk(os.path.curdir, followlinks=__followLinksBoolean):
                    for __file in __files:
                        if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                        or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                        or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                        or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                        or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                        or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm")\
                        or str(__file).lower().endswith(".crw") or str(__file).lower().endswith(".cr2")\
                        or str(__file).lower().endswith(".nef") or str(__file).lower().endswith(".dng")\
                        or str(__file).lower().endswith(".raf") or str(__file).lower().endswith(".dcr")\
                        or str(__file).lower().endswith(".mos") or str(__file).lower().endswith(".kdc"):
                            __filePathList.append(os.path.join(__root, __file))
            else:
                for __root, __dirs, __files in os.walk(os.path.curdir, followlinks=__followLinksBoolean):
                    for __file in __files:
                        if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                        or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                        or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                        or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                        or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                        or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm"):
                            __filePathList.append(os.path.join(__root, __file))
        else:
            if __rawsBoolean == True:
                for __file in os.listdir(os.path.curdir):
                    if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                    or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                    or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                    or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                    or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                    or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm")\
                    or str(__file).lower().endswith(".crw") or str(__file).lower().endswith(".cr2")\
                    or str(__file).lower().endswith(".nef") or str(__file).lower().endswith(".dng")\
                    or str(__file).lower().endswith(".raf") or str(__file).lower().endswith(".dcr")\
                    or str(__file).lower().endswith(".mos") or str(__file).lower().endswith(".kdc"):
                        __filePathList.append(os.path.join(os.path.curdir, __file))
            else:
                if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                or str(__file).lower().endswith(".bmp") or str(__file).lower().endswith(".jp2")\
                or str(__file).lower().endswith(".j2k") or str(__file).lower().endswith(".jpf")\
                or str(__file).lower().endswith(".jpx") or str(__file).lower().endswith(".jpm"):
                    __filePathList.append(os.path.join(os.path.curdir, __file))
    return __filePathList

def generateHashDict(__imagePathList, __hashAlgorithmString, __hashSizeInt):

    from os import path
    from os import remove
    from rawpy import imread
    from imageio import imsave
    from PIL import Image
    from imagehash import dhash
    from imagehash import dhash_vertical
    from imagehash import average_hash
    from imagehash import phash
    from imagehash import phash_simple
    from imagehash import whash

    __imageHashDict = {}
    __image = None

    if __hashSizeInt == None:
        __hashSizeInt = 8
    for __imagePath in __imagePathList:
        print("Hashing " + str(__imagePath))
        if str(__imagePath).lower().endswith(".crw") or str(__imagePath).lower().endswith(".cr2")\
        or str(__imagePath).lower().endswith(".nef") or str(__imagePath).lower().endswith(".dng")\
        or str(__imagePath).lower().endswith(".raf") or str(__imagePath).lower().endswith(".dcr")\
        or str(__imagePath).lower().endswith(".mos") or str(__imagePath).lower().endswith(".kdc"):
            if path.isfile(__imagePath + ".jpg"):
                __image = Image.open(__imagePath + ".jpg")
                if __hashAlgorithmString == 'dhash':
                    __imageHashDict[__imagePath] = dhash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'dhash_vertical':
                    __imageHashDict[__imagePath] = dhash_vertical(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'ahash':
                    __imageHashDict[__imagePath] = average_hash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'phash':
                    __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'phash_simple':
                    __imageHashDict[__imagePath] = phash_simple(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'whash_haar':
                    __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'whash_db4':
                    __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt, mode='db4')
                elif __hashAlgorithmString == None:
                    __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
                __image.close
            else:
                __image = imread(__imagePath)
                __image = __image.postprocess()
                imsave(__imagePath + ".jpg", __image)
                __image = Image.open(__imagePath + ".jpg")
                remove(__imagePath + ".jpg")
                if __hashAlgorithmString == 'dhash':
                    __imageHashDict[__imagePath] = dhash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'dhash_vertical':
                    __imageHashDict[__imagePath] = dhash_vertical(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'ahash':
                    __imageHashDict[__imagePath] = average_hash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'phash':
                    __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'phash_simple':
                    __imageHashDict[__imagePath] = phash_simple(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'whash_haar':
                    __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt)
                elif __hashAlgorithmString == 'whash_db4':
                    __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt, mode='db4')
                elif __hashAlgorithmString == None:
                    __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
                __image.close
        else:
            __image = Image.open(__imagePath)
            if __hashAlgorithmString == 'dhash':
                __imageHashDict[__imagePath] = dhash(__image, hash_size=__hashSizeInt)
            elif __hashAlgorithmString == 'dhash_vertical':
                __imageHashDict[__imagePath] = dhash_vertical(__image, hash_size=__hashSizeInt)
            elif __hashAlgorithmString == 'ahash':
                __imageHashDict[__imagePath] = average_hash(__image, hash_size=__hashSizeInt)
            elif __hashAlgorithmString == 'phash':
                __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
            elif __hashAlgorithmString == 'phash_simple':
                __imageHashDict[__imagePath] = phash_simple(__image, hash_size=__hashSizeInt)
            elif __hashAlgorithmString == 'whash_haar':
                __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt)
            elif __hashAlgorithmString == 'whash_db4':
                __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt, mode='db4')
            elif __hashAlgorithmString == None:
                __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
            __image.close

    return __imageHashDict


def compareHashes(__imageHashDict):

    __reverseMultiDict = {}
    __duplicateListOfSets = {}
    __duplicateListOfLists = []

    for __key, __value in __imageHashDict.items():
        __reverseMultiDict.setdefault(__value, set()).add(__key)
    __duplicateListOfSets = [__values for __key, __values in __reverseMultiDict.items() if len(__values) > 1]
    for __i in range(0, len(__duplicateListOfSets)):
        __duplicateListOfLists.append(list(__duplicateListOfSets[__i]))
    return __duplicateListOfLists

def printDuplicates(__imageListOfLists):

    for __i in range(0, len(__imageListOfLists)):
        for __j in range(0, len(__imageListOfLists[__i])):
            print("Found possible duplicate: " + str(__imageListOfLists[__i][__j]))
    return __imageListOfLists

def displayImage(__imageListOfLists, __viewerCommandString, __viewerOptionsString):

    import webbrowser
    import subprocess

    for __i in range(0, len(__imageListOfLists)):
        input("Press enter to open the next set of possible duplicates: ")
        if __viewerCommandString is None:
            for __j in range(0, len(__imageListOfLists[__i])):
                webbrowser.open(__imageListOfLists[__i][__j])
        elif __viewerCommandString is not None and __viewerOptionsString is None:
            subprocess.run([__viewerCommandString] + __imageListOfLists[__i])
        else:
            subprocess.run([__viewerCommandString, __viewerOptionsString] + __imageListOfLists[__i])

def main():

    from sys import exit

    __args = None

    __args = createArgumentParser()
    displayImage(printDuplicates(compareHashes(generateHashDict(getImagePaths(__args.directory, __args.recursive, __args.links, __args.raws, __args.algorithm), __args.algorithm, __args.hash_size))), __args.program, __args.options)
    exit()

main()
