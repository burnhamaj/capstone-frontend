"""Subclass of _mainFrame, which is generated by wxFormBuilder."""

import wx
import _window
import cPickle

# Implementing _mainFrame
class _interface( _window._mainFrame ):
    def __init__( self, parent, lessonsManager ):
        _window._mainFrame.__init__( self, None )
        self.parent = parent
        self.lessonsManager = lessonsManager

        i = 1
        while(self.lessonsManager.Exists(i)):
            self.lessonsManager.ChangeLesson(i)
            lesson = wx.MenuItem( self.m_menu1, wx.ID_ANY, self.lessonsManager.GetName(), wx.EmptyString, wx.ITEM_NORMAL )
            self.LessonMenu.AppendItem( lesson )
            self.Bind( wx.EVT_MENU, lambda evt, temp=i: self.OnLessonClicked(evt, temp), id = lesson.GetId() )
            i += 1

        self.lessonsManager.ChangeLesson(1)
        self.ConfigureLesson()

    def OnPreviousButtonClicked( self, event ):
        self.lessonsManager.StoreCode(self.CodeBox.GetValue())
        self.lessonsManager.PreviousLesson()
        self.ConfigureLesson()

    def OnNextButtonClicked( self, event ):
        self.lessonsManager.StoreCode(self.CodeBox.GetValue())
        self.lessonsManager.NextLesson()
        self.ConfigureLesson()

    def ConfigureLesson( self ):
        self.CodeBox.SetValue(self.lessonsManager.LoadCode())
        self.LessonName.SetLabelText(self.lessonsManager.GetName())
        self.InstructionsWindow.SetPage(self.lessonsManager.GetInstructions(), "")
        self.StatusBar.SetStatusText("Ready")

    def OnOpenClicked( self, event):
        openFileDialog = wx.FileDialog(self, "Open blink file", "", "", "blink files (*.blink)|*.blink", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return

        try:
            f = open(openFileDialog.GetPath(),'r')
            self.lessonsManager.code = cPickle.loads(f.read())
            f.close()
        except:
            wx.LogError("Cannot open file '%s'."%openFileDialog.GetPath())
            self.StatusBar.SetStatusText("Failed To Open File...")
        finally:
            self.StatusBar.SetStatusText("Saved")
            self.ConfigureLesson()

    def OnSaveClicked( self, event ):
        if(self.lessonsManager.saveFilePath == None):
            return self.OnSaveAsClicked(None)

        try:
            f = open(self.lessonsManager.saveFilePath,'w')
            f.write(cPickle.dumps(self.lessonsManager.code))
            f.close()
        except:
            wx.LogError("Cannot save current contents in file '%s'."%self.lessonsManager.saveFilePath)
            self.StatusBar.SetStatusText("Save Failed... Please Try Again With A Differnt File Name")
        finally:
            self.StatusBar.SetStatusText("Saved")
            self.lessonsManager.modified = False

    def OnSaveAsClicked( self, event ):
        self.lessonsManager.StoreCode(self.CodeBox.GetValue())
        saveFileDialog = wx.FileDialog(self, "Save blink file", "", "", "blink files (*.blink)|*.blink", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return

        self.lessonsManager.saveFilePath = saveFileDialog.GetPath()
        self.OnSaveClicked(None)

    def OnStartShowClicked( self, event ):
        # TODO: Implement OnStartShowClicked
        pass

    def OnExitClicked( self, event ):
        self.Close()

    def OnRunProgramClicked( self, event ):
        self.parent.load(self.CodeBox.GetText())

    def OnLessonClicked( self, event, lesson ):
        self.lessonsManager.ChangeLesson(lesson)
        self.ConfigureLesson()

    def OnApplicationClosing( self, event ):
        if(self.lessonsManager.modified == True):
            dlg = wx.MessageDialog(self, 'You have unsaved work. Would you like to save your progress?', 'Save', wx.YES_NO | wx.ICON_QUESTION)
            dlg.Destroy()
            if(dlg.ShowModal() == wx.ID_YES):
                self.OnSaveClicked(None)
        event.Skip()

    def OnAboutClicked( self, event ):
        # TODO: Implement OnAboutClicked
        pass

    def OnCodeModified( self, event ):
        self.lessonsManager.modified = True

