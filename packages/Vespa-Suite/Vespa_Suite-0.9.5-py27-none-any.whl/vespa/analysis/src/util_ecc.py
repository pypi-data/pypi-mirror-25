# Python imports
from __future__ import division


# 3rd party imports

# Our imports
import dialog_dataset_browser


def select_ecc_dataset(datasets):
    dialog = dialog_dataset_browser.DialogDatasetBrowser(datasets)
    dialog.ShowModal()
    dataset = dialog.dataset
    dialog.Destroy()
    return dataset
