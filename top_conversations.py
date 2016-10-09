#!/usr/bin/env python


from utilities import getFormatedVolume
from utilities import getProtocolName
from utilities import getApplicationName
from utilities import getRowset
from time_panel import TimeControlPanel
from utilities import panel_size
import wx
from socket import *

sql = "select srcaddr as src_addr, dstaddr as dst_addr, srcport as src_port, protocol, sum(octets) from flow group by srcaddr, dstaddr order by sum(octets) desc limit 100"

class TopConversationsPanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__( self, parent)

        self.listControl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES)
        self.listControl.SetInitialSize(panel_size)
        self.timeControlPanel = TimeControlPanel(self)
        #self.listControl.SetForegroundColour(wx.Colour(50, 50, 204))
        self.listControl.SetForegroundColour(wx.Colour(50, 50, 204))
        #self.listControl.SetBackgroundColour(wx.Colour(219, 219, 112))

        self.listControl.InsertColumn(0,"Source IP")
        self.listControl.SetColumnWidth(0, 200)
        self.listControl.InsertColumn(1,"Destination IP")
        self.listControl.SetColumnWidth(1, 200)
        self.listControl.InsertColumn(2,"Application")
        self.listControl.SetColumnWidth(2, 200)
        self.listControl.InsertColumn(3,"Port")
        self.listControl.SetColumnWidth(3, 110)
        self.listControl.InsertColumn(4,"Protocol")
        self.listControl.SetColumnWidth(4, 100)
        self.listControl.InsertColumn(5,"Volume")
        self.listControl.SetColumnWidth(5, 200)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.timeControlPanel, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.listControl, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)

        self.SetSize(panel_size)
        self.Fit()

        rowset = getRowset(sql)
        #print rowset
        for row in rowset:
            #print row
            max_rows = 100
            
            src_addr, dst_addr, src_port, protocol, sum = row
            application = getApplicationName(src_port)
            protocol = getProtocolName(protocol)
            index = self.listControl.InsertStringItem(max_rows, src_addr)
            sum = getFormatedVolume(sum)
            self.listControl.SetStringItem(index, 1, dst_addr)
            self.listControl.SetStringItem(index, 2, application)
            self.listControl.SetStringItem(index, 3, str(src_port))
            self.listControl.SetStringItem(index, 4, str(protocol))
            self.listControl.SetStringItem(index, 5, str(sum))