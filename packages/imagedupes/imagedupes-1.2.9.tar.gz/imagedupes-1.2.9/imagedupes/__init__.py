#!/usr/bin/python3
from argparse import ArgumentParser
from sys import exit
from os import walk
from os import path
from os import listdir
import shelve
from imagehash import dhash
from imagehash import dhash_vertical
from imagehash import average_hash
from imagehash import phash
from imagehash import phash_simple
from imagehash import whash
from os import remove
from rawpy import imread
from imageio import imsave
from PIL import Image
import webbrowser
import subprocess

def createArgumentParser():
    "Creates the command line argument parser and the possible arguments/options"

    args = None
    parser = None

    parser = ArgumentParser(description="Finds visually similar images and opens them in an image viewer, one group of matches at a time. If no options are specified, it defaults to searching the current working directory non-recursively using a perceptual image hash algorithm with a hash size of 8, opens images in the system default image handler (all members of a group of matches at once), and does not follow symbolic links or use a persistent database.")
    parser.add_argument("-a",
                        "--algorithm",
                        type=str,
                        help="Specify a hash algorithm to use. Acceptable inputs:\n'dhash' (horizontal difference hash),\n'dhash_vertical',\n'ahash' (average hash),\n'phash' (perceptual hash),\n'phash_simple',\n'whash_haar' (Haar wavelet hash),\n'whash_db4' (Daubechles wavelet hash). Defaults to 'phash' if not specified.")
    parser.add_argument("-d",
                        "--directory",
                        type=str,
                        help="Directory to search for images. Defaults to the current working directory if not specified.")
    parser.add_argument("-D",
                        "--database",
                        type=str,
                        help="Use a database to cache hash results and speed up hash comparisons. Argument should be the path to which you want to save or read from the database. Warning: runnning the program multiple times with the same database but a different hash algorithm (or different hash size) will lead to missed matches. Defaults to no database if not specified.")
    parser.add_argument("-l",
                        "--links",
                        action="store_true",
                        help="Follow symbolic links. Defaults to off if not specified.")
    parser.add_argument("-o",
                        "--options",
                        type=str,
                        help="Option parameters to pass to the program opened by the --program flag. Defaults to no options if not specified.")
    parser.add_argument("-p",
                        "--program",
                        type=str,
                        help="Program to open the matched images with. Defaults to your system's default image handler if not specified.")
    parser.add_argument("-r",
                        "--recursive",
                        action="store_true",
                        help="Search through directories recursively. Defaults to off if not specified.")
    parser.add_argument("-R",
                        "--raws",
                        action="store_true",
                        help="Process and hash raw image files. Note: Very slow. You might want to leave it running overnight for large image sets. Using the --database option in tandem is highly recommended. Defaults to off if not specified.")
    parser.add_argument("-s",
                        "--hash_size",
                        type=int,
                        help="Resolution of the hash; higher is more sensitive to differences. Some hash algorithms require that it be a power of 2 (2, 4, 8, 16...) so using a power of two is recommended. Defaults to 8 if not specified. Values lower than 8 may not work with some hash algorithms.")
    args = parser.parse_args()
    return args

def checkHashAlgorithmChoice(hashAlgorithmString):
    "Checks input for validity against available hash algorithm choices"

    acceptableChoicesList = None

    acceptableChoicesList = ['dhash',
                            'dhash_vertical',
                            'ahash',
                            'phash',
                            'phash_simple',
                            'whash_haar',
                            'whash_db4']
    if hashAlgorithmString not in acceptableChoicesList:
        print("Error: please choose a valid hash algorithm. Use the -h command line flag for help.")
        exit()

def getImagePaths(directoryPath,
                recursiveBoolean,
                followLinksBoolean,
                rawsBoolean,
                hashAlgorithmString):
    "Creates a list of image paths within a given directory (possibly recursively)"

    filePathList = []

    if directoryPath is not None:
        directoryPath = path.normcase(
                        path.normpath(
                        path.abspath(
                        path.expanduser(
                        path.expandvars(
                        directoryPath)))))
    if hashAlgorithmString is not None:
        checkHashAlgorithmChoice(hashAlgorithmString)
    print("Searching for duplicate images...")
    if directoryPath is not None:
        if recursiveBoolean == True:
            if rawsBoolean == True:
                for root, dirs, files in walk(directoryPath, followlinks=followLinksBoolean):
                    for file in files:
                        if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                        or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                        or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                        or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                        or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                        or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm")\
                        or str(file).lower().endswith(".3fr") or str(file).lower().endswith(".ari")\
                        or str(file).lower().endswith(".arw") or str(file).lower().endswith(".bay")\
                        or str(file).lower().endswith(".crw") or str(file).lower().endswith(".cr2")\
                        or str(file).lower().endswith(".cap") or str(file).lower().endswith(".data")\
                        or str(file).lower().endswith(".dcs") or str(file).lower().endswith(".dcr")\
                        or str(file).lower().endswith(".dng") or str(file).lower().endswith(".drf")\
                        or str(file).lower().endswith(".eip") or str(file).lower().endswith(".erf")\
                        or str(file).lower().endswith(".fff") or str(file).lower().endswith(".gpr")\
                        or str(file).lower().endswith(".iiq") or str(file).lower().endswith(".k25")\
                        or str(file).lower().endswith(".kdc") or str(file).lower().endswith(".mdc")\
                        or str(file).lower().endswith(".mef") or str(file).lower().endswith(".mos")\
                        or str(file).lower().endswith(".mrw") or str(file).lower().endswith(".nef")\
                        or str(file).lower().endswith(".nrw") or str(file).lower().endswith(".obm")\
                        or str(file).lower().endswith(".orf") or str(file).lower().endswith(".pef")\
                        or str(file).lower().endswith(".ptx") or str(file).lower().endswith(".pxn")\
                        or str(file).lower().endswith(".r3d") or str(file).lower().endswith(".raf")\
                        or str(file).lower().endswith(".raw") or str(file).lower().endswith(".rwl")\
                        or str(file).lower().endswith(".rw2") or str(file).lower().endswith(".rwz")\
                        or str(file).lower().endswith(".sr2") or str(file).lower().endswith(".srf")\
                        or str(file).lower().endswith(".srw") or str(file).lower().endswith(".x3f"):
                            filePathList.append(
                            path.normcase(
                            path.normpath(
                            path.abspath(
                            path.expanduser(
                            path.expandvars(
                            path.join(
                            root, file)))))))
            else:
                for root, dirs, files in walk(directoryPath, followlinks=followLinksBoolean):
                    for file in files:
                        if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                        or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                        or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                        or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                        or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                        or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm"):
                            filePathList.append(
                            path.normcase(
                            path.normpath(
                            path.abspath(
                            path.expanduser(
                            path.expandvars(
                            path.join(
                            root, file)))))))
        else:
            if rawsBoolean == True:
                for file in listdir(directoryPath):
                    if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                    or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                    or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                    or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                    or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                    or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm")\
                    or str(file).lower().endswith(".3fr") or str(file).lower().endswith(".ari")\
                    or str(file).lower().endswith(".arw") or str(file).lower().endswith(".bay")\
                    or str(file).lower().endswith(".crw") or str(file).lower().endswith(".cr2")\
                    or str(file).lower().endswith(".cap") or str(file).lower().endswith(".data")\
                    or str(file).lower().endswith(".dcs") or str(file).lower().endswith(".dcr")\
                    or str(file).lower().endswith(".dng") or str(file).lower().endswith(".drf")\
                    or str(file).lower().endswith(".eip") or str(file).lower().endswith(".erf")\
                    or str(file).lower().endswith(".fff") or str(file).lower().endswith(".gpr")\
                    or str(file).lower().endswith(".iiq") or str(file).lower().endswith(".k25")\
                    or str(file).lower().endswith(".kdc") or str(file).lower().endswith(".mdc")\
                    or str(file).lower().endswith(".mef") or str(file).lower().endswith(".mos")\
                    or str(file).lower().endswith(".mrw") or str(file).lower().endswith(".nef")\
                    or str(file).lower().endswith(".nrw") or str(file).lower().endswith(".obm")\
                    or str(file).lower().endswith(".orf") or str(file).lower().endswith(".pef")\
                    or str(file).lower().endswith(".ptx") or str(file).lower().endswith(".pxn")\
                    or str(file).lower().endswith(".r3d") or str(file).lower().endswith(".raf")\
                    or str(file).lower().endswith(".raw") or str(file).lower().endswith(".rwl")\
                    or str(file).lower().endswith(".rw2") or str(file).lower().endswith(".rwz")\
                    or str(file).lower().endswith(".sr2") or str(file).lower().endswith(".srf")\
                    or str(file).lower().endswith(".srw") or str(file).lower().endswith(".x3f"):
                        filePathList.append(
                        path.normcase(
                        path.normpath(
                        path.abspath(
                        path.expanduser(
                        path.expandvars(
                        path.join(
                        directoryPath, file)))))))
            else:
                for file in listdir(directoryPath):
                    if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                    or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                    or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                    or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                    or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                    or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm"):
                        filePathList.append(
                        path.normcase(
                        path.normpath(
                        path.abspath(
                        path.expanduser(
                        path.expandvars(
                        path.join(
                        directoryPath, file)))))))
    else:
        if recursiveBoolean == True:
            if rawsBoolean == True:
                for root, dirs, files in walk(path.curdir, followlinks=followLinksBoolean):
                    for file in files:
                        if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                        or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                        or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                        or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                        or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                        or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm")\
                        or str(file).lower().endswith(".3fr") or str(file).lower().endswith(".ari")\
                        or str(file).lower().endswith(".arw") or str(file).lower().endswith(".bay")\
                        or str(file).lower().endswith(".crw") or str(file).lower().endswith(".cr2")\
                        or str(file).lower().endswith(".cap") or str(file).lower().endswith(".data")\
                        or str(file).lower().endswith(".dcs") or str(file).lower().endswith(".dcr")\
                        or str(file).lower().endswith(".dng") or str(file).lower().endswith(".drf")\
                        or str(file).lower().endswith(".eip") or str(file).lower().endswith(".erf")\
                        or str(file).lower().endswith(".fff") or str(file).lower().endswith(".gpr")\
                        or str(file).lower().endswith(".iiq") or str(file).lower().endswith(".k25")\
                        or str(file).lower().endswith(".kdc") or str(file).lower().endswith(".mdc")\
                        or str(file).lower().endswith(".mef") or str(file).lower().endswith(".mos")\
                        or str(file).lower().endswith(".mrw") or str(file).lower().endswith(".nef")\
                        or str(file).lower().endswith(".nrw") or str(file).lower().endswith(".obm")\
                        or str(file).lower().endswith(".orf") or str(file).lower().endswith(".pef")\
                        or str(file).lower().endswith(".ptx") or str(file).lower().endswith(".pxn")\
                        or str(file).lower().endswith(".r3d") or str(file).lower().endswith(".raf")\
                        or str(file).lower().endswith(".raw") or str(file).lower().endswith(".rwl")\
                        or str(file).lower().endswith(".rw2") or str(file).lower().endswith(".rwz")\
                        or str(file).lower().endswith(".sr2") or str(file).lower().endswith(".srf")\
                        or str(file).lower().endswith(".srw") or str(file).lower().endswith(".x3f"):
                            filePathList.append(
                            path.normcase(
                            path.normpath(
                            path.abspath(
                            path.expanduser(
                            path.expandvars(
                            path.join(
                            root, file)))))))
            else:
                for root, dirs, files in walk(path.curdir, followlinks=followLinksBoolean):
                    for file in files:
                        if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                        or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                        or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                        or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                        or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                        or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm"):
                            filePathList.append(
                            path.normcase(
                            path.normpath(
                            path.abspath(
                            path.expanduser(
                            path.expandvars(
                            path.join(
                            root, file)))))))
        else:
            if rawsBoolean == True:
                for file in listdir(path.curdir):
                    if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                    or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                    or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                    or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                    or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                    or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm")\
                    or str(file).lower().endswith(".3fr") or str(file).lower().endswith(".ari")\
                    or str(file).lower().endswith(".arw") or str(file).lower().endswith(".bay")\
                    or str(file).lower().endswith(".crw") or str(file).lower().endswith(".cr2")\
                    or str(file).lower().endswith(".cap") or str(file).lower().endswith(".data")\
                    or str(file).lower().endswith(".dcs") or str(file).lower().endswith(".dcr")\
                    or str(file).lower().endswith(".dng") or str(file).lower().endswith(".drf")\
                    or str(file).lower().endswith(".eip") or str(file).lower().endswith(".erf")\
                    or str(file).lower().endswith(".fff") or str(file).lower().endswith(".gpr")\
                    or str(file).lower().endswith(".iiq") or str(file).lower().endswith(".k25")\
                    or str(file).lower().endswith(".kdc") or str(file).lower().endswith(".mdc")\
                    or str(file).lower().endswith(".mef") or str(file).lower().endswith(".mos")\
                    or str(file).lower().endswith(".mrw") or str(file).lower().endswith(".nef")\
                    or str(file).lower().endswith(".nrw") or str(file).lower().endswith(".obm")\
                    or str(file).lower().endswith(".orf") or str(file).lower().endswith(".pef")\
                    or str(file).lower().endswith(".ptx") or str(file).lower().endswith(".pxn")\
                    or str(file).lower().endswith(".r3d") or str(file).lower().endswith(".raf")\
                    or str(file).lower().endswith(".raw") or str(file).lower().endswith(".rwl")\
                    or str(file).lower().endswith(".rw2") or str(file).lower().endswith(".rwz")\
                    or str(file).lower().endswith(".sr2") or str(file).lower().endswith(".srf")\
                    or str(file).lower().endswith(".srw") or str(file).lower().endswith(".x3f"):
                        filePathList.append(
                        path.normpath(
                        path.normcase(
                        path.abspath(
                        path.expanduser(
                        path.expandvars(
                        path.join(
                        path.curdir, file)))))))
            else:
                for file in listdir(path.curdir):
                    if str(file).lower().endswith(".jpg") or str(file).lower().endswith(".jpeg")\
                    or str(file).lower().endswith(".png") or str(file).lower().endswith(".tif")\
                    or str(file).lower().endswith(".tiff") or str(file).lower().endswith(".webp")\
                    or str(file).lower().endswith(".bmp") or str(file).lower().endswith(".jp2")\
                    or str(file).lower().endswith(".j2k") or str(file).lower().endswith(".jpf")\
                    or str(file).lower().endswith(".jpx") or str(file).lower().endswith(".jpm"):
                        filePathList.append(
                        path.normcase(
                        path.normpath(
                        path.abspath(
                        path.expanduser(
                        path.expandvars(
                        path.join(
                        path.curdir, file)))))))
    return filePathList

def readDatabase(databasePath):

    db = None
    imageHashDict = {}

    if databasePath is not None:
        if path.exists(databasePath):
            print("Reading from database at " + databasePath)
            with shelve.open(databasePath, writeback=True) as db:
                for key in db:
                    imageHashDict[key] = db[key]
    return imageHashDict

def checkRaw(imagePath):

    if str(imagePath).lower().endswith(".3fr") or str(imagePath).lower().endswith(".ari")\
    or str(imagePath).lower().endswith(".arw") or str(imagePath).lower().endswith(".bay")\
    or str(imagePath).lower().endswith(".crw") or str(imagePath).lower().endswith(".cr2")\
    or str(imagePath).lower().endswith(".cap") or str(imagePath).lower().endswith(".data")\
    or str(imagePath).lower().endswith(".dcs") or str(imagePath).lower().endswith(".dcr")\
    or str(imagePath).lower().endswith(".dng") or str(imagePath).lower().endswith(".drf")\
    or str(imagePath).lower().endswith(".eip") or str(imagePath).lower().endswith(".erf")\
    or str(imagePath).lower().endswith(".fff") or str(imagePath).lower().endswith(".gpr")\
    or str(imagePath).lower().endswith(".iiq") or str(imagePath).lower().endswith(".k25")\
    or str(imagePath).lower().endswith(".kdc") or str(imagePath).lower().endswith(".mdc")\
    or str(imagePath).lower().endswith(".mef") or str(imagePath).lower().endswith(".mos")\
    or str(imagePath).lower().endswith(".mrw") or str(imagePath).lower().endswith(".nef")\
    or str(imagePath).lower().endswith(".nrw") or str(imagePath).lower().endswith(".obm")\
    or str(imagePath).lower().endswith(".orf") or str(imagePath).lower().endswith(".pef")\
    or str(imagePath).lower().endswith(".ptx") or str(imagePath).lower().endswith(".pxn")\
    or str(imagePath).lower().endswith(".r3d") or str(imagePath).lower().endswith(".raf")\
    or str(imagePath).lower().endswith(".raw") or str(imagePath).lower().endswith(".rwl")\
    or str(imagePath).lower().endswith(".rw2") or str(imagePath).lower().endswith(".rwz")\
    or str(imagePath).lower().endswith(".sr2") or str(imagePath).lower().endswith(".srf")\
    or str(imagePath).lower().endswith(".srw") or str(imagePath).lower().endswith(".x3f"):
        return True
    else:
        return False

def calculateHash(hashAlgorithmString,
                imageHashDict,
                imagePath,
                image,
                hashSizeInt):

    if hashAlgorithmString == 'dhash':
        imageHashDict[imagePath] = dhash(image, hash_size=hashSizeInt)
    elif hashAlgorithmString == 'dhash_vertical':
        imageHashDict[imagePath] = dhash_vertical(image, hash_size=hashSizeInt)
    elif hashAlgorithmString == 'ahash':
        imageHashDict[imagePath] = average_hash(image, hash_size=hashSizeInt)
    elif hashAlgorithmString == 'phash':
        imageHashDict[imagePath] = phash(image, hash_size=hashSizeInt)
    elif hashAlgorithmString == 'phash_simple':
        imageHashDict[imagePath] = phash_simple(image, hash_size=hashSizeInt)
    elif hashAlgorithmString == 'whash_haar':
        imageHashDict[imagePath] = whash(image, hash_size=hashSizeInt)
    elif hashAlgorithmString == 'whash_db4':
        imageHashDict[imagePath] = whash(image,
                                        hash_size=hashSizeInt,
                                        mode='db4')
    elif hashAlgorithmString == None:
        imageHashDict[imagePath] = phash(image, hash_size=hashSizeInt)
    return imageHashDict

def writeDatabase(databasePath, imageHashDict):

    if databasePath is not None:
        with shelve.open(databasePath) as db:
            for key in imageHashDict:
                db[key] = imageHashDict[key]

def generateHashDict(imagePathList,
                    hashAlgorithmString,
                    hashSizeInt,
                    databasePath,
                    imageHashDict):

    image = None

    if hashSizeInt == None:
        hashSizeInt = 8
    for imagePath in imagePathList:
        if imagePath not in imageHashDict.keys():
            print("Hashing " + str(imagePath))
            if checkRaw(imagePath):
                if path.isfile(imagePath + ".jpg"):
                    with Image.open(imagePath + ".jpg") as image:
                        imageHashDict = calculateHash(hashAlgorithmString,
                                                    imageHashDict,
                                                    imagePath,
                                                    image,
                                                    hashSizeInt)
                        writeDatabase(databasePath, imageHashDict)
                else:
                    image = imread(imagePath)
                    image = image.postprocess()
                    imsave(imagePath + ".jpg", image)
                    with Image.open(imagePath + ".jpg") as image:
                        imageHashDict = calculateHash(hashAlgorithmString,
                                                    imageHashDict,
                                                    imagePath,
                                                    image,
                                                    hashSizeInt)
                        writeDatabase(databasePath, imageHashDict)
                    remove(imagePath + ".jpg")
            else:
                with Image.open(imagePath) as image:
                    imageHashDict = calculateHash(hashAlgorithmString,
                                                imageHashDict,
                                                imagePath,
                                                image,
                                                hashSizeInt)
                    writeDatabase(databasePath, imageHashDict)
    return imageHashDict

def pruneDatabase(databasePath, imageHashDict):

    db = None

    if databasePath is not None:
        if path.exists(databasePath):
            with shelve.open(databasePath, writeback=True) as db:
                for key in db.keys():
                    if not path.exists(key):
                        if key in imageHashDict:
                            del imageHashDict[key]
                        del db[key]
                for key in imageHashDict.keys():
                    if not path.exists(key):
                        if imageHashDict[key] in db:
                            del db[key]
                        del imageHashDict[key]
    return imageHashDict

def compareHashes(imageHashDict):

    reverseMultiDict = {}
    duplicateListOfSets = {}
    duplicateListOfLists = []

    for key, value in imageHashDict.items():
        reverseMultiDict.setdefault(value, set()).add(key)
    duplicateListOfSets = [values for key, values in reverseMultiDict.items() if len(values) > 1]
    for i in range(0, len(duplicateListOfSets)):
        duplicateListOfLists.append(list(duplicateListOfSets[i]))
    return duplicateListOfLists

def printDuplicates(imageListOfLists):

    for i in range(0, len(imageListOfLists)):
        for j in range(0, len(imageListOfLists[i])):
            print("Found possible duplicate: " + str(imageListOfLists[i][j]))
    return imageListOfLists

def displayImage(imageListOfLists, viewerCommandString, viewerOptionsString):

    for i in range(0, len(imageListOfLists)):
        input("Press enter to open the next set of possible duplicates: ")
        if viewerCommandString is None:
            for j in range(0, len(imageListOfLists[i])):
                webbrowser.open(imageListOfLists[i][j])
        elif viewerCommandString is not None and viewerOptionsString is None:
            subprocess.run([viewerCommandString] + imageListOfLists[i])
        else:
            subprocess.run([viewerCommandString, viewerOptionsString]
                            + imageListOfLists[i])

def main():

    args = None

    args = createArgumentParser()
    displayImage(
    printDuplicates(
    compareHashes(
    pruneDatabase(
    args.database,
    generateHashDict(
    getImagePaths(
    args.directory,
    args.recursive,
    args.links,
    args.raws,
    args.algorithm),
    args.algorithm,
    args.hash_size,
    args.database,
    readDatabase(
    args.database))))),
    args.program,
    args.options)
    exit()

main()
