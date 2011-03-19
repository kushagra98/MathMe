#!/usr/bin/env python
#-*-coding: utf-8 -*-
# Copyright (C) 2011, Hiram Jeronimo Perez <worg@linuxmail.org>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
from gobject import timeout_add
import pango
import sqlite
from random import randint, randrange
from gettext import gettext as _

class Numbers:
    timeout  = 0
    hasOp    = True
    oldSign  = 0
    lifes    = 2
    animControl = 1
    
    def __init__(self, runAsLib = True):
        self.builder = gtk.Builder() 
        self.builder.add_from_file('num.ui')
        self.window = self.builder.get_object('numWindow')
        self.menuView = self.builder.get_object('menuView')
        self.lbTitle = self.builder.get_object('lbTitle')
        self.lbSubt  = self.builder.get_object('lbSubt')
        self.btnEasy = self.builder.get_object('btnEasy')
        self.btnHard = self.builder.get_object('btnHard')
        self.btnMed  = self.builder.get_object('btnMed')
        self.gameView = self.builder.get_object('gameView')
        self.lbNum1 = self.builder.get_object('lbNum1')
        self.lbNum2 = self.builder.get_object('lbNum2')
        self.lbSign = self.builder.get_object('lbSign')
        self.lbEqual = self.builder.get_object('lbEqual')
        self.txtRes = self.builder.get_object('txtRes')
        self.lbMsg  = self.builder.get_object('lbMsg')
        self.imgCheck  = self.builder.get_object('imgCheck')
        self.pBar = self.builder.get_object('progressBar')
        self.btnCalc = self.builder.get_object('btnCalc')
        self.btnNext = self.builder.get_object('btnNext')
        self.lifeBox = self.builder.get_object('lifeBox')
                
        self.widget = self.window.get_child()
        
        self.lbLife = [gtk.Label(), gtk.Label(), gtk.Label(), gtk.Label()]
        i = 0
        for label in self.lifeBox.get_children():
            self.lbLife[i] = label
            self.pangoLabel(self.lbLife[i], self.rgbToPango(153,84,244), 2)
            i += 1
                
        self.markMe(self.btnCalc)
        self.markMe(self.btnNext)
        self.pangoLabel(self.lbNum1, self.rgbToPango(29, 97, 252), 5)
        self.pangoLabel(self.lbNum2, self.rgbToPango(227, 126, 0), 5)
        self.pangoLabel(self.lbSign, self.rgbToPango(255,0,0), 5)
        self.pangoLabel(self.lbEqual, self.rgbToPango(145, 225, 36), 5)
        self.forceLocales()
        
        self.builder.connect_signals(self)
        
        if not runAsLib:
            self.window.show_all()
        
    def numbers_term(self, widget, data = 0):
        gtk.main_quit()
    
    def numbers_calcOp(self, widget):
        if not self.hasOp:
            self.lbMsg.set_label(' ')
            num1 = int(self.lbNum1.get_label())
            num2 = int(self.lbNum2.get_label())
            sign = self.lbSign.get_label()
            res = 0.0
            txRes = int(self.txtRes.get_text())
            
            if sign == '+':
                res = num1 + num2
            elif sign == '-':
                res = num1 - num2
            elif sign == '×':
                res = num1 * num2
            elif sign == '÷':
                res = num1 / num2
            
            if(txRes == res):
                self.sendMsg(True)
            else:
                self.sendMsg(False, res)
            self.btnNext.grab_focus()
    
    def numbers_oper(self, widget = gtk.Widget):
        self.imgCheck.clear()
        self.lbMsg.set_label('')
        num1 = randint(1,10)
        num2 = randrange(1,10)
        newSign = randint(1,4)
        sign = ''
        
        if self.lifes < 0 and self.hasOp:
            self.initLifes()
            
        
        while newSign == self.oldSign:
            newSign = randrange(1,4)
                    
        self.oldSign = newSign
            
        if newSign == 1:
            sign = '+'
        elif newSign == 2:
            sign = '-'
        elif newSign == 3:
            sign = '×'
        elif newSign == 4:
            sign = '÷'
            
        if(self.hasOp):
            if sign == '÷':
                while num1 % num2 != 0 or num1 == num2 or (num1 == 1 or num2 == 1):
                    num1 = randint(1,10)
                    num2 = randrange(1,10)
            elif sign == '-':
                while num1 < num2 or num1 == num2:
                    num1 = randint(1,10)
                    num2 = randrange(1,10)
            self.lbNum1.set_label(str(num1))
            self.lbNum2.set_label(str(num2))
            self.lbSign.set_label(sign)
            self.txtRes.set_text('')
            self.hasOp = False
        else:
            self.lbMsg.set_label('<span foreground = "white" background = "#095DF0" size = "x-large">  %s  </span>' % (_('Type the result, then press calculate')))
        self.txtRes.grab_focus()
        timeout_add(self.timeout,self.setProgress)
        
    def numbers_txtActivate(self, widget):
        if widget.get_text() != '':
                    self.btnCalc.grab_focus()
        
    def numbers_chDiff(self,action):
        actionN = action.get_name()
        if actionN == 'easy':            
            self.timeout  = 100
        elif actionN == 'medium':
            self.timeout  = 50
        elif actionN == 'hard':
            self.timeout  = 25
            
        self.gameView.show()
        self.menuView.hide()
        self.numbers_oper()
            
    def markMe(self, widget,data = 0):
        widgetLabel = widget.get_child() #153, 38, 244 RGB
        foreg = self.rgbToPango(153, 38, 244)
        self.pangoLabel(widgetLabel, foreg, 1.5)
            
    def sendMsg(self, isRight, res = 0):
        if isRight:
            self.lbMsg.set_label('<span foreground = "white" background = "#4DC406" size = "x-large">  %s  </span>' % (_('Great!')))
            self.imgCheck.set_from_file('icons/face-laugh.png')
        else:
            if(self.lifes < 0):
                self.lbMsg.set_label('<span foreground = "white" background = "purple" size = "x-large">  %s <b>%d  </b>, %s</span>' % (_('The result is:'), res, _('Game Over')))
            else:
                self.lbMsg.set_label('<span foreground = "white" background = "orange" size = "x-large">  %s <b>%d  </b></span>' % (_('The result is:'), res))
            self.imgCheck.set_from_file('icons/face-sad.png')
            self.lbLife[self.lifes].set_label(' ')
            self.lifes -= 1
            
        self.hasOp = True
    
    def setProgress(self):
        fraction = self.pBar.get_fraction()
        fraction += 0.01
        if not self.hasOp:
            if fraction < 1:
                self.pBar.set_fraction(fraction)
            else:
                if self.txtRes.get_text() == '':
                    self.txtRes.set_text('0')
                self.numbers_calcOp(self.btnCalc)
                self.pBar.set_fraction(0.0)
        else:
            self.pBar.set_fraction(0.0)
        
        return not self.hasOp
        
    def initLifes(self):
        i = 0
        while i < 3:
            self.lbLife[i].set_label('☺')
            i += 1
        self.gameView.hide()
        self.menuView.show()
        self.pBar.set_fraction(1)
        self.btnEasy.grab_focus()
        self.lifes = 3

    def forceLocales(self):
        #This nasty function is needed due to lack of doc of how-to localize a GtkBuilder activity
        lbTitle = self.builder.get_object('lbTitle')
        lbSubt  = self.builder.get_object('lbSubt')
        btnEasy = self.builder.get_object('btnEasy')
        btnHard = self.builder.get_object('btnHard')
        btnMed  = self.builder.get_object('btnMed')
         
        self.lbTitle.set_label(_('New Game'))
        self.pangoLabel(self.lbTitle,(0,0,0),3)
        self.lbSubt.set_label(_('Choose difficulty'))
        self.pangoLabel(self.lbSubt,(0,0,0),1.5)
        self.btnEasy.set_label(_('_Easy'))
        self.btnMed.set_label(_('_Medium'))
        self.btnHard.set_label(_('_Hard'))
        self.btnNext.set_label(_('_Next'))
        self.btnCalc.set_label(_('_Calculate'))
        
    def pangoLabel(self, label, fg, scale):
        atr = pango.AttrList()
        foreg = pango.AttrForeground(fg[0], fg[1], fg[2],0, 100) #153, 38, 244 RGB
        scale = pango.AttrScale(scale, 0, 100)
        atr.insert(foreg)
        atr.insert(scale)
        label.set_attributes(atr)
        
    def rgbToPango(self, r, g, b):
        r = (r * 65535)/255
        g = (g * 65535)/255
        b = (b * 65535)/255
        
        return (r,g,b)
            
if __name__ == '__main__':
        Numbers(False)
        gtk.main()
