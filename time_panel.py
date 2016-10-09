#!/usr/bin/env python

import wx
import time

class TimeControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent)
        self.time_choices = ["Hour", "Day", "Week", "Month", "Year"]
        self.start_hour_choices = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
        self.start_minute_choices = ["00", "10", "20", "30", "40", "50"]
        self.choiceTimePeriod = wx.Choice(self, -1, choices=self.time_choices)
        self.choiceTimePeriod.SetToolTipString("Report by last 'Hour', 'Day', 'Week', 'Month' or 'Year'")
        self.choice_start_hour = wx.Choice(self, -1, choices=self.start_hour_choices)
        self.choice_start_minute = wx.Choice(self, -1, choices=self.start_minute_choices)
        self.choice_end_hour = wx.Choice(self, -1, choices=self.start_hour_choices)
        self.choice_end_minute = wx.Choice(self, -1, choices=self.start_minute_choices)

        self.labelStartDate = wx.StaticText(self, -1, "  Start Date", style=wx.ALIGN_CENTRE)
        #self.labelStartTime = wx.StaticText(self, -1, "Start Time", style=wx.ALIGN_CENTRE)
        self.datepicker_start_date = wx.DatePickerCtrl(self, -1)
        self.datepicker_start_date.SetMinSize((115, 30))
        self.datepicker_start_date.SetToolTipString("Pick Start Date")

        self.choice_start_hour.SetToolTipString("Start hour, in 24-Hour format")
        self.choice_start_minute.SetToolTipString("Start minute")
        self.choice_end_hour.SetToolTipString("End hour, in 24-Hour format")
        self.choice_end_minute.SetToolTipString("End minute")

        self.labelEndDate = wx.StaticText(self, -1, "End Date", style=wx.ALIGN_CENTRE)
        self.datepicker_end_date = wx.DatePickerCtrl(self, -1)
        self.datepicker_end_date.SetMinSize((115, 30))
        self.datepicker_end_date.SetToolTipString("Pick end Date")
        self.buttonDatesChanged = wx.Button(self, -1, "Generate")
        #self.buttonRefresh = wx.Button(self, -1, "Refresh")
        self.buttonDatesChanged.SetToolTipString("Generate graph based on selected dates & time")
        #self.buttonRefresh.SetToolTipString("Refresh data/graph")
        #self.buttonDatesChanged.SetBackgroundColour(wx.Colour(159, 159, 95))
        self.labelStartTime = wx.StaticText(self, -1, "Time:", style=wx.ALIGN_CENTRE)
        self.labelEndTime = wx.StaticText(self, -1, "Time:", style=wx.ALIGN_CENTRE)

        self.radio_btn_inbound = wx.RadioButton(self, -1, "INBOUND")
        self.radio_btn_outbound = wx.RadioButton(self, -1, "OUTBOUND")
        self.radio_btn_outbound.SetToolTipString("Select for outbound traffic")
        self.radio_btn_inbound.SetToolTipString("Select for inbound traffic")
        self.radio_btn_inbound.SetForegroundColour(wx.Colour(50, 50, 204))
        self.radio_btn_outbound.SetForegroundColour(wx.Colour(35, 142, 35))
        sizer_radio_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_radio_buttons.Add(self.radio_btn_inbound, 0, 0, 0)
        sizer_radio_buttons.Add(self.radio_btn_outbound, 0, 0, 0)

        #self.start_hour =
        #print "parent = ", self.GetParent()

        self.choiceTimePeriod.SetMinSize((90, 31))
        self.choiceTimePeriod.SetSelection(0)           # Default is report last hour


        sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.static_line = wx.StaticLine(self, -1)
        #self.static_line.SetMinSize((1000, 10))
        self.static_line.SetBackgroundColour(wx.Colour(50, 153, 204))
        sizer_main.Add(self.static_line, 0, wx.EXPAND, 0)
        
       # do layout
        sizer_minor = wx.BoxSizer(wx.HORIZONTAL)
        sizer_minor.Add(self.choiceTimePeriod, 0, 0, 0)
        #sizer_minor.Add((30, 20), 0, 0, 0)
        sizer_minor.Add(sizer_radio_buttons, 0, 0, 0)
        sizer_minor.Add(self.labelStartDate, 0, 0, 0)
        sizer_minor.Add(self.datepicker_start_date, 0, 0, 0)
        sizer_minor.Add(self.labelStartTime, 0, 0, 0)
        sizer_minor.Add(self.choice_start_hour, 0, 0, 0)
        sizer_minor.Add(self.choice_start_minute, 0, 0, 0)
        sizer_minor.Add(self.labelEndDate, 0, 0, 0)
        sizer_minor.Add(self.datepicker_end_date, 0, 0, 0)
        sizer_minor.Add(self.labelEndTime, 0, 0, 0)
        sizer_minor.Add(self.choice_end_hour, 0, 0, 0)
        sizer_minor.Add(self.choice_end_minute, 0, 0, 0)
        
        sizer_minor.Add(self.buttonDatesChanged, 0, 0, 0)
        #sizer_minor.Add(self.buttonRefresh, 0, 0, 0)


        #sizer_minor.Fit(self)

        sizer_main.Add(sizer_minor, 0, 0, 0, wx.EXPAND)

        #self.start_date = self.datepicker_start_date.GetValue()
        self.start_date = ""
        self.end_date = self.datepicker_end_date.GetValue()

        #Event Handlers
        self.Bind(wx.EVT_CHOICE, self.eventTimeChoiceChanged, self.choiceTimePeriod)
        self.Bind(wx.EVT_BUTTON, self.eventDatesChanged, self.buttonDatesChanged)
        #self.Bind(wx.EVT_BUTTON, lambda evt, ants_start_date=self.start_date: self.eventDatesChanged(evt, ants_start_date))

        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()

    def GetStartDate(self):
        return self.start_date

    def eventTimeChoiceChanged(self, event):
        #print "Event handler `eventTimeChoiceChanged' Time selected = %s" % self.time_choices[self.choiceTimePeriod.GetSelection()]
        event.Skip()

    def eventDatesChanged(self, event):
        #print "time panel, parameter = ", ants_start_date
        self.start_date = self.datepicker_start_date.GetValue()
        self.end_date = self.datepicker_end_date.GetValue()
        #start_date = self.start_date
        pattern='%a %d %b %Y %H:%M:%S %Z'
        epoch_start = int(time.mktime(time.strptime(str(self.start_date), pattern)))
        epoch_end = int(time.mktime(time.strptime(str(self.end_date), pattern)))
        #print "Event handler `eventDatesChanged' start date = %s, epoch = %d" % (self.start_date, epoch_start)
        #print "Event handler `eventDatesChanged' end date = %s, epoch = %d" % (self.end_date, epoch_end)
        event.Skip()
        
        

