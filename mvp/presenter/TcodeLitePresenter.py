# !/bin/python
import logging

import wx

from mvp.model import TcodeLiteModel
from mvp.presenter import TcodeLiteInteractor
from mvp.view import TcodeLiteView
from utils.DateUtil import DateUtil
from utils.ExcelUtil import ExcelUtil


class TcodeLitePresenter(object):

    def __init__(self, model: TcodeLiteModel, view: TcodeLiteView,
                 interactor: TcodeLiteInteractor) -> object:
        logging.info('Initial TcodeLitePresenter.')

        self.m = model
        self.v = view
        self.i = interactor
        self.i.install(self, view)

        # logging.info(inspect.getsource(TcodeNEWPresenter))

    def start_app(self):
        logging.info('TcodeLite is running now.')
        self.load_all_data_into_table()
        self.on_load_log()
        self.v.start()
        logging.info('TcodeLite is shutting down.\n\n')

    def load_data_into_table(self, data):
        self.v.table.DeleteAllItems()
        for idx, row in enumerate(data):
            self.v.table.AppendItem(row)

    def load_all_data_into_table(self):
        self.load_data_into_table(self.m.db.fetchAllTcode())

    def on_load_log(self):
        with open(ExcelUtil.get_log_file_path(self.m.logfilename), 'r', encoding='utf8') as file:
            self.v.logContents.SetValue(file.read())

        self.v.logContents.AppendText('')
        self.v.logContents.ScrollLines(-1)

    def on_clean_log(self):
        with open(ExcelUtil.get_log_file_path(self.m.logfilename), 'w', encoding='utf8') as file:
            file.write('Clean Tcode log@' + DateUtil.get_now_in_str() + '\n')
        self.on_load_log()

    def on_exit(self):
        self.v.Close(True)

    def on_perform(self):
        self.m.db.insertOrUpdateTcode(
            self.v.TCODE.GetValue(),
            self.v.TCODE_DESC.GetValue(),
            self.v.comments.GetValue(),
            self.v.favorite.GetValue()
        )
        self.load_all_data_into_table()
        self.on_load_log()

    def on_delete_tcode(self):
        tcode = self.v.TCODE.GetValue()
        self.m.db.deleteTcode(tcode)
        self.on_reset()

    def on_search(self, evt, source):
        tcode = self.v.TCODE.GetValue()
        if source == 'tcode' and evt.GetKeyCode() == wx.WXK_BACK and len(tcode) < 1:
            self.on_reset()
            return
        tcode_desc = self.v.TCODE_DESC.GetValue()
        comments = self.v.comments.GetValue()
        favorite = self.v.favorite.GetValue()

        if (len(tcode) > 0 or len(tcode_desc) > 0 or len(comments) > 0 or len(favorite) > 0):
            data = self.m.db.searchTcode(tcode, tcode_desc, comments, favorite, '500')
            self.load_data_into_table(data)
        else:
            self.load_all_data_into_table()

        self.on_load_log()
        evt.Skip()

    def on_reset(self):
        self.v.TCODE.ChangeValue('')
        self.v.TCODE_DESC.ChangeValue('')
        self.v.comments.ChangeValue('')
        self.v.favorite.ChangeValue('')

        self.load_all_data_into_table()
        self.on_load_log()

    def on_choose_file(self):
        logging.info('TcodeLite-> on_choose_file')

        with wx.FileDialog(self.v, "Load Excel", wildcard="excel files (*.xls)|*.xlsx",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            for pathname in fileDialog.GetPaths():

                logging.info(f'Load Excel from {pathname}')

                data = ExcelUtil.get_data_from_excel_file(pathname, 1, 16)
                logging.info(str(data))

                # 0 TCODE
                # 1 TCODE_DESC

                for idx, row in enumerate(data):
                    self.m.db.insertOrUpdateTcode(row[1], row[2])

        self.load_all_data_into_table()
        self.on_load_log()

    def on_table_item_selection_changed(self, evt):
        selectedRow = self.v.table.GetSelectedRow()
        if selectedRow != wx.NOT_FOUND:
            self.v.TCODE.ChangeValue(self.v.table.GetTextValue(selectedRow, 0))
            self.v.TCODE_DESC.ChangeValue(
                self.v.table.GetTextValue(selectedRow, 1))
            self.v.comments.ChangeValue(
                self.v.table.GetTextValue(selectedRow, 2))
            self.v.favorite.ChangeValue(
                self.v.table.GetTextValue(selectedRow, 3))
