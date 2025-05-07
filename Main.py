#!/usr/bin/env python3

from GeckoModel import GeckoModel
from GeckoController import GeckoController
from GeckoView import GeckoView

gecko = GeckoModel
geckoView = GeckoView
geckoController = GeckoController(gecko, geckoView)

geckoController.startView()
