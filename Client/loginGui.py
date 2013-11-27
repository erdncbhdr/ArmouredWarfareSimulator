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

class MainFrame ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Super Secure Login", pos = wx.DefaultPosition, size = wx.Size( 300,190 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Username:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.userBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 130,-1 ), 0 )
		fgSizer1.Add( self.userBox, 0, wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.passBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 130,-1 ), wx.TE_PASSWORD|wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.passBox, 0, wx.ALL, 5 )
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Clear Fields", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_button1, 0, wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.Size( 130,-1 ), 0 )
		fgSizer1.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.createNew = wx.Button( self, wx.ID_ANY, u"Create an account", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.createNew, 0, wx.ALL, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.passBox.Bind( wx.EVT_TEXT_ENTER, self.suchSending )
		self.m_button1.Bind( wx.EVT_BUTTON, self.soClear )
		self.m_button2.Bind( wx.EVT_BUTTON, self.suchSending )
		self.createNew.Bind( wx.EVT_BUTTON, self.doCreate )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def suchSending( self, event ):
		event.Skip()
	
	def soClear( self, event ):
		event.Skip()
	
	
	def doCreate( self, event ):
		event.Skip()
	

###########################################################################
## Class newAccount
###########################################################################

class newAccount ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Create a new account", pos = wx.DefaultPosition, size = wx.Size( 350,170 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.inst = wx.StaticText( self, wx.ID_ANY, u"Please enter your details to create a new account.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.inst.Wrap( -1 )
		bSizer1.Add( self.inst, 0, wx.ALL, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.userL = wx.StaticText( self, wx.ID_ANY, u"New Username:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.userL.Wrap( -1 )
		fgSizer2.Add( self.userL, 0, wx.ALL, 5 )
		
		self.userBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer2.Add( self.userBox, 0, wx.ALL, 5 )
		
		self.passL = wx.StaticText( self, wx.ID_ANY, u"New Password:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.passL.Wrap( -1 )
		fgSizer2.Add( self.passL, 0, wx.ALL, 5 )
		
		self.passB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PASSWORD )
		fgSizer2.Add( self.passB, 0, wx.ALL, 5 )
		
		self.canB = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.canB, 0, wx.ALL, 5 )
		
		self.createB = wx.Button( self, wx.ID_ANY, u"Create Account", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.createB, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.canB.Bind( wx.EVT_BUTTON, self.cancelCreate )
		self.createB.Bind( wx.EVT_BUTTON, self.createAccount )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def cancelCreate( self, event ):
		event.Skip()
	
	def createAccount( self, event ):
		event.Skip()
	

