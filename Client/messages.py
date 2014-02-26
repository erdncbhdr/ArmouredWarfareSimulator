__author__ = 'harry'
import wx


def YesNo(parent, question, caption='Yes or no?'):
    """Brings up a simple yes or no dialog"""
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


def Info(parent, message, caption='Info'):
    """Brings up an information box"""
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


def Warn(parent, message, caption='Warning!'):
    """Brings up a warning box"""
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()
