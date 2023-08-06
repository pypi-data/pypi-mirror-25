'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import PyQt5.QtGui as qtGui
import logging
logger = logging.getLogger(__name__)

SCAN_COL_WIDTH = 40
CMD_COL_WIDTH = 240
NUM_PTS_COL_WIDTH = 40
MINIMUM_WIDGET_WIDTH = 420
SCAN_COL = 0
CMD_COL = 1
NUM_PTS_COL = 2

class ScanBrowser(qtWidgets.QDialog):
    '''
    '''
    # Define some signals that this class will provide to users
    scanSelected = qtCore.pyqtSignal(list, name="scanSelected")
    scanLoaded = qtCore.pyqtSignal(bool, name="scanLoaded")
              
    def __init__(self, parent=None):
        '''
        constructor
        '''
        super(ScanBrowser, self).__init__(parent)
        layout = qtWidgets.QHBoxLayout()
        self.scanList = qtWidgets.QTableWidget()
        #
        font = qtGui.QFont("Helvetica", pointSize=10)
        self.scanList.setFont(font)
        self.scanList.setEditTriggers(qtWidgets.QAbstractItemView.NoEditTriggers)
        self.scanList.setRowCount(1)
        self.scanList.setColumnCount(3)
        self.scanList.setColumnWidth(SCAN_COL, SCAN_COL_WIDTH)
        self.scanList.setColumnWidth(CMD_COL, CMD_COL_WIDTH)
        self.scanList.setColumnWidth(NUM_PTS_COL, NUM_PTS_COL_WIDTH)
        self.scanList.setHorizontalHeaderLabels(['S#', 'Command', 'Points'])
        self.scanList.setSelectionBehavior(qtWidgets.QAbstractItemView.SelectRows)
        self.setMinimumWidth(400)
        self.setMaximumWidth(600)
        layout.addWidget(self.scanList)
        self.setLayout(layout)
        self.show()
        
        self.scanList.itemSelectionChanged.connect(self.scanSelectionChanged)

    def loadScans(self, scans, newFile=True):
        self.scanList.setRowCount(len(scans.keys()) )
        row = 0
        scanKeys = sorted(scans, key=int)
        logger.debug("scanKeys %s" % str(scanKeys))
        for scan in scanKeys:
            scanItem = qtWidgets.QTableWidgetItem(str(scans[scan].scanNum))
            self.scanList.setItem(row, SCAN_COL, scanItem)
            cmdItem = qtWidgets.QTableWidgetItem(scans[scan].scanCmd)
            self.scanList.setItem(row, CMD_COL, cmdItem)
            nPointsItem = qtWidgets.QTableWidgetItem(str(len(scans[scan].data_lines)))
            self.scanList.setItem(row, NUM_PTS_COL, nPointsItem)
            row += 1
        self.scanLoaded.emit(newFile)
            
    def filterByScanTypes(self, scans, scanTypes):
        filteredScans = {}
        scanKeys = sorted(scans, key=int)
        if scanTypes is None:
            raise ValueError("Invalid ScanFilter %s" % scanTypes)
        for scan in scanKeys:
            if len(scanTypes) > 0:
                thisType = scans[scan].scanCmd.split()[0]
                if thisType in scanTypes:
                    filteredScans[scan] = scans[scan]
            else:
                filteredScans[scan] = scans[scan]
        logger.debug ("Filtered Scans %s" % filteredScans)
        self.loadScans(filteredScans, newFile = False)

    def getCurrentScan(self):
        return str(self.scanList.item(self.scanList.currentRow(), 0).text())
        
    def setCurrentScan(self, row):
        logger.debug("Entered")
        self.scanList.setCurrentCell(row, 0)

    @qtCore.pyqtSlot()
    def scanSelectionChanged(self):
        logger.debug("Entered")
        selectedItems = self.scanList.selectedIndexes()
        selectedScans = []
        for item in selectedItems:
            if item.column() == 0:
                scan = str(self.scanList.item(item.row(),0).text())
                selectedScans.append(scan)
        logger.debug("Selected scans %s" % selectedScans)
        self.scanSelected[list].emit(selectedScans)