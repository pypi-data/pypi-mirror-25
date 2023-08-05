# Python modules
from __future__ import division
import copy
import collections

# 3rd party modules
import numpy as np
import xml.etree.cElementTree as ElementTree

# Our modules
import constants
import block_raw
import block_raw_probep
import block_raw_edit_fidsum
import block_prep_identity
import block_prep_fidsum
import block_prep_timeseries
import block_prep_wbnaa
import block_prep_edit_fidsum
import block_spectral
import block_spectral_identity
import block_fit_voigt
import block_fit_giso
import block_fit_identity
import block_quant_watref
import block_quant_identity
import util
import mrs_user_prior
import vespa.common.util.misc as util_misc
import vespa.common.util.xml_ as util_xml
import vespa.common.constants as common_constants
import vespa.common.mrs_data_raw as mrs_data_raw
import vespa.common.mrs_data_raw_fidsum as mrs_data_raw_fidsum
import vespa.common.mrs_data_raw_timeseries as mrs_data_raw_timeseries

from vespa.common.constants import Deflate



###########    Start of "private" constants, functions and classes    #########

#_HLSVD_FILTER_UUID = water_filter_hlsvd.WaterFilterHlsvd.ID
_HLSVD_FILTER_UUID = "14023031-ad45-4662-a89c-4e35d8732244"     # deprecates, so hard wired

# _XML_TAG_TO_SLOT_CLASS_MAP maps XML element tags to 2-tuples of
# (slot name, block class) where slot name is one of "raw", "prep", "spectral",
# or "fit" and the class can be any class appropriate for that slot.
_XML_TAG_TO_SLOT_CLASS_MAP = {
    "block_raw"                 : ("raw", block_raw.BlockRaw),
    "block_raw_probep"          : ("raw", block_raw_probep.BlockRawProbep),
    "block_raw_edit_fidsum"     : ("raw", block_raw_edit_fidsum.BlockRawEditFidsum),
    "block_prep_identity"       : ("prep", block_prep_identity.BlockPrepIdentity),
    "block_prep_fidsum"         : ("prep", block_prep_fidsum.BlockPrepFidsum),
    "block_prep_timeseries"     : ("prep", block_prep_timeseries.BlockPrepTimeseries),
    "block_prep_edit_fidsum"    : ("prep", block_prep_edit_fidsum.BlockPrepEditFidsum),
    "block_prep_wbnaa"          : ("prep", block_prep_wbnaa.BlockPrepWbnaa),
    "block_spectral_identity"   : ("spectral", block_spectral_identity.BlockSpectralIdentity),
    "block_spectral"            : ("spectral", block_spectral.BlockSpectral),
    "block_fit_identity"        : ("fit", block_fit_identity.BlockFitIdentity),
    # block_voigt is an older name for what is now block_fit_voigt.
    "block_voigt"               : ("fit", block_fit_voigt.BlockFitVoigt),
    "block_fit_voigt"           : ("fit", block_fit_voigt.BlockFitVoigt),
    "block_fit_giso"            : ("fit", block_fit_giso.BlockFitGiso),
    "block_quant_watref"        : ("quant", block_quant_watref.BlockQuantWatref),
}

# DEFAULT_BLOCK_CLASSES defines which block slots are filled and with which
# classes when a Dataset object is instantiated. We use mostly identity
# classes which means they're not very useful as-is but they serve as
# lightweight placeholders.
# This dict is also a model for custom dicts that might get passed to
# dataset_from_raw().
# This dict should be read-only, and if Python had a read-only dict I would
# use it here. Don't modify it at runtime.
DEFAULT_BLOCK_CLASSES = {
    "raw"       : block_raw.BlockRaw,
    "prep"      : block_prep_identity.BlockPrepIdentity,
    "spectral"  : block_spectral_identity.BlockSpectralIdentity,
    "fit"       : block_fit_identity.BlockFitIdentity,
    "quant"     : block_quant_identity.BlockQuantIdentity,
}


###########    End of "private" constants, functions and classes    #########



############    Start of public constants, functions and classes    ##########


def dataset_from_raw(raw, block_classes={ }, zero_fill_multiplier=0):
    """
    Given a DataRaw object and some optional params, returns a dataset
    containing the minimal set of operational blocks for use in Analysis: raw
    and spectral. Other block slots (prep and fit) contain identity blocks.

    If block_classes is populated, it must be a dict that maps slot names
    to block classes like the dict DEFAULT_BLOCK_CLASSES in this module. The
    classes specified will be used in the slots specified.

    It's not necessary to specify all slots. For instance, to force data to
    be banana-shaped, a caller could pass a dict like this:
        { "prep" : block_prep_banana.BlockPrepBanana }

    If the zero_fill_multiplier is non-zero, it is applied to the newly-created
    dataset.
    """
    dataset = Dataset()

    # Replace the default raw block. Note that even if the default raw block
    # is of the correct type (which is probably the case), I can't just call
    # its inflate() method because _create_block() does other stuff besides
    # just inflating the block.
    klass = block_classes.get("raw", block_raw.BlockRaw)
    dataset._create_block(("raw", klass), raw.deflate(Deflate.DICTIONARY))

    if "prep" in block_classes:
        # Replace the default prep block
        dataset._create_block( ("prep", block_classes["prep"]) )
    #else:
        # The default identity block is just fine.

    klass = block_classes.get("spectral", block_spectral.BlockSpectral)
    dataset._create_block(("spectral", klass))

    # At present, we never create/replace a fit block via this method.

    # Update the user_prior spectrum now that the spectral block exists.
    dataset.user_prior.spectrum.calculate_spectrum(dataset)

    # Adjust the zerofill if necessary.
    if zero_fill_multiplier:
        dataset.update_for_zerofill_change(zero_fill_multiplier)

    return dataset


class Dataset(object):
    """
    This is the fundamental object being manipulated in the Analysis program.

    On the GUI side, the primary Analysis application is just an AUI notebook
    filled with dataset tabs. These can be opened, closed, and organized on
    the screen in many ways, but each dataset tab contains only one dataset
    object.

    As an object, a Dataset contains a list of processing blocks that are
    used to store, process and analyze MRS data. Each processing block has
    a reference to the previous step which hold the input data for the current
    processing step. It also contains results arrays to store the final output.
    Each processing block also has a 'chain' object that is used to perform
    the actual scientific algorithms on the data. Finally, each block has a
    'settings' object that contain the actual processing parameter settings.
    These are kept in a separate object within each block to delineate the
    inputs from the outputs (or helper/temporary) variables.

    The blocks attribute is an ordered dict of objects, all of which derive
    from the block.Block type and implement its interface. The dict is
    keyed with the names "raw", "prep", "spectral", and "fit", in that order.
    These represent "slots", each of which can be filled with one block of
    the appropriate type.

    The first slot contains an inert raw data block. All the other blocks
    have the option of transforming the data somehow. When a slot's
    transformation doesn't need to do anything, it's filled with a lightweight
    version of the block that just performs the identity transform on the
    data.
    """
    # The XML_VERSION enables us to change the XML output format in the future
    XML_VERSION = "1.1.0"

    def __init__(self, attributes=None):
        #------------------------------------------------------------
        # Set up elements of the processing chain for the data set
        #
        # Each dataset tab is located in the "outer" notebook which
        # is used to organize the one or more data sets that are open
        # in the application.
        #
        # - The blocks list contain objects that correspond to the
        #   processing tabs in the dataset (or "inner") notebook. A
        #   "block" contains a "chain" object that contains
        #   the code to run the functor chain of processing steps for
        #   a given block. The functor chain is dynamically allocated
        #   for each call depending on the widget settings in the tab.
        #
        #------------------------------------------------------------

        self.id = util_misc.uuid()

        # dataset_filename is only set on-the-fly (as opposed to being set
        # via inflate()). It's only set when the current dataset was read from
        # or saved to a VIFF file.
        self.dataset_filename = ''

        self.behave_as_preset = False

        self.user_prior = mrs_user_prior.UserPrior()

        # Create default blocks. We replace these as needed. Note that the
        # order in which these are added drives the order of the blocks and
        # tabs in the application as a whole.
        self.blocks = collections.OrderedDict()
        for name in ("raw", "prep", "spectral", "fit", "quant"):
            self._create_block( (name, DEFAULT_BLOCK_CLASSES[name]) )

        if attributes is not None:
            self.inflate(attributes)

        # Update the user prior spectrum now that the spectral block is self.blocks["prep"].is_identity
        # inflated and set up as it should be.
        self.user_prior.spectrum.calculate_spectrum(self)


    @property
    def raw_dims(self):
        """Raw data dimensionality. It's read only."""
        if self.blocks:
            if self.blocks["prep"].is_identity:
                return self.blocks["raw"].dims
            else:
                return self.blocks["prep"].dims
        return None

    @property
    def spectral_dims(self):
        """Spectral data dimensionality. It's read only."""
        if self.blocks:
            spectral_dims = self.raw_dims
            zfmult   = self.zero_fill_multiplier
            if zfmult:
                spectral_dims[0] *= zfmult
                return spectral_dims
        return None

    @property
    def sw(self):
        """Raw/All data sweep width. It's read only."""
        if self.blocks:
            return self.blocks["raw"].sw
        return None

    @property
    def raw_hpp(self):
        """Raw/All data center frequency. It's read only."""
        if self.blocks:
            return self.sw / self.raw_dims[0]
        return None

    @property
    def spectral_hpp(self):
        """Raw/All data center frequency. It's read only."""
        if self.blocks:
            spectral_dims = self.spectral_dims
            if spectral_dims:
                return self.sw / spectral_dims[0]
        return None

    @property
    def frequency(self):
        """Raw/All data center frequency. It's read only."""
        if self.blocks:
            return self.blocks["raw"].frequency
        return None

    @property
    def resppm(self):
        """Raw/All data resonance PPM value. It's read only."""
        if self.blocks:
            return self.blocks["raw"].resppm
        return None

    @property
    def midppm(self):
        """Raw/All data middle point PPM value. It's read only."""
        if self.blocks:
            return self.blocks["raw"].midppm
        return None

    @property
    def echopeak(self):
        """
        Acquisition echo peak value (typically 0.0 for FID data, 0.5 for full echo).
        It's read only.
        """
        if self.blocks:
            return self.blocks["raw"].echopeak
        return None

    @property
    def is_fid(self):
        """Boolean. It's read only."""
        if self.blocks:
            return self.blocks["raw"].is_fid
        return None

    @property
    def seqte(self):
        """Acquisition echo time in msec. It's read only."""
        if self.blocks:
            return self.blocks["raw"].seqte
        return None

    @property
    def nucleus(self):
        """Acquisition nucleus. It's read only."""
        if self.blocks:
            return self.blocks["raw"].nucleus
        return None

    @property
    def zero_fill_multiplier(self):
        """Spectral dimension zero fill factor. It's read only."""
        if self.blocks:
            return self.blocks["spectral"].set.zero_fill_multiplier
        return None

    @property
    def phase_1_pivot(self):
        """Spectral phase 1 pivot location in ppm. It's read only."""
        if self.blocks:
            return self.blocks["spectral"].set.phase_1_pivot
        return None

    @property
    def auto_b0_range_start(self):
        """
        Returns PPM range over which automated B0 shift routine searches.
        Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.auto_b0_range_start

    @property
    def auto_b0_range_end(self):
        """
        Returns PPM range over which automated B0 shift routine searches.
        Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.auto_b0_range_end

    @property
    def auto_phase0_range_start(self):
        """
        Returns PPM range over which automated Phase0 routine is applied.
        Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.auto_phase0_range_start

    @property
    def auto_phase0_range_end(self):
        """
        Returns PPM range over which automated Phase0 routine is applied.
        Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.auto_phase0_range_end

    @property
    def auto_phase1_range_start(self):
        """
        Returns PPM range over which automated Phase1 routine is applied.
        Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.auto_phase1_range_start

    @property
    def auto_phase1_range_end(self):
        """
        Returns PPM range over which automated Phase1 routine is applied.
        Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.auto_phase1_range_end

    @property
    def auto_phase1_pivot(self):
        """
        Returns PPM value at which automated Phase1 routine rotates phase.
        Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.auto_phase1_pivot

    @property
    def metinfo(self):
        """
        Returns the Metinfo object stored in Dataset. This provides info about
        literature values of metabolites, such as concentrations and spins that
        are used in the fitting initial values routines.
        """
        return self.user_prior.metinfo

    @property
    def user_prior_summed_spectrum(self):
        """
        Returns Numpy array with frequency spectrum created from the UserPrior
        values in that dialog. This is the model spectrum used in the automated
        B0 and Phase routines. This spectrum matches the spectral resolution of
        the data. Obtained from UserPrior object in Dataset. Read only!
        """
        return self.user_prior.spectrum.summed

    @property
    def all_voxels(self):
        """ return list of all voxel indices based on spectral_dims """
        dims = self.spectral_dims
        all = []
        for k in range(dims[3]):
            for j in range(dims[2]):
                for i in range(dims[1]):
                    all.append((i,j,k))
        return all

    @property
    def measure_time(self):
        """
        Returns a Numpy array of floating point values. These values are the 
        acquisition times for each FID in the data array. Each value is the 
        time since midnight in seconds at which the acquisition started. Most
        use cases will normalize this value into 0 for the first FID and some
        delta seconds from 0 for each subsequent FID.
        
        This functions gathers measure_time values from the Prep block since
        the number of FIDs may change if we 'massage' the data. Eg. if we 
        average every other or every 3/4/N FIDs to improve SNR. In this case
        the new measure_time array is calculted in the Prep block/functor. If
        no measure_time attribute is available in Prep block, we look for one
        in the Raw block. If there is none in Raw we default to a 'range' of
        integer steps.
        
        Eg. For data taken from DICOM files, the 'measure_time' tag is used.
        This tag stores the time since midnight in an HHMMSS.fraction string. 
        We convert this string to seconds in float format. 
        
        Eg. At this time we don't have other examples, but anyone writing code
        for this attribute could just start from 0 and increment as desired. 
        Any subsequent normalization would subtract from the first point and
        it would work just fine.
        
        """
        if self.blocks:
            if self.blocks["prep"].is_identity:
                block = self.blocks["raw"]
                try:
                    val = block.measure_time
                except AttributeError:
                    val = range(raw_dims[1])
            else:
                block = self.blocks["prep"]
                try:
                    val = block.measure_time
                except AttributeError:
                    block = self.blocks["raw"]
                    try:
                        val = block.measure_time
                    except AttributeError:
                        val = range(raw_dims[1])
        return val


    def __str__(self):
        return self.__unicode__().encode("utf-8")


    def __unicode__(self):
        lines = [ ]

        lines.append(u"-----------  Dataset %s  -----------" % self.id)
        lines.append("filename: %s" % self.dataset_filename)
        for block in self.blocks.itervalues():
            lines.append(unicode(block))

        return u'\n'.join(lines)


##########################    Public methods    #########################

    def add_fit(self, type, force=False, full_range=False):
        """
        Replaces the fit identity block with a typed fitting block. If the
        current fit block is not an indentiy block, this code does nothing.

        The force flag is used in the apply_preset method to force a new
        'fit' object to be created if needed

        Returns the new fit block if one was created, or None otherwise.

        """
        if self.blocks["fit"].is_identity or force:
            # The existing Fit block is the Identity block. Replace it.
            # FIXME bjs Adding a fit block does a calc_full_basis_set()
            block = self._create_block(type)

            ppm_str = block.set.prior_ppm_start
            ppm_end = block.set.prior_ppm_end
            if full_range:
                ppm_str = None
                ppm_end = None

            prior = block.set.prior
            prior.calculate_full_basis_set(ppm_str, ppm_end, self)
            return block
        else:
            # The existing Fit block is not the Identity block. Don't touch it.
            return None


    def add_voigt(self, force=False):
        """ replace fit identity block with a FitVoigt block """ 
        return self.add_fit('block_fit_voigt')


    def add_giso(self, force=False):
        """ replace fit identity block with a FitGiso block """ 
        return self.add_fit('block_fit_giso')
        

    def add_watref(self, force=False):
        """
        Replaces the quant identity block with a QuantWatref block. If the
        current fit block is not an indentiy block, this code does nothing.

        The force flag is used in the apply_preset method to force a new
        'fit' object to be created if needed

        Returns the new fit voigt block if one was created, or None otherwise.
        """
        if self.blocks["quant"].is_identity or force:
            # The existing Quant block is the Identity block. Replace it.
            block = self._create_block("block_quant_watref")

            return block
        else:
            # The existing Quant block is not the Identity block. Don't touch it.
            return None


    def batch_fit_all(self, statusbar=None):

        voxels = self.all_voxels
        nvox   = len(voxels)

        for i,voxel in enumerate(voxels):
            
            if statusbar: statusbar.SetStatusText(' Batch Fitting Voxel %d/%d ' % (i+1,nvox), 0)

            do_init = True if i == 0 else False     # triggers init of global vars in chain.run() if needed.

            block = self.blocks["spectral"]
            res = block.chain.run([voxel], entry='all')

            block = self.blocks["fit"]
            res = block.chain.run([voxel], entry='full_fit', do_init=do_init)

# FIXME bjs - need to add this in some day
#
#             block = self.blocks["quant"]
#             res = block.chain.run([voxel], entry='quant')
        


    def set_associated_datasets(self, datasets):
        for block in self.blocks.itervalues():
            block.set_associated_datasets(datasets)


    def update_for_zerofill_change(self, zf_mult):
        """
        Here we assume that the dims coming in are for the new setting of
        the zero fill parameter. We check if we already match those values
        or if we need to reset block and chain dimensional results arrays

        """
        self.blocks["spectral"].set.zero_fill_multiplier = zf_mult
        # Let everyone know that the zerofill changed
        for block in self.blocks.itervalues():
            block.set_dims(self)
        self.user_prior.spectrum.calculate_spectrum(self)


    def update_for_preprocess_change(self):
        """
        Here we assume that the dims coming in are for the new setting of
        the zero fill parameter. We check if we already match those values
        or if we need to reset block and chain dimensional results arrays

        """
        # Let everyone know that the dims in preprocess block have changed
        for block in self.blocks.itervalues():
            block.set_dims(self)


    def set_behave_as_preset(self, flag):
        """
        This will set all 'behave_as_preset' flags in the dataset and in
        the self.blocks list to the value of flag. User is responsible for
        setting/resetting these flags using this function.

        """
        val = flag == True
        self.behave_as_preset = flag
        for block in self.blocks.itervalues():
            block.behave_as_preset = val


    def apply_preset(self, preset, voxel=(0,0,0), block_run=False):
        '''
        Given a 'preset' dataset object (an actual dataset object that may
        or may not have data in it depending on whether it was saved as a
        preset file or dataset file), we extract the parameter settings for:

        - the user_prior object
        - each processing block and apply them to the current dataset
        - we ensure that the data dimensionality between blocks is properly
          maintained (e.g. zerofilling).
        - Finally, we run each block.process() method

        Things to know about Presets

        Each object in the presets blocks list (raw, prep, spectral, fit) is
        compared to the object class name in this dataset. If the names match
        the Settings object is copied over. If the class names do not match,
        no settings are copied over.

        The 'spectral' object has a few extra values copied over, like the
        phases and shift_frequencies.  Both the 'spectral' and 'fit' objects
        also need some run-time values recalculated after the settings are
        copied over.

        '''
        self.user_prior = copy.deepcopy(preset.user_prior)
        self.user_prior.spectrum.calculate_spectrum(self)  # parent dataset may have different points/dwell

        if self.blocks['raw'].__class__.__name__ == preset.blocks['raw'].__class__.__name__:
            self.blocks['raw'].set = copy.deepcopy(preset.blocks['raw'].set)

        if self.blocks['prep'].__class__.__name__ == preset.blocks['prep'].__class__.__name__:
            if not preset.blocks['prep'].is_identity:
                block = self.blocks['prep']
                block.set = copy.deepcopy(preset.blocks['prep'].set)
                block._reset_dimensional_data(self)

        if self.blocks['spectral'].__class__.__name__ == preset.blocks['spectral'].__class__.__name__:

            block = self.blocks['spectral']

            # We do a deep copy of all the settings from the preset dataset
            # into the current dataset, and check the result array dimensions
            
            block.set              = copy.deepcopy(preset.blocks['spectral'].set)
            block._phase_0         = copy.deepcopy(preset.blocks['spectral']._phase_0)
            block._phase_1         = copy.deepcopy(preset.blocks['spectral']._phase_1)
            block._frequency_shift = copy.deepcopy(preset.blocks['spectral']._frequency_shift)

            block.frequency_shift_lock = preset.blocks['spectral'].frequency_shift_lock
            block.phase_lock           = preset.blocks['spectral'].phase_lock
            block.phase_1_lock_at_zero = preset.blocks['spectral'].phase_1_lock_at_zero
            block.kiss_off_correction  = preset.blocks['spectral'].kiss_off_correction
            block._reset_dimensional_data(self)

        if not preset.blocks['fit'].is_identity:

            # create fit object if it does not exist
            if   isinstance(preset.blocks['fit'], block_fit_voigt.BlockFitVoigt):
                self.add_voigt(force=True)
            elif isinstance(preset.blocks['fit'], block_fit_giso.BlockFitGiso):
                self.add_giso(force=True)

            # copy preset values into fit block and recalc as needed
            block = self.blocks['fit']
            block.set = copy.deepcopy(preset.blocks['fit'].set)
            prior = block.set.prior
            if   isinstance(preset.blocks['fit'], block_fit_voigt.BlockFitVoigt):
                prior.calculate_full_basis_set(block.set.prior_ppm_start, block.set.prior_ppm_end, self)
            elif isinstance(preset.blocks['fit'], block_fit_giso.BlockFitGiso):
                prior.calculate_full_basis_set(None, None, self)
            block._reset_dimensional_data(self)

        if not preset.blocks['quant'].is_identity:

            # create 'block_quant_watref' object if it does not exist
            self.add_watref(force=True)

            # copy preset values into watref block 
            block = self.blocks['quant']
            block.set = copy.deepcopy(preset.blocks['quant'].set)



########################   Inflate()/Deflate()    ########################


    def deflate(self, flavor=Deflate.ETREE, is_main_dataset=True):

        associated = []
        # associated datasets are gathered here so that they can be returned as
        # a result of this deflate in a list, they are positioned first in the
        # list that is returned to ensure that they are available for inflate
        # prior to the inflate of the main data set with which they associate.
        #
        # In some cases a file may be associated twice, as in the case of GE
        # Pfiles that associate water and water suppressed in both raw and
        # possibly the ECC filter in Spectral tab. We only want to save once
        # so we gather all associated datasets, filter for uniqueness, change
        # the id, deflate it then change the id back for the currently open
        # dataset.
        all_datasets = []
        unique_datasets = []

        for block in self.blocks.itervalues():
            # gather all associated datasets, unique or not
            all_datasets += block.get_associated_datasets(is_main_dataset)

        for item in all_datasets:
            # create list of unique associated datasets maintaining order but
            # also be sure that we do not include ourselves. This could occur
            # in Edited datasets which have on/off/add/sub states.
            if item not in unique_datasets and item is not self:
                unique_datasets.append(item)

        for dataset in unique_datasets:
            # As we save these associated datasets, we want to use unique
            # ids that won't collide with ids in memory now, should they
            # be loaded right back in again. So here the dataset.id is changed
            # and deflated. Then all the rest of the main dataset (including
            # any refs to the associated datasets) are deflated. Then the
            # associated datasets ids are restored

            dataset.id_saved = dataset.id
            dataset.id = util_misc.uuid()

            # FIXME - BJS test if this is a true thing, we do NOT want
            #   to save any associated datasets when we do presets save
            if not self.behave_as_preset:
                associated.append(dataset.deflate(flavor, is_main_dataset=False))

        if flavor == Deflate.ETREE:
            e = ElementTree.Element("dataset",
                                      { "id" : self.id,
                                        "version" : self.XML_VERSION})

            if self.behave_as_preset:
                util_xml.TextSubElement(e, "behave_as_preset", self.behave_as_preset)

            e.append(self.user_prior.deflate())

            ee = ElementTree.SubElement(e, "blocks")

            for block in self.blocks.itervalues():
                if not block.is_identity:
                    ee.append(block.deflate())
                #else:
                    # We don't clutter up the XML with identity blocks.

            if associated:
                associated.append(e)
                e = associated

            return e

        elif flavor == Deflate.DICTIONARY:
            return self.__dict__.copy()

        for dataset in unique_datasets:
            # Restore the original UUID in associated datasets
            dataset.id = dataset.id_saved


    def inflate(self, source):
        if hasattr(source, "makeelement"):
            # Quacks like an ElementTree.Element
            xml_version = source.get("version")
            self.id = source.get("id")

            val = source.findtext("behave_as_preset")       # default is False
            if val is not None:
                self.behave_as_preset = util_xml.BOOLEANS[val]

            #==================================================================
            # This code chunk deals with earlier version datasets that need
            # to be parsed into the current layout of the dataset object
            #==================================================================

            if xml_version == "1.0.0":
                # For this version, user prior information is extracted from
                # the basic block (below).
                pass
            else:
                # In all other versions, user prior resides in its own node.
                self.user_prior.inflate(source.find("user_prior"))

            # The individual <block> elements are wrapped in a <blocks>
            # element. The <blocks> element has no attributes and its only
            # children are <block> elements. <blocks> is just a wrapper.
            # Note that ElementTree elements with children are designed to
            # behave quite a lot like ordinary Python lists, and that's how we
            # regard this one.
            block_elements = source.find("blocks")
            if block_elements:
                if block_elements[0].tag == "block_raw_fidsum":
                    # Prior to Vespa 0.7.0, fidsum was expressed in a special
                    # raw_fidsum block rather than in prep. Here we split the
                    # raw_fidsum element into a regular raw element and a
                    # prep_fidsum element.
                    raw = block_elements[0]

                    # A BlockPrepFidsum looks enough like a BlockRawFidsum
                    # object that we can inflate the former from the latter's
                    # data simply by renaming the settings object.
                    raw_settings = raw.find("block_raw_fidsum_settings")
                    raw_settings.tag = "settings"
                    prep = block_prep_fidsum.BlockPrepFidsum(raw)
                    # Deflate the object back into an ElementTree element and
                    # slip it into the appropriate place amongst it siblings.
                    # This may seem a bit stupid since we just inflated it, but
                    # the goal here is to make the old XML (or the ETree
                    # representation of it) look as much like the new style
                    # as possible.
                    prep = prep.deflate()
                    block_elements.insert(1, prep)

                    # Now make the block_raw_fidsum element look like a plain
                    # old block_raw element.
                    raw.tag = "block_raw"
                    raw.remove(raw_settings)
                    # Replace the data subelement with the raw subelement.
                    raw.remove(raw.find("data"))
                    raw.find("raw").tag = "data"


                if xml_version == "1.0.0":
                    # Version 1.0.0 has a basic block. As of Vespa >= 0.6.3
                    # a.k.a. XML_VERSION 1.1.0, there's no more basic block
                    # but instead a UserPrior object hanging off of the dataset.
                    # Find and extract the basic block and turn it into
                    # a UserPrior object.
                    for i, block_element in enumerate(block_elements):
                        if block_element.tag == "block_basic":
                            break
                    block_basic = block_elements[i]
                    block_elements.remove(block_basic)

                    block_basic_settings = block_basic.find("block_basic_settings")

                    auto_prior = block_basic_settings.find("auto_prior")
                    auto_prior.tag = "user_prior_spectrum"

                    self.user_prior.inflate(block_basic_settings)

                    # Some confusion here...due to an oversight, there are two
                    # versions of XML format 1.0.0. One version has HLVSD as
                    # a separate block/tab, the other has it merged with
                    # spectral. The code below handles the case where HLSVD
                    # is separate.
                    # The SVD block/tab was subsumed into spectral starting
                    # with Vespa 0.6.1.
                    hlsvd = None
                    spectral = None
                    for i, block_element in enumerate(block_elements):
                        if block_element.tag == "block_hlsvd":
                            hlsvd = block_element
                            hlsvd_index = i
                        if block_element.tag == "block_spectral":
                            spectral = block_element

                        if hlsvd and spectral:
                            # move hlsvd attribs to spectral block
                            excludes = ("dim", )
                            for item in hlsvd:
                                if item.tag not in excludes:
                                    spectral.append(item)

                            # scrounge the threshold value from the previous
                            # hlsvd water filter settings if available
                            settings = spectral.find("block_spectral_settings")
                            water_filter = settings.find("water_filter")

                            if water_filter is not None:
                                # Ensure this is the HLSVD filter and not some
                                # other kind.
                                if water_filter.attrib['id'] == _HLSVD_FILTER_UUID:
                                    # Copy threshold info to spectral
                                    threshold = water_filter.findtext("threshold")
                                    util_xml.TextSubElement(settings,
                                                            "svd_threshold",
                                                            threshold)
                                    apply_ = water_filter.findtext("apply_as_water_filter")
                                    util_xml.TextSubElement(settings,
                                                            "svd_apply_threshold",
                                                            apply_)
                            #else:
                                # No water filter, nothing to worry about.

                            block_elements.remove(hlsvd)
                #else:
                    # Nothing to do, the XML version is current.
            else:
                # block_elements is None or has no kids. If either of these
                # conditions occurs, we are in undefined territory since every
                # dataset has at least a raw block.
                raise ValueError, "<block> element must have children"

            # end parsing of previous dataset versions
            #==================================================================

            for block_element in block_elements:
                self._create_block(block_element.tag, block_element)


        elif hasattr(source, "keys"):
            # Quacks like a dict
            raise NotImplementedError



    #################################################################
    ##### Public functions for Phase0/1 Frequency Shift
    #####
    ##### Phase 0 and 1 are used in a number of processing tabs (for
    ##### View typically). To facilitate set/get of these values,
    ##### which are traditionally stored in the Spectral processing
    ##### module, we create these helper functions at the level of
    ##### the Dataset
    #################################################################

    def get_phase_0(self, xyz):
        """ Returns 0th order phase for the voxel at the xyz tuple """
        return self.blocks["spectral"].get_phase_0(xyz)

    def set_phase_0(self, phase_0, xyz):
        """ Sets 0th order phase for the voxel at the xyz tuple """
        self.blocks["spectral"].set_phase_0(phase_0, xyz)

    def get_phase_1(self, xyz):
        """ Returns 1st order phase for the voxel at the xyz tuple """
        return self.blocks["spectral"].get_phase_1(xyz)

    def set_phase_1(self, phase_1, xyz):
        """ Sets 1st order phase for the voxel at the xyz tuple """
        self.blocks["spectral"].set_phase_1(phase_1, xyz)

    def get_frequency_shift(self, xyz):
        """ Returns frequency_shift for the voxel at the xyz tuple """
        return self.blocks["spectral"].get_frequency_shift(xyz)

    def set_frequency_shift(self, frequency_shift, xyz):
        """ Sets frequency_shift for the voxel at the xyz tuple """
        self.blocks["spectral"].set_frequency_shift(frequency_shift, xyz)

    def get_source_data(self, block_name):
        """
        Returns the data from the first block to the left of the named block
        that is not None

        """
        keys = self.blocks.keys()
        keys = keys[0:keys.index(block_name)]
        for key in keys[::-1]:
            data = self.blocks[key].data
            if data is not None:
                return data
        return self.blocks[block_name].data


    def get_source_chain(self, block_name):
        """
        Returns the chain object from the first block to the left of the named
        block that is not None

        """
        keys = self.blocks.keys()
        keys = keys[0:keys.index(block_name)]
        for key in keys[::-1]:
            data = self.blocks[key].chain
            if data is not None:
                return data
        return self.blocks[block_name].chain
    
    
#    def get_block(self, block_name):
#        """
#        Returns the block object even if None
#
#        """
#        keys = self.blocks.keys()
#        if not block_name in keys:
#            return None
#        
#        return self.blocks[block_name]



########################   "Private" Methods    ########################


    def _create_block(self, type_info, attributes=None):
        """
        Given block type info (see below) and optional attributes (suitable
        for passing to inflate()), creates a block of the specified type,
        places it in this dataset's dict of blocks, and returns the
        newly-created block.

        The type_info can be either one of the keys in _XML_TAG_TO_SLOT_CLASS_MAP
        or a 2-tuple of (slot name, class). In the former case,
        _XML_TAG_TO_SLOT_CLASS_MAP is used to look up the 2-tuple. That makes
        this method very convenient for calling from Dataset.inflate().

        In both cases, this method replaces the class in the slot name with
        an instance of the class in the 2-tuple.

        The newly-created block is also asked to create its chain and
        set its dims.
        """
        if type_info in _XML_TAG_TO_SLOT_CLASS_MAP:
            name, klass = _XML_TAG_TO_SLOT_CLASS_MAP[type_info]
        else:
            # If this isn't a tuple, there's going to be trouble!
            name, klass = type_info

        # Instantiate and replace the existing block with the new one.
        block = klass(attributes)
        self.blocks[name] = block
        block.set_dims(self)
        # setting of helper attributes self.raw_xxx depends on self.data
        # having correct dimensions, so this has to follow set_dims()
        block.create_chain(self)

        return block





