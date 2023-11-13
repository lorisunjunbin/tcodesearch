# !/bin/python

import logging

import wx
import os
import wx.dataview
from wx.adv import TBI_DOCK

from utils.DateUtil import *


class TcodeLiteView(wx.Frame):

    def __init__(self, model):
        logging.info('Initial TcodeLiteView.')

        self.m = model

        self.app = wx.App(0)
        wx.Frame.__init__(self, None)
        self.SetTitle(self.m.title)
        self.SetIcon(wx.Icon(os.path.realpath('image') + '/TCode.ico'))
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.CreateStatusBar()
        self.make_action_panel()
        self.make_table()
        self.make_log_reader()
        self.border = wx.BoxSizer()

        self.border.Add(self.main_sizer, 800, wx.ALL, 0)
        self.SetSizerAndFit(self.border)
        self.SetStatusText(
            f"Wonderful day today, running @CW{str(DateUtil.get_week_num(DateUtil.get_now()))}-{DateUtil.get_now_in_str('%Y/%m/%d %H:%M:%S')}")
        _icon = wx.NullIcon
        _logo_path = os.path.realpath('image') + "/TCode.png"
        _icon.CopyFromBitmap(wx.Bitmap(_logo_path, wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        _tbiIcon = wx.adv.TaskBarIcon(iconType=TBI_DOCK)
        _tbiIcon.frame = self
        _tbiIcon.SetIcon(_icon, "TCode")

        self.tbicon = _tbiIcon

    def make_table(self):
        self.table = wx.dataview.DataViewListCtrl(
            self, wx.ID_ANY, size=(1000, 400))

        self.table.AppendTextColumn("TCODE", width=200)
        self.table.AppendTextColumn("TCODE_DESC", width=400)
        self.table.AppendTextColumn("comments", width=800)
        self.table.AppendTextColumn("favorite", width=100)

        self.main_sizer.Add(self.table, proportion=4,
                            flag=wx.EXPAND | wx.ALL, border=1)

    def make_action_panel(self):
        hbox = wx.BoxSizer()
        panel = wx.Panel(self)
        panel.SetSizer(hbox)

        self.chooseFileBtn = wx.Button(panel, label='import')
        self.performBtn = wx.Button(panel, label='Save')
        self.deleteBtn = wx.Button(panel, label='Delete')
        self.resetBtn = wx.Button(panel, label='Reset')

        self.TCODE = wx.TextCtrl(panel, size=[200, 22])
        self.TCODE.SetHint('TCODE')

        self.TCODE_DESC = wx.TextCtrl(panel, size=[200, 22])
        self.TCODE_DESC.SetHint('TCODE_DESC')

        self.comments = wx.TextCtrl(panel, size=[200, 22])
        self.comments.SetHint('comments')

        self.favorite = wx.TextCtrl(panel, size=[100, 22])
        self.favorite.SetHint('favorite')

        hbox.Add(self.TCODE, border=10)
        hbox.AddSpacer(5)
        hbox.Add(self.TCODE_DESC, border=10)

        hbox.AddSpacer(5)
        hbox.Add(self.comments, border=10)

        hbox.AddSpacer(5)
        hbox.Add(self.favorite, border=10)

        hbox.AddSpacer(10)
        hbox.Add(self.resetBtn, border=10)

        hbox.AddSpacer(10)
        hbox.Add(self.performBtn, border=10)

        hbox.AddSpacer(10)
        hbox.Add(self.chooseFileBtn, border=10)

        hbox.AddSpacer(10)
        hbox.Add(self.deleteBtn, border=10)

        self.main_sizer.Add(panel, flag=wx.EXPAND | wx.ALL, border=10)

    def make_log_reader(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        panel.SetSizer(vbox)
        # self.logContents = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL, size=(1000, 100))
        self.logContents = wx.TextCtrl(panel, wx.ID_ANY, "",
                                       style=wx.BORDER_NONE | wx.TE_DONTWRAP | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY)
        # self.logContents.SetBackgroundColour(wx.Colour(78, 78, 78))
        self.logContents.SetForegroundColour(wx.Colour(0, 255, 0))

        vbox.Add(self.logContents, proportion=2,
                 flag=wx.EXPAND | wx.ALL, border=0)

        hbox = wx.BoxSizer()
        panelBtn = wx.Panel(self)
        panelBtn.SetSizer(hbox)
        self.loadButton = wx.Button(panelBtn, label=' Reload ', size=(100, 40))
        self.cleanButton = wx.Button(panelBtn, label=' Clean ', size=(100, 40))
        hbox.AddSpacer(10)
        hbox.Add(self.loadButton, border=5)
        hbox.AddSpacer(10)
        hbox.Add(self.cleanButton, border=5)

        self.main_sizer.Add(panel, proportion=2,
                            flag=wx.EXPAND | wx.ALL, border=1)
        self.main_sizer.Add(panelBtn, flag=wx.EXPAND | wx.ALL, border=1)

    def start(self):
        self.Show()
        self.TCODE.SetFocus()
        self.CenterOnScreen()
        self.app.MainLoop()
