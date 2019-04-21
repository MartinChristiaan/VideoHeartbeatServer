from os import path
import json

folder = "savedClasses/"

def saveJson(someclass):
    path = type(someclass).__name__
    jsontring = json.dumps(someclass.__dict__)
    f= open(folder+path,'w')
    f.write(jsontring)
    f.close()

def LoadFromJson(someclass):
    """Loads Input data for class"""
    savedDict = dict()
    path = type(someclass).__name__
    try:
        f= open(folder+path,'r')
        savedDict = json.loads(f.read())
        f.close()
        print("Found inputdata ")
    except:
        print("Input settings not found, Creating new")

    classDict = someclass.__dict__
    for fieldname,field in classDict.items():
        if savedDict.__contains__(fieldname):
            classDict[fieldname] = savedDict[fieldname]
            
    

