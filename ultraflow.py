#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""Ultraflow is a Cisco Netflow analyser and visualiser written by Anthony Mapfumo.
It is aimed at small organisations with a handfull of Cisco routers

"""

__author__="Anthony Mapfumo, mapfumo@gmail.com"
__date__ ="$16/08/2009"



#from top_volume import TopVolumePlotPanel
from top_conversations import TopConversationsPanel
from top_destinations import TopDestinationsPanel
from top_volume import VolumePanel
#from top_applications import TopApplicationsPlotPanel
from top_talkers import TopTalkersPlotPanel
import wx

class TopTalkers(wx.Panel):
   def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #topTalkersPlotPanel = TopTalkersPlotPanel(self)
        TopTalkersPlotPanel(self)

class TopDestinations(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        TopDestinationsPanel(self)

"""class Applications(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        TopApplicationsPlotPanel(self)"""

class Volume(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        VolumePanel(self)


class Conversations(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        TopConversationsPanel(self)


class UltraFlow(wx.Frame):
    def __init__(self):
        #wx.Frame.__init__(self, None, title="UltraFlow Netflow Analyser")
        #wx.Frame.__init__(self,None,-1,"Ultr@Flow - Netflow Analyser",wx.DefaultPosition, wx.Size(1000, 900))
        wx.Frame.__init__(self,None,-1,"Ultr@Flow - Netflow Analyser",wx.DefaultPosition, wx.Size(1024, 700),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        # The application is based on pages/tabs which are implemented using the
        # wxNotebook control: Overview, To Talkers, Conversations, Applications, Destinations, Volume
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create menus for Ultr@Flow
        menuBar = wx.MenuBar()          # menu bar
        menuFile = wx.Menu()            # create a File menu
        exitMenuItem = menuFile.Append(-1, "Exit", "Exit Ultr@Flow")

        menuHelp = wx.Menu()            # create a File menu
        menuHelp.Append(-1, "Help", "Online Help")
        aboutMenuItem = menuHelp.Append(-1, "About", "About Ultr@Flow")
        menuBar.Append(menuFile, "File")
        menuBar.Append(menuHelp, "Help")
        #menuBar.Append(menuHelp, "About")
        self.Bind(wx.EVT_MENU, self.aboutMenuEvent, aboutMenuItem)
        self.Bind(wx.EVT_MENU, self.exitMenuEvent, exitMenuItem)

        self.SetMenuBar(menuBar)
        
        # create the page windows as children of the notebook
        #applications = Applications(nb)
        conversations = Conversations(nb)
        topdestinations = TopDestinations(nb)
        toptalkers = TopTalkers(nb)
        volume = Volume(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(toptalkers, "Top Talkers")
        #nb.AddPage(applications, "Applications")
        nb.AddPage(volume, "Volume")
        nb.AddPage(conversations, "Conversations")
        nb.AddPage(topdestinations, "Destinations")

        # Put the notebook in a sizer for the panel to manage the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        self.Centre()

    def aboutMenuEvent(self, event):
        aboutInfo = "UltraFlow - Cisco Netflow Analyser.\nCopyright © 2011-2012 Anthony Mapfumo\nmapfumo@gmail.com\n\nPowered by Python, wxPython, Matplotlib & SQLite"
        aboutBox = wx.MessageDialog(self, message=aboutInfo, caption='About Ultr@Flow', style = wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK)
        if aboutBox.ShowModal() == wx.ID_OK: # Until the user clicks OK, show the message
            aboutBox.Destroy()


    def exitMenuEvent(self, event):
        """Exit programme."""
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    UltraFlow().Show()
    app.MainLoop()

