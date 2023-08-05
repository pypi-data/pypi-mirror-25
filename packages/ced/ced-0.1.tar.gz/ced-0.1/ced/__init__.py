import imp
import os

ced_module = imp.load_source("ced", os.path.join(os.path.dirname(__file__), "ced"))
