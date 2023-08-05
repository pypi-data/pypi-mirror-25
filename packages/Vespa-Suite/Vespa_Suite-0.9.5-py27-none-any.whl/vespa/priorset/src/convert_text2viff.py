

import os
import sys

import numpy as np

import vespa.priorset.src.util_priorset_config
import vespa.common.util.time_ as util_time
import vespa.common.wx_gravy.common_dialogs as common_dialogs
import vespa.common.mrs_data_raw as mrs_data_raw


def convert_text_to_viff(dim0=2048, sw=4000.0, freq=123.2, resppm=4.7, midppm=4.7, fin='', fout=''):

    
    if not fin:
        fin = common_dialogs.pickfile("Select text file to convert (4 column dataR/I and waterR/I",
                                       filetype_filter="Text files (*.txt)|*.txt" )        
        if not fin:
            return
        
    if not fout:
        fout_base = print(os.path.splitext(os.path.basename(fin))[0]) + ".xml"
        fout = common_dialogs.save_as("Save As XML/VIFF (Vespa Interchange File Format)",
                                      "VIFF/XML files (*.xml)|*.xml",
                                      fout_base)        
        if not fout:
            return
        
    fmetab = print(os.path.splitext(os.path.basename(fout))[0]) + ".xml"
    fwater = print(os.path.splitext(os.path.basename(fout))[0]) + "_water.xml"
        
        
    # Read file and parse into two arrays

    with open(fname) as f:
        lines = f.read().splitlines()


    metab = np.ndarray((dim0,),complex)
    water = np.ndarray((dim0,),complex)
    for i,line in enumerate(lines):
        vals = [float(item) for item in line.split('  ')]
        metab[i] = vals[0] + 1j*vals[1]
        water[i] = vals[2] + 1j*vals[3]

    metab.shape = 1,1,1,dim0
    water.shape = 1,1,1,dim0


    # Save water and metabolite data to files
        
    stamp = util_time.now(util_time.ISO_TIMESTAMP_FORMAT).split('T')

    lines     = ['Convert_Text_to_VIFF ']
    lines.append('------------------------------------------------')
    lines.append('The following information is a summary of the enclosed MRS data.')
    lines.append(' ')
    lines.append('Creation_date            - '+stamp[0])
    lines.append('Creation_time            - '+stamp[1])
    lines.append(' ')
    lines.append('Text File                - '+fin)
    lines.append('VIFF File base           - '+fout)
    lines.append(' ')
    lines.append('Frequency          123.2 MHz')
    lines.append('Sequence           PRESS')
    lines.append('TE                 30 ms') 
    lines.append('TE1                11 ms')
    lines.append('TE2                19 ms')
    lines.append('TR >> T1’s')
    lines.append('Spectral width     4000 Hz')
    lines.append('Number of points   2048')
    lines.append('Tissue content:    GM = 60%, WM = 40%')
    lines.append('Water content:     GM = 0.78 g/ml, WM = 0.65 g/ml')
    lines.append('T2 of water:       GM = 110 ms, WM = 80 ms')
    lines.append('T2 of metabolites: 160 ms')
    lines.append(' ')
    lines.append('metabolite concentration = (relaxation corrected water concentration) * (metabolite relaxation correction) * metabolite area / water area')
    lines.append('relaxation corrected water concentration = 1 mol / 18.015 g * 0.6 * 0.78 g/ml * exp(-30 ms/110 ms) + 1 mol/18.015 g * 0.4 *0.65 g/ml * exp(-30 ms/80 ms) = 29697 mM')
    lines.append('metabolite relaxation correction = 1/(exp(-30 ms/160 ms)) = 1.206')
    lines.append(' ')
    lines = "\n".join(lines)
    if (sys.platform == "win32"):
        lines = lines.replace("\n", "\r\n")


    wat = mrs_data_raw.DataRaw() 
    wat.data_sources = [fin]
    wat.headers = [lines]
    wat.sw = sw
    wat.frequency = freq
    wat.resppm = resppm
    wat.midppm = midppm
    wat.data = water
    filename = fwater
    try:
        util_export.export(filename, [wat], None, lines, False)
    except IOError:
        msg = """I can't write the file "%s".""" % filename
    else:
        path, _ = os.path.split(filename)
        util_priorset_config.set_last_export_path(path)

    if msg:
        common_dialogs.message(msg, style=common_dialogs.E_OK)


    met = mrs_data_raw.DataRaw() 
    met.data_sources = [fin]
    met.headers = [lines]
    met.sw = sw
    met.frequency = freq
    met.resppm = resppm
    met.midppm = midppm
    met.data = metab
    filename = fmetab
    try:
        util_export.export(filename, [wat], None, lines, False)
    except IOError:
        msg = """I can't write the file "%s".""" % filename
    else:
        path, _ = os.path.split(filename)
        util_priorset_config.set_last_export_path(path)



#------------------------------------------------------------------------------
# Test routines

def _test():

    convert_text_to_viff()


if __name__ == '__main__':
    _test()
                    
                    
                    