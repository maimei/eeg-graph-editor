.. view:

****
View
****

This is the documentation of the module view, which only contains the class :class:`GraphView`.

.. class:: GraphView

GraphView instances are created when a GraphModel instance's :meth:`__init__()` method is called. It calls the :meth:`setupUi()` method which sets up the GUI. So the function of GraphView instances is to display the programm's graphical view.

GraphView extends QtGui.QWidget.

    .. method:: GraphView.setupUi(Form)
	
	sets up the graphical user interface of the graph editor and settles the taborder.
	
        **parameter** Form:
	    
    	    the parameter Form is of the type QtGui.QWidget. An instance of it is created in the model module.

    .. method:: GraphView.retranslateUI(Form)
 	
	sets the text for every label and button in the GUI. This method is called within :meth:`setup()`
	
	**parameter** Form:
	    
    	    the parameter Form is of the type QtGui.QWidget. An instance of it is created in the model module.
