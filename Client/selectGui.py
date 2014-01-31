# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Armoured Warfare", pos=wx.DefaultPosition,
                          size=wx.Size(400, 350), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.tankLab = wx.StaticText(self, wx.ID_ANY, u"Select a tank:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.tankLab.Wrap(-1)
        fgSizer1.Add(self.tankLab, 0, wx.ALL, 5)

        tankChoiceChoices = []
        self.tankChoice = wx.ComboBox(self, wx.ID_ANY, u"Select a tank", wx.DefaultPosition, wx.DefaultSize,
                                      tankChoiceChoices, 0)
        fgSizer1.Add(self.tankChoice, 0, wx.ALL, 5)

        self.statsLablab = wx.StaticText(self, wx.ID_ANY, u"Tank stats:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.statsLablab.Wrap(-1)
        fgSizer1.Add(self.statsLablab, 0, wx.ALL, 5)

        self.statsBox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, 150),
                                    wx.TE_MULTILINE | wx.TE_READONLY)
        fgSizer1.Add(self.statsBox, 0, wx.ALL, 5)

        self.serveLab = wx.StaticText(self, wx.ID_ANY, u"Server Address:Port:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.serveLab.Wrap(-1)
        fgSizer1.Add(self.serveLab, 0, wx.ALL, 5)

        self.AddressBox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        fgSizer1.Add(self.AddressBox, 0, wx.ALL, 5)

        self.goButton = wx.Button(self, wx.ID_ANY, u"Roll out!", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.goButton, 0, wx.ALL, 5)

        fgSizer1.AddSpacer(( 0, 0), 1, wx.EXPAND, 5)

        self.upgradeButton = wx.Button(self, wx.ID_ANY, u"Upgrade tank", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.upgradeButton, 0, wx.ALL, 5)

        self.m_button16 = wx.Button(self, wx.ID_ANY, u"Buy a tank", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_button16, 0, wx.ALL, 5)

        bSizer2.Add(fgSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.tankChoice.Bind(wx.EVT_COMBOBOX, self.doStats)
        self.AddressBox.Bind(wx.EVT_TEXT, self.setHost)
        self.AddressBox.Bind(wx.EVT_TEXT_ENTER, self.goToBattle)
        self.goButton.Bind(wx.EVT_BUTTON, self.goToBattle)
        self.upgradeButton.Bind(wx.EVT_BUTTON, self.doUpgrade)
        self.m_button16.Bind(wx.EVT_BUTTON, self.doBuy)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def doStats(self, event):
        event.Skip()

    def setHost(self, event):
        event.Skip()

    def goToBattle(self, event):
        event.Skip()


    def doUpgrade(self, event):
        event.Skip()

    def doBuy(self, event):
        event.Skip()


###########################################################################
## Class TankBuy
###########################################################################

class TankBuy(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Purchase a tank", pos=wx.DefaultPosition,
                          size=wx.Size(300, 200), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        fgSizer3 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText16 = wx.StaticText(self, wx.ID_ANY, u"XP To spend:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText16.Wrap(-1)
        fgSizer3.Add(self.m_staticText16, 0, wx.ALL, 5)

        self.xpBox = wx.TextCtrl(self, wx.ID_ANY, u"SELECT A TANK", wx.DefaultPosition, wx.Size(160, -1),
                                 wx.TE_READONLY)
        fgSizer3.Add(self.xpBox, 0, wx.ALL, 5)

        self.toBuy = wx.StaticText(self, wx.ID_ANY, u"Tank to buy:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.toBuy.Wrap(-1)
        fgSizer3.Add(self.toBuy, 0, wx.ALL, 5)

        TankBoxChoices = []
        self.TankBox = wx.ComboBox(self, wx.ID_ANY, u"Select a tank", wx.DefaultPosition, wx.DefaultSize,
                                   TankBoxChoices, 0)
        fgSizer3.Add(self.TankBox, 0, wx.ALL, 5)

        self.m_staticText18 = wx.StaticText(self, wx.ID_ANY, u"Price:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText18.Wrap(-1)
        fgSizer3.Add(self.m_staticText18, 0, wx.ALL, 5)

        self.priceBox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(160, -1),
                                    wx.TE_READONLY)
        fgSizer3.Add(self.priceBox, 0, wx.ALL, 5)

        self.buyB = wx.Button(self, wx.ID_ANY, u"Buy!", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer3.Add(self.buyB, 0, wx.ALL, 5)

        self.m_button18 = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size(160, -1), 0)
        fgSizer3.Add(self.m_button18, 0, wx.ALL, 5)

        self.SetSizer(fgSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.TankBox.Bind(wx.EVT_COMBOBOX, self.changeTankPrice)
        self.buyB.Bind(wx.EVT_BUTTON, self.buyTank)
        self.m_button18.Bind(wx.EVT_BUTTON, self.cancel)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def changeTankPrice(self, event):
        event.Skip()

    def buyTank(self, event):
        event.Skip()

    def cancel(self, event):
        event.Skip()


###########################################################################
## Class UpgradeForm
###########################################################################

class UpgradeForm(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Upgrade A Tank", pos=wx.DefaultPosition,
                          size=wx.Size(400, 420), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        fgSizer2 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.a = wx.StaticText(self, wx.ID_ANY, u"Upgrading Tank:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.a.Wrap(-1)
        fgSizer2.Add(self.a, 0, wx.ALL, 5)

        self.tankL = wx.StaticText(self, wx.ID_ANY, u"[Error]", wx.DefaultPosition, wx.DefaultSize, 0)
        self.tankL.Wrap(-1)
        fgSizer2.Add(self.tankL, 0, wx.ALL, 5)

        self.xpL = wx.StaticText(self, wx.ID_ANY, u"XP to spend: [ERROR]", wx.DefaultPosition, wx.DefaultSize, 0)
        self.xpL.Wrap(-1)
        fgSizer2.Add(self.xpL, 0, wx.ALL, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"Hit points:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)
        fgSizer2.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.curHP = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curHP, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button2, 0, wx.ALL, 5)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"Damage:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        fgSizer2.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.curDam = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curDam, 0, wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button3, 0, wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"Penetration:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        fgSizer2.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.curPen = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curPen, 0, wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button4, 0, wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"Reload:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        fgSizer2.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.curRel = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curRel, 0, wx.ALL, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button5, 0, wx.ALL, 5)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"Armour:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        fgSizer2.Add(self.m_staticText8, 0, wx.ALL, 5)

        self.curArm = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curArm, 0, wx.ALL, 5)

        self.m_button6 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button6, 0, wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"Hull Traverse:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        fgSizer2.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.curHTra = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curHTra, 0, wx.ALL, 5)

        self.m_button7 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button7, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"Turret Traverse:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        fgSizer2.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.curTTra = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curTTra, 0, wx.ALL, 5)

        self.m_button8 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button8, 0, wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"Speed:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        fgSizer2.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.curSpe = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        fgSizer2.Add(self.curSpe, 0, wx.ALL, 5)

        self.m_button9 = wx.Button(self, wx.ID_ANY, u"Upgrade", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button9, 0, wx.ALL, 5)

        self.Cancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.Cancel, 0, wx.ALL, 5)

        self.con = wx.Button(self, wx.ID_ANY, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.con, 0, wx.ALL, 5)

        self.SetSizer(fgSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.upHP)
        self.m_button3.Bind(wx.EVT_BUTTON, self.upDam)
        self.m_button4.Bind(wx.EVT_BUTTON, self.upPen)
        self.m_button5.Bind(wx.EVT_BUTTON, self.upRel)
        self.m_button6.Bind(wx.EVT_BUTTON, self.upArm)
        self.m_button7.Bind(wx.EVT_BUTTON, self.upHTr)
        self.m_button8.Bind(wx.EVT_BUTTON, self.upTTra)
        self.m_button9.Bind(wx.EVT_BUTTON, self.upSp)
        self.Cancel.Bind(wx.EVT_BUTTON, self.cancelEdit)
        self.con.Bind(wx.EVT_BUTTON, self.confirmEdit)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def upHP(self, event):
        event.Skip()

    def upDam(self, event):
        event.Skip()

    def upPen(self, event):
        event.Skip()

    def upRel(self, event):
        event.Skip()

    def upArm(self, event):
        event.Skip()

    def upHTr(self, event):
        event.Skip()

    def upTTra(self, event):
        event.Skip()

    def upSp(self, event):
        event.Skip()

    def cancelEdit(self, event):
        event.Skip()

    def confirmEdit(self, event):
        event.Skip()
	

