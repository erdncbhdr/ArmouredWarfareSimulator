__author__ = 'harry'
import wx


def YesNo(parent, question, caption='Yes or no?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


def ServerRun(parent):
    dlg = wx.MessageDialog(parent, "Server about to start. Press OK. (Window will crash)", "Server running",
                           wx.OK | wx.ICON_ASTERISK)
    dlg.ShowModal()
    dlg.Destroy()


def Info(parent, message, caption='Insert program title'):
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


def Warn(parent, message, caption='Warning!'):
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()