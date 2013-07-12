import sys
import os
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.split(CURRENT_DIR)[0]
sys.path.append(BASE_DIR)
from gui.main import MainFrame
import wx

if __name__  == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
