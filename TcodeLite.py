# !/bin/python

import logging

import utils.Logger as Logger
from mvp.model.TcodeLiteModel import TcodeLiteModel
from mvp.presenter.TcodeLiteInteractor import TcodeLiteInteractor
from mvp.presenter.TcodeLitePresenter import TcodeLitePresenter
from mvp.view.TcodeLiteView import TcodeLiteView
from utils.DateUtil import DateUtil
from utils.SystemConfig import SystemConfig


def build_model():
    config = SystemConfig("/TcodeLiteConfig.yaml")
    model = TcodeLiteModel(config)
    return model


def init_logger():
    Logger.init('TcodeLite')

    logging.info("\n\n----system starting---->>>\n"
                 + "|  " + DateUtil.get_now_in_str("%Y-%m-%d %H:%M:%S") + "   |\n"
                 + "-----------------------<<<")


if __name__ == '__main__':
    init_logger()

    model = build_model()
    view = TcodeLiteView(model)
    presenter = TcodeLitePresenter(
        model, view, TcodeLiteInteractor())

    presenter.start_app()
