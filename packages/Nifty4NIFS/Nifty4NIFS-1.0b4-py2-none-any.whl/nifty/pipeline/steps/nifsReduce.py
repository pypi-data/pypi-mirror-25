#!/usr/bin/env python

# MIT License

# Copyright (c) 2015, 2017 Marie Lemoine-Busserolle

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

################################################################################
#                Import some useful Python utilities/modules                   #
################################################################################

# STDLIB

import sys, glob, shutil, getopt, os, time, logging, glob, sgmllib, urllib, re, traceback, pkg_resources
import pexpect as p
from pyraf import iraf, iraffunctions
import astropy.io.fits
from astropy.io.fits import getdata, getheader
import numpy as np
from scipy.interpolate import interp1d
from scipy import arange, array, exp
from scipy.ndimage.interpolation import shift
import pylab as pl
import matplotlib.pyplot as plt

# LOCAL

# Import config parsing.
from ..configobj.configobj import ConfigObj
# Import custom Nifty functions.
from ..nifsUtils import datefmt, listit, writeList, checkLists, makeSkyList, MEFarith, convertRAdec
# Import Nifty python data cube merging script.
from .nifsMerge import mergeCubes

# Define constants
# Paths to Nifty data.
RECIPES_PATH = pkg_resources.resource_filename('nifty', 'recipes/')
RUNTIME_DATA_PATH = pkg_resources.resource_filename('nifty', 'runtimeData/')

def start(kind, telluricDirectoryList="", scienceDirectoryList=""):
    """

    start(kind): Do a full reduction of either Science or Telluric data.

    nifsReduce- for the telluric and science data reduction.

    Reduces NIFS telluric and science frames and attempts a flux calibration.

    Parameters are loaded from runtimeData/config.cfg. This script will
    automatically detect if it is being run on telluric data or science data.

    There are 6 steps.

    INPUT:
    + Raw files
        - Science frames
        - Sky frames
    + Calibration files
        - MDF shift file
        - Bad Pixel Mask (BPM)
        - Flat field frame
        - Reduced arc frame
        - Reduced ronchi mask frame
        - arc and ronchi database/ files

    OUTPUT:
        - If telluric reduction an efficiency spectrum used to telluric correct and absolute flux
          calibrate science frames
        - If science reduction a reduced science data cube.

    Args:
        kind(string): either 'Telluric' or 'Science'.

    """

    # TODO(nat): Right now the pipeline will crash if you decide to skip, say, doing a bad
    # pixel correction. This is because each step adds a prefix to the frame name, and most following
    # steps depend on that prefix being there.
    # One way to fix this is if a step is to be skipped, iraf.copy() is called instead to copy the frame and
    # add the needed prefix. Messy but it might work for now.

    ###########################################################################
    ##                                                                       ##
    ##                  BEGIN - GENERAL REDUCTION SETUP                      ##
    ##                                                                       ##
    ###########################################################################

    # Store current working directory for later use.
    path = os.getcwd()

    # Set up the logging file.
    log = os.getcwd()+'/Nifty.log'

    logging.info('\n#################################################')
    logging.info('#                                               #')
    logging.info('# Start the NIFS Science and Telluric Reduction #')
    logging.info('#                                               #')
    logging.info('#################################################\n')

    # Set up/prepare IRAF.
    iraf.gemini()
    iraf.gemtools()
    iraf.gnirs()
    iraf.nifs()

    # Reset to default parameters the used IRAF tasks.
    iraf.unlearn(iraf.gemini,iraf.gemtools,iraf.gnirs,iraf.nifs,iraf.imcopy)

    # From http://bishop.astro.pomona.edu/Penprase/webdocuments/iraf/beg/beg-image.html:
    # Before doing anything involving image display the environment variable
    # stdimage must be set to the correct frame buffer size for the display
    # servers (as described in the dev$graphcap file under the section "STDIMAGE
    # devices") or to the correct image display device. The task GDEVICES is
    # helpful for determining this information for the display servers.
    iraf.set(stdimage='imt2048')

    # Prepare the IRAF package for NIFS.
    # NSHEADERS lists the header parameters used by the various tasks in the
    # NIFS package (excluding headers values which have values fixed by IRAF or
    # FITS conventions).
    iraf.nsheaders("nifs",logfile=log)

    # Set clobber to 'yes' for the script. This still does not make the gemini
    # tasks overwrite files, so:
    # YOU WILL LIKELY HAVE TO REMOVE FILES IF YOU RE_RUN THE SCRIPT.
    user_clobber=iraf.envget("clobber")
    iraf.reset(clobber='yes')

    # This helps make sure all variables are initialized to prevent bugs.
    continuuminter = None
    hlineinter = None
    hline_method = None
    spectemp = None
    mag = None
    scienceSkySubtraction = None
    telluricSkySubtraction = None
    telluricCorrectionMethod = None
    telinter = None
    efficiencySpectrumCorrection = None
    use_pq_offsets = None
    im3dtran = None
    fluxCalibrationMethod = None

    # Load reduction parameters from runtimeData/config.cfg.
    with open('./config.cfg') as config_file:
        config = ConfigObj(config_file, unrepr=True)
        # Read general pipeline config.
        over = config['over']
        manualMode = config['manualMode']
        merge = config['merge']
        calDirList = config['calibrationDirectoryList']

        if kind == 'Telluric':
            # Telluric reduction specific config.
            telluricReductionConfig = config['telluricReductionConfig']
            if telluricDirectoryList:
                observationDirectoryList = telluricDirectoryList
            elif not telluricDirectoryList:
                observationDirectoryList = config['telluricDirectoryList']
            start = telluricReductionConfig['telStart']
            stop = telluricReductionConfig['telStop']
            telluricSkySubtraction = telluricReductionConfig['telluricSkySubtraction']
            continuuminter = telluricReductionConfig['continuuminter']
            hlineinter = telluricReductionConfig['hlineinter']
            hline_method = telluricReductionConfig['hline_method']
            spectemp = telluricReductionConfig['spectemp']
            mag = telluricReductionConfig['mag']

        if kind == 'Science':
            # Science reduction specific config.
            scienceReductionConfig = config['scienceReductionConfig']
            if scienceDirectoryList:
                observationDirectoryList = scienceDirectoryList
            elif not scienceDirectoryList:
                observationDirectoryList = config['scienceDirectoryList']
            start = scienceReductionConfig['sciStart']
            stop = scienceReductionConfig['sciStop']
            scienceSkySubtraction = scienceReductionConfig['scienceSkySubtraction']
            telluricCorrectionMethod = scienceReductionConfig['telluricCorrectionMethod']
            telinter = scienceReductionConfig['telinter']
            fluxCalibrationMethod = scienceReductionConfig['fluxCalibrationMethod']
            use_pq_offsets = scienceReductionConfig['use_pq_offsets']
            im3dtran = scienceReductionConfig['im3dtran']

    ###########################################################################
    ##                                                                       ##
    ##                 COMPLETE - GENERAL REDUCTION SETUP                    ##
    ##                                                                       ##
    ###########################################################################

    # nifsReduce has two nested loops that reduced data.
    # It loops through each science (or telluric) directory, and
    # runs through a series of calibrations steps on the data in that directory.

    # Loop through all the observation (telluric or science) directories to perform a reduction on each one.
    for observationDirectory in observationDirectoryList:

        ###########################################################################
        ##                                                                       ##
        ##                  BEGIN - OBSERVATION SPECIFIC SETUP                   ##
        ##                                                                       ##
        ###########################################################################

        # Print the current directory of data being reduced.
        logging.info("\n#################################################################################")
        logging.info("                                   ")
        logging.info("  Currently working on reductions in")
        logging.info("  in "+ str(observationDirectory))
        logging.info("                                   ")
        logging.info("#################################################################################\n")

        os.chdir(observationDirectory)
        tempObs = observationDirectory.split(os.sep)

        # Find the Calibrations_grating directory that corresponds to the observation date and grating.
        # The observation date and grating are found from directory paths.
        for calDir in calDirList:
            tempCal = calDir.split(os.sep)
            # Need two cases because science directory paths are shorter than telluric
            # directory paths.
            # For science observation directories:
            # IF dates in path names match AND gratings in path names match, break.
            if tempObs[-3]==tempCal[-2] and tempObs[-2] == tempCal[-1][-1]:
                calDir = calDir+'/'
                break
            # For telluric observation directories.
            # IF dates in path names match AND gratings in path names match, break.
            elif tempObs[-4]==tempCal[-2] and tempObs[-3] == tempCal[-1][-1]:
                calDir = calDir+'/'
                break

        obsid = tempObs[-1]

        # Change the iraf directory to the current directory.
        pwd = os.getcwd()
        iraffunctions.chdir(pwd)

        # Copy relevant calibrations over to the science directory.
        # Open and store the name of the MDF shift reference file from shiftfile into shift.
        shift = calDir+str(open(calDir+"shiftfile", "r").readlines()[0]).strip()
        # Open and store the name of the flat frame from flatfile in flat.
        flat = calDir+str(open(calDir+"flatfile", "r").readlines()[0]).strip()
        # Open and store the bad pixel mask name from sflat_bpmfile in sflat_bpm.
        sflat_bpm = calDir+str(open(calDir+"sflat_bpmfile", "r").readlines()[0]).strip()
        # Open and store the name of the reduced spatial correction ronchi flat frame name from ronchifile in ronchi.
        ronchi = open(calDir+"ronchifile", "r").readlines()[0].strip()
        # Copy the spatial calibration ronchi flat frame from Calibrations_grating to the observation directory.
        iraf.copy(calDir+ronchi+".fits", output="./")
        # Open and store the name of the reduced wavelength calibration arc frame from arclist in arc.
        arc = "wrgn"+str(open(calDir+"arclist", "r").readlines()[0]).strip()
        # Copy the wavelength calibration arc frame from Calibrations_grating to the observation directory.
        iraf.copy(calDir+arc+".fits", output="./")
        # Make sure the database files are in place. Current understanding is that
        # these should be local to the reduction directory, so need to be copied from
        # the calDir.
        if os.path.isdir("./database"):
            if over:
                shutil.rmtree("./database")
                os.mkdir("./database")
        elif not os.path.isdir("./database"):
            os.mkdir('./database/')
        iraf.copy(input=calDir+"database/*", output="./database/")

        if telluricSkySubtraction or scienceSkySubtraction:
            # Read the list of sky frames in the observation directory.
            try:
                skyFrameList = open("skyFrameList", "r").readlines()
                skyFrameList = [frame.strip() for frame in skyFrameList]
            except:
                logging.info("\n#####################################################################")
                logging.info("#####################################################################")
                logging.info("")
                logging.info("     WARNING in reduce: No sky frames were found in a directory.")
                logging.info("              Please make a skyFrameList in: " + str(os.getcwd()))
                logging.info("")
                logging.info("#####################################################################")
                logging.info("#####################################################################\n")
                raise SystemExit
            sky = skyFrameList[0]

        # If we are doing a telluric reduction, open the list of telluric frames in the observation directory.
        # If we are doing a science reduction, open the list of science frames in the observation directory.
        if kind == 'Telluric':
            tellist = open('tellist', 'r').readlines()
            tellist = [frame.strip() for frame in tellist]
        elif kind == 'Science':
            scienceFrameList = open("scienceFrameList", "r").readlines()
            scienceFrameList = [frame.strip() for frame in scienceFrameList]
            # For science frames, check to see if the number of sky frames matches the number of science frames.
            # IF NOT duplicate the sky frames and rewrite the sky file and skyFrameList.
            if scienceSkySubtraction:
                if not len(skyFrameList)==len(scienceFrameList):
                    skyFrameList = makeSkyList(skyFrameList, scienceFrameList, observationDirectory)

        ###########################################################################
        ##                                                                       ##
        ##                 COMPLETE - OBSERVATION SPECIFIC SETUP                 ##
        ##                BEGIN DATA REDUCTION FOR AN OBSERVATION                ##
        ##                                                                       ##
        ###########################################################################

        # Check start and stop values for reduction steps. Ask user for a correction if
        # input is not valid.
        valindex = start
        while valindex > stop  or valindex < 1 or stop > 6:
            logging.info("\n#####################################################################")
            logging.info("#####################################################################")
            logging.info("")
            logging.info("     WARNING in reduce: invalid start/stop values of observation")
            logging.info("                           reduction steps.")
            logging.info("")
            logging.info("#####################################################################")
            logging.info("#####################################################################\n")

            valindex = int(raw_input("\nPlease enter a valid start value (1 to 7, default 1): "))
            stop = int(raw_input("\nPlease enter a valid stop value (1 to 7, default 7): "))

        while valindex <= stop :

            ###########################################################################
            ##  STEP 1: Prepare raw data; science, telluric and sky frames ->n       ##
            ###########################################################################

            if valindex == 1:
                if manualMode:
                    a = raw_input("About to enter step 1: locate the spectrum.")
                if kind=='Telluric':
                    tellist = prepare(tellist, shift, sflat_bpm, log, over)
                elif kind=='Science':
                    scienceFrameList = prepare(scienceFrameList, shift, sflat_bpm, log, over)
                if telluricSkySubtraction or scienceSkySubtraction:
                    skyFrameList = prepare(skyFrameList, shift, sflat_bpm, log, over)
                logging.info("\n##############################################################################")
                logging.info("")
                logging.info("  STEP 1: Locate the Spectrum (and prepare raw data) ->n - COMPLETED ")
                logging.info("")
                logging.info("##############################################################################\n")

            ###########################################################################
            ##  STEP 2: Sky Subtraction ->sn                                         ##
            ###########################################################################

            elif valindex == 2:
                if manualMode:
                    a = raw_input("About to enter step 2: sky subtraction.")
                # Combine telluric sky frames.
                if kind=='Telluric':
                    if telluricSkySubtraction:
                        if len(skyFrameList)>1:
                            combineImages(skyFrameList, "gn"+sky, log, over)
                        else:
                            copyImage(skyFrameList, 'gn'+sky+'.fits', over)
                        skySubtractTel(tellist, "gn"+sky, log, over)
                    else:
                        for image in tellist:
                            iraf.copy('n'+image+'.fits', 'sn'+image+'.fits')

                if kind=='Science':
                    if scienceSkySubtraction:
                        skySubtractObj(scienceFrameList, skyFrameList, log, over)
                    else:
                        for image in scienceFrameList:
                            iraf.copy('n'+image+'.fits', 'sn'+image+'.fits')

                logging.info("\n##############################################################################")
                logging.info("")
                logging.info("  STEP 2: Sky Subtraction ->sn - COMPLETED ")
                logging.info("")
                logging.info("##############################################################################\n")

            ##############################################################################
            ##  STEP 3: Flat field, slice, subtract dark and correct bad pixels ->brsn  ##
            ##############################################################################

            elif valindex == 3:
                if manualMode:
                    a = raw_input("About to enter step 3: flat fielding and bad pixels correction.")
                if kind=='Telluric':
                    applyFlat(tellist, flat, log, over, kind)
                    fixBad(tellist, log, over)
                elif kind=='Science':
                    applyFlat(scienceFrameList, flat, log, over, kind)
                    fixBad(scienceFrameList, log, over)
                logging.info("\n##############################################################################")
                logging.info("")
                logging.info("  STEP 3: Flat fielding and Bad Pixels Correction ->brsn - COMPLETED ")
                logging.info("")
                logging.info("##############################################################################\n")


            ###########################################################################
            ##  STEP 4: Derive and apply 2D to 3D transformation ->tfbrsn            ##
            ###########################################################################

            elif valindex == 4:
                if manualMode:
                    a = raw_input("About to enter step 4: 2D to 3D transformation and Wavelength Calibration.")
                if kind=='Telluric':
                    fitCoords(tellist, arc, ronchi, log, over, kind)
                    transform(tellist, log, over)
                elif kind=='Science':
                    fitCoords(scienceFrameList, arc, ronchi, log, over, kind)
                    transform(scienceFrameList, log, over)
                logging.info("\n##############################################################################")
                logging.info("")
                logging.info("  STEP 4: 2D to 3D transformation and Wavelength Calibration ->tfbrsn - COMPLETED ")
                logging.info("")
                logging.info("##############################################################################\n")

            ############################################################################
            ##  STEP 5 (tellurics): For telluric data derive a telluric               ##
            ##                     correction ->gxtfbrsn                              ##
            ##  STEP 5 (science): For science apply an efficiency correction and make ##
            ##           a data cube (not necessarily in that order).                 ##
            ##           (i) Python method applies correction to nftransformed cube.  ##
            ##           Good for faint objects.                        ->cptfbrsn    ##
            ##           (ii) iraf.telluric method applies correction to              ##
            ##           nftransformed result (not quite a data cube) then            ##
            ##           nftransforms cube.                             ->catfbrsn    ##
            ##           (iii) If no telluric correction/flux calibration to be       ##
            ##           applied make a plain data cube.                ->ctfbrsn     ##
            ############################################################################

            elif valindex == 5:
                if manualMode:
                    a = raw_input("About to enter step 5.")
                # For telluric data:
                # Make a 1D telluric correction spectrum from reduced telluric data.
                if kind=='Telluric':
                    extractOneD(tellist, kind, log, over)
                    logging.info("\n##############################################################################")
                    logging.info("")
                    logging.info("  STEP 5: Extract 1D Spectra and Make Combined Telluric")
                    logging.info("          1D spectrum ->gxtfbrsn - COMPLETED")
                    logging.info("")
                    logging.info("##############################################################################\n")

                # For science data, either:
                # Make an uncorrected data cube.
                # Make a telluric corrected data cube.
                # Make a roughly flux-calibrated data cube.
                elif kind=='Science':
                    extract = True
                    if extract:
                        extractOneD(scienceFrameList, kind, log, over)
                        copyExtracted(scienceFrameList, over)
                    makeCube('tfbrsn', scienceFrameList, log, over)
                    if telluricCorrectionMethod == "gnirs":
                        applyTelluricCube(scienceFrameList)
                    if fluxCalibrationMethod == "gnirs":
                        fluxCalibrate(scienceFrameList)

                    logging.info("\n##############################################################################")
                    logging.info("")
                    logging.info("  STEP 5: Make uncorrected, telluric corrected and flux calibrated data cubes,")
                    logging.info("          ->ctgbrsn, ->actfbrsn or ->factfbrsn - COMPLETED")
                    logging.info("")
                    logging.info("##############################################################################\n")

            ###########################################################################
            ##  STEP 6 (Tellurics): Create an efficiency spectrum ->cgxtfbrsn        ##
            ##  STEP 6 (Science): Create a final combined 3D data cube               ##
            ##    ->[date]_[obsid]_merged.fits (and ->TOTAL_merged[grating].fits, if ##
            ##    multiple observations to be merged).                               ##
            ###########################################################################

            elif valindex == 6:
                if manualMode:
                    a = raw_input("About to enter step 6.")
                if kind == 'Telluric':
                    makeTelluricCorrection(
                        observationDirectory, path, continuuminter, hlineinter,
                        hline_method, spectemp, mag, log, over)
                    logging.info("\n##############################################################################")
                    logging.info("")
                    logging.info("  STEP 6: Create Efficiency Spectrum ->fcatfbrsn or ->fctfbrsn - COMPLETED ")
                    logging.info("")
                    logging.info("##############################################################################\n")
                # After the last science reduction, possibly merge final cubes to a single cube.
                if kind == 'Science' and merge and os.getcwd() == observationDirectoryList[-1]:
                    # There are three types of merging to choose from. You can:
                    # Merge uncorrected cubes. These have the "ctfbrsn" prefix.
                    mergeUncorrected = True
                    if mergeUncorrected:
                        mergeCubes(observationDirectoryList, "uncorrected", use_pq_offsets, im3dtran, over)
                    # Merge telluric corrected cubes. These have the "actfbrsn" prefix.
                    mergeTelluricCorrected = True
                    if mergeTelluricCorrected:
                        mergeCubes(observationDirectoryList, "telluricCorrected", use_pq_offsets, im3dtran, over)
                    # Merge telluric corrected AND flux calibrated cubes. These have the "factfbrsn" prefix.
                    mergeTelCorAndFluxCalibrated = True
                    if mergeTelCorAndFluxCalibrated:
                        mergeCubes(observationDirectoryList, "telCorAndFluxCalibrated", use_pq_offsets, im3dtran, over)

                    logging.info("\n##############################################################################")
                    logging.info("")
                    logging.info("  STEP 6: Create Combined Final 3D Cube - path/scienceObjectName/Merged/ - COMPLETED ")
                    logging.info("")
                    logging.info("##############################################################################\n")

            valindex += 1

        logging.info("\n##############################################################################")
        logging.info("")
        logging.info("  COMPLETE - Reductions completed for " + str(observationDirectory))
        logging.info("")
        logging.info("##############################################################################\n")

    # Return to directory script was begun from.
    os.chdir(path)
    return

##################################################################################################################
#                                                     ROUTINES                                                   #
##################################################################################################################

def prepare(inlist, shiftima, sflat_bpm, log, over):
    """Prepare list of frames using iraf.nfprepare. Output: -->n.

    Processing with NFPREPARE (this task is used only for NIFS data
    but other instruments have their own preparation tasks
    with similar actions) will rename the data extension and add
    variance and data quality extensions. By default (see NSHEADERS)
    the extension names are SCI for science data, VAR for variance, and
    DQ for data quality (0 = good). Generation of the data quality
    plane (DQ) is important in order to fix hot and dark pixels on the
    NIFS detector in subsequent steps in the data reduction process.
    Various header keywords (used later) are also added in NFPREPARE.
    NFPREPARE will also add an MDF file (extension MDF) describing the
    NIFS image slicer pattern and how the IFU maps to the sky field.

    """

    # Update frames with mdf offset value and generate variance and data quality extensions.
    for frame in inlist:
        if os.path.exists("n"+frame+".fits"):
            if over:
                os.remove("n"+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping prepare_list")
                continue
        iraf.nfprepare(frame, rawpath="", shiftimage=shiftima, fl_vardq="yes", bpm=sflat_bpm, fl_int='yes', fl_corr='no', fl_nonl='no', logfile=log)
    inlist = checkLists(inlist, '.', 'n', '.fits')
    return inlist

#--------------------------------------------------------------------------------------------------------------------------------#

def combineImages(inlist, out, log, over):
    """Gemcombine multiple frames. Output: -->gn."""

    if os.path.exists(out+".fits"):
        if over:
            iraf.delete(out+".fits")
        else:
            logging.info("Output file exists and -over not set - skipping combine_ima")
            return

    iraf.gemcombine(listit(inlist,"n"),output=out,fl_dqpr='yes', fl_vardq='yes',masktype="none", combine="median", logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def copyImage(input, output, over):
    """Copy a frame (used to add the correct prefix when skipping steps)."""

    if os.path.exists(output):
        if over:
            iraf.delete(output)
        else:
            logging.info("Output file exists and -over not set - skipping copy_ima")
            return

    iraf.copy('n'+input[0]+'.fits', output)

#--------------------------------------------------------------------------------------------------------------------------------#

def skySubtractObj(objlist, skyFrameList, log, over):
    """"Sky subtraction for science using iraf.gemarith. Output: ->sgn"""

    for i in range(len(objlist)):
        frame = str(objlist[i])
        sky = str(skyFrameList[i])
        if os.path.exists("sn"+frame+".fits"):
           if over:
               os.remove("sn"+frame+".fits")
           else:
               logging.info("Output file exists and -over not set - skipping skysub_list")
               continue
        iraf.gemarith ("n"+frame, "-", "n"+sky, "sn"+frame, fl_vardq="yes", logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def skySubtractTel(tellist, sky, log, over):
    """Sky subtraction for telluric using iraf.gemarith. Output: ->sgn"""

    for frame in tellist:
        if os.path.exists("sn"+frame+".fits"):
            if over:
                os.remove("sn"+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping skySubtractTel.")
                continue
        iraf.gemarith ("n"+frame, "-", sky, "sn"+frame, fl_vardq="yes", logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def applyFlat(objlist, flat, log, over, kind, dark=""):
    """Flat field and cut the data with iraf.nsreduce. Output: ->rsgn.

    NSREDUCE is used for basic reduction of raw data - it provides a
    single, unified interface to several tasks and also allows for
    the subtraction of dark frames and dividing by the flat. For
    NIFS reduction, NSREDUCE is used to call the NSCUT and NSAPPWAVE
    routines.

    """

    # By default don't subtract darks from tellurics.
    fl_dark = "no"
    if dark != "":
        fl_dark = "yes"

    for frame in objlist:
        frame = str(frame).strip()
        if os.path.exists("rsn"+frame+".fits"):
            if over:
                os.remove("rsn"+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping apply_flat_list")
                continue
        iraf.nsreduce("sn"+frame, fl_cut="yes", fl_nsappw="yes", fl_dark="no", fl_sky="no", fl_flat="yes", flatimage=flat, fl_vardq="yes",logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def fixBad(objlist, log, over):
    """Interpolate over bad pixels flagged in the DQ plane with iraf.nffixbad. Output: -->brsn.

    NFFIXBAD - Fix Hot/Cold pixels on the NIFS detector.

    This routine uses the information in the Data Quality
    extensions to fix hot and cold pixels in the NIFS science
    fields. NFFIXBAD is a wrapper script which calls the task
    FIXPIX, using the DQ plane to define the pixels to be corrected.

    """

    for frame in objlist:
        frame = str(frame).strip()
        if os.path.exists("brsn"+frame+".fits"):
            if over:
                os.remove("brsn"+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping fixbad_list")
                continue
        iraf.nffixbad("rsn"+frame,logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def fitCoords(objlist, arc, ronchi, log, over, kind):
    """Derive the 2D to 3D spatial/spectral transformation with iraf.nsfitcoords.
    Output: -->fbrsn

    NFFITCOORDS - Compute 2D dispersion and distortion maps.

    This routine uses as inputs the output from the NSWAVELENGTH
    and NFSDIST routines. NFFITCOORDS takes the spatial and
    spectral rectification information from NSWAVELENGTH and
    NFSDIST and converts this into a calculation of where the data
    information should map to in a final IFU dataset.

    """

    for frame in objlist:
        frame = str(frame).strip()
        if os.path.exists("fbrsn"+frame+".fits"):
            if over:
                os.remove("fbrsn"+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping fitcoord_list")
                continue
        iraf.nsfitcoords("brsn"+frame, lamptransf=arc, sdisttransf=ronchi, lxorder=3, lyorder=2, sxorder=3, syorder=3, logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def transform(objlist, log, over):
    """Apply the transformation determined in iraf.nffitcoords with
    iraf.nstransform. Output: -->tfbrsgn

    NSTRANSFORM - Spatially rectify and wavelength calibrate data.

    NFTRANSFORM applies the wavelength solution found by
    NSWAVELENGTH and the spatial correction found by NFSDIST,
    aligning all the IFU extensions consistently onto a common
    coordinate system. The output of this routine is still in 2D
    format, with each of the IFU slices represented by its own data
    extension.

    """

    for frame in objlist:
        frame = str(frame).strip()
        if os.path.exists("tfbrsn"+frame+".fits"):
            if over:
                iraf.delete("tfbrsn"+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping transform_list")
                continue
        iraf.nstransform("fbrsn"+frame, logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def makeCube(pre, scienceFrameList, log, over):
    """ Reformat the data into a 3-D datacube using iraf.nifcube. Output: -->ctfbrsgn.

    NIFCUBE - Construct 3D NIFS datacubes.

    NIFCUBE takes input from data output by either NFFITCOORDS or
    NFTRANSFORM and converts the 2D data images into data cubes
    that have coordinates of x, y, lambda.

    """
    for frame in scienceFrameList:
        if os.path.exists("c"+pre+frame+".fits"):
            if over:
                iraf.delete("c"+pre+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping make_cube_list")
                continue
        iraf.nifcube (pre+frame, outcubes = 'c'+pre+frame, logfile=log)

#--------------------------------------------------------------------------------------------------------------------------------#

def extractOneD(inputList, kind, log, over):
    """Extracts 1-D spectra with iraf.nfextract and combines them with iraf.gemcombine.
    iraf.nfextract is currently only done interactively. Output: -->xtfbrsn and gxtfbrsn

    NFEXTRACT - Extract NIFS spectra.

    This could be used to extract a 1D spectra from IFU data and is
    particularly useful for extracting the bright spectra of
    telluric calibrator stars. Note that this routine only works
    on data that has been run through NFTRANSFORM.

    """

    for frame in inputList:
        frame = str(frame).strip()
        if os.path.exists("xtfbrsn"+frame+".fits"):
            if over:
                iraf.delete("xtfbrsn"+frame+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping nfextract in extract1D")
                continue

        iraf.nfextract("tfbrsn"+frame, outpref="x", xc=15.0, yc=33.0, diameter=2.5, fl_int='no', logfile=log)

    # Combine all the 1D spectra to one final output file with the name of the first input file.
    combined = str(inputList[0]).strip()
    if len(inputList) > 1:
        if os.path.exists("gxtfbrsn"+combined+".fits"):
            if over:
                iraf.delete("gxtfbrsn"+combined+".fits")
            else:
                logging.info("Output file exists and -over not set - skipping gemcombine in extract1D")
                return
        iraf.gemcombine(listit(inputList,"xtfbrsn"),output="gxtfbrsn"+combined, statsec="[*]", combine="median",masktype="none",fl_vardq="yes", logfile=log)
    else:
        if over:
            iraf.delete("gxtfbrsn"+combined+".fits")
        iraf.copy(input="xtfbrsn"+combined+".fits", output="gxtfbrsn"+combined+".fits")

    if kind == 'Telluric':
        # Put the name of the final combined file into a text file called
        # telluricfile to be used by the pipeline later.
        open("telluricfile", "w").write("gxtfbrsn"+combined)
    elif kind == 'Science':
        open("combinedOneD", "w").write("gxtfbrsn"+combined)

#--------------------------------------------------------------------------------------------------------------------------------#

def copyExtracted(scienceFrameList, over):
    """
    Copy all extracted 1D spectra to objectname/ExtractedOneD/date_obsname/,
    and combined 1D spectra to objectname/ExtractedOneD
    """
    # TODO(nat): make this clearer.
    obsDir = os.getcwd()
    temp1 = os.path.split(obsDir)
    temp2 = os.path.split(temp1[0])
    temp3 = os.path.split(temp2[0])
    temp4 = os.path.split(temp3[0])
    objname = temp4[1]
    date = temp3[1]
    obsid = temp1[1]
    obsPath = temp3[0]
    os.chdir(obsDir)
    # Create a directory called ExtractedOneD and copy all the data cubes to this directory.
    if not os.path.exists(obsPath+'/ExtractedOneD/'):
        os.mkdir(obsPath+'/ExtractedOneD/')
        logging.info('I am creating a directory called ExtractedOneD')
    ExtractedOneD = obsPath+'/ExtractedOneD'
    # Make the appropriate directory structure.
    if not os.path.exists(ExtractedOneD+'/'+date+'_'+obsid):
        os.mkdir(ExtractedOneD+'/'+date+'_'+obsid)
        logging.info('I am creating a directory with date and abs ID inside ExtractedOneD ')
    # Get the filenames of the uncombined spectra.
    uncombinedSpectra = glob.glob('xtfbrsnN*.fits')
    # Copy the uncombined spectra to the appropriate directory.
    for spectra in uncombinedSpectra:
        if os.path.exists(ExtractedOneD+'/'+date+'_'+obsid+'/'+spectra):
            if over:
                os.remove(ExtractedOneD+'/'+date+'_'+obsid+'/'+spectra)
                shutil.copy(spectra, ExtractedOneD+'/'+date+'_'+obsid)
            else:
                logging.info("Output file exists and -over not set - skipping copy one D spectra")
        else:
            shutil.copy(spectra, ExtractedOneD+'/'+date+'_'+obsid)
    # Get the file name of the combined spectra
    combinedSpectrum = glob.glob('gxtfbrsnN*.fits')
    combinedSpectrum = combinedSpectrum[0]
    # Copy the combined spectrum to the appropriate directory.
    if os.path.exists(ExtractedOneD+'/'+combinedSpectrum):
        if over:
            os.remove(ExtractedOneD+'/'+combinedSpectrum)
            shutil.copy(combinedSpectrum, ExtractedOneD)
        else:
            logging.info("Output file exists and -over not set - skipping copy combined one D spectra")
    else:
        shutil.copy(spectra, ExtractedOneD+'/combined'+date+'_'+obsid+'.fits')

#--------------------------------------------------------------------------------------------------------------------------------#

def makeTelluricCorrection(
    telluricDirectory, path, continuuminter, hlineinter, hline_method="vega", spectemp=9700,
    mag=None, log="test.log", over=False):
    """FLUX CALIBRATION
    Consists of this start function and six required functions at the end of
    this file.
    """
    """iraf.gemini(_doprint=0, motd="no")
    iraf.gnirs(_doprint=0)
    iraf.imutil(_doprint=0)
    iraf.onedspec(_doprint=0)
    iraf.nsheaders('nifs',Stdout='/dev/null')"""
    # Overview of Telluric Correction procedure:
    # We make a telluric correction by:
    # Remove H-lines from combined 1D standard star spectrum.
    # Divide by H-line corrected standard spectrum by continuum fit.
    # We apply a telluric correction by:
    # Dividing the cube by the correction spectrum (with iraf.telluric) to figure out the shift and scaling.
    # Dividing again by the continuum to add a continuum shape back in.
    # Telluric correction done.


    # Overview of flux calibration procedure:
    # Make a blackbody spectrum.
    # Scale to the observed magnitude of the standard.
    # Multiply telluric corrected target spectrum by this scaled blackbody.
    # Done!
    iraffunctions.chdir(telluricDirectory)

    logging.info('I am starting to create telluric correction spectrum and blackbody spectrum')
    logging.info('I am starting to create telluric correction spectrum and blackbody spectrum ')

    # Open the combine extracted 1d spectrum.
    try:
        combined_extracted_1d_spectra = str(open('telluricfile', 'r').readlines()[0]).strip()
    except:
        logging.info("No telluricfile found in " + str(telluricDirectory) + "Skipping telluric correction and flux calibration.")
        return
    if not os.path.exists('scienceMatchedTellsList'):
        logging.info("No scienceMatchedTellsList found in " + str(telluricDirectory))
        return
    telheader = astropy.io.fits.open(combined_extracted_1d_spectra+'.fits')
    grating = telheader[0].header['GRATING'][0]
    RA = telheader[0].header['RA']
    Dec = telheader[0].header['DEC']

    # Make directory PRODUCTS above the Telluric observation directory
    # telluric_hlines.txt is stored there.
    if not os.path.exists('../PRODUCTS'):
        os.mkdir('../PRODUCTS')

    # Make pretty Right Ascensions and Declinations, to pass to SIMBAD.
    if '-' in str(Dec):
        coordinates = str(RA)+'d'+str(Dec)+'d'
    else:
        coordinates = str(RA)+'d+'+str(Dec)+'d'

    # Get standard star spectral type, teff, and magnitude from the interwebs. Go forth, brave parser!
    getStandardInfo(coordinates, path, mag, grating)

    logging.info("\n##############################################################################")
    logging.info("")
    logging.info("  STEP 6a - Find standard star information - COMPLETED ")
    logging.info("")
    logging.info("##############################################################################\n")

    hLineCorrection(combined_extracted_1d_spectra, grating, path, hlineinter, hline_method, log, over)

    logging.info("\n##############################################################################")
    logging.info("")
    logging.info("  STEP 6b - Apply or do not apply hline correction to standard star - COMPLETED ")
    logging.info("")
    logging.info("##############################################################################\n")

    # Fit a continuum from the standard star spectrum, saving both continuum and continuum divided standard spectrum.
    fitContinuum(continuuminter, grating)
    # Divide the standard star spectrum by the continuum to normalize it.
    if os.path.exists("telluricCorrection.fits"):
        os.remove("telluricCorrection.fits")
    iraf.imarith('final_tel_no_hlines_no_norm', "/", 'fit', result='telluricCorrection',title='',divzero=0.0,hparams='',pixtype='',calctype='',verbose='no',noact='no',mode='al')
    # Done deriving telluric correction! We have two new products:
    # 1) A continuum-normalized telluric correction spectrum, telluricCorrection.fits, and
    # 2) The continuum we used to normalize it, fit.fits.

#--------------------------------------------------------------------------------------------------------------------------------#

def applyTelluricCube(scienceFrameList):
    """
    Apply a telluric correction to each cube in a science directory.

    TODO(nat): only uses one telluric correction per science observation. Fix this!
    """

    # Store current directory.
    # os.path.split(os.getcwd()) returns something like "obs20"
    scienceObservation = os.path.split(os.getcwd())
    # Final continuum divided telluric spectrum is now in ./correctionSpectra

    grating = "K"
    telluricinter = "no"
    # For each cube in uncorrectedCubes:
    for item in scienceFrameList:
        # Apply a telluric correction to an on-target part of the cube (to a 1D spectrum).
        # If didn't find a telluric correction spectrum, skip this run.
        if not getTelluricSpec(item):
            continue
        # Get shift and scale of spec from one part of the cube.
        get1dSpecFromCube("ctfbrsn"+item+".fits")
        tellshift, scale = getShiftScale("telluricCorrection.fits", grating, telluricinter)
        # Shift and scale the telluric correction spectrum and continuum fit to the telluric correction spectrum.
        shiftScaleSpec("telluricCorrection.fits", "scaledShiftedTelluric.fits", tellshift, scale)
        shiftScaleSpec("fit.fits", "fitShifted.fits", tellshift, scale)
        # Divide every spectrum in the cube by the shifted continuum to add a continuum shape back in.
        divideCubebyTelandContinuuum("ctfbrsn"+item+".fits", "scaledShiftedTelluric.fits", "fitShifted.fits")
        # Done! Now have a telluric-corrected science cube.
        shutil.move("telluricCorrection.fits", "telCor"+item+".fits")
        shutil.move("cubeslice.fits", "cubeslice"+item+".fits")
        shutil.move("scaledShiftedTelluric.fits", "finaltelCor"+item+'.fits')

#--------------------------------------------------------------------------------------------------------------------------------#

def fluxCalibrate(scienceFrameList):
    # This looks more like flux calibration code.........
    """
    Flux calibrate input science cubes.
    """
    for scienceObjectName in scienceFrameList:

        # Get science grating.
        scienceHeader = astropy.io.fits.open(scienceObjectName+'.fits')
        grating = scienceHeader[0].header['GRATING'][0]

        # Get mag and telluric standard exposure time.
        mag, std_exp_time, status = readMagnitude(scienceObjectName, grating)
        # Check that the last step succeeded; if not skip flux cal for this cube.
        if not status:
            continue

        # Flambda is just a constant.
        flambda = makeFLambda(scienceObjectName, mag, grating, std_exp_time)

        # Make a (hopefully) properly scaled black body spectrum.
        makeScaledBlackBody(scienceObjectName, flambda)

        # Multiply the telluric corrected cubes by this spectrum.
        multiplyByBlackBody(scienceObjectName)

#--------------------------------------------------------------------------------------------------------------------------------#


##################################################################################################################
#                                               TELLURIC TASKS                                               #
##################################################################################################################

#--------------------------- makeTelluric() tasks(includes hlinecorrection tasks) -------------------------------#

def fitContinuum(continuuminter, grating):
    """
    Fit a continuum to the telluric correction spectrum to normalize it. The continuum
    fitting regions were derived by eye and can be improved.

    Results are in fit<Grating>.fits
    """
    # These were found to fit the curves well by hand. You can probably improve them; feel free to fiddle around!
    if grating == "K":
        order = 5
        sample = "20279:20395,20953:24283"
    elif grating == "J":
        order = 5
        sample = "11561:12627,12745:12792,12893:13566"
    elif grating == "H":
        order = 5
        sample = "*"
    elif grating == "Z":
        order = 5
        sample = "9453:10015,10106:10893,10993:11553"
    if os.path.exists("fit.fits"):
        os.remove("fit.fits")
    iraf.continuum(input='final_tel_no_hlines_no_norm',output='fit',ask='yes',lines='*',bands='1',type="fit",replace='no',wavescale='yes',logscale='no',override='no',listonly='no',logfiles='',inter=continuuminter,sample=sample,naverage=1,func='spline3',order=order,low_rej=1.0,high_rej=3.0,niterate=2,grow=1.0,markrej='yes',graphics='stdgraph',cursor='',mode='ql')
    # Plot the telluric correction spectrum with the continuum fit.
    final_tel_no_hlines_no_norm = astropy.io.fits.open('final_tel_no_hlines_no_norm.fits')[0].data
    fit = astropy.io.fits.open('fit.fits')[0].data
    if continuuminter:
        plt.title('Unnormalized Telluric Correction and Continuum fit Used to Normalize')
        plt.plot(final_tel_no_hlines_no_norm)
        plt.plot(fit)
        plt.show()

#------------------------------------- hlinecorrection tasks ----------------------------------------------------#

def hLineCorrection(combined_extracted_1d_spectra, grating, path, hlineinter, hline_method, log, over, airmass_std=1.0):
    """
    Remove hydrogen lines from the spectrum of a telluric standard,
    using a model of vega's atmosphere.

    """

    # File for recording shift/scale from calls to "telluric"
    telluric_shift_scale_record = open('telluric_hlines.txt', 'w')

    # Remove H lines from standard star correction spectrum
    no_hline = False
    if os.path.exists("final_tel_no_hlines_no_norm.fits"):
        if over:
            iraf.delete("final_tel_no_hlines_no_norm.fits")
        else:
            no_hline = True
            logging.info("Output file exists and -over- not set - skipping H line removal")

    if hline_method == "vega" and not no_hline:
        vega(combined_extracted_1d_spectra, grating, path, hlineinter, telluric_shift_scale_record, log, over)

    #if hline_method == "linefitAuto" and not no_hline:
    #    linefitAuto(combined_extracted_1d_spectra, grating)

    # Disabled and untested because interactive scripted iraf tasks are broken...
    #if hline_method == "linefitManual" and not no_hline:
    #    linefitManual(combined_extracted_1d_spectra+'[sci,1]', grating)

    #if hline_method == "vega_tweak" and not no_hline:
        #run vega removal automatically first, then give user chance to interact with spectrum as well
    #    vega(combined_extracted_1d_spectra,grating, path, hlineinter, telluric_shift_scale_record, log, over)
    #    linefitManual("final_tel_no_hlines_no_norm", grating)

    #if hline_method == "linefit_tweak" and not no_hline:
        #run Lorentz removal automatically first, then give user chance to interact with spectrum as well
    #    linefitAuto(combined_extracted_1d_spectra,grating)
    #    linefitManual("final_tel_no_hlines_no_norm", grating)

    if hline_method == "none" and not no_hline:
        #need to copy files so have right names for later use
        iraf.imcopy(input=combined_extracted_1d_spectra+'[sci,'+str(1)+']', output="final_tel_no_hlines_no_norm", verbose='no')
    # Plot the non-hline corrected spectrum and the h-line corrected spectrum.
    uncorrected = astropy.io.fits.open(combined_extracted_1d_spectra+'.fits')[1].data
    corrected = astropy.io.fits.open("final_tel_no_hlines_no_norm.fits")[0].data
    if hlineinter:
        plt.title('Before and After HLine Correction')
        plt.plot(uncorrected)
        plt.plot(corrected)
        plt.show()

def vega(spectrum, band, path, hlineinter, telluric_shift_scale_record, log, over, airmass=1.0):
    """
    Use iraf.telluric to remove H lines from standard star, then remove
    normalization added by telluric with iraf.imarith.

    The extension for vega_ext.fits is specified from band (from header of
    telluricfile.fits).

    Args:
        spectrum (string): filename from 'telluricfile'.
        band: from telluricfile .fits header. Eg 'K', 'H', 'J'.
        path: usually top directory with Nifty scripts.
        hlineinter (boolean): Interactive H line fitting. Specified with -i at
                              command line. Default False.
        airmass: from telluricfile .fits header.
        telluric_shift_scale_record: "pointer" to telluric_hlines.txt.
        log: path to logfile.
        over (boolean): overwrite old files. Specified at command line.

    """
    if band=='K':
        ext = '1'
        sample = "21537:21778"
        scale = 0.8
    if band=='H':
        ext = '2'
        sample = "16537:17259"
        scale = 0.7
    if band=='J':
        ext = '3'
        sample = "11508:13492"
        scale = 0.885
    if band=='Z':
        ext = '4'
        sample = "*"
        scale = 0.8
    if os.path.exists("tell_nolines.fits"):
            if over:
                os.remove("tell_nolines.fits")
                tell_info = iraf.telluric(input=spectrum+"[1]", output='tell_nolines', cal= RUNTIME_DATA_PATH+'vega_ext.fits['+ext+']', xcorr='yes', tweakrms='yes', airmass=airmass, inter=hlineinter, sample=sample, threshold=0.1, lag=3, shift=0., dshift=0.05, scale=scale, dscale=0.05, offset=0., smooth=1, cursor='', mode='al', Stdout=1)
            else:
                logging.info("Output file exists and -over not set - skipping H line correction")
    else:
        tell_info = iraf.telluric(input=spectrum+"[1]", output='tell_nolines', cal= RUNTIME_DATA_PATH+'vega_ext.fits['+ext+']', xcorr='yes', tweakrms='yes', inter=hlineinter, airmass=airmass, sample=sample, threshold=0.1, lag=3, shift=0., dshift=0.05, scale=scale, dscale=0.05, offset=0., smooth=1, cursor='', mode='al', Stdout=1)

    # need this loop to identify telluric output containing warning about pix outside calibration limits (different formatting)
    if "limits" in tell_info[-1].split()[-1]:
        norm=tell_info[-2].split()[-1]
    else:
        norm=tell_info[-1].split()[-1]

    if os.path.exists("final_tel_no_hlines_no_norm.fits"):
        if over:
            os.remove("final_tel_no_hlines_no_norm.fits")
            iraf.imarith(operand1='tell_nolines', op='/', operand2=norm, result='final_tel_no_hlines_no_norm', title='', divzero=0.0, hparams='', pixtype='', calctype='', verbose='yes', noact='no', mode='al')
        else:
            logging.info("Output file exists and -over not set - skipping H line normalization")
    else:
        iraf.imarith(operand1='tell_nolines', op='/', operand2=norm, result='final_tel_no_hlines_no_norm', title='', divzero=0.0, hparams='', pixtype='', calctype='', verbose='yes', noact='no', mode='al')

# TODO(nat): linefitAuto and linefitManual could be useful at some point.
def linefitAuto(spectrum, band):
    """automatically fit Lorentz profiles to lines defined in existing cur* files
    Go to x position in cursor file and use space bar to find spectrum at each of those points
    """

    specpos = iraf.bplot(images=spectrum+'[SCI,1]', cursor='cur'+band, Stdout=1, StdoutG='/dev/null')
    specpose = str(specpos).split("'x,y,z(x):")
    nextcur = 'nextcur'+band+'.txt'
    # Write line x,y info to file containing Lorentz fitting commands for bplot
    write_line_positions(nextcur, specpos)
    iraf.delete('final_tel_no_hlines_no_norm.fits',ver="no",go_ahead='yes',Stderr='/dev/null')
    # Fit and subtract Lorentz profiles. Might as well write output to file.
    iraf.bplot(images=spectrum+'[sci,1]',cursor='nextcur'+band+'.txt', new_image='final_tel_no_hlines_no_norm', overwrite="yes",StdoutG='/dev/null',Stdout='Lorentz'+band)

def linefitManual(spectrum, band):
    """ Enter splot so the user can fit and subtract lorents (or, actually, any) profiles
    """

    iraf.splot(images=spectrum, new_image='final_tel_no_hlines_no_norm', save_file='../PRODUCTS/lorentz_hlines.txt', overwrite='yes')
    # it's easy to forget to use the 'i' key to actually write out the line-free spectrum, so check that it exists:
    # with the 'tweak' options, the line-free spectrum will already exists, so this lets the user simply 'q' and move on w/o editing (too bad if they edit and forget to hit 'i'...)
    while True:
        try:
            with open("final_tel_no_hlines_no_norm.fits") as f: pass
            break
        except IOError as e:
            logging.info("It looks as if you didn't use the i key to write out the lineless spectrum. We'll have to try again. --> Re-entering splot")
            iraf.splot(images=spectrum, new_image='final_tel_no_hlines_no_norm', save_file='../PRODUCTS/lorentz_hlines.txt', overwrite='yes')

#------------------------------------- applyTelluric() tasks ----------------------------------------------------#

def getTelluricSpec(scienceObjectName):
    """
    For a given science cube, copies appropriate telluric correction spectrum to current directory.
    TODO(nat): have to be able to choose telluric spectrum that is closest in time!
    """
    observationDirectory = os.getcwd()
    # Get the efficiency spectrum we will use to do a telluric correction and flux calibration at the same time.
    os.chdir('../Tellurics')
    # Find a list of all the telluric observation directories.
    telDirList_temp = glob.glob('obs*')
    for telDir in telDirList_temp:
        # Change to the telluric directory
        print os.getcwd()
        os.chdir(telDir)
        # Make sure an scienceMatchedTellsList is present.
        try:
            scienceMatchedTellsList = open('scienceMatchedTellsList', 'r').readlines()
            scienceMatchedTellsList = [item.strip() for item in scienceMatchedTellsList]
        except:
            os.chdir('..')
            continue
        foundTelluricFlag = False
        if scienceObjectName in scienceMatchedTellsList:
            print "made it here"
            # Open the correction efficiency spectrum.
            if os.path.exists(observationDirectory + "/telluricCorrection.fits"):
                os.remove(observationDirectory + "/telluricCorrection.fits")
            shutil.copy("telluricCorrection.fits", observationDirectory)
            if os.path.exists(observationDirectory+"/fit.fits"):
                os.remove(observationDirectory+"/fit.fits")
            shutil.copy("fit.fits", observationDirectory)
            os.chdir(observationDirectory)
            logging.info("\nUsing combined standard spectrum from " + str(telDir) + " for " + str(scienceObjectName))
            foundTelluricFlag = True
            break
        else:
            os.chdir('..')
            continue
    if not foundTelluricFlag:
        logging.info("\nWARNING: No Telluric correction spectrum found for " + str(scienceObjectName))
    os.chdir(observationDirectory)
    return foundTelluricFlag

def get1dSpecFromCube(inputcube):
    """
    Turn a cube into a 1D spec, used to find shift and scale values of telluric spectrum.
    Currently: Extracts 1D spectra from center of cube.
    """
    cube = astropy.io.fits.open(inputcube)
    cubeheader = cube[1].header
    cubeslice = cube[1].data[:,30,30]
    # Create a PrimaryHDU object to encapsulate the data and header.
    hdu = astropy.io.fits.PrimaryHDU(cubeslice)
    # Modify the cd1_1 and CRVAL1 values; this adds the wavelength calibration to the correct cube dimension.
    hdu.header = cubeheader
    hdu.header['CRVAL1'] = cubeheader['CRVAL3']
    hdu.header['CD1_1'] = cubeheader['CD3_3']
    hdu.header['CRPIX1'] = 1.
    if os.path.exists('cubeslice.fits'):
        os.remove('cubeslice.fits')
    # Write the spectrum and header to a new .fits file.
    hdu.writeto('cubeslice.fits', output_verify="ignore")

def getShiftScale(standardspectra, grating, telluricinter, airmass_target=1.0):
    """
    Use iraf.telluric() to get the best shift and scale of a telluric correction spectrum.
    """
    if os.path.exists('oneDcorrected.fits'):
        os.remove('oneDcorrected.fits')
    tell_info = iraf.telluric(input='cubeslice.fits[0]',output='oneDcorrected.fits',cal=standardspectra+"[0]",airmass=airmass_target,answer='yes',ignoreaps='yes',xcorr='yes',tweakrms='yes',inter=telluricinter,sample="*",threshold=0.1,lag=3,shift=0.,dshift=0.1,scale=1.0,dscale=0.1, offset=1,smooth=1,cursor='',mode='al',Stdout=1)
    # Get shift and scale from the list of values iraf.telluric() returns.
    # Sample tell_info:
    # ['cubeslice.fits[0]: norm.fits[1]: cubeslice.fits[0]: dshift 5.', 'window:again:window:window:again:window:window:again:window:TELLURIC:',
    # '  Output: vtella - HE1353-1917', '  Input: cubeslice.fits[0] - HE1353-1917', '
    # Calibration: norm.fits[1] - Hip70765', '  Tweak: shift = 59.12, scale = 1.323,
    # normalization = 0.9041', '  WARNING: 3 pixels outside of calibration limits']
    tellshift = 0.
    scale = 1.0
    for i in range(len(tell_info)):
        # Now string looks like '  Tweak: shift = 59.12, scale = 1.323, normalization = 0.9041'
        if "Tweak" in tell_info[i]:
            # Remove the first 9 characters,
            temp = tell_info[i][9:]
            # Split into a list; now it looks like '['shift', '=', '59.12,', 'scale', '=', '1.323,', 'normalization', '=', '0.9041']'
            temp = temp.split()
            # Index two is the shift value with a trailing comma, index 5 is the scale value with a trailing comma.
            # Remove trailing comma.
            tellshift = temp[2].replace(',', '')
            # Turn it into a float.
            tellshift = float(tellshift) # Convert to a clean float
            # Do the same for the scale.
            scale = temp[5].replace(',', '')
            scale = float(scale)
    return tellshift, scale

def shiftScaleSpec(inputspec, outspec, tellshift, scale):
    """
    Shifts and scales a spectrum using scipy.
    Replaces overflow with 1.
    """
    spectrum = astropy.io.fits.open(inputspec)
    spectrumData = spectrum[0].data
    # Shift using SciPy, substituting 1 where data overflows.
    spectrumData = shift(spectrumData, -1*int(tellshift), cval=1.)
    # Scale by simple multiplication; 1D spectrum times a scalar.
    spectrumData = spectrumData * scale
    spectrum[0].data = spectrumData
    # Write to a new file;
    if os.path.exists(outspec):
        os.remove(outspec)
    spectrum.writeto(outspec)

def divideCubebyTelandContinuuum(inputcube, telluricSpec, continuumSpec):
    """
    Divide every element of a data cube by the derived telluric correction spectrum.
    """
    # Open the data cube.
    cube = astropy.io.fits.open(inputcube)
    # Open the shifted, scaled telluric correction spectrum.
    telluricSpec = astropy.io.fits.open(telluricSpec)
    # Open the continuum fit to the cube.
    continuumSpec = astropy.io.fits.open(continuumSpec)
    # Divide each spectrum in the cubedata array by the telluric correction spectrum.
    for i in range(cube[1].header['NAXIS2']):         # NAXIS2 is the y axis of the final cube.
        for j in range(cube[1].header['NAXIS1']):     # NAXIS1 is the x axis of the final cube.
            cube[1].data[:,i,j] /= (telluricSpec[0].data)
            cube[1].data[:,i,j] /= (continuumSpec[0].data)
    # Write the corrected cube to a new file with a "cp" prefix, "p" for "python corrected".
    if os.path.exists("a"+inputcube):
        os.remove("a"+inputcube)
    cube.writeto('a'+inputcube, output_verify='ignore')

#------------------------------------- utilities ----------------------------------------------------------------#

def extrap1d(interpolator):
    """Extrap1d takes an interpolation function and returns a function which can also extrapolate.
    From https://stackoverflow.com/questions/2745329/how-to-make-scipy-interpolate-give-an-extrapolated-result-beyond-the-input-range
    """
    xs = interpolator.x
    ys = interpolator.y
    def pointwise(x):
        if x < xs[0]:
            return ys[0]+(x-xs[0])*(ys[1]-ys[0])/(xs[1]-xs[0])
        elif x > xs[-1]:
            return ys[-1]+(x-xs[-1])*(ys[-1]-ys[-2])/(xs[-1]-xs[-2])
        else:
            return interpolator(x)
    def ufunclike(xs):
        return array(map(pointwise, array(xs)))
    return ufunclike

def readCube(cube):
    """Open a data cube with astropy.io.fits. Read the data header to find the starting wavelength and wavelength increment.
        Create a 1D array with length equal to the spectral dimension of the cube.
        For each element in array, element[i] = starting wavelength + (i * wavelength increment).

        Returns:
            cube (object reference):   Reference to the opened data cube.
            cubewave (1D numpy array): array representing pixel-wavelength mapping of data cube.

    """
    # read cube into an HDU list
    cube = astropy.io.fits.open(cube)

    # find the starting wavelength and the wavelength increment from the science header of the cube
    wstart = cube[1].header['CRVAL3']
    wdelt = cube[1].header['CD3_3']

    # initialize a wavelength array
    cubewave = np.zeros(2040)

    # create a wavelength array using the starting wavelength and the wavelength increment
    for i in range(2040):
        cubewave[i] = wstart+(i*wdelt)

    return cube, cubewave

def write_line_positions(nextcur, var):
    """Write line x,y info to file containing Lorentz fitting commands for bplot

    """

    curfile = open(nextcur, 'w')
    i=-1
    for line in var:
        i+=1
        if i!=0:
            var[i]=var.split()
            var[i][2]=var[i][2].replace("',",'').replace("']", '')
        if not i%2 and i!=0:
            #even number, means RHS of H line
            #write x and y position to file, also "k" key
            curfile.write(var[i][0]+" "+var[i][2]+" 1 k \n")
            #LHS of line, write info + "l" key to file
            curfile.write(var[i-1][0]+" "+var[i-1][2]+" 1 l \n")
            #now repeat but writing the "-" key to subtract the fit
            curfile.write(var[i][0]+" "+var[i][2]+" 1 - \n")
            curfile.write(var[i-1][0]+" "+var[i-1][2]+" 1 - \n")
        curfile.write("0 0 1 i \n")
        curfile.write("0 0 q \n")
        curfile.close()

#--------------------------------------------------------------------------------------------------------------------------------#

##################################################################################################################
#                                       FLUX CALIBRATION TASKS                                                   #
##################################################################################################################

def getStandardInfo(name, path, mag, band, spectemp=9700):
    """Find standard star spectral type, temperature, and magnitude. Write results
       to std_star.txt in cwd.

    Executes a SIMBAD query and parses the resulting html to find spectal type,
    temperature and/or magnitude.

        Args:
            name (string): RA, d, Dec, d (for negatives); RA, +d, Dec, d (for positives).
            path: current working directory (usually with Nifty files).
            spectemp: specified at command line with -e.
            mag: specified at command line with -f.
            band: from the telluric standard .fits file header. Eg 'J', 'K'.

    """

    starfile = 'std_star.txt'
    kelvinfile = RUNTIME_DATA_PATH+'new_starstemp.txt'

    sf = open(starfile,'w')
    klf = open (kelvinfile)
    Kmag = ''
    Jmag = ''
    Hmag = ''

    # check to see if a spectral type or temperature has been given
    """if spectemp:
        if not isinstance(spectemp[0], int):
            spectral_type = spectemp
            specfind = False
            tempfind = True
        else:
            kelvin = spectemp
            tempfind = False
            specfind = False
    else:
        specfind = True
        tempfind = True"""
    specfind = False
    tempfind = False
    kelvin = str(9700)
    if mag:
        magfind = False
        if band=='K':
            Kmag=mag
        if band=='H':
            Hmag=mag
        if band=='J':
            Jmag=mag
    else:
        magfind = True

    if specfind or tempfind or magfind:
        #Construct URL based on standard star coords, execute SIMBAD query to find spectral type
        name = name.replace("+","%2b")
        name = name.replace("-", "%2D")
        start_name='http://simbad.u-strasbg.fr/simbad/sim-coo?Coord='
        end_name = '&submit=submit%20query&Radius.unit=arcsec&Radius=10'
        www_page = start_name+name+end_name
        f = urllib.urlopen(www_page)
        html2 = f.read()
        html2 = html2.replace(' ','')
        search_error = str(html2.split('\n'))

        #Exit if the lookup found nothing.
        if 'Noastronomicalobjectfound' in search_error:
            logging.info("ERROR: no object was found at the coordinates you entered. You'll need to supply information in a file; see the manual for instructions.")

        #If >1 object found, decrease search radius and try again
        if 'Numberofrows:' in search_error:
            start_name='http://simbad.u-strasbg.fr/simbad/sim-coo?Coord='
            end_name = '&submit=submit%20query&Radius.unit=arcsec&Radius=1'
            www_page = start_name+name+end_name
            f = urllib.urlopen(www_page)
            html2 = f.read()
            html2 = html2.replace(' ','')
            search_error = str(html2.split('\n'))

        #If that didn't return anything, exit and let the user sort it out
        if 'Noastronomicalobjectfound' in search_error:
            logging.info("ERROR: didn't find a star at your coordinates within a search radius of 10 or 1 arcsec. You'll need to supply information in a file; see the manual for instructions.")
            sys.exit()

        # Split source by \n into a list
        html2 = html2.split('\n')

        if specfind:
            count = 0
            aux = 0
            for line in html2:
                if (line[0:13] == 'Spectraltype:') :
                    numi = aux + 5
                    count = 0
                    break
                else:
                    count += 1
                aux += 1
            logging.info(html2[aux:numi+1])
            spectral_type = str(html2[numi][0:3])
            if count > 0:
                logging.info("ERROR: problem with SIMBAD output. You'll need to supply the spectral type or temperature in the command line prompt.")
                sys.exit()

        if magfind:
            for line in html2:
                if 'Fluxes' in line:
                    i = html2.index(line)
                    break
            while 'IMGSRC' not in html2[i]:
                if all(s in html2[i] for s in ('K', '[', ']')):
                    if 'C' in html2[i+2]:
                        index = html2[i].index('[')
                        Kmag = html2[i][1:index]
                if all(s in html2[i] for s in ('H', '[', ']')):
                    if 'C' in html2[i+2]:
                        index = html2[i].index('[')
                        Hmag = html2[i][1:index]
                if all(s in html2[i] for s in ('J', '[', ']')):
                    if 'C' in html2[i+2]:
                        index = html2[i].index('[')
                        Jmag = html2[i][1:index]
                i+=1
                if i>len(html2):
                    logging.info("ERROR: problem with SIMBAD output. You'll need to supply the magniture in the command line prompt.")

        if not Kmag:
            Kmag = 'nothing'
        if not Jmag:
            Jmag = 'nothing'
        if not Hmag:
            Hmag = 'nothing'

        if tempfind:
            #Find temperature for this spectral type in kelvinfile
            count = 0
            for line in klf:
                if '#' in line:
                    continue
                else:
                    if	spectral_type in line.split()[0]:
                        kelvin = line.split()[1]
                        count = 0
                        break
                    else:
                        count+=1

            if count > 0:
                logging.info("ERROR: can't find a temperature for spectral type"+ str(spectral_type)+". You'll need to supply information in a file; see the manual for instructions.")
                sys.exit()

        # Write results to std_star.txt
        if (Kmag or Jmag or Hmag) and Kmag!='x' and magfind:
            logging.info("magnitudes retrieved OK")
            sf.write('k K '+Kmag+' '+kelvin+'\n')
            sf.write('h H '+Hmag+' '+kelvin+'\n')
            sf.write('j J '+Jmag+' '+kelvin+'\n')
            sf.write('j J '+Jmag+' '+kelvin+'\n')

        elif (Kmag or Jmag or Hmag) and Kmag!='x' and not magfind:
            sf.write('k K '+Kmag+' '+kelvin+'\n')
        elif Kmag=='x':
            logging.info("WARNING: no magnitudes found for standard star. Doing relative flux calibration only.")
            sf.write('k K N/A '+kelvin+' \n')
            sf.write('h H N/A '+kelvin+' \n')
            sf.write('j J N/A '+kelvin+' \n')
            sf.write('j J N/A '+kelvin+' \n')

    sf.close()
    klf.close()

def readMagnitude(scienceObjectName, grating):
    """
    - From input cube name, find a matching telluric directory based on the scienceMatchedTellsList.
    - Find appropriate mag from that std_star.txt file. If grating == 'Z' use grating == 'J'
    - Find standard exp time from telluric headers
    - Sets magnitude to None if no std_star.txt file found.
    - Will only return True if standard exposure time and magnitude are found and read properly.
    """
    """
    # Try using this code if things don't seem to work well!
    # Make blackbody spectrum to be used in nifsScience.py
    file = open('std_star.txt','r')
    lines = file.readlines()
    #Extract stellar temperature from std_star.txt file , for use in making blackbody
    # star_kelvin = float(lines[0].replace('\n','').split()[3])
    # Just use A0V star temperature for now
    star_kelvin = 9700
    #Extract mag from std_star.txt file
    #find out if a matching grating mag exists in std_star.txt
    logging.info("Band = " + str(grating))
    if grating == 'K':
        star_mag = lines[0].replace('\n','').split()[2]
        star_mag = float(star_mag)
    elif grating == 'H':
        star_mag = lines[1].replace('\n','').split()[2]
        star_mag = float(star_mag)
    elif grating == 'J':
        star_mag = lines[2].replace('\n','').split()[2]
        star_mag = float(star_mag)
    else:
        #if not no relative flux cal. attempted
        logging.info("\n#####################################################################")
        logging.info("#####################################################################")
        logging.info("")
        logging.info("     WARNING in nifsReduce: No " + str(grating) + " grating magnitude found for this star.")
        logging.info("                            No relative flux calibration will be performed.")
        logging.info("")
        logging.info("#####################################################################")
        logging.info("#####################################################################\n")

        logging.info("star_kelvin=" + str(star_kelvin))
        logging.info("star_mag=" + str(star_mag))"""
    observationDirectory = os.getcwd()
    status = False
    mag = None
    std_exp_time = None
    # 2MASS doesn't have Z band magnitudes. Use J for rough absolute flux scaling.
    if grating == 'Z':
        grating = 'J'
    # Now we start looking for a matching telluric observation directory.
    os.chdir('../Tellurics')
    # Find a list of all the telluric observation directories.
    telDirList_temp = glob.glob('obs*')
    for telDir in telDirList_temp:
        # Change to the telluric directory
        os.chdir(telDir)
        # Make sure an scienceMatchedTellsList is present.
        try:
            scienceMatchedTellsList = open('scienceMatchedTellsList', 'r').readlines()
            scienceMatchedTellsList = [item.strip() for item in scienceMatchedTellsList]
        except:
            os.chdir('..')
            continue
        foundTelluricFlag = False
        if scienceObjectName in scienceMatchedTellsList:
            # Read magnitude from std_star.txt
            try:
                with open("std_star.txt") as f:
                    lines = f.read()
                # Split into a list; it should then look something like this:
                # ['k', 'K', '7.615', '9700', 'h', 'H', '7.636', '9700', 'j', 'J', '7.686', '9700', 'j', 'J', '7.686', '9700']
                lines = lines.split()
                # Mag is entry after the grating, but may also be N/A. Check for that.
                for i in range(len(lines)):
                    if grating in lines[i] and lines[i+1] != "N/A":
                        mag = lines[i+1]
                        logging.info("Found standard star magnitude to be " + str(mag))
            except IOError:
                logging.info("No std_star.txt file found; no absolute flux cal will be attempted.")
            # Look up the telluric exposure time while we are here.
            combined_extracted_1d_spectra = str(open('telluricfile', 'r').readlines()[0]).strip()
            telheader = astropy.io.fits.open(combined_extracted_1d_spectra+'.fits')
            std_exp_time = telheader[0].header['EXPTIME']
            status = True
            break
        else:
            os.chdir('..')
            continue
    os.chdir(observationDirectory)
    return mag, std_exp_time, status

def makeFLambda(scienceObjectName, mag, grating, std_exp_time):
    """
    - Multiply magnitude expression by appropriate constant for grating.
    - Multiple by ratio of experiment times.
    - If no magnitude, set flambda to 1. No absolute flux calibration performed.
    Returns:
        -flambda: floating point constant.
    """
    if grating == "K":
        constant = 4.283E-11
    elif grating == "H":
        constant = 1.33E-10
    elif grating == "J" or "Z":
        constant = 3.129E-10
    try:
        mag = float(mag)
        flambda = (10**((-1*mag)/2.5)) * constant
        absolute_cal = True
    except:
        # If no magnitude set to 1; no absolute flux cal. attempted
        flambda = 1
        absolute_cal = False
    # Look up the target exposure time.
    target_header = astropy.io.fits.open(scienceObjectName+'.fits')
    tgt_exp_time = target_header[0].header['EXPTIME']
    # Scale by ratio of exposure times.
    flambda *= float(std_exp_time) / float(tgt_exp_time)
    return flambda

def makeScaledBlackBody(scienceObjectName, flambda):
    """
    - From Z header information from the cube, make a black body.
    - Make scale factor: mean of black body over flambda.
    - Multiply blackbody spectrum by scale factor.
    Creates:
        - Unscaled blackbody, bbody.fits
        - A scaled 1D blackbody spectrum, scaledBlackBody.fits[0]
    """
    # Find the start and end wavelengths of the blackbody from our cube header.
    target_header = astropy.io.fits.open('actfbrsn'+scienceObjectName+'.fits')
    wstart = target_header[1].header['CRVAL3']
    wdelt = target_header[1].header['CD3_3']
    wend = wstart + (2040 * wdelt)
    crpix3 = target_header[1].header['CRPIX3']
    if crpix3 != 1.:
        logging.info("WARNING in Reduce: CRPIX of wavelength axis not equal to one. Exiting flux calibration.")
        raise SystemExit
    # Make a blackbody for each of the 2040 NIFS spectral pixels.
    if os.path.exists("bbody.fits"):
        os.remove("bbody.fits")
    iraf.mk1dspec(input="bbody",output="bbody",title='',ncols=2040,naps=1,header='',wstart=wstart,wend=wend,temperature=9700)
    # Scale the black body by the ratio of the black body mean flux to flambda.
    meana = iraf.imstat(images="bbody", fields="mean", lower='INDEF', upper='INDEF', nclip=0, lsigma=3.0, usigma=3.0, binwidth=0.1, format='yes', cache='no', mode='al',Stdout=1)
    # Scale factor is flambda / (mean flux of black body)
    scalefac = flambda / float(meana[1].replace("'",""))
    if os.path.exists("scaledBlackBody.fits"):
        os.remove("scaledBlackBody.fits")
    iraf.imarith(operand1="bbody", op="*", operand2=scalefac, result="scaledBlackBody",title='',divzero=0.0,hparams='',pixtype='',calctype='',verbose='no',noact='no',mode='al')
    # We now have a scaled blackbody, scaledBlackBody.fits

def multiplyByBlackBody(scienceObjectName):
    """
    - Multiply each slice of "actfbrsn"+scienceObjectName+".fits"[1].data
      by the scaled black body.

    Creates:
        - Flux calibrated cube, "factfbrsn"+scienceObjectName+".fits"
    """
    # Open the telluric corrected, un-fluxcalibrated data cube.
    cube = astropy.io.fits.open('actfbrsn'+scienceObjectName+'.fits')
    # Open the scaled blackbody. We will multiply the cube by this.
    scaledBlackBody = astropy.io.fits.open('scaledBlackBody.fits')
    # Divide each spectrum in the cubedata array by the telluric correction spectrum.
    for i in range(cube[1].header['NAXIS2']):         # NAXIS2 is the y axis of the final cube.
        for j in range(cube[1].header['NAXIS1']):     # NAXIS1 is the x axis of the final cube.
            cube[1].data[:,i,j] *= (scaledBlackBody[0].data)
    # Write the corrected cube to a new file with a "cp" prefix, "p" for "python corrected".
    if os.path.exists("factfbrsn"+scienceObjectName+'.fits'):
        os.remove('factfbrsn'+scienceObjectName+'.fits')
    cube.writeto('factfbrsn'+scienceObjectName+'.fits', output_verify='ignore')

if __name__ == '__main__':
    a = raw_input('Enter <Science> for science reduction or <Telluric> for telluric reduction: ')
    start(a)
