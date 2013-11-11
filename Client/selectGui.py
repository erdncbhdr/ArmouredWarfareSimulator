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

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Armoured Warfare", pos = wx.DefaultPosition, size = wx.Size( 400,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.tankLab = wx.StaticText( self, wx.ID_ANY, u"Select a tank:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tankLab.Wrap( -1 )
		fgSizer1.Add( self.tankLab, 0, wx.ALL, 5 )
		
		tankChoiceChoices = []
		self.tankChoice = wx.ComboBox( self, wx.ID_ANY, u"Select a tank", wx.DefaultPosition, wx.DefaultSize, tankChoiceChoices, 0 )
		fgSizer1.Add( self.tankChoice, 0, wx.ALL, 5 )
		
		self.statsLablab = wx.StaticText( self, wx.ID_ANY, u"Tank stats:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.statsLablab.Wrap( -1 )
		fgSizer1.Add( self.statsLablab, 0, wx.ALL, 5 )
		
		self.statsBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,150 ), wx.TE_MULTILINE )
		fgSizer1.Add( self.statsBox, 0, wx.ALL, 5 )
		
		self.serveLab = wx.StaticText( self, wx.ID_ANY, u"Server Address:Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.serveLab.Wrap( -1 )
		fgSizer1.Add( self.serveLab, 0, wx.ALL, 5 )
		
		self.AddressBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer1.Add( self.AddressBox, 0, wx.ALL, 5 )
		
		self.goButton = wx.Button( self, wx.ID_ANY, u"Roll out!", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.goButton, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.tankChoice.Bind( wx.EVT_COMBOBOX, self.doStats )
		self.AddressBox.Bind( wx.EVT_TEXT, self.setHost )
		self.goButton.Bind( wx.EVT_BUTTON, self.goToBattle )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def doStats( self, event ):
		event.Skip()
	
	def setHost( self, event ):
		event.Skip()
	
	def goToBattle( self, event ):
		event.Skip()
	

