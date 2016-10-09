#!/usr/bin/env python

from utilities import getFormatedVolume
from utilities import getRowset
from time_panel import TimeControlPanel
from utilities import panel_size
import wx
from socket import *

sql = "select dst_addr, sum(octets) from flows where dst_addr not like '192.168.0.%' group by dst_addr order by sum(octets) desc limit 100"
sql_total_outbound_traffic = "select sum(octets) from flows where dst_addr not like '192.168.0.%'"
class TopDestinationsPanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__( self, parent)
        # initialize matplotlib stuff

        self.listControl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES)
        self.listControl.SetInitialSize(panel_size)
        self.timeControlPanel = TimeControlPanel(self)
        #self.listControl.SetForegroundColour(wx.Colour(50, 50, 204))
        self.listControl.SetForegroundColour(wx.Colour(50, 50, 204))
        #self.listControl.SetBackgroundColour(wx.Colour(219, 219, 112))

        self.listControl.InsertColumn(0,"Destination IP")
        self.listControl.SetColumnWidth(0, 200)
        self.listControl.InsertColumn(1,"Volume")
        self.listControl.SetColumnWidth(5, 200)
        self.listControl.InsertColumn(2,"Percentage")
        self.listControl.SetColumnWidth(5, 200)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.timeControlPanel, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.listControl, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)

        self.SetSize(panel_size)
        self.Fit()

        rowset = getRowset(sql)
        traffic_volume = getRowset(sql_total_outbound_traffic)[0]
        total_outbound_volume = float(traffic_volume[0])
        #print total_outbound_volume
        #print rowset
        for row in rowset:
            #print row
            max_rows = 100
            dst_addr, sum = row
            percentage_volume =  ("%.2f" % (100*(sum/total_outbound_volume)))
            print percentage_volume
            #application = getApplicationName(src_port)
            #protocol = getProtocolName(protocol)
            index = self.listControl.InsertStringItem(max_rows, dst_addr)
            sum = getFormatedVolume(sum)
            self.listControl.SetStringItem(index, 1, sum)
            if (float(percentage_volume)>1.00):
                self.listControl.SetStringItem(index, 2, (str(percentage_volume)+" %"))
            else:
                self.listControl.SetStringItem(index, 2, "<1 %")
