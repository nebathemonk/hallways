#   Programmer:  Christoph Zwerschke
#   E-mail:      cito@users.sourceforge.net
#
#   Copyright 2005 Christoph Zwerschke
#
# Distributed under the terms of the GPL (GNU Public License)
#
#    DrPython is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#Plugin
#ToDoList

#orgininal Version: Nathan Jones
#0.2.0 Christoph Zwerschke
#Updated for DrPython 1.65 and wxPython 2.8: FS

#Version: 0.2.1, 08.04.2007.
#Version: 0.2.2, 23.05.2007. Bug report and fix by Matthew Fremont
#[1723629 ] ToDoList plugin preferences fails with KeyError

import wx
import drPrefsFile

def OnAbout(DrFrame):
    DrFrame.ShowMessage('''ToDoList:
Version: 0.2.2

By Christoph Zwerschke

Based on the ToDo plugin by Nathan Jones

Released under the GPL.''',
    "About: ToDoList")

def OnHelp(DrFrame):
    DrFrame.ShowMessage('''A simple to do list.

Enter the word TODO in the code as a mark for a
to do task. Indicate priority by exclamation mark(s).

Open the ToDoList panel with "Toggle ToDo List" in
the View menu. Clicking an entry in the ToDoList panel
gets you quickly to the corresponding line in the code.

You can sort the tasks in the ToDoList panel by clicking on
the header. Tasks with highest priority are highlighted.
You can change this and other settings in the preferences.''',
    "Help: ToDoList")

class PrefsDialog(wx.Dialog):

    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, "Preferences: ToDoList")

        prefs = parent.ToDoList.prefs

        s = wx.BoxSizer(wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)

        s2 = wx.BoxSizer(wx.VERTICAL)

        w = wx.RadioBox(self, -1, "Panel Position:",
            wx.DefaultPosition, wx.DefaultSize,
            ["Left", "Right"], 2, wx.RA_SPECIFY_COLS | wx.NO_BORDER)
        w.SetSelection(prefs["position"])
        self.position = w
        s2.Add(w, 1, wx.EXPAND)

        w = wx.StaticBox(self, -1, "ToDo label:")
        s3 = wx.StaticBoxSizer(w, wx.VERTICAL)
        w = wx.TextCtrl(self, -1, "TODO", size=(40,-1))
        w.SetValue(prefs["label"])
        self.label = w
        s3.Add(w, 1, wx.EXPAND|wx.ALL, 4)
        w = wx.CheckBox(self, -1, "case sensitive")
        w.SetValue(prefs["Case"])
        self.case = w
        s3.Add(w, 0, wx.ALL, 4)
        s2.Add(s3)

        s1.Add(s2, 0, wx.ALL, 4)

        w = wx.StaticBox(self, -1, "Priority:")
        s2 = wx.StaticBoxSizer(w, wx.VERTICAL)
        w = wx.CheckBox(self, -1, "show")
        w.SetValue(prefs["ShowPrio"])
        self.showprio = w
        s2.Add(w, 0, wx.ALL, 4)
        w = wx.CheckBox(self, -1, "highlight top")
        w.SetValue(prefs["MarkPrio"])
        self.markprio = w
        s2.Add(w, 0, wx.ALL, 4)
        w = wx.CheckBox(self, -1, "order by")
        w.SetValue(prefs["SortPrio"])
        self.sortprio = w
        s2.Add(w, 0, wx.ALL, 4)

        s1.Add(s2, 0, wx.ALL, 4)

        s.Add(s1)

        w = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        s.Add(w, 0, wx.GROW|wx.ALL, 4)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        w = wx.Button(self, wx.ID_OK, " OK ")
        w.SetDefault()
        s1.Add(w, 0, wx.ALIGN_CENTRE|wx.ALL, 4)
        w = wx.Button(self, wx.ID_CANCEL, " Cancel ")
        s1.Add(w, 0, wx.ALIGN_CENTRE|wx.ALL, 4)
        s.Add(s1, 1, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetAutoLayout(True)
        self.SetSizer(s)
        s.Fit(self)

def OnPreferences(DrFrame):
    d = PrefsDialog(DrFrame, -1)
    if d.ShowModal() == wx.ID_OK:
        prefs = DrFrame.ToDoList.prefs
        prefs["position"] = int(d.position.GetSelection())
        prefs["label"] = d.label.GetValue()
        prefs["Case"] = int(d.case.GetValue())
        prefs["ShowPrio"] = int(d.showprio.GetValue())
        prefs["MarkPrio"] = int(d.markprio.GetValue())
        prefs["SortPrio"] = int(d.sortprio.GetValue())
        d.Destroy()
        DrFrame.ToDoList.writeprefs()
        panel = DrFrame.ToDoList.panel
        if panel:
            visible = DrFrame.mainpanel.IsVisible(panel.position, panel.Index)
            panel.Close()
            if visible: ToggleToDo(DrFrame)
    else:
        d.Destroy()

class ToDoPanel(wx.Panel):

    def __init__(self, parent, id,  Index):
        wx.Panel.__init__(self, parent, id)

        self.panelparent = parent.GetGrandParent().GetParent()
        self.parent = self.panelparent.GetParent()

        self.Index = Index
        for pref, value in self.parent.ToDoList.prefs.items():
            setattr(self, pref, value)

        self.ID_LIST = 11001
        self.ID_CLOSE = 11002
        self.ID_REFRESH = 11003

        s = wx.BoxSizer(wx.VERTICAL)

        w = wx.ListCtrl(self, self.ID_LIST,
            style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        w.InsertColumn(0, '', width=0)
        w.InsertColumn(1, "Line",
            format=wx.LIST_FORMAT_RIGHT, width=48)
        if self.ShowPrio:
            w.InsertColumn(2, '!',
            format=wx.LIST_FORMAT_CENTER, width=20)
            self.taskcol = 3
        else:
            self.taskcol = 2
        w.InsertColumn(self.taskcol, "Task",
            format=wx.LIST_FORMAT_LEFT, width=wx.LIST_AUTOSIZE)
        self.taskcolwidth = w.GetColumnWidth(self.taskcol)
        self.todolist = w
        s.Add(w, 1, wx.EXPAND)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        w = wx.Button(self, self.ID_REFRESH, "&Refresh")
        s1.Add(w, 0, wx.SHAPED | wx.ALIGN_LEFT)
        w = wx.Button(self, self.ID_CLOSE, "&Close")
        s1.Add(w, 0, wx.SHAPED | wx.ALIGN_RIGHT)
        s.Add(s1, 0, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=self.ID_CLOSE)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, id=self.ID_REFRESH)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, id=self.ID_LIST)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnRowClick, id=self.ID_LIST)
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnRowClick, id=self.ID_LIST)

        self.Browse()

        self.SetAutoLayout(True)
        self.SetSizer(s)

    def Browse(self):
        if self.Case:
            Label = self.label
        else:
            Label = self.label.upper()
        lenLabel = len(Label)
        self.tododata = [[], [], []]
        index = lineNum = maxprio = 0
        minprio = None
        for line in self.parent.txtDocument.GetText().splitlines():
            lineNum += 1
            if self.Case:
                Line = line
            else:
                Line = line.upper()
            i = Line.find(Label)
            if i < 0: continue
            i += lenLabel
            if Line[i:i+1] == ':': i += 1
            line = line[i:].strip()
            Line = line.upper()
            prio = Line.count("!")
            if prio > maxprio:
                maxprio = prio
            if minprio is None or prio < minprio:
                minprio = prio
            self.tododata[0].append(lineNum)
            self.tododata[1].append(-prio)
            self.tododata[2].append(Line)
            item = self.todolist.InsertStringItem(index, "")
            self.todolist.SetStringItem(index, 1, str(lineNum))
            if self.ShowPrio:
                self.todolist.SetStringItem(index, 2, str(prio))
            self.todolist.SetStringItem(index, self.taskcol, line)
            self.todolist.SetItemData(item, index)
            index += 1
        if self.MarkPrio and minprio is not None and maxprio > minprio:
            while index:
                index -= 1
                if self.tododata[1][index] == -maxprio:
                    item = self.todolist.GetItem(index)
                    item.SetBackgroundColour("YELLOW")
                    self.todolist.SetItem(item)
        if self.SortPrio: self.Sort(1)
        self.todolist.SetColumnWidth(self.taskcol, wx.LIST_AUTOSIZE)
        colwidth = self.todolist.GetColumnWidth(self.taskcol)
        if colwidth < self.taskcolwidth:
            self.todolist.SetColumnWidth(self.taskcol, self.taskcolwidth)

    def Close(self):
        self.parent.ToDoList.panel = None
        self.panelparent.ClosePanel(self.position, self.Index)

    def OnClose(self, event):
        self.Close()

    def Refresh(self):
        self.todolist.DeleteAllItems()
        self.Browse()

    def OnRefresh(self, event):
        self.Refresh()

    def Sort(self, col):
        def ListCompareFunction(item1, item2):
            return (cmp(self.tododata[col][item1],
                self.tododata[col][item2]) or cmp(item1, item2))
        self.todolist.SortItems(ListCompareFunction)

    def OnColClick(self, event):
        col = event.GetColumn()
        if col == self.taskcol: col = 3
        col -= 1
        self.Sort(col)

    def OnRowClick(self, event):
        index = event.GetIndex()
        lineNum = self.tododata[0][index] - 1
        parent = self.parent
        if parent.prefs.docfolding:
            parent.txtDocument.EnsureVisible(lineNum)
        parent.txtDocument.ScrollToLine(lineNum)
        parent.txtDocument.GotoLine(lineNum)
        parent.SetFocus()

def ToggleToDo(self):
    panel = self.ToDoList.panel
    if panel:
        if not self.mainpanel.IsVisible(panel.position, panel.Index):
            panel.Refresh()
        self.mainpanel.TogglePanel(panel.position, panel.Index)
    else:
        position = self.ToDoList.prefs["position"]
        target, Index = self.mainpanel.GetTargetNotebookPage(position, "ToDo List")
        panel = ToDoPanel(target, -1, Index)
        target.SetPanel(panel)
        self.mainpanel.ShowPanel(position, Index)
        self.ToDoList.panel = panel

class ToDoList:

    prefs = {
        "position": 1, # right panel
        "label": "TODO", # ToDo label
        "Case": 1, # case sensitive
        "ShowPrio": 1, # show priority
        "MarkPrio": 1, # highlight priority
        "SortPrio": 0 # order by priority
    }

    def __init__(self, prefsfile):
        self.prefsfile = prefsfile
        self.readprefs()
        self.panel = None

    def readprefs(self):
        try:
            text = open(self.prefsfile, 'r').read()
            for pref, value in self.prefs.items():
                self.prefs[pref] = drPrefsFile.GetPrefFromText(
                        value, text, pref, type(value)==type(1))
        except:
            pass

    def writeprefs(self):
        try:
            f = open(self.prefsfile, 'w')
            for pref, value in self.prefs.items():
                f.write("<%s>%s</%s>\n" % (pref, str(value), pref))
            f.close()
        except:
            pass

def Plugin(DrFrame):

    prefsfile = os.path.join(DrFrame.pluginspreferencesdirectory, "ToDoList.preferences.dat")
    DrFrame.ToDoList = ToDoList(prefsfile)

    def OnToggleToDo(event):
        ToggleToDo(DrFrame)

    #for testing purposes (reloading plugin)
    try:
        DrFrame.ToDoListLoadFlag
    except:
        DrFrame.ToDoListLoadFlag = 0
        DrFrame.LoadPluginShortcuts("ToDoList")

        ID_TOGGLE_TODO = DrFrame.GetNewId()
        DrFrame.viewmenu.AppendSeparator()
        DrFrame.viewmenu.Append(ID_TOGGLE_TODO, "Toggle ToDo List")
        DrFrame.Bind(wx.EVT_MENU, OnToggleToDo, id=ID_TOGGLE_TODO)

