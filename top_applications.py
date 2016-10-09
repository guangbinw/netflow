#!/usr/bin/env python

from utilities import panel_size
from utilities import application_dictionary
from utilities import getRowset
from time_panel import TimeControlPanel
from pylab import *         #includes arange
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


sql = "select dstport as dst_port, sum(octets) from flow where srcaddr like '192.168.0.%' group by dstport order by sum(octets) desc"
sql_total_volume = "select sum(octets) from flow where srcaddr like '192.168.0%'"

class TopApplicationsPlotPanel(wx.Panel):
    def __init__( self, parent):

        wx.Panel.__init__( self, parent)
        # initialize matplotlib stuff
        self.figure = Figure()
        self.canvas = FigureCanvas( self, -1, self.figure )
        self.ax = self.figure.add_subplot(111)

        #print "Top Applications ..."
        self.timeControlPanel = TimeControlPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.timeControlPanel, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.canvas, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
       
        self.SetSize(panel_size)
        self.add_toolbar()  # comment this out for no toolbar
        self.ax.set_title('Most active applications', bbox={'facecolor':'0.8', 'pad':5})

        self.Fit()
        #print sql
        rowset = getRowset(sql)
        print "sql = " + sql_total_volume
        total_traffic_volume = getRowset(sql_total_volume)
        labels = []
        prot_num_array = []
        prot_totals_array=[]
        total_outbound_traffic = 0;
        for row in total_traffic_volume:
            total_outbound_traffic = row[0]
        #print total_outbound_traffic
        other_traffic = 0
        less_than_one_percent = 0
        for row in rowset:
            port_num = row[0]
            port_total = row[1]
            percentage = (float(port_total)/total_outbound_traffic)*100
            if application_dictionary.has_key(port_num):
                #print port_num
                if (percentage>1):
                    #print percentage
                    prot_num_array.append(port_num)
                    prot_totals_array.append(port_total)
                else:
                    less_than_one_percent = less_than_one_percent + port_total
            else:
                other_traffic  = other_traffic + port_total
        for item in prot_num_array:
            labels.append(application_dictionary.__getitem__(item))
        labels.append("<1%")
        labels.append("Other")
        prot_totals_array.append(less_than_one_percent)
        prot_totals_array.append(other_traffic)

        #print labels
        self.ax.pie(prot_totals_array, explode=None, labels=labels, autopct='%1.1f%%', shadow=True)
        #title('Most active applications', bbox={'facecolor':'0.8', 'pad':5})

    def add_toolbar(self):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        if wx.Platform == '__WXMAC__':
             self.SetToolBar(self.toolbar)
        else:
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            self.toolbar.SetSize(wx.Size(fw, th))
            self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()


