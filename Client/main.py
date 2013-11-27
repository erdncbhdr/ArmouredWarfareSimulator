__author__ = 'harry'
import os
import sys

sys.path.append(os.getcwd())
import login


try:
    assert(os.winver)
    os = "windows"
    f = open("wx.pth", "w")
    f.write("wx-2.8-msw-unicode")
    f.close()

except AssertionError:
    os = "unix"
    f = open("wx.pth", "w")
    f.write("wx-2.8-gtk2-unicode")
    f.close()

if __name__ == "__main__":
    login.startLogin()