#!/usr/bin/env python

# Python modules
from __future__ import division
import os
import webbrowser
import struct

# 3rd party modules
import wx
import numpy as np

# Our modules
import constants
import block_raw_probep
import block_raw_edit_fidsum
import block_prep_fidsum
import block_prep_wbnaa
import block_prep_megalaser
import block_prep_timeseries
import mrs_dataset
import notebook_datasets
import util_menu
import util_analysis_config
import util_import

import vespa.analysis.src.fileio.raw_reader as fileio_raw_reader
import vespa.analysis.src.fileio.vasf as fileio_vasf
import vespa.analysis.src.fileio.vasf_fidsum as fileio_vasf_fidsum
import vespa.analysis.src.fileio.bruker as fileio_bruker
import vespa.analysis.src.fileio.ge_probe as fileio_ge_probe
import vespa.analysis.src.fileio.varian as fileio_varian
import vespa.analysis.src.fileio.siemens_rda as fileio_siemens_rda
import vespa.analysis.src.fileio.philips_spar as fileio_philips_spar
import vespa.analysis.src.fileio.philips_fidsum as fileio_philips_fidsum
import vespa.analysis.src.fileio.dicom_siemens as fileio_dicom_siemens
import vespa.analysis.src.fileio.dicom_siemens_fidsum as fileio_dicom_siemens_fidsum
import vespa.analysis.src.fileio.dicom_siemens_timeseries as fileio_dicom_siemens_timeseries

import vespa.common.configobj as configobj
import vespa.common.mrs_data_raw as mrs_data_raw
import vespa.common.mrs_data_raw_probep as mrs_data_raw_probep
import vespa.common.mrs_data_raw_fidsum as mrs_data_raw_fidsum
import vespa.common.mrs_data_raw_timeseries as mrs_data_raw_timeseries
import vespa.common.mrs_data_raw_uncomb as mrs_data_raw_uncomb
import vespa.common.mrs_data_raw_wbnaa as mrs_data_raw_wbnaa
import vespa.common.mrs_data_raw_edit_fidsum as mrs_data_raw_edit_fidsum
import vespa.common.constants as common_constants
import vespa.common.util.init as util_init
import vespa.common.util.misc as util_misc
import vespa.common.util.export as util_export
import vespa.common.wx_gravy.common_dialogs as common_dialogs
import vespa.common.wx_gravy.util as wx_util
import vespa.common.images as images
import vespa.common.dialog_export as dialog_export
import vespa.common.dialog_experiment_browser as dialog_experiment_browser



_MSG_MULTIFILE_ATTRIBUTE_MISMATCH = """
The dimensions and/or sweep widths in the selected data files differ.

Multifile selection is only available for single voxel data files.

Please select single voxel data files with same dimensions and sweep width."""

_MSG_MULTIFILE_TYPE_MISMATCH = """
More that one set of raw data was read from the file(s) selected, however, not all were of the same format type (summed FIDs or not).

Where multifile selection is allowed, or multiple datasets are being read out of one file, all files must return the same types of data."""

_MSG_PRESET_MISMATCH = """
One or more of the selected VIFF files is an Analysis Preset file. These can not be opened as datasets.
"""

_MSG_OPEN_ATTRIBUTE_MISMATCH = """
The dimensions and/or sweep width of the currently open datasets differ from those of the file(s) you asked to open.

You can open these files, but first you have to close all currently open datasets.
"""

_MSG_OPEN_TYPE_MISMATCH = """
The currently open datasets differ from those of the file(s) you asked to open in that they are not all of the same format type (summed FIDs or not).

You can open these files, but first you have to close all currently open datasets.
"""

_MSG_UNSUPPORTED_DIMENSIONALITY = """
The file(s) you opened contains SI datasets. Vespa doesn't support SI at this time.
"""

_MSG_OPEN_ZEROFILL_MISMATCH = """
The zerofill factor of the currently open datasets differ from those of the file you asked to open.

You can open this file, but the zero fill factor of the open datasets needs to be changed.
"""

_MSG_NO_DATASETS_FOUND = """The file "%s" doesn't contain any datasets."""


#----------------------------------------------------------------------


class Main(wx.Frame):

    def __init__(self, db, position, size):

        self._left,  self._top    = position
        self._width, self._height = size

        style = wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX |           \
                wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.RESIZE_BORDER |   \
                wx.CLIP_CHILDREN

        wx.Frame.__init__(self, None, wx.ID_ANY, "Analysis",
                          (self._left, self._top),
                          (self._width, self._height), style)

        self.db = db
        
        # flags for global control ----------------------------------
        
        self.close_all = False

        # GUI Creation ----------------------------------------------

        self.datasets = {}

        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self.SetIcon(images.Mondrian.GetIcon())

        self.statusbar = self.CreateStatusBar(4, 0)
        self.statusbar.SetStatusText("Ready")

        # I make the status bar and the update_title method globally available
        # because multiple places in the app want to use them.
        wx.GetApp().vespa.statusbar = self.statusbar
        wx.GetApp().vespa.update_title = self.update_title

        bar = util_menu.AnalysisMenuBar(self)
        self.SetMenuBar(bar)
        util_menu.bar = bar

        self.build_panes()
        self.bind_events()


    ##############                                    ############
    ##############     Internal helpers are below     ############
    ##############       in alphabetical order        ############
    ##############                                    ############

    def bind_events(self):
        self.Bind(wx.EVT_MENU,  self.on_menu_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.on_self_close)
        self.Bind(wx.EVT_SIZE,  self.on_self_coordinate_change)
        self.Bind(wx.EVT_MOVE,  self.on_self_coordinate_change)


    def build_panes(self):
        # Create & show these panes

        self.notebook_datasets  = notebook_datasets.NotebookDatasets(self, self)

        # Center pane
        self._mgr.AddPane(self.notebook_datasets,
                          wx.aui.AuiPaneInfo().CenterPane())


        # "commit" all changes made to AuiManager
        self._mgr.Update()



    ##############                                    ############
    ##############      Event handlers are below      ############
    ##############       in alphabetical order        ############
    ##############                                    ############

    def on_menu_exit(self, event):
        self.Close(False)


    def on_self_close(self, event):

        if not self.notebook_datasets.is_welcome_tab_open:
            msg = "Are you sure you want to exit Analysis?"
            if wx.MessageBox(msg, "Quit Analysis", wx.YES_NO, self) != wx.YES:
                event.Veto()
                return

        # Save my coordinates
        config = util_analysis_config.Config()

        config.set_window_coordinates("main", self._left, self._top,
                                      self._width, self._height)

        config.set_window_maximized("main", self.IsMaximized())
        config.write()

        self.Destroy()


    def on_self_coordinate_change(self, event):
        # This is invoked for move & size events
        if self.IsMaximized() or self.IsIconized():
            # Bah, forget about this. Recording coordinates doesn't make sense
            # when the window is maximized or minimized. This is only a
            # concern on Windows; GTK and OS X don't produce move or size
            # events when a window is minimized or maximized.
            pass
        else:
            if event.GetEventType() == wx.wxEVT_MOVE:
                self._left, self._top = self.GetPositionTuple()
            else:
                # This is a size event
                self._width, self._height = self.GetSizeTuple()



    ##############                                    ############
    ##############       Menu handlers are below      ############
    ##############       in the order they appear     ############
    ##############             on the menu            ############
    ##############                                    ############

    ######  File menu  ######

    def on_open_viff(self, event):
        self.Freeze()
        self._open_viff_dataset_file()
        self.Thaw()
        self.notebook_datasets.Layout()


    def on_import_mrs_data_raw(self, event):
        datasets = self._import_viff_raw_file()
        if datasets:
            # although this format only allows us to import single files, it
            # still returns the one dataset in a list to mesh with the
            # functionality in add_dataset_tab() to deal with multiple files
            self.Freeze()
            self.notebook_datasets.add_dataset_tab(datasets)
            self.Thaw()
            self.notebook_datasets.Layout()


    def on_import_bruker(self, event):
        self._import_file(fileio_bruker.RawReaderBruker(),
                          "import_bruker")

    def on_import_ge_probe(self, event):
        self._import_file(fileio_ge_probe.RawReaderGeProbe(),
                          "import_ge_probe")

    def on_import_philips_spar(self, event):
        self._import_file(fileio_philips_spar.RawReaderPhilipsSpar(),
                          "import_philips_spar")


    def on_import_philips_fidsum(self, event):
        self._import_file(fileio_philips_fidsum.RawReaderPhilipsFidsum(),
                          "import_philips_fidsum")


    def on_import_siemens_dicom(self, event):
        self._import_file(fileio_dicom_siemens.RawReaderDicomSiemens(),
                          "import_siemens_dicom")


    def on_import_siemens_dicom_fidsum(self, event):
        self._import_file(fileio_dicom_siemens_fidsum.RawReaderDicomSiemensFidsum(),
                          "import_siemens_dicom_fidsum")

    def on_import_siemens_dicom_timeseries(self, event):
        self._import_file(fileio_dicom_siemens_timeseries.RawReaderDicomSiemensTimeseries(),
                          "import_siemens_dicom_timeseries")

    def on_import_siemens_rda(self, event):
        self._import_file(fileio_siemens_rda.RawReaderSiemensRda(),
                          "import_siemens_rda")


    def on_import_varian(self, event):
        self._import_file(fileio_varian.RawReaderVarian(),
                          "import_varian")


    def on_import_vasf(self, event):
        self._import_file(fileio_vasf.RawReaderVasf(), "import_vasf")


    def on_import_vasf_fidsum(self, event):
        self._import_file(fileio_vasf_fidsum.RawReaderVasfFidsum(), "import_vasf_fidsum")


    def on_import_user_item(self, event):
        # This is triggered for all user-defined menu items created via
        # analysis_menu_additions.ini. They hang off of File/Import.

        # Get the id of the menu item that triggered this event
        id_ = event.GetId()

        # Find the reader class & INI file name associated with that id.
        reader, ini_name = util_menu.bar.get_user_menu_item_info(id_)

        self._import_file(reader(), ini_name)


    def on_save_viff(self, event, save_as=False):
        # This event is also called programmatically by on_save_as_viff().
        if self.notebook_datasets.active_tab:
            dataset = self.notebook_datasets.active_tab.dataset

            filename = dataset.dataset_filename
            if filename and (not save_as):
                # This dataset already has a filename which means it's already
                # associated with a VIFF file. We don't bug the user for a
                # filename, we just save it.
                pass
            else:
                # Prompt the user for the save filename & location
                if filename:
                    # Prompt using the existing VIFF filename
                    path, filename = os.path.split(filename)
                else:
                    # Construct a filename from the raw filename.
                    raw = dataset.blocks["raw"]
                    filename = raw.data_source

                    path, filename = os.path.split(filename)
                    filename = os.path.splitext(filename)[0] + ".xml"

                filename = common_dialogs.save_as("Save As XML/VIFF (Vespa Interchange Format File)",
                                                  "VIFF/XML files (*.xml)|*.xml",
                                                  path, filename)

            if filename:
                dataset.dataset_filename = filename

                self._save_viff(dataset)


    def on_save_as_viff(self, event):
        self.on_save_viff(event, True)


    def on_close_dataset(self, event):
        if self.notebook_datasets:
            self.notebook_datasets.close_active_dataset()

    def on_close_all(self, event):
        msg = "This will close all open datasets with no opportunity to save results, continue?"
        if wx.MessageBox(msg, "Close All Datasets", wx.YES_NO, self) != wx.YES:
            event.Veto()
        else:
            self.close_all = True
            while self.datasets:
                self.notebook_datasets.close_active_dataset()
            self.close_all = False


    def on_load_preset_from_file(self, event):

        tab = self.notebook_datasets.active_tab

        if tab:

            dataset = tab.dataset
            file_type = common_constants.MrsFileTypes.VIFF
            ini_name  = "load_preset"       # "open_viff"
            default_path = util_analysis_config.get_path(ini_name)

            # Note that we only allow people to open a single VIFF file as
            # opposed to DICOM & VASF where we allow them to open multiple.
            filetype_filter="Spectra Preset (*.xml,*.xml.gz,*.viff,*.vif)|*.xml;*.xml.gz;*.viff;*.vif"
            filename = common_dialogs.pickfile(filetype_filter=filetype_filter,
                                                multiple=False,
                                                default_path=default_path)
            if filename:
                msg = ""
                try:
                    importer = util_import.DatasetImporter(filename)
                except IOError:
                    msg = """I can't read the preset file "%s".""" % filename
                except SyntaxError:
                    msg = """The preset file "%s" isn't valid Vespa Interchange File Format.""" % filename

                if msg:
                    common_dialogs.message(msg, "Analysis - Open Preset File",  common_dialogs.E_OK)
                else:
                    # Time to rock and roll!
                    wx.BeginBusyCursor()
                    presets = importer.go()
                    wx.EndBusyCursor()

                    preset = presets[0]

                    wx.BeginBusyCursor()

                    # update dataset object with preset blocks and chains
                    dataset.apply_preset(presets[0], voxel=tab.voxel)

                    # Get the active dataset tab to update itself
                    self.notebook_datasets.on_preset_loaded()

                    # Check dimensionality on ALL other loaded datasets
                    preset_zf = dataset.zero_fill_multiplier
                    self.notebook_datasets.global_block_zerofill_update(preset_zf)

                    # Check gui on ALL tabs for zero fill consistency
                    self.notebook_datasets.global_tab_zerofill_update(preset_zf)

                    path, _ = os.path.split(filename)
                    util_analysis_config.set_path(ini_name, path)

                    wx.EndBusyCursor()


    def on_load_preset_from_tab(self, event):
        print "Not yet Implemented - on_load_preset_from_tab"


    def on_save_preset_to_file(self, event):

        tab = self.notebook_datasets.active_tab
        if tab:
            # get the dataset object if it exists, save settings to preset file
            dataset  = tab.dataset
            filename = 'vespa_analysis_preset.xml'
            dialog = dialog_export.DialogExport(self, False, filename=filename)
            dialog.ShowModal()

            if dialog.export:
                filename = dialog.filename
                comment  = dialog.comment
                compress = dialog.compress

                wx.BeginBusyCursor()
                # Many of these objects can deflate themselves into a
                # more compact form when being deflated as presets, so
                # we temporarily set a flag on them to let them know
                # how to behave during deflate(). This hack turns out
                # to be easier than passing a flag to the deflate()
                # calls.
                dataset.set_behave_as_preset(True)

                try:
                    util_export.export(filename, [dataset], None, comment, compress)
                except IOError, (error_number, error_string):
                    msg = """Exporting to "%s" failed. The operating system message is below --\n\n""" % filename
                    msg += error_string
                    common_dialogs.message(msg, "Vespa Export", common_dialogs.E_OK)

                wx.EndBusyCursor()

                # Here we undo the behave_as_preset hack from above.
                dataset.set_behave_as_preset(False)


    def on_close_window(self, event):
        self.Destroy()


    ######  Processing menu  ######

    def on_add_voigt_tab(self, event):
        self.notebook_datasets.on_add_voigt_tab(event)

    def on_add_giso_tab(self, event):
        self.notebook_datasets.on_add_giso_tab(event)

    def on_add_watref_tab(self, event):
        self.notebook_datasets.on_add_watref_tab(event)

    def on_user_prior(self, event):
        self.notebook_datasets.on_user_prior(event)

    def on_user_metabolite_info(self, event):
        self.notebook_datasets.on_user_metabolite_info(event)

    def on_show_inspection_tool(self, event):
        wx_util.show_wx_inspector(self)


    ######  View  menu  ######

    # View options affect plots in a dataset - we pass these events on to the
    # specific dataset notebook tab that needs to react to them.

    def on_menu_view_option(self, event):
        self.notebook_datasets.on_menu_view_option(event)

    def on_menu_view_output(self, event):
        self.notebook_datasets.on_menu_view_output(event)

    def on_menu_view_results(self, event):
        self.notebook_datasets.on_menu_view_results(event)

    def on_menu_plot_x(self, event):
        self.notebook_datasets.on_menu_plot_x(event)


    ######  Help menu  ######

    def on_user_manual(self, event):
        path = util_misc.get_vespa_install_directory()
        path = os.path.join(path, "docs", "analysis_user_manual.pdf")
        webbrowser.open(path, 1)


    def on_analysis_help_online(self, event):
        webbrowser.open("http://scion.duhs.duke.edu/vespa/analysis", 1)


    def on_vespa_help_online(self, event):
        webbrowser.open("http://scion.duhs.duke.edu/vespa", 1)


    def on_about(self, event):
        bit = str(8 * struct.calcsize('P')) + '-bit Python'
        info = wx.AboutDialogInfo()
        info.SetVersion(util_misc.get_vespa_version())
        info.SetCopyright("Copyright 2010, Duke University. All rights reserved.")
        info.SetDescription("Analysis is an advanced spectral processing and analysis environment. Running on "+bit)
        info.SetWebSite("http://scion.duhs.duke.edu/vespa/")
        wx.AboutBox(info)



    ##############
    ##############   Public  functions  alphabetized  below
    ##############

    def update_title(self):
        """Updates the main window title to reflect the current dataset."""
        name = ""

        # Create an appropriate name for whatever is selected.
        tab = self.notebook_datasets.active_tab
        if tab and tab.dataset.dataset_filename:
            name = " - " + tab.dataset.dataset_filename
        #else:
            # If there's no active tab or the dataset_filename isn't set, we
            # don't add anything in the titlebar.
            # At present, opening a VIFF file always populates dataset_filename.
            # Importing does not.

        self.SetTitle("Analysis" + name)


    ##############
    ##############   Internal  helper  functions  alphabetized  below
    ##############

    def _import_file(self, reader, ini_name):
        datasets = [ ]

        default_path = util_analysis_config.get_path(ini_name)

        if reader.pickfile(default_path):

            tab = self.notebook_datasets.active_tab

            open_dataset = (tab.dataset if tab else None)

            msg = ""
            wx.BeginBusyCursor()
            try:
                # Step 1
                #
                # Return one or more DataRawXxxx objects that indicate what
                # sort of data was read in by the reader
                raws = reader.read_raws(open_dataset=open_dataset)
            except IOError:
                msg = "One or more of the files couldn't be read due to a disk error."

            except fileio_raw_reader.MultifileAttributeMismatchError:
                msg = _MSG_MULTIFILE_ATTRIBUTE_MISMATCH

            except fileio_raw_reader.MultifileTypeMismatchError:
                msg = _MSG_MULTIFILE_TYPE_MISMATCH

            except fileio_raw_reader.UnsupportedDimensionalityError:
                # Note that this also catches SIDataError which is a
                # subclass of UnsupportedDimensionalityError
                msg = _MSG_UNSUPPORTED_DIMENSIONALITY

            except fileio_raw_reader.OpenFileAttributeMismatchError:
                msg = _MSG_OPEN_ATTRIBUTE_MISMATCH

            except fileio_raw_reader.OpenFileTypeMismatchError:
                msg = _MSG_OPEN_TYPE_MISMATCH

            except fileio_raw_reader.FileNotFoundError, error_instance:
                msg = unicode(error_instance)

            except fileio_raw_reader.OpenFileUserReadRawError, error_instance:
                if not error_instance:
                    error_instance = "User read_raw raised OpenFileUserReadRawError"
                msg = unicode(error_instance)

            finally:
                wx.EndBusyCursor()

            if msg:
                common_dialogs.message(msg, "Analysis - Open File")
            else:
                # All is well. Convert these raw objects into fully-fledged
                # dataset objects.
                if open_dataset:
                    zero_fill_multiplier = open_dataset.zero_fill_multiplier
                else:
                    zero_fill_multiplier = 0

                # Step 2
                #
                # See if any data types need special classes. We usually only
                # look for raw fidsum classes which trigger a prep fidsum block.
                block_class_specs = [ ]
                for raw in raws:
                    d = { }
                    if isinstance(raw, mrs_data_raw_probep.DataRawProbep):
                        d["raw"] = block_raw_probep.BlockRawProbep
                    if isinstance(raw, mrs_data_raw_edit_fidsum.DataRawEditFidsum):
                        d["raw"] = block_raw_edit_fidsum.BlockRawEditFidsum
                    if isinstance(raw, mrs_data_raw_fidsum.DataRawFidsum):
                        d["prep"] = block_prep_fidsum.BlockPrepFidsum
                    if isinstance(raw, mrs_data_raw_timeseries.DataRawTimeseries):
                        d["prep"] = block_prep_timeseries.BlockPrepTimeseries
                    if isinstance(raw, mrs_data_raw_uncomb.DataRawUncomb):
                        d["prep"] = block_prep_fidsum.BlockPrepFidsum
                    if isinstance(raw, mrs_data_raw_wbnaa.DataRawWbnaa):
                        d["prep"] = block_prep_wbnaa.BlockPrepWbnaa
                    if isinstance(raw, mrs_data_raw_edit_fidsum.DataRawEditFidsum):
                        d["prep"] = block_prep_fidsum.BlockPrepFidsum
                    block_class_specs.append(d)

                f = lambda raw, block_classes: mrs_dataset.dataset_from_raw(raw,
                                                                  block_classes,
                                                           zero_fill_multiplier)
                datasets = map(f, raws, block_class_specs)

        if datasets:
            # We opened something successfully, so we write the path to the
            # INI file.
            path, _ = os.path.split(reader.filenames[0])
            util_analysis_config.set_path(ini_name, path)

            for i,dataset in enumerate(datasets):

                # Step 3
                #
                # sometimes the datasets returned from the reader need to know
                # about each other. For instance, the PROBE-P GE data from a Pfile
                # contains both water and water suppressed data, so it would be
                # good if when we go to save to a VIFF file that we save both so
                # they are available again when we open it.
                if isinstance(dataset.blocks['raw'], block_raw_probep.BlockRawProbep):
                    if i == 0 and len(datasets)>=2:
                        dataset.blocks['raw'].set_associated_datasets([datasets[1]])

                # Here the edited data reader should return four datasets, one for
                # each state of editing pulses ON, OFF and calculated SUM and DIFF.
                # We associate all four files into the raw block. This will save
                # provenance for all states. Note that when we go to save the dataset
                # the copy of self that is in the associated raw datasets will be
                # filtered out.
                if isinstance(raws[0], mrs_data_raw_edit_fidsum.DataRawEditFidsum):
                    dataset.blocks['raw'].set_associated_datasets([datasets[0], datasets[1], datasets[2], datasets[3]])

            self.Freeze()
            self.notebook_datasets.add_dataset_tab(datasets)
            self.Thaw()
            self.notebook_datasets.Layout()
            self.Layout()



    def _import_viff_raw_file(self):
        # VIFF is our XML format.
        # Note that this is NOT an Analysis dataset but only raw mrs
        # data, so we treat it differently from ordinary VIFF.
        dataset = None

        ini_name = "import_viff_raw"
        default_path = util_analysis_config.get_path(ini_name)

        filetype_filter="Raw Spectra (*.xml,*.xml.gz,*.viff,*.vif)|*.xml;*.xml.gz;*.viff;*.vif"
        filename = common_dialogs.pickfile(filetype_filter=filetype_filter,
                                            multiple=False,
                                            default_path=default_path)
        if filename:
            msg = ""
            try:
                importer = util_import.DataRawImporter(filename)
            except IOError:
                msg = """I can't read the file "%s".""" % filename
            except SyntaxError:
                msg = """The file "%s" isn't valid Vespa Interchange File Format.""" % filename

            if msg:
                common_dialogs.message(msg, "Analysis - Open File",
                                       common_dialogs.E_OK)
            else:
                # Time to rock and roll!
                wx.BeginBusyCursor()
                raws = importer.go()
                wx.EndBusyCursor()

                if raws:
                    # As of this writing (Jan 2012), having multiple, top level
                    # raw data elements in a VIFF file is only a theoretical
                    # construct. That's why we discard everything after the
                    # first element here.
                    raw = raws[0]

                    if self.datasets:
                        # There are one or more datasets already open. The attributes
                        # of the currently open dataset(s) must match those of the
                        # dataset(s) that we're trying to open.
                        # To compare, we grab one of the currently open datasets. It
                        # doesn't matter which one since they all have matching
                        # attributes.
                        open_dataset = self.datasets.values()[0]
                        if (raw.dims == open_dataset.raw_dims) and \
                           (raw.sw   == open_dataset.sw):
                            # All is well!
                            pass
                        else:
                            # The dimensions don't match. We can't open these files.
                            common_dialogs.message(_MSG_OPEN_ATTRIBUTE_MISMATCH,
                                                   "Analysis - Dimension Mismatch")
                            return
                    else:
                        open_dataset = None

                    if open_dataset:
                        zero_fill_multiplier = open_dataset.zero_fill_multiplier
                    else:
                        zero_fill_multiplier = 0

                    dataset = mrs_dataset.dataset_from_raw(raw, {},
                                                           zero_fill_multiplier)

                    path, _ = os.path.split(filename)
                    util_analysis_config.set_path(ini_name, path)
                else:
                    msg = """No Vespa raw data found in that VIFF file."""
                    common_dialogs.message(msg, "Analysis - Import Data",
                                           common_dialogs.E_OK)


            return [dataset]


    def _open_viff_dataset_file(self):
        """
        VIFF - Vespa Interchange File Format - is the XML format for data
        saved from or opened up into the Analysis application. This is the
        only format that is actually 'opened' by Analysis, all other formats
        are considered 'imports'.

        Note that we only allow people to open a single VIFF file as opposed
        to DICOM, VASF or other imported formats where we allow users to
        open multiple files which are then concatenated into one Dataset
        object.

        If the open is successful (and the dimensions match to any existing
        data), the dataset is opened into a new dataset tab.

        The Dataset object is returned (or None if the user
        doesn't choose a file), along with a list of the filenames opened.
        """
        file_type = common_constants.MrsFileTypes.VIFF
        ini_name = "open_viff"
        default_path = util_analysis_config.get_path(ini_name)

        # Note that we only allow people to open a single VIFF file as
        # opposed to DICOM & VASF where we allow them to open multiple.
        filetype_filter="Spectra (*.xml,*.xml.gz,*.viff,*.vif)|*.xml;*.xml.gz;*.viff;*.vif"
        filenames = common_dialogs.pickfile(filetype_filter=filetype_filter,
                                            multiple=True,
                                            default_path=default_path)
        if filenames:
            datasets = []
            for filename in filenames:
                msg = ""
                try:
                    importer = util_import.DatasetImporter(filename)
                except IOError:
                    msg = """I can't read the file "%s".""" % filename
                except SyntaxError:
                    msg = """The file "%s" isn't valid Vespa Interchange File Format.""" % filename
    
                if msg:
                    common_dialogs.message(msg, "Analysis - Open File",
                                           common_dialogs.E_OK)
                else:
                    # Time to rock and roll!
                    wx.BeginBusyCursor()
                    dsets = importer.go()
                    wx.EndBusyCursor()
    
                    for dataset in dsets:
                        # check to ensure that none of the selected files is
                        # actually an Analysis Preset file
                        if dataset.behave_as_preset:
                            # No data in Preset file, can't load
                            common_dialogs.message(_MSG_PRESET_MISMATCH,
                                                   "Analysis - Preset Filetype Mismatch")
                            return
                    
                    for item in dsets:
                        datasets.append(item)


            if datasets:

                for dataset in datasets:
                    if self.datasets:
                        # There are one or more datasets already open. The
                        # attributes open_dataset.raw_dims of the
                        # currently open dataset(s) must match those of the
                        # dataset(s) that we're trying to open.
                        # To compare, we grab one of the currently open
                        # datasets. It doesn't matter which one since they
                        # all have matching attributes.
                        #
                        # Note. Dimensionality rules also apply to zerofill

                        open_dataset = self.datasets.values()[0]
                        if (dataset.raw_dims == open_dataset.raw_dims) and \
                           (dataset.sw       == open_dataset.sw):
                            # All is well!
                            pass
                        else:
                            # The dimensions don't match. We can't open these files.
                            common_dialogs.message(_MSG_OPEN_ATTRIBUTE_MISMATCH,
                                                   "Analysis - Dimension Mismatch")
                            return

                        open_dataset = self.datasets.values()[0]
                        if (dataset.spectral_dims == open_dataset.spectral_dims):
                            # All is well!
                            pass
                        else:
                            # The zerofill factors don't match. We can't open these files.
                            common_dialogs.message(_MSG_OPEN_ZEROFILL_MISMATCH,
                                                   "Analysis - Dimension Mismatch")
                            return


                for dataset in datasets:
                    if dataset.id == datasets[-1].id:
                        # this is last one and assumedly the one that all the
                        # associated datasets are supposed to associate with
                        dataset.set_associated_datasets(datasets)
                        dataset.dataset_filename = filename
                        # dataset.filename is an attribute set only at run-time
                        # to maintain the name of the VIFF file that was read in
                        # rather than deriving a filename from the raw data
                        # filenames with *.xml appended. But we need to set this
                        # filename only for the primary dataset, not the associated
                        # datasets. Associated datasets will default back to their
                        # raw filenames if we go to save them for any reason
                    else:
                        dataset.dataset_filename = ''

                if datasets:
                    self.notebook_datasets.add_dataset_tab(datasets)

                path, _ = os.path.split(filenames[0])
                util_analysis_config.set_path(ini_name, path)

            else:
                if not datasets:
                    common_dialogs.message(_MSG_NO_DATASETS_FOUND % filename,
                                           "Analysis - Open VIFF")


    def _open_viff_dataset_file_orig(self):
        """
        VIFF - Vespa Interchange File Format - is the XML format for data
        saved from or opened up into the Analysis application. This is the
        only format that is actually 'opened' by Analysis, all other formats
        are considered 'imports'.

        Note that we only allow people to open a single VIFF file as opposed
        to DICOM, VASF or other imported formats where we allow users to
        open multiple files which are then concatenated into one Dataset
        object.

        If the open is successful (and the dimensions match to any existing
        data), the dataset is opened into a new dataset tab.

        The Dataset object is returned (or None if the user
        doesn't choose a file), along with a list of the filenames opened.
        """
        file_type = common_constants.MrsFileTypes.VIFF
        ini_name = "open_viff"
        default_path = util_analysis_config.get_path(ini_name)

        # Note that we only allow people to open a single VIFF file as
        # opposed to DICOM & VASF where we allow them to open multiple.
        filetype_filter="Spectra (*.xml,*.xml.gz,*.viff,*.vif)|*.xml;*.xml.gz;*.viff;*.vif"
        filename = common_dialogs.pickfile(filetype_filter=filetype_filter,
                                            multiple=True,
                                            default_path=default_path)
        if filename:
            msg = ""
            try:
                importer = util_import.DatasetImporter(filename)
            except IOError:
                msg = """I can't read the file "%s".""" % filename
            except SyntaxError:
                msg = """The file "%s" isn't valid Vespa Interchange File Format.""" % filename

            if msg:
                common_dialogs.message(msg, "Analysis - Open File",
                                       common_dialogs.E_OK)
            else:
                # Time to rock and roll!
                wx.BeginBusyCursor()
                datasets = importer.go()
                wx.EndBusyCursor()

                for dataset in datasets:
                    # check to ensure that none of the selected files is
                    # actually an Analysis Preset file
                    if dataset.behave_as_preset:
                        # No data in Preset file, can't load
                        common_dialogs.message(_MSG_PRESET_MISMATCH,
                                               "Analysis - Preset Filetype Mismatch")
                        return


                for dataset in datasets:
                    if self.datasets:
                        # There are one or more datasets already open. The
                        # attributes open_dataset.raw_dims of the
                        # currently open dataset(s) must match those of the
                        # dataset(s) that we're trying to open.
                        # To compare, we grab one of the currently open
                        # datasets. It doesn't matter which one since they
                        # all have matching attributes.
                        #
                        # Note. Dimensionality rules also apply to zerofill

                        open_dataset = self.datasets.values()[0]
                        if (dataset.raw_dims == open_dataset.raw_dims) and \
                           (dataset.sw       == open_dataset.sw):
                            # All is well!
                            pass
                        else:
                            # The dimensions don't match. We can't open these files.
                            common_dialogs.message(_MSG_OPEN_ATTRIBUTE_MISMATCH,
                                                   "Analysis - Dimension Mismatch")
                            return

                        open_dataset = self.datasets.values()[0]
                        if (dataset.spectral_dims == open_dataset.spectral_dims):
                            # All is well!
                            pass
                        else:
                            # The zerofill factors don't match. We can't open these files.
                            common_dialogs.message(_MSG_OPEN_ZEROFILL_MISMATCH,
                                                   "Analysis - Dimension Mismatch")
                            return


                for dataset in datasets:
                    if dataset.id == datasets[-1].id:
                        # this is last one and assumedly the one that all the
                        # associated datasets are supposed to associate with
                        dataset.set_associated_datasets(datasets)
                        dataset.dataset_filename = filename
                        # dataset.filename is an attribute set only at run-time
                        # to maintain the name of the VIFF file that was read in
                        # rather than deriving a filename from the raw data
                        # filenames with *.xml appended. But we need to set this
                        # filename only for the primary dataset, not the associated
                        # datasets. Associated datasets will default back to their
                        # raw filenames if we go to save them for any reason
                    else:
                        dataset.dataset_filename = ''

                if datasets:
                    self.notebook_datasets.add_dataset_tab(datasets)

                path, _ = os.path.split(filename)
                util_analysis_config.set_path(ini_name, path)

                if not datasets:
                    common_dialogs.message(_MSG_NO_DATASETS_FOUND % filename,
                                           "Analysis - Open VIFF")
                    

    def _save_viff(self, dataset):
        msg = ""
        filename = dataset.dataset_filename
        try:
            util_export.export(filename, [dataset], None, None, False)
            path, _ = os.path.split(filename)
            util_analysis_config.set_path("save_viff", path)
        except IOError:
            msg = """I can't write the file "%s".""" % filename

        if msg:
            common_dialogs.message(msg, style=common_dialogs.E_OK)
        else:
            # dataset.filename is an attribute set only at run-time to maintain
            # the name of the VIFF file that was read in rather than deriving
            # a filename from the raw data filenames with *.xml appended. We
            # set it here to indicate the current name that the dataset has
            # been saved to VIFF file as.
            dataset.dataset_filename = filename

        self.update_title()



#--------------------------------------------------------------------

if __name__ == "__main__":

    # Having a function for app init is handy for profiling with cProfile

    app, db_path = util_init.init_app("Analysis")

    import util_db

    db = util_db.Database(db_path, True)

    # My settings are in simulation.ini
    config = util_analysis_config.Config()

    position, size = config.get_window_coordinates("main")
    frame = Main(db, position, size)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()



