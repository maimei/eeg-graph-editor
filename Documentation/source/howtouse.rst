.. howtouse:


**********
How to use
**********

In order to launch the GraphEditor run the model.py module in the project folder. For the editor to work you need to have the libraries Networkx and Matplotlib imported.

Then the following editor should appear:

.. image:: _static/GraphEditor.png

Steps
-----

 1. Please choose either "EEG graph" or "Phase shift graph" so that the model module knows in which color to draw the graph when a button is clicked.
 2. Then browse a .csv file. At this point there are three issues to take care of. 

 * The filename should look something like: "<Dateibeschreibung>_1.csv" as the previous and next button split the filname at "_" and "." in order to generate the previous or next file directory.
 * Further the float values in the file should look like: 8.5 instead of 8,5 in order to be read in correctly to the networkx graph. 
 * Plus the edges in the .csv file should be seperated by spaces. 

   If these conditions are given a graph of your file should automatically be drawn in an extern window.

 3. After having chosen a file you can excute certain actions on the graph:
You can ...
 * click on "Next segment" to get the graph of the next time step.
 * click on "Previous segment" to load the graph of the time step before.
 * choose a particular node whose degree you'd like to know and then hit "OK"
 * fade out some of the edges and nodes by entering a lower and upper limit and then hit "submit"
 * switch to another graph type and continue your actions or browse a new file
 * save the changes you have made to the graph as a png, pdf, ps, eps or svg file.
 4. When executing an unsupported action you will be informed by a warning.

**Note**: Please make sure that you use the right backend for printing the graph with matplotlib. Otherwise you might not be able to interact with the graph window but only with the editor. The default backend for this programm is "Qt4Agg". You might have to change it using matplotlib.use("backendname"). You can find a list of various backends on `matplotlib.org <http://matplotlib.org/faq/usage_faq.html#what-is-a-backend>`_.
