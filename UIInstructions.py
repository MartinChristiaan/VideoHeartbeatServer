from flask import Flask
from flask import render_template
import os
from os import path
import json
import csv

inputDataPath = "input.json"


class UIElement:
    def __init__(self,fieldname,classname,uiname,onupdate,myclass):   
        self.fieldname = fieldname
        self.uiname = uiname
        self.onupdate = onupdate
        self.classname = classname
        self.value = myclass.__dict__[fieldname]
        self.myclass = myclass

    def performUpdate(self):
        if self.onupdate!=None:
           getattr(self.myclass, self.onupdate)()

class Switch(UIElement):
    def __init__(self,fieldname,classname,uiname,myclass,onupdate):
        UIElement.__init__(self,fieldname,classname,uiname,onupdate,myclass)

    def getInstructions(self):
        return ["switch",self.classname,self.uiname,self.value]

    def updateValue(self,_):
        self.myclass.__dict__[self.fieldname] = not self.myclass.__dict__[self.fieldname] 

class Slider(UIElement):
    def __init__(self,fieldname,classname,uiname,min,max,myclass,onupdate):
        UIElement.__init__(self,fieldname,classname,uiname,onupdate,myclass)
        self.min = min
        self.max = max
    def getInstructions(self):
        return ["slider",self.classname,self.uiname, self.min,self.max,self.value]
    
    def updateValue(self,value):
        self.myclass.__dict__[self.fieldname] = float(value)

class Dropdown(UIElement):
    def __init__(self,fieldname,classname,uiname,myclass,options,optionlabels,onupdate):
        UIElement.__init__(self,fieldname,classname,uiname,onupdate,myclass)
        if isinstance(self.value, (list,)):
            self.value = tuple(self.value)
        try:
            self.value = optionlabels[options.index((self.value))]
        except:
            for i,option in enumerate(options):
                if type(option) == type(self.value):
                    self.value = optionlabels[i]
        self.options = options
        self.optionlabels = optionlabels
        # Maybe also execute some callback in myclass
  
    def getInstructions(self):
        return ["dropdown",self.classname,self.uiname,self.value] + self.optionlabels 

    def updateValue(self,label):
        self.myclass.__dict__[self.fieldname] = self.options[self.optionlabels.index(label)]
   

class TimeFigure():
    def updateValues(self):
        self.t += 0.01
        self.y = [self.myclass.__dict__[yFieldName] for yFieldName in self.yfieldnames]

    def __init__(self,myclass,xfieldName,yFieldNames,xname,ynames):
        self.xfieldname = xfieldName
        self.yfieldnames = yFieldNames
        self.myclass = myclass      
        self.ynames= ynames
        self.updatePol = "Add"
        self.t = 0
        self.y = [self.myclass.__dict__[yFieldName] for yFieldName in self.yfieldnames]
        
    def getInstructions(self):
        return ["figure",0,len(self.y),self.updatePol,"Time"] + self.ynames + [self.t] + self.y

    def getUpdateInstructions(self):
        self.updateValues()
        return [1,len(self.y), self.t] + self.y




# uiInstructions = {"SkinClassifier": [
#             Slider("minh","Min Hue",0,255,0).__dict__,
#             Slider("maxh","Max Hue",0,255,20).__dict__    
#             ],
#             "Camera":[
#             Dropdown("resolution","Resolution",["360p","480p","720p","1080p"]).__dict__    
#             ]    
#     }



def load_uiData(myclass):
    # sliderDict = dict()
    # categories = dict()
    # with open('sliders.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     line_count = 0
    #     for row in csv_reader:
    #         if line_count > 0:
    #             sliderDict[row[0]] = tuple(row[1:])
    #         line_count += 1
    
    # mainDict = myclass.__dict__
    # updatedItems = set()
    # for category in mainDict.items():
    #     subdict = category[1].__dict__
    #     itemsInCat = 0
    #     for (name,value) in subdict.items():
    #         if sliderDict.__contains__(name):
    #             subdict[name] = sliderDict[name][1]
    #             updatedItems.add(name)
    #             itemsInCat+=1
    #     categories[category[0]] = itemsInCat
    

    return uiInstructions
    


    # unwantedkeys = []
    # for key in sliderDict.keys():
    #     if not updatedItems.__contains__(key):
    #         unwantedkeys.append(key)
    #         print(key + " is not in the codebase")
    
    # for key in unwantedkeys:
    #     sliderDict.pop(key,None)


    #return recursiveDeserialize(inputs.__dict__,inputData)


    

# def saveInputs(sliderData):
#     slidercsv = open('sliders.csv')
#     lines = slidercsv.readlines()
#     slidercsv.close()
#     slidercsv = open('sliders.csv','w')
    
#     values = sliderData.values()
#     for i,line in enumerate(lines):
#         if i>0:
#             cols = line.split(',')
#             cols[2] = 



