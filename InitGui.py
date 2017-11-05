import FreeCADGui
import logging

logging.basicConfig()


class OSEDevWorkbench(FreeCADGui.Workbench):
    MenuText = "OSEDev Workbench"
    ToolTip = "Open Source Ecology Development Workbench"
    Icon = """
    /* XPM */
    static const char *test_icon[]={
    "16 16 2 1",
    "a c #000000",
    ". c None",
    "................",
    "................",
    "..##...###..###.",
    ".#..#..#....#...",
    ".#..#..###..###.",
    ".#..#....#..#...",
    "..##...###..###.",
    "................",
    ".###............",
    ".#..#..##..#..#.",
    ".#..#.#..#.#..#.",
    ".#..#.####.#..#.",
    ".#..#.#.....##..",
    ".###...##...##..",
    "................",
    "................"};
    """

    def Initialize(self):
        from service import OSEDevService
        window = FreeCADGui.getMainWindow()
        service = OSEDevService(window)
        self.appendToolbar("OSEDev", service.command_names)
        self.appendMenu("OSEDev", service.command_names)
        for command in service.commands:
            FreeCADGui.addCommand(command.id, command)

    def Activated(self):
        #from PySide import QtGui
        #tab = self.getComboView(mw)
        #tab2=QtGui.QDialog()
        #tab2 = FreeCADGui.PySideUic.loadUi('ui/login.ui')
        #tab.addTab(tab2,"A Special Tab")
        #tab2.show()
        pass

    def Deactivated(self):
        pass

    def getComboView(self, mw):
        from PySide import QtGui
        dw=mw.findChildren(QtGui.QDockWidget)
        for i in dw:
            if str(i.objectName()) == "Combo View":
                return i.findChild(QtGui.QTabWidget)
            elif str(i.objectName()) == "Python Console":
                return i.findChild(QtGui.QTabWidget)
        raise Exception ("No tab widget found")


FreeCADGui.addWorkbench(OSEDevWorkbench)
