# !/bin/python

import logging
import sys

import wx
import wx.dataview
import wx.lib.colourutils
from wx.dataview import *

from mvp.presenter import TcodeLitePresenter
from mvp.view import TcodeLiteView


class TcodeLiteInteractor(object):

    def __init__(self):
        logging.info('Initial TcodeLiteInteractor.')

    def install(self, presenter: TcodeLitePresenter, view: TcodeLiteView):
        logging.info('Install TcodeLiteInteractor.')

        self.p = presenter
        self.v = view

        self.v.Bind(wx.EVT_BUTTON, self.on_load_log, self.v.loadButton)
        self.v.Bind(wx.EVT_BUTTON, self.on_clean_log, self.v.cleanButton)

        self.v.Bind(wx.EVT_BUTTON, self.on_perform, self.v.performBtn)
        self.v.Bind(wx.EVT_BUTTON, self.on_choose_file, self.v.chooseFileBtn)
        self.v.Bind(wx.EVT_BUTTON, self.on_delete_tcode, self.v.deleteBtn)
        self.v.Bind(wx.EVT_BUTTON, self.on_reset, self.v.resetBtn)

        self.v.TCODE.Bind(wx.EVT_KEY_UP, self.on_search_by_tcode)
        self.v.TCODE_DESC.Bind(wx.EVT_KEY_UP, self.on_search)
        self.v.comments.Bind(wx.EVT_KEY_UP, self.on_search)
        self.v.favorite.Bind(wx.EVT_KEY_UP, self.on_search)

        self.v.Bind(EVT_DATAVIEW_SELECTION_CHANGED, self.on_table_item_selection_changed, self.v.table)

        # glbal exception hanlder.
        sys.excepthook = self.except_hook

    def except_hook(self, exctype, value, traceback):
        sys.__excepthook__(exctype, value, traceback)
        logging.error(f'{exctype} -~- {value}')
        self.p.on_load_log()

    def on_delete_tcode(self, evt):
        self.p.on_delete_tcode()

    def on_perform(self, evt):
        self.p.on_perform()

    def on_search(self, evt):
        self.p.on_search(evt,'other')
    def on_search_by_tcode(self, evt):
        self.p.on_search(evt, 'tcode')

    def on_reset(self, evt):
        self.p.on_reset()

    def on_choose_file(self, evt):
        self.p.on_choose_file()

    def on_load_log(self, evt):
        self.p.on_load_log()

    def on_clean_log(self, evt):
        self.p.on_clean_log()

    def on_exit(self, evt):
        self.p.on_exit()

    def on_table_item_selection_changed(self, evt):
        self.p.on_table_item_selection_changed(evt)
