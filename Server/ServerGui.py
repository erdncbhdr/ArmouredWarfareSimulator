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
## Class Mainframe
###########################################################################

class Mainframe ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Armoured Warfare Server", pos = wx.DefaultPosition, size = wx.Size( 350,200 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.interLab = wx.StaticText( self, wx.ID_ANY, u"Interface:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.interLab.Wrap( -1 )
		fgSizer1.Add( self.interLab, 0, wx.ALL, 5 )
		
		interfaceChoiceChoices = [ u"No Interfaces" ]
		self.interfaceChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), interfaceChoiceChoices, 0 )
		self.interfaceChoice.SetSelection( 1 )
		fgSizer1.Add( self.interfaceChoice, 0, wx.ALL, 5 )
		
		self.ipLab = wx.StaticText( self, wx.ID_ANY, u"IP Address:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ipLab.Wrap( -1 )
		fgSizer1.Add( self.ipLab, 0, wx.ALL, 5 )
		
		self.ipBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer1.Add( self.ipBox, 0, wx.ALL, 5 )
		
		self.portLab = wx.StaticText( self, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.portLab.Wrap( -1 )
		fgSizer1.Add( self.portLab, 0, wx.ALL, 5 )
		
		self.portBox = wx.TextCtrl( self, wx.ID_ANY, u"9999", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.portBox, 0, wx.ALL, 5 )
		
		self.startServerButton = wx.Button( self, wx.ID_ANY, u"Start Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.startServerButton, 0, wx.ALL, 5 )
		
		self.stopServerButton = wx.Button( self, wx.ID_ANY, u"Stop Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.stopServerButton, 0, wx.ALL, 5 )
		
		self.statusLab = wx.StaticText( self, wx.ID_ANY, u"Server is not running.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.statusLab.Wrap( -1 )
		fgSizer1.Add( self.statusLab, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.interfaceChoice.Bind( wx.EVT_CHOICE, self.changeInterface )
		self.startServerButton.Bind( wx.EVT_BUTTON, self.startServer )
		self.stopServerButton.Bind( wx.EVT_BUTTON, self.stopServer )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def changeInterface( self, event ):
		event.Skip()
	
	def startServer( self, event ):
		event.Skip()
	
	def stopServer( self, event ):
		event.Skip()
	

###########################################################################
## Class FillerFrame
###########################################################################

class FillerFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 200,100 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.qwqq = wx.StaticText( self, wx.ID_ANY, u"There is a game in progress", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.qwqq.Wrap( -1 )
		bSizer2.Add( self.qwqq, 0, wx.ALL, 5 )
		
		self.stopGame = wx.Button( self, wx.ID_ANY, u"STOP THE GAME!!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.stopGame, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.stopGame.Bind( wx.EVT_BUTTON, self.stopEvent )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def stopEvent( self, event ):
		event.Skip()
	

