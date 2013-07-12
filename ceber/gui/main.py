import os
import matplotlib
import wx
import wx.grid as gridlib
import wx.lib.agw.aui as aui
import wx.lib.scrolledpanel as scrolled
import wx.lib.agw.advancedsplash as AS
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from data import data
from calculations import expt

ID_MainToolBar_file = wx.NewId()
ID_MainToolBar_save = wx.NewId()
ID_MainToolBar_open = wx.NewId()
ID_Button_Expt_Run  = wx.NewId()
ID_Choice_Expt_Run  = wx.NewId()
ID_FinalFerric_calc = wx.NewId()
ID_Absorbance_calc  = wx.NewId()
ID_help_menu        = wx.NewId()
ID_About            = wx.NewId()

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.split(CURRENT_DIR)[0]

# PATHS
IMAGE_PATH = os.path.join(BASE_DIR, "images")

frame = wx.Frame

class MainFrame(frame):
    """
        CLASS WHERE THE MAIN APP IS DISPLAYED FROM

        FUNCTIONS:
            __init__ (self, parent, if, dpi)
            {constructor that initiates the plot}
                -> self._mgr    = aui.AuiManager()
                -> self.CreateSplashScreen()
                -> self.CreateStatusBar()
                -> self.BuildPanes()
                -> self.BindEvents()

            BuildPanes (self) -> __init__()
            {function that builds the panes for the managed window}
                -> self.CreateNotebookPlot()
                -> self.CreateExptSideMenu()
                -> self.CreateModelSideMenu()
                -> self.CreateBioleachSideMenu()
                -> self.CreateDataOutputPane()

            BindEvents() -> __init__()
    """
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="Data Plotting", size=(1000, 700))
        self._mgr   = aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        #~ Setting the page Icon
        #~ self.SetIcon(images.Mondrian.GetIcon())
        #~ self.SetIcon("logo.ICO")

        self.CreateSplashScreen()

        LOGO_PATH = os.path.join(IMAGE_PATH, "logo.ico")
        pic = wx.Icon(LOGO_PATH, wx.BITMAP_TYPE_ICO)
        self.SetIcon(pic)

        #~ Set Up Default Notebook Styles
        self._notebook_style    = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme    = 0

        #~ Creating The Status Bar
        self.CreateStatusBar()
        self.GetStatusBar().SetStatusText("Ready")
        self.CreateTopMenu()
        self.BuildPanes()
        self.BindEvents()

    def BuildPanes(self):
        self.SetMinSize(wx.Size(400, 300))
        """
            Creating The Datadisplay Pane for the Bottom
        """
        #~ The Main Note Book Page
        (self._mgr.AddPane(self.CreateNotebookPlot(),
                           aui.AuiPaneInfo().
                           Name("notebook_content").
                           CenterPane().
                           PaneBorder(True).
                           Floatable(False)))

        #~ The Side Panel for the Notebooks
        (self._mgr.AddPane(self.CreateExptSideMenu(),
                           aui.AuiPaneInfo().
                           Name("ExptSideMenu").
                           BestSize(wx.Size(250, 50)).
                           MinSize(wx.Size(250,50)).
                           Caption("Experiment Results").
                           Layer(2).Position(0).Left().
                           MinimizeButton(False).
                           MaximizeButton(False).
                           CloseButton(False).
                           RightDockable(True).
                           Floatable(False).
                           PaneBorder(False)))

        (self._mgr.AddPane(self.CreateModelSideMenu(),
                           aui.AuiPaneInfo().
                           Name("ModelSideMenu").
                           BestSize(wx.Size(250, 300)).
                           MinSize(wx.Size(250, 300)).
                           Caption("Modelling").
                           Layer(2).
                           Position(1).
                           Left().
                           MinimizeButton(False).
                           MaximizeButton(False).
                           CloseButton(False).
                           RightDockable(True).
                           Floatable(False).
                           PaneBorder(False)))

        (self._mgr.AddPane(self.CreateBioleachSideMenu(),
                           aui.AuiPaneInfo().
                           Name("BioleachSideMenu").
                           BestSize(wx.Size(250, 100)).
                           MinSize(wx.Size(250, 100)).
                           Caption("Bioleaching").
                           Layer(2).
                           Position(2).
                           Left().
                           MinimizeButton(False).
                           MaximizeButton(False).
                           CloseButton(False).
                           RightDockable(True).
                           Floatable(False).
                           PaneBorder(False)))

        #~ The DataOutput Pane
        (self._mgr.AddPane(self.CreateDataOutputPane(),
                           aui.AuiPaneInfo().
                           Name("OutputData").
                           Caption("Output Data").
                           Layer(1).
                           Position(1).
                           Bottom().
                           MinimizeButton(True).
                           MaximizeButton(True).
                           CloseButton(False).
                           BottomDockable(True).
                           Floatable(False)))

        self._mgr.Update()

    """
        ====================================================================================================
            BINDING EVENTS
        ====================================================================================================
    """



    def BindEvents(self):
        #~ Menu Events
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)

        #~ Expt Menu Events
        self.Bind(wx.EVT_BUTTON, self.RunExpt, id = ID_Button_Expt_Run)
        self.Bind(wx.EVT_CHOICE, self.SetExptChoiceValue, id = ID_Choice_Expt_Run)

    """
                                    END OF BINDING EVENTS
        ====================================================================================================
    """

    """
        ====================================================================================================
                                    CREATING MENUS, WIDGETS AND WXPANES
        ====================================================================================================
    """
    def CreateTopMenu(self):
        menubar     = wx.MenuBar()

        #~ Creating The File Button
        file_menu   = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")

        #~ Creating the Calculate Menu
        calc_menu   = wx.Menu()
        calc_menu.Append(ID_FinalFerric_calc, "Final Ferric Conc")
        calc_menu.Append(ID_Absorbance_calc, "Absorbance")

        help_menu   = wx.Menu()
        help_menu.Append(ID_help_menu, "Help")
        help_menu.Append(ID_About, "About")

        menubar.Append(file_menu, "File")
        menubar.Append(calc_menu, "Calculate")
        menubar.Append(help_menu, "Help")

        self.SetMenuBar(menubar)


    #~ CREATING THE EXPERIMENT PLOTTING side menu
    def CreateExptSideMenu(self):
        sidepanel = scrolled.ScrolledPanel(self,
                                           -1,
                                           size=wx.Size(200, 200),
                                           style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER,
                                           name="Exptsidepanel")

        bagSizer = wx.GridBagSizer(5, 5)
        topSizer = wx.BoxSizer(wx.VERTICAL)

        choice_list = data.run_keys()
        choice_list.sort()

        self.choice_1 = wx.Choice(sidepanel,
                                  ID_Choice_Expt_Run,
                                  size=(60, 25),
                                  choices = choice_list)

        self.button_expt_run = wx.Button(sidepanel,
                                         ID_Button_Expt_Run,
                                         "Calculate", (60, 25))

        self.cb_Expt_1 = wx.CheckBox(sidepanel, -1, 'Single Cu')
        self.cb_Expt_2 = wx.CheckBox(sidepanel, -1, 'All Cu')
        self.cb_Expt_3 = wx.CheckBox(sidepanel, -1, 'Single Fe')
        self.cb_Expt_4 = wx.CheckBox(sidepanel, -1, 'All Fe')
        self.cb_Expt_5 = wx.CheckBox(sidepanel, -1, 'Eh')
        self.cb_Expt_6 = wx.CheckBox(sidepanel, -1, 'pH')
        self.cb_Expt_7 = wx.CheckBox(sidepanel, -1, 'Rates')

        self.cb_Expt_2.SetValue(True)
        self.cb_Expt_4.SetValue(True)

        bagSizer.Add(self.choice_1,pos=(0, 0), flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(self.button_expt_run, pos=(0, 1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        bagSizer.Add(self.cb_Expt_1, pos=(1, 0), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(self.cb_Expt_2, pos=(1, 1), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bagSizer.Add(self.cb_Expt_3, pos=(2, 0), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(self.cb_Expt_4, pos=(2, 1), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bagSizer.Add(self.cb_Expt_5, pos=(3, 0), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(self.cb_Expt_6, pos=(3, 1), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bagSizer.Add(self.cb_Expt_7, pos=(4, 0), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        topSizer.Add(bagSizer, 0, wx.ALL | wx.EXPAND, 5)
        sidepanel.SetSizer(topSizer)

        sidepanel.SetAutoLayout(1)
        sidepanel.SetupScrolling()

        return sidepanel

    #~ CREATING THE MODELING side menu

    def CreateModelSideMenu(self):
        modelsidepanel = scrolled.ScrolledPanel(self,
                                                -1,
                                                size = wx.Size(200, 200),
                                                style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER,
                                                name="modelsidepanel")
        sizer   = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        list_1  = ['Chemical Leach', 'Bacteria Growth', 'Both']

        #~ Creating the BagSizer
        bagSizer    = wx.GridBagSizer(5, 5)

        #~ Creating The Model Interaction Widget
        text1           = wx.StaticText(modelsidepanel, label="Choose the Model To Run")
        choice_m_1      = wx.Choice(modelsidepanel, -1, size = (150, 25), choices = list_1)

        #~ Placing the Model interaction widget on the window
        bagSizer.Add(text1, pos=(0,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(choice_m_1, pos=(1,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        #~ Creating The Metals Check Box
        text2 = wx.StaticText(modelsidepanel, label="Choose To Metal(s) to Model")

        cb_Cu = wx.CheckBox(modelsidepanel, -1, 'Cu')
        cb_Zn = wx.CheckBox(modelsidepanel, -1, 'Zn')
        cb_Pb = wx.CheckBox(modelsidepanel, -1, 'Pb')
        cb_Al = wx.CheckBox(modelsidepanel, -1, 'Al')
        cb_Sn = wx.CheckBox(modelsidepanel, -1, 'Sn')
        cb_Fe = wx.CheckBox(modelsidepanel, -1, 'Fe')

        #~ Placing the Metals checkbox widgets on the pane using the grid bag sizer
        bagSizer.Add(text2, pos=(2, 0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bagSizer.Add(cb_Cu, pos=(3, 0), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(cb_Zn, pos=(3, 1), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(cb_Pb, pos=(3, 2), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bagSizer.Add(cb_Al, pos=(4, 0), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(cb_Sn, pos=(4, 1), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(cb_Fe, pos=(4, 2), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        #~ Creating Bacterial Species for Bacterial Growth Rate
        list_2      = ['Acidiothiobacillus Ferrooxidaans', 'Leptospirillum Ferriphillum', 'Both']

        text_3 = wx.StaticText(modelsidepanel, label="Choose Bacterial Species To Model")
        choice_2 = wx.Choice(modelsidepanel, -1, size = (150, 25), choices = list_2)

        text_4 = wx.StaticText(modelsidepanel, label="Choose Ratio in % of AtF : Lf")
        spinc = wx.SpinCtrl(modelsidepanel, -1, "", (30, 50))
        spinc.SetRange(0,100)
        spinc.SetValue(0)

        textbox_1 = wx.StaticText(modelsidepanel, -1, "This will will Contain Updated val", wx.DefaultPosition)

        bagSizer.Add(text_3, pos=(5,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(choice_2, pos=(6,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bagSizer.Add(text_4, pos=(7,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(spinc, pos=(8,0), span=(1, 2), flag =  wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(wx.StaticText(modelsidepanel, -1, "% Atf", wx.DefaultPosition), pos=(8,2), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(textbox_1, pos=(9,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        #~ Create Run Model Button
        button  = wx.Button(modelsidepanel, -1, "Run Model", (60, 25))
        bagSizer.Add(button, pos=(10,0), span=(1, 3), flag = wx.EXPAND | wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        #~ Adding the widgets to the panel using the SetSizer Method
        modelsidepanel.SetSizer(bagSizer)
        modelsidepanel.SetAutoLayout(1)
        modelsidepanel.SetupScrolling()

        return modelsidepanel

     #~ CREATING THE BIOLEACH MENU, purpose is to model heap leaching data

    def CreateBioleachSideMenu(self):
        """
            (wx.Frame) -> Panel Object
            Creates the Bioleach Side Menu
        """
        bioleachsidepanel = scrolled.ScrolledPanel(self, -1, size = wx.Size(200,200), style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER, name="modelsidepanel")
        sizer = wx.BoxSizer(wx.VERTICAL)

        list_1 = ['Ferrous Sulphate', 'Pyrite', 'Chalcopyrite']
        list_2 = ['Acidiothiobacillus Ferrooxidaans', 'Leptospirillum Ferriphillum', 'Both']

        #~ Creating the BagSizer
        bagSizer    = wx.GridBagSizer(5, 5)

        #~ Creating The Model Interaction Widget
        text1           = wx.StaticText(bioleachsidepanel, label="Choose the Bioleach System")
        choice_m_1      = wx.Choice(bioleachsidepanel, -1, size = (150, 25), choices = list_1)

        #~ Placing the Model interaction widget on the window
        bagSizer.Add(text1, pos=(0,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(choice_m_1, pos=(1,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)


        text_3      = wx.StaticText(bioleachsidepanel, label="Choose Bacterial Species To Model")
        choice_2    = wx.Choice(bioleachsidepanel, -1, size = (150, 25), choices = list_2)

        text_4      = wx.StaticText(bioleachsidepanel, label="Choose Ratio in % of AtF : Lf")
        spinc = wx.SpinCtrl(bioleachsidepanel, -1, "", (30, 50))
        spinc.SetRange(0,100)
        spinc.SetValue(0)

        textbox_1   = wx.StaticText(bioleachsidepanel, -1, "This will will Contain Updated val", wx.DefaultPosition)

        bagSizer.Add(text_3, pos=(2,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(choice_2, pos=(3,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bagSizer.Add(text_4, pos=(4,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(spinc, pos=(5,0), span=(1, 2), flag =  wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(wx.StaticText(bioleachsidepanel, -1, "% Atf", wx.DefaultPosition), pos=(5,2), flag = wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border = 10)
        bagSizer.Add(textbox_1, pos=(6,0), span=(1, 3), flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        #~ Create Run Model Button
        button  = wx.Button(bioleachsidepanel, -1, "Run Model", (60, 25))
        bagSizer.Add(button, pos=(7,0), span=(1, 3), flag = wx.EXPAND | wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 10)

        bioleachsidepanel.SetSizer(bagSizer)
        bioleachsidepanel.SetAutoLayout(1)
        bioleachsidepanel.SetupScrolling()
        return bioleachsidepanel

    #~ CREATING NEW INSTANCE OF NOTEBOOK, purpose is to add to pane

    def CreateNotebookPlot(self):
        """ self -> notebook object

        Returns a notebook object that is attached to panel by self._mgr and has name notebook_content
        """
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0
        client_size = self.GetClientSize()

        self.newtab = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y), wx.Size(430, 200), agwStyle = self._notebook_style)
        arts = [aui.AuiDefaultTabArt, aui.AuiSimpleTabArt, aui.VC71TabArt, aui.FF2TabArt, aui.VC8TabArt, aui.ChromeTabArt]
        art = arts[len(arts)-1]()
        self.newtab.SetArtProvider(art)

        self.page_bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.newtab, 1, wx.EXPAND)
        self.SetSizer(sizer)

        return self.newtab

    #~ CREATING THE DATA OUTPUT PANE AT THE BOTTOM OF THE WINDOW

    def CreateDataOutputPane(self):
        panel   = scrolled.ScrolledPanel(self,
                                         -1,
                                         wx.Point(0, 0),
                                         wx.Size(20, 100))

        panel.SetAutoLayout(1)
        panel.SetupScrolling()
        return panel

    #~ CREATING THE SPLASH SCREEN BUT SHOULD PROBABLY BE CREATED OUTSIDE THE DOCUMENT

    def CreateSplashScreen(self):
        #~ bitmap = wx.Bitmap("logo.PNG", wx.BITMAP_TYPE_PNG)

        BITMAP_PATH = os.path.join(IMAGE_PATH, "CeBER.jpg")
        bitmap = wx.Bitmap(BITMAP_PATH, wx.BITMAP_TYPE_JPEG)
        shadow = wx.BLACK

        frame = AS.AdvancedSplash(self, bitmap=bitmap, timeout=1000,
                              agwStyle=AS.AS_TIMEOUT |
                              AS.AS_CENTER_ON_PARENT |
                              AS.AS_SHADOW_BITMAP,
                              shadowcolour=shadow)

    """
                                    END OF CREATE WIDGETS AND PANES
        ====================================================================================================
    """

    """
        ====================================================================================================
        DIFFERENT SET AND GET METHODS
        ====================================================================================================
    """
    def SetExptChoiceValue(self, event):
        self.Exptvalue = float(event.GetString())

    def GetExptChoiceValue(self):
        return self.Exptvalue

    """
                                    END OF SET AND GET METHODS
        ====================================================================================================
    """

    """
        ====================================================================================================
            THE BIND EVENTS FUNCTIONS
        ====================================================================================================
    """

    def RunExpt(self, event):
        """ (wx.Frame, event [that has been handled]) -> Null

        The function is called by event [wx.EVT_BUTTON] with ID = [ID_Button_Expt_Run],
        calls 4 functions which:
            1) cause the program to delete tabs from notebook object,
            2) create a new notebook object and populates it
            3) deletes and updates content for the DataPane display at the bottom
            4) Updates the windows after all the changes have been made
        """
        self.DeletePages()
        self.UpdateNotebook()
        self.UpdateDataPane()
        self.DoUpdate()

    def OnExit(self, event):
        self.Close()

    def OnAbout(self, event):
        msg = "E-waste modelling Unit \n" + \
              "Trying to make the world a better place \n"
        dlg = wx.MessageDialog(self, msg, "About wx.aui Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    """
                                    END OF BOUND EVENTS
        ====================================================================================================
    """

    """
        ====================================================================================================
            RUN EXPT FUNCTIONS
        ====================================================================================================
    """

    def DeletePages(self):
        """(wx.Frame) -> null

        Deletes all the pages of the notebook
        """
        auinotebook = self._mgr.GetPane("notebook_content").window
        for pages in range (auinotebook.GetPageCount()):
            auinotebook.DeletePage(0)

    def UpdateNotebook(self):
        """
        auinotebook = self._mgr.GetPane("notebook_content").window
        Include the Code Below to Nest Pages
        auinotebook.AddPage(self.CreateNotebookPlot(), "")
        """

        self.ExptRun(run=self.GetExptChoiceValue())

        self.KeyShow()

        if self.cb_Expt_1.IsChecked():
            self.CopperShow()

        if self.cb_Expt_2.IsChecked():
            self.CopperShowAll()

        if self.cb_Expt_3.IsChecked():
            self.IronShow()

        if self.cb_Expt_4.IsChecked():
            self.IronShowAll()

    """
        Function that updates the data pane by getting all the children, deleting them and updating the data
        This function is called by RunExpt() from bound event with id = ID_Button_Expt_Run
    """
    def UpdateDataPane(self):
        datapane    = self._mgr.GetPane("OutputData").window
        datapane.DestroyChildren()

        # if datapane.GetChildren():
        #     print "I have children"
            #~ for child in datapane.GetChildren():
                #~ child.DestroyChildren()


        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.DataArrayToGrid(datapane)
        sizer   = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.DataArrayToGrid(datapane), 1, wx.EXPAND, 5)
        datapane.SetSizer(sizer)

    def DoUpdate(self):
        self._mgr.Update()
        self.Refresh()

    def ExptRun(self, run=None):
        self.plot_data = expt.Data(run = run)
        self.iron_conc = self.plot_data.iron_conc()
        self.copper_conc = self.plot_data.copper_conc()
        self.raw_data = self.plot_data.GetRawIronData()


    """
                                    END OF RUN EXPERIMENTS
        ====================================================================================================
    """

    """
        PUTTING THE DATA INTO DICTIONARIES FOR DISPLAY
        will do this in a new class
    """

    def GetDataArrayColumns(self):
        return len(self.DataDictToArray())

    def GetDataArrayRows(self):
        return len(self.DataDictToArray()[0])

    def DataArrayToGrid(self, parent):
        grid = gridlib.Grid(parent)
        grid.CreateGrid(25, 25)
        grid.EnableEditing(False)
        grid.SetRowLabelSize(0)
        grid.SetColLabelSize(0)

        data_str    = 'The Run is ' + str(self.plot_data.GetExptRun()) + "\n"
        grid.SetCellValue(0,0, data_str)

        i = 0
        for item_array in self.DataDictToArray():
            j = 1
            for item in item_array:
                if isinstance(item, (float)):
                    item = "%.3f" % item

                grid.SetCellValue(j,i, str(item))
                grid.SetReadOnly(j,i, True)
                j += 1
            i += 1
        return grid

    """
        Creating a Function that gathers all the data to a [[], []] array for out put purposes
    """
    def DataDictToArray(self):
        data_array  = []

        for dict_key in self.raw_data:
            data_array.append("%s g / L" % dict_key)
            #~ Parsing the Raw Data
            self.raw_data[dict_key][0].insert(0, "Time (Min)")
            self.raw_data[dict_key][1].insert(0, "Fe3+ Abs")
            self.raw_data[dict_key][2].insert(0, "FeTot Abs")

            for item in self.raw_data[dict_key]:
                data_array.append(item)

            #~ Parsing the Iron Concentration
            self.iron_conc[dict_key][0].insert(0, "Time (Min)")
            self.iron_conc[dict_key][1].insert(0, "Fe3+ (g/l)")
            self.iron_conc[dict_key][2].insert(0, "FeTot (g/ls)")

            for item in self.iron_conc[dict_key]:
                if item not in data_array:
                    data_array.append(item)

            #~ Parsing the Copper Concentration
            """
                copper_conc[dict_key][0] shares the same memory location as raw_data[dict_key][0].
            """
            self.copper_conc[dict_key][1].insert(0, "Copper (g/L)")

            for item in self.copper_conc[dict_key]:
                if item not in data_array:
                    data_array.append(item)

        return data_array

    """
        SETTING THE DATA TO BE PLOTTED (ideally need to do this in a different class but don't know how to)
    """

    def CopperShow(self):
        for k in self.copper_conc:
            figure = self.Add('Copper_data ' + str(k) + 'g/L').gca(ylabel="Copper conc in g", xlabel="Time (min)")
            figure.plot(self.copper_conc[k][0], self.copper_conc[k][1], '-x', label=str(k)+"g/L")
            figure.legend(loc="lower center", bbox_to_anchor=(0.5, 0), ncol=2, fancybox=True, shadow=True)

    def CopperShowAll(self):
        figure = self.Add('Show All Copper Data').gca(ylabel="Copper conc in g", xlabel="Time (min)")
        for k in self.copper_conc:
            figure.plot(self.copper_conc[k][0], self.copper_conc[k][1], '-x', label=str(k)+"g/L Copper")
            figure.legend(loc="lower center", bbox_to_anchor=(0.5, 0), ncol=2, fancybox=True, shadow=True)

    def IronShow(self):
        for k in self.iron_conc:
            figure = self.Add('Iron_data ' + str(k) + 'g/L').gca(ylabel = "iron conc in g", xlabel = "Time (min)")
            figure.plot(self.iron_conc[k][0], self.iron_conc[k][1], '-x', label=str(k)+"g/L Fe2+")
            figure.plot(self.iron_conc[k][0], self.iron_conc[k][2], '-x', label=str(k)+"g/L Fe3+")
            figure.legend(['Actual', 'Actual'], 7)
            figure.legend(loc = "upper center", bbox_to_anchor = (0.5, 1.1), ncol = 4, fancybox = True, shadow = True)

    def IronShowAll(self):
        figure = self.Add('Show All Iron Data').gca(ylabel = "iron conc in g", xlabel = "Time (min)")
        for k in self.iron_conc:
            figure.plot(self.iron_conc[k][0], self.iron_conc[k][1], '-x', label = str(k)+"g/L Fe2+")
            figure.plot(self.iron_conc[k][0], self.iron_conc[k][2], '-x', label = str(k)+"g/L Fe3+")
            figure.legend(loc = "upper center", bbox_to_anchor = (0.5, 1.1), ncol = 4, fancybox = True, shadow = True)

    def KeyShow(self):
        panel = wx.Panel(self, id=-1)
        self.newtab.AddPage(panel, "Data Key", True, self.page_bmp)

    def Add(self, name = None):
        page = Plot(self.newtab)
        self.newtab.AddPage(page, name, True, self.page_bmp)
        return page.figure

class Plot(wx.Panel):
    """
        THE PLOT CLASS TAKES IS MEANT TO DISPLAY THE MATPLOTLIB DATA PLOT INSTANCE

        FUNCTIONS:
            INIT(self, parent, if, dpi)
                -> constructor that initiates the plot
    """
    def __init__(self, parent, id = -1, dpi = None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = matplotlib.figure.Figure(dpi = dpi, figsize=(2, 2))
        self.canvas = Canvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        #~ Setting the size of the plot
        sizer   = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)

if __name__  == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
