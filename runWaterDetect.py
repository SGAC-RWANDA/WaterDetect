# #!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
import argparse
import waterdetect

"""
Author: Mauricio Cordeiro
"""


def main():
    """
    The main function is just a wrapper to create a entry point script called waterdetect.
    With the package installed you can just call waterdetect -h in the command prompt to see the options.
    """
    parser = argparse.ArgumentParser(description='The waterdetect is a high speed water detection algorithm for sate'
                                                 'llite images. It will loop through all images available in the input '
                                                 'folder and write results for every combination specified in the'
                                                 ' .ini file to the output folder. It can also run for single images '
                                                 'from Python console or Jupyter notebook. Refer to the online'
                                                 'documentation ',
                                     epilog="To copy the package's default .ini file into the current directory, type:"
                                            ' `waterdetect -GC .` without other arguments and it will copy  '
                                            'WaterDetect.ini into the current directory.')

    parser.add_argument("-GC", "--GetConfig", help="Copy the WaterDetect.ini from the package into the current "
                                                   "directory and skips the processing. Once copied you can edit the "
                                                   ".ini file and launch the waterdetect without -c option.",
                        action="store_true")
    parser.add_argument("-i", "--input", help="The products input folder. Required.", required=False, type=str)
    parser.add_argument("-o", "--out", help="Output directory. Required.", required=False, type=str)
    parser.add_argument("-s", "--shp", help="SHP file. Optional.", type=str)
    parser.add_argument("-sm", "--single", help="Run WaterDetect over only one image instead of a directory of images. "
                                                "Optional.", action='store_true')
    parser.add_argument("-p", "--product", help='The product to be processed (S2_THEIA, L8_USGS, S2_L1C or S2_S2COR)',
                        default='S2_THEIA', type=str)
    parser.add_argument("-pk", "--pekel", help='Optional path for an occurrence base map like Pekel',
                        required=False, type=str)
    parser.add_argument('-c', '--config', help='Configuration .ini file. If not specified WaterDetect.ini '
                                               'from current dir and used as default', type=str)
    parser.add_argument('-v', '--version', help='Displays current package version', action='store_true')
    parser.add_argument('-d', '--debug', help='Debug basic parameters (paths/files)', action='store_true')

    # product type (theia, sen2cor, landsat, etc.)
    # optional shape file
    # generate graphics (boolean)
    # name of config file with the bands-list for detecting, saving graphics, etc. If not specified, use default name
    #   if clip MIR or not, number of pixels to plot in graph, number of clusters, max pixels to process, etc.
    # name of the configuration .ini file (optional, default is WaterDetect.ini in the same folder

    args = parser.parse_args()

    # If GetConfig option, just copy the WaterDetect.ini to the current working directory
    if args.GetConfig:
        src = Path(__file__).parent/'WaterDetect.ini'
        dst = Path(os.getcwd())/'WaterDetect.ini'

        print(f'Copying {src} into current dir.')
        dst.write_text(src.read_text())
        print(f'WaterDetect.ini copied into {dst.parent}.')
    elif args.version:
        print(f'WaterDetect version: {waterdetect.__version__}')

    elif args.debug:
        debug(args)

    else:
        if (args.input is None) or (args.out is None):
            print('Please specify input and output folders (-i, -o)')

        elif args.single:
            waterdetect.DWWaterDetect.run_single(image_folder=args.input, output_folder=args.out, shape_file=args.shp,
                                                 product=args.product, config_file=args.config)
        else:
            waterdetect.DWWaterDetect.run_batch(input_folder=args.input, output_folder=args.out, shape_file=args.shp,
                                                product=args.product, config_file=args.config, pekel=args.pekel)

    return


def debug(args):
    print(f'Working directory: {os.getcwd()}')
    print(f'Script running: {__file__}')
    debug_path(args.config, 'Config file')
    debug_path(args.input, 'Input', list_files=True)
    debug_path(args.out, 'Output', list_files=False)
    debug_path(args.pekel, 'Pekel mask')
    debug_path(args.shp, 'Shape file')


def debug_path(path,  name, list_files=False,):
    if path is not None:
        in_dir = Path(path)
        print(f'[{name}] exists={in_dir.exists()} - {str(in_dir)}')

        if list_files & in_dir.exists():
            print(f'Files')
            for f in in_dir.iterdir():
                print(str(f))
    else:
        print(f'[{name}] not specified')


# check if this file has been called as script
if __name__ == '__main__':
    main()

