'''
Created on 09.09.2013

@author: hmeissner
'''

import sys
from PyQt4 import QtGui, QtCore
from view import GraphView
from graph import CorrelGraph

class GraphModel(QtGui.QDialog, GraphView, CorrelGraph):
    ''' represents the model of the GraphEditor
        is the mediator between the view (GUI) and the graph (logical component)
        connects every graphical component to a logical function '''
    
    def __init__(self, form):
        QtGui.QDialog.__init__(self)

        self.gw = GraphView(form)
        self.gw.setupUi(self) # sets up the GUI in the module 'view'
        self.gr = None # the current graph instance
        self.currentPath = '' # the path of the file that is currently used
        
        # all push buttons are being connected to a particular method 
        # the method is called when the button is being clicked
        self.connect(self.gw.pushButton, QtCore.SIGNAL('clicked()'), self.onBrowse)
        self.connect(self.gw.pushButton_2 , QtCore.SIGNAL('clicked()'), self.onSave)
        self.connect(self.gw.pushButton_3, QtCore.SIGNAL('clicked()'), self.onSelectOk)
        self.connect(self.gw.pushButton_4, QtCore.SIGNAL('clicked()'), self.onFadeOk)
        self.connect(self.gw.nextButton, QtCore.SIGNAL('clicked()'), self.onNext)
        self.connect(self.gw.previousButton, QtCore.SIGNAL('clicked()'), self.onPrevious)     
        
    def onBrowse(self): 
        ''' creates a graph from the chosen csv file
        gets the file path
        depending on which graph type is chosen, a new graph is created and drawn
        gives a warning if no graph type is chosen or if the browsing is canceled '''
        # clear warning messages
        self.gw.warning.setText('') 
        self.gw.warning2.setText('')
        # clear spin box values
        self.gw.doubleSpinBox.setValue(0.00)
        self.gw.doubleSpinBox_2.setValue(0.00)
         
        try:
            filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV data files (*.csv)')) # saves the file path
            self.currentPath = filename  
            self.gr = CorrelGraph(filename) # generate a new graph
            if self.gw.eeg.isChecked():                
                self.gr.addNodes('eeg') # add nodes to it
            elif self.gw.phaseshift.isChecked():
                self.gr.addNodes('ps')
            else:
                self.gw.warning.setText('Choose a graph type !')
            self.setNewSpinBoxLimits()
            self.gw.lineEdit.setText(filename)
        except IOError:
            print('File not found !')
            
    def onSave(self):
        ''' saves a graph into the folder in the path.
            gets the file path including the name of the created file.
            calls the graph's saveGraph() method '''
        try:
            filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File', '')) # saves the path of the new file
            self.gr.saveGraph(filename)
        except AttributeError:
            print('Saving was canceled !')
    
    def onSelectOk(self):
        ''' displays the degree of the given node    
        checks which graph type is selected 
        calls the getDegree method of the selected graph
        gives a warning if you try to get the degree of a node in a phase shift
        gives a warning if no graph type is selected and no file has been browsed '''
        # clear warning message
        self.gw.warning2.setText('')
        
        if self.gw.eeg.isChecked() or self.gw.phaseshift.isChecked() and self.gr != None:
            node = int(self.gw.spinBox.text())
            degree = str(self.gr.getDegree(node))
            self.gw.label_6.setText(degree)
        else:
            self.gw.warning2.setText('Create a graph first !')
    
    def onFadeOk(self):
        ''' fades out all edges in the graph if its value is not within the limits    
        converts the values (type: QString) in the spin boxes into floats
        calls the modifyGraph method of the chosen graph
        gives a warning if no graph type is chosen or if no file has been been selected '''
        # clear warning message
        self.gw.warning3.setText('')
        
        try:
            lowerLim = self.gw.doubleSpinBox.text()
            lowerLim = lowerLim.replace(',', '.') # e.g. 1,00 -> 1.00 
            lowerLim = float(lowerLim)                     
            upperLim = self.gw.doubleSpinBox_2.text()
            upperLim = upperLim.replace(',', '.')
            upperLim = float(upperLim)             
            if self.gw.eeg.isChecked():
                self.gr.modifyGraph(lowerLim, upperLim, 'eeg') 
            elif self.gw.phaseshift.isChecked():
                self.gr.modifyGraph(lowerLim, upperLim, 'ps')
            else:
                self.gw.warning3.setText('Choose a graph type first !')
        except AttributeError:
            self.gw.warning3.setText('Create a graph first !')
        except ValueError:
            self.gw.warning3.setText('No valid limits !')
    
    def onNext(self):
        ''' generates the next file path, creates and draws a new graph from the file path     
        gives a warning when file path couldn't be found or no file was browsed before '''
        # clear warning messages
        self.gw.warning.setText('')        
        self.gw.warning2.setText('')
        # clear spin box values
        self.gw.doubleSpinBox.setValue(0.00)
        self.gw.doubleSpinBox_2.setValue(0.00)
        
        try:    
            newPath = self.generatePath(1) 
                  
            self.gr = CorrelGraph(newPath)
            if self.gw.eeg.isChecked():
                self.gr.addNodes('eeg')
            elif self.gw.phaseshift.isChecked():
                self.gr.addNodes('ps')
            self.setNewSpinBoxLimits()
            self.gw.lineEdit.setText(newPath)   
        except IOError:
            path = self.currentPath.split('/')
            filename = path[len(path)-1] # name of the file, e.g. data_01.csv  
            self.gw.warning.setText('File %s not found!' %filename)
        except IndexError:
            self.gw.warning.setText('Select a file first !')
        except ValueError:
            self.gw.warning.setText('Please browse again !')
    
    def onPrevious(self):
        ''' generates the file path of the previous file, creates and draws a new graph from the file path  
        gives a warning when file path couldn't be found or no file was browsed before '''
        # clear warning messages
        self.gw.warning.setText('') 
        self.gw.warning2.setText('')
        # clear spin box values
        self.gw.doubleSpinBox.setValue(0.00)
        self.gw.doubleSpinBox_2.setValue(0.00)
        
        try:         
            newPath = self.generatePath(-1)
            
            self.gr = CorrelGraph(newPath)
            if self.gw.eeg.isChecked():                
                self.gr.addNodes('eeg')      
            elif self.gw.phaseshift.isChecked():
                self.gr.addNodes('ps')
            self.setNewSpinBoxLimits()
            self.gw.lineEdit.setText(newPath)
        except IOError:
            self.gw.warning.setText('File not found !')
        except IndexError:
            self.gw.warning.setText('Select a file first !')         
        except ValueError:
            self.gw.warning.setText('Please browse again !')
    
    def generatePath(self, num):
        ''' generates a new path from the current one
        valid parameters only are 1 or -1
        parameter 1: home/../data_2.csv -> home/../data_3.csv
        parameter -1: home/../data_2.csv - > home/../data_1.csv
        return: returns a string that represents the new file path '''
        if num == 1 or num == -1:
            path = self.currentPath.rsplit('/', 1) #path of the file, e.g. /home/.../data_1.csv
            fname = path[len(path)-1] #name of the file, e.g. data_1.csv      
            filename = fname  
            fname = fname.split('_') # ['data', '1.csv']
            fname = fname[1].split('.') # ['1', 'csv']
            fname = fname[0] # '1'
            number = int(fname) # 1
    
            newFilename = filename.replace('%s' %str(number), '%s' %str(number+num)) # e.g. data_1.csv -> data_2.csv
            
            # replaces the current path with the previous or rather next one
            # e.g. /home/../data_5.csv -> /home/../data_4.csv
            # e.g /home/../data_5.csv -> /home/../data.6.csv
            newPath = self.currentPath.replace(filename, newFilename)
            self.currentPath = newPath
            return newPath
        else:
            raise ValueError('parameter must either be 1 or -1.')        
                        
    def setNewSpinBoxLimits(self):
        ''' sets the min and max value for the spinboxes
        method is called every time a new graph is created '''
        self.gw.spinBox.setMaximum(self.gr.number_of_nodes() - 1) #sets the max of the spinbox
        self.gw.doubleSpinBox.setMaximum(max(self.gr.edgeList)) #sets the max of the doublespinbox
        self.gw.doubleSpinBox_2.setMaximum(max(self.gr.edgeList)) #sets the max of the doublespinbox2
        self.gw.doubleSpinBox.setMinimum(min(self.gr.edgeList)) #sets the max of the doublespinbox
        self.gw.doubleSpinBox_2.setMinimum(min(self.gr.edgeList)) #sets the max of the doublespinbox2

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = QtGui.QWidget()
    dialog = GraphModel(form)
    dialog.show()    
    sys.exit(app.exec_())
    