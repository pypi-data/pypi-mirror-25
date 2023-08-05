# Python modules
from __future__ import division
import os

# 3rd party modules
import wx
import wx.html
import wx.aui as aui


# Our modules
import tab_priorset
import vespa.common.wx_gravy.util as wx_util
import vespa.common.wx_gravy.notebooks as vespa_notebooks
import vespa.common.util.misc as util_misc



class NotebookPriorset(vespa_notebooks.VespaAuiNotebook):
    # I need the path to the welcome tab image which is in vespa/common.
    _path = util_misc.get_vespa_install_directory()
    _path = os.path.join(_path, "common", "resources", "prior_welcome.png")

    WELCOME_TAB_TEXT = """
    <html><body>
    <h1>Welcome to Vespa - Priorset</h1>
    <img src="%s" alt="Time-Freq Plots" />
    <p><b>Currently there are no priorsets loaded.</b></p>
    <p>You can use the Priorset menu to browse for a Vespa-Simulation experiment from which to create a priorset.</p>
    </body></html>
    """ % _path
    # I tidy up my namespace by deleting this temporary variable.
    del _path
    
    
    def __init__(self, top):

        vespa_notebooks.VespaAuiNotebook.__init__(self, top)

        self.top    = top
        self.count  = 0
        
        self.show_welcome_tab()

        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_tab_close)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.on_tab_closed)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_tab_changed)
        

    #=======================================================
    #
    #           Global and Menu Event Handlers 
    #
    #=======================================================

    def on_menu_view_option(self, event):
        if self.active_tab:
            self.active_tab.on_menu_view_option(event)

    def on_menu_view_output(self, event):
        if self.active_tab:
            self.active_tab.on_menu_view_output(event)

    def on_tab_changed(self, event):

        self._set_title()
            
        if self.active_tab:
            self.active_tab.on_activation()
            
            
    def on_tab_close(self, event):
        """
        This is a two step event. Here we give the user a chance to cancel 
        the Close action. If user selects to continue, then the on_tab_closed()
        event will also fire.  
        
        """
        msg = "Are you sure you want to close this priorset?"
        if wx.MessageBox(msg, "Close Priorset", wx.YES_NO, self) != wx.YES:
            event.Veto()



    def on_tab_closed(self, event):        
        """
        At this point the tab is already closed and the priorset removed from
        memory.        
        """
        if not self.tabs:
            self.show_welcome_tab()

        self._set_title()


    #=======================================================
    #
    #           Public methods shown below
    #             in alphabetical order 
    #
    #=======================================================

    def add_priorset_tab(self, priorset=None):

        # If the welcome tab is open, close it.
        if self.is_welcome_tab_open:
            self.remove_tab(index=0)

        self.count += 1
        name = "Priorset%d" % self.count

        # create new notebook tab with process controls 
        tab = tab_priorset.TabPriorset(self, self.top, priorset)
        self.AddPage(tab, name, True)


    def close_priorset(self):
        if self.active_tab:
            wx_util.send_close_to_active_tab(self)


    #=======================================================
    #
    #           Internal methods shown below
    #             in alphabetical order 
    #
    #=======================================================

    def _set_title(self):
        title = "Priorset"

        if self.active_tab:
            tab = self.active_tab

            if tab.priorset:
                title += " - " + tab.priorset.experiment.name

        wx.GetApp().GetTopWindow().SetTitle(title)


