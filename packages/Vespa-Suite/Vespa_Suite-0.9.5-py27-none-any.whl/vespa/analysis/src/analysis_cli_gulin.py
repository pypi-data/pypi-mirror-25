# Python modules
from __future__ import division
import argparse
import os
import sys
import platform
import imp
import xml.etree.cElementTree as ElementTree

# 3rd party modules


# Our modules
import mrs_dataset
import block_prep_fidsum
import util_import

import vespa.common.configobj as configobj
import vespa.common.util.misc as util_misc
import vespa.common.util.export as util_export
import vespa.common.constants as common_constants
import vespa.common.mrs_data_raw_fidsum as mrs_data_raw_fidsum



DESC =  \
"""Command line interface to process MRS data in Vespa-Analysis. 
 Data filename, preset file name, data type string and CSV output 
 file name values are all required for this command to function 
 properly.
  
 Note. You may have to enclose data/preset/output strings in double 
 quotation marks for them to process properly if they have  
 spaces or other special characters embedded in them.
"""

def clean_header(header):
    """ converts all values in ICE dict into a long string"""
    return "need to write"


def analysis_cli_gulin(data, header, verbose=False, debug=False):
    
    # Test input arguments for consistency --------------------------
    
    msg = ''
    # if not os.path.isfile(datafile):
    #    msg = """DATAFILE does not exist "%s".""" % datafile 

    # Load DATA data into a Dataset object --------------------------
    
    if verbose: print "Load Data data into a Dataset object"    
    try:
       
        d = []

        # need to write code to create string version of what comes from ICE
        # d["header"] = clean_header(header)
        
        d["filename"]       = "Siemens VB19 ICE Transfer - semi-LASER"
        d["sw"]             = 1.0 / float(header["dwell_time"] * 1e-9)
        d["readout_os"]     = header["readout_os"]
        d["sequence_type"]  = header["sequence_type"]
        d["frequency"]      = float(header["frequency"])/1000000.0
        d["dims"]           = mrs_data_raw.DataRaw.DEFAULT_DIMS
        d["dims"][0]        = int(header["dim0"]) * int(d["readout_os"])
        d["dims"][1]        = 1 # this updates as raw.concatenate is applied
        d["dims"][2]        = 1
        d["dims"][3]        = 1 
        d["seqte"]          = float(header["seqte"])*1e-6
        d["nucleus"]        = header["nucleus"]
    
        if header["nucleus"] == '1H':
            d["midppm"] = common_constants.DEFAULT_PROTON_CENTER_PPM
        else:
            d["midppm"] = common_constants.DEFAULT_XNUCLEI_CENTER_PPM
    
    
        # Read data, too, if the caller wants me to do so. 
        dims = d["dims"]
        shape = dims[::-1]
        del d["dims"]

        datas = data.copy()

        # Create a DataRawFidsum out of the first set of data in the list.
        d["data"] = datas[0]
        raw = mrs_data_raw_fidsum.DataRawFidsum(d)
        
        # Concatenate the remainder onto the first.
        for data in datas[1:]:
            data.shape = shape
            d["data"] = data
            raw.concatenate(mrs_data_raw_fidsum.DataRawFidsum(d))

        b = {}
        b["prep"] = block_prep_fidsum.BlockPrepFidsum
        dataset = mrs_dataset.dataset_from_raw(raw, b, 0)
            
    except:
        msg = """Unknown exception reading Data file "%s".""" % filename 
        print >> sys.stderr, msg
        sys.exit(-1)
    
    
    # Load PRESET data ----------------------------------------------
    
    if verbose: print "Load Preset into the Dataset object"    
    try:
        msg = ""
        
        preset_string  = header["preset_string"]
        preset_element = ElementTree.fromstring(preset_string)
        
        try:
            importer = util_import.DatasetImporter(preset_element)
        except IOError:
            msg = """I can't read the preset file "%s".""" % presetfile
        except SyntaxError:
            msg = """The preset file "%s" isn't valid Vespa Interchange File Format.""" % presetfile

        if msg:
            print >> sys.stderr, msg
            sys.exit(-1)
        else:
            # Time to rock and roll!
            presets = importer.go()
            preset  = presets[0]

            # update dataset object with preset blocks and chains
            dataset.apply_preset(preset, voxel=(0,0,0))
    except:
        msg = """Unknown exception reading Preset file "%s".""" % filename 
        print >> sys.stderr, msg
        sys.exit(-1)


    # Process and fit data ------------------------------------------
    
    if verbose: print "Running dataset chain objects"

    #FIXME-bjs  Need a routine to 'get all voxels' here
    
    voxel = [(0,0,0),]
    for key in dataset.blocks.keys():
        block = dataset.blocks[key]
        block.chain.run(voxel, entry='all')

    # Create unique name ID for this dataset ------------------------
    #
    # Some data files use the same base name over and over again (eg. twix 
    # uses meas.dat for all data files), so we mix either one or two
    # parent directory names to get a unique name to report in the csv file
    # and to use in the output XML file.
    
    base = os.path.basename(datafile)
    base,  _     = os.path.splitext(base)
    path1, _     = os.path.split(datafile)  
    path3, path2 = os.path.split(path1)
    if not twodir:
        # unique output name using one parent directory
        outxml = os.path.join(path1, path2+'_'+base+'.xml')
    else: 
        # unique output name using two parent directories
        _ , path4 = os.path.split(path3)
        outxml = os.path.join(path1, path4+'_'+path2+'_'+base+'.xml')
    
    dataset.dataset_filename = outxml

    # Save results to CSV file --------------------------------------

    if verbose: print """Saving results to CSV file "%s". """ % csvfile
    
    fit = dataset.blocks["fit"]
    data_source = dataset.blocks["raw"].get_data_source(voxel[0])
    
    val, hdr = fit.results_as_csv(voxel[0], fit.chain.fitted_lw,
                                            fit.chain.minmaxlw[0],
                                            fit.chain.minmaxlw[1], 
                                            data_source, outxml)
    nhdr = len(hdr)
    val = ",".join(val)
    hdr = ",".join(hdr)
    val += "\n"
    hdr += "\n"
     
    hdr_flag = True
    if os.path.isfile(csvfile):
        with open(csvfile, 'r+') as f:
            data = f.readlines()
            if len(data)>1:
                last = data[-1]
                nlast = len(last.split(','))
                if nlast == nhdr:
                    hdr_flag = False
                
    with open(csvfile, 'a') as f:
        if hdr_flag:
            f.write(hdr)
        f.write(val)

    # Save results to XML if flag set -------------------------------
    
    if savexml:
        if verbose: print """Saving dataset to XML file "%s". """ % outxml
        
        try:
            util_export.export(outxml, [dataset], None, None, False)
        except:
            msg = """I can't write the file "%s".""" % outxml
            print >> sys.stderr, msg
            sys.exit(-1)
            
               






    
    
def create_parser():

    parser = argparse.ArgumentParser(prog='analysis_cli', 
                                     usage='%(prog)s [options] datafile datatype presetfile csvfile',
                                     description=DESC)
    
    parser.add_argument("datafile",   help='file name of data to be processed')
    parser.add_argument("datatype",   help='string name of type of data in file')
    parser.add_argument("presetfile", help='xml file of preset values to use in processing')
    parser.add_argument("csvfile",    help='name of file where CSV result values are saved')
    
    parser.add_argument('-x', '--savexml', dest='savexml',
                                action="store_true", 
                                help='save dataset and results to VIFF XML format')
    parser.add_argument('-t', '--twodir', dest='twodir',
                                action="store_true", 
                                help='use two directory names in unique data id')
    parser.add_argument('-d', '--debug',   dest='debug',
                                action="store_true", 
                                help='print out command line to console only')
    parser.add_argument('-v', '--verbose', dest='verbose', 
                                action="store_true", 
                                help='increase output verbosity')
    return parser    


def main():

    parser = create_parser()
    args = parser.parse_args()
      
    analysis_cli(args.datafile, 
                 args.datatype, 
                 args.presetfile, 
                 args.csvfile, 
                 savexml=args.savexml,
                 twodir=args.twodir,
                 verbose=args.verbose, 
                 debug=args.debug)
    
#     # generalize the call to the local testdata directory, wherever it is
#     fpath = os.path.dirname(os.path.realpath(__file__))
#  
#     datafile   = fpath+r'/testdata/1/meas.dat'
#     presetfile = fpath+r'/testdata/preset_analysis_wbnaa_from_paper.xml'
#     csvfile    = fpath+r'/testdata/outcsv1.txt'
#    
#     analysis_cli(datafile, 'wbnaa', presetfile, csvfile, twodir=True, verbose=True)
        

#     # this gets all files *.dat in all subdirectories of STARTDIR
#     STARTDIR = 'D:\\bsoher\\Dropbox\\23_VB_Datasets4BrianSoher'
#     datfiles = []
#     for dirpath, dirnames, filenames in os.walk(STARTDIR):
#         for filename in [f for f in filenames if f.endswith(".dat")]:
#             datfiles.append(os.path.join(dirpath, filename))
#             print os.path.join(dirpath, filename)
#      
#     # this demonstrates how to use one or two levels of parent directories
#     # to create a uniques filename for a twix meas.dat        
#     twodir = True
#     for datafile in datfiles:
#         base = os.path.basename(datafile)
#         base,  _     = os.path.splitext(base)
#         path1, _     = os.path.split(datafile)  # unique output name for XML save file if needed
#         path3, path2 = os.path.split(path1)
#         if not twodir:
#             outxml = os.path.join(path1, path2+'_'+base+'.xml')
#         else: 
#             _ , path4 = os.path.split(path3)
#             outxml = os.path.join(path1, path4+'_'+path2+'_'+base+'.xml')   
#         print outxml 

#     # this gets all files *.dat in all subdirectories of STARTDIR
#     STARTDIR = 'D:\\bsoher\\3xWBNAA_Young_Controls'
#     datafiles = []
#     for dirpath, dirnames, filenames in os.walk(STARTDIR):
#         for filename in [f for f in filenames if f.endswith(".dat")]:
#             datafiles.append(os.path.join(dirpath, filename))
#             print os.path.join(dirpath, filename)
# 
#     presetfile = STARTDIR+'\\preset_wbnaa_analysis_v4.xml'
#     csvfile    = STARTDIR+'\\outcsv1.txt'
# 
#     for datafile in datafiles:
#         analysis_cli(datafile, 'wbnaa', presetfile, csvfile, twodir=True, verbose=True)

        
if __name__ == '__main__':
    main()        
        