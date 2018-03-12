'''
Created on 05.09.2013

@author: hmeissner
'''

from networkx import draw, MultiDiGraph, degree, function, layout
import matplotlib

# uses the Qt4Agg backend to print the graph with matplotlib
#lets you use both the graph and the editor thread 
# otherwise the graph window is frozen
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt

class CorrelGraph(MultiDiGraph):
    '''represents a graph that shows the correlations between the nodes
       nodes can be added to the graph, the graph can then be modified
       every nodes' degree can be requested'''
    
    def __init__(self, csvData):
        MultiDiGraph.__init__(self)
        
        self.data = open(csvData)
        self.colors = [] # saves the color of each edge in the graph
        self.modifiedOnce = False # tells if the graph has already been modified one
        self.modifiedGraph = None # saves the modified graph
        #self.colorGradient = ['#00a500', '#1ea500', '#3ca500', '#5ab400', '#78b400', '#96c300',
                            #'#b4d200', '#d2d200', '#f0e100', '#fff000', '#ffd200', '#ffb400',
                            #'#ff9600', '#ff7800', '#ff5a00', '#f04b00', '#ff3c00', '#f02d00',
                            #'#e11e00', '#d20f00', '#b40000'] # color list from red to green
        self.colorGradient = ['#fffb2c', '#ffea47', '#ffdc6b', '#ffd06a', '#ffc573', '#ffbd7a',
                              '#ffb482', '#ffb28b', '#ffa789', '#ff9c8d', '#ff8b87', '#ff8fa4',
                              '#ff9ccc', '#ff93e0', '#ff7ff0', '#f86aff', '#df52ff', '#b23fff'] # color list for an eeg graph
        self.colorGradient2 = ['#fff52d', '#ffff3f', '#edff4e', '#e3ff64', '#e6ff74', '#dbff86',
                               '#c8ff8e', '#b2ff82', '#a0ff86', '#87ff8b', '#7dffaf', '#7cffc6',
                               '#67ffd9', '#5cddf9', '#57ffff', '#49e7ff', '#3ed5ff', '#3ab3ff'] # color list for a phase shift graph
        self.edgeList = [] # saves all the edges in the graph

    def addNodes(self, grtype):
        ''' adds all nodes and edges to the graph
        checks for each edge if it's not 0, if so adds the edge to the graph
        maps every edge value to a color in the colorGradient list and draws the graph 
        parameter grtype: type of the graph, either 'eeg' or 'ps' string '''
        plt.clf() # clears the drawn figure
        
        rowCounter = 0 #the current row
        for line in self.data.readlines(): #reads every line of the .csv file
            edgesPL = line.split() #edgesPL: edges per line
            columnCounter = 0 #the current column
            for edge in edgesPL:
                if rowCounter == columnCounter:
                    columnCounter += 1
                    continue                
                else:
                    self.add_edge(rowCounter, columnCounter, weight = float(edge))
                    self.edgeList.append(float(edge))
                    columnCounter += 1           
            rowCounter += 1     
        self.mapValueToColor(self.edgeList, grtype)
        draw(self, pos = layout.circular_layout(self), node_size=300, node_color='#474747', edge_color=self.colors, alpha=0.8) # draws the graph
        plt.ion()
        #plt.show(block = True) # displays the figure
        plt.pause(0.1)
        #plt.show(block = True)
        #plt.ioff()
    
    def modifyGraph(self, lowerLim, upperLim, grtype):
        ''' fades out all edges with values not within the limits        
        parameter lowerLim: the lower limit, only edges with a higher or equal value are kept in the graph
        parameter upperLim: the upper limit, only edges with a lower or equal value are kept in the graph '''
        plt.clf() # clears the drawn figure
        graphCopy = self.copy() # creates a copy of the graph, which will be manipulated
        edges = []
        weights = function.get_edge_attributes(graphCopy, 'weight') # saves all the edges and its values (weight)
        
        # checks for each edge if its value is not within the limits, if so the edge is removed
        for edge in graphCopy.edges(data = True):
            edgeWeight = weights[(edge[0], edge[1])]
            if edgeWeight < lowerLim or edgeWeight > upperLim:
                graphCopy.remove_edge(edge[0], edge[1]) 
            else:
                edges.append(edgeWeight) # saves the value of the remaining edges to create a color list for the drawing
                
        # checks for each node if its neighbors count is 0, if so it's removed                  
        for node in graphCopy.nodes():
            if degree(graphCopy, node) == 0:
                graphCopy.remove_node(node)
        
        self.modifiedOnce = True      
        self.modifiedGraph = graphCopy
        self.mapValueToColor(edges, grtype) # every remaining edge is mapped to a color
        plt.ion() 
        draw(graphCopy, pos = layout.circular_layout(self), node_size=300, node_color='#474747', edge_color=self.colors, alpha=0.8)
        #plt.show() # displays the figure
        plt.pause(0.1)
        #plt.ioff()                   
                        
    def getDegree(self, key):      
        ''' returns the number of edges (degree) coming from the given node      
        key: number of the node '''       
        if not self.modifiedOnce:
            return degree(self, key)/2
        else:
            return len(self.modifiedGraph.neighbors(key))
           
    def mapValueToColor(self, edges, grtype):
        ''' maps a color string to each edge in the graph '''
        self.colors = [] #clears the color list for the drawing
        
        #detects the min and max values over all edges
        minValue = min(edges)
        maxValue = max(edges)
        
        for value in edges:
            if minValue != maxValue:
                fl = (value - minValue) / float(maxValue - minValue) #calculates a float factor fl for every edge value
            else:
                fl = 0.5
            if grtype == 'eeg':
                index = int(round(len(self.colorGradient) - 1) * fl) #gets an index from the factor fl
                self.colors.append(self.colorGradient[index]) #gets a color from the colorGradient list
            elif grtype == 'ps':
                index = int(round(len(self.colorGradient2) - 1) * fl) #gets an index from the factor fl
                self.colors.append(self.colorGradient2[index]) #gets a color from the colorGradient list
                
    def saveGraph(self, fname):
        ''' saves the graph in the given path
            supported formats: png, pdf, ps, eps and svg
            parameter fname: the path of the saved file '''
        if not self.modifiedOnce:
            draw(self, pos = layout.circular_layout(self), node_size=300, node_color='#474747', edge_color=self.colors, alpha=0.8)
        else:
            draw(self.modifiedGraph, pos = layout.circular_layout(self), node_size=300, node_color='#474747', edge_color=self.colors, alpha=0.8)
        plt.savefig(fname)
        