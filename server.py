from flask import Flask,Response
from flask import render_template
import os
from os import path
from flask import request
import json
from flask_cors import CORS
# Model Definition
import math
import serialization
import numpy as np
import types
from enum import Enum

pathToPython = "/home/martin/repos/AudioAnalysisClient/src/pythonTypes.fs"

def create_type_provider(classlibrary):
    lines = ["module PythonTypes \n"]
    lines +=["type ClassName = string \n"]
    lines +=["type FieldName = string \n"]
    lines +=["type EnumName = FieldName \n"]
    lines +=["type EnumOptions = string list \n"]
    lines +=["type MethodName = FieldName \n"]
           
    
    for c in classlibrary:
        classname = type(c).__name__
        for field in dir(c):
            attr = getattr(c,field)
            if type(attr)== types.MethodType:
               lines+=["let " + classname + "_"+ str(field) + " : ClassName*MethodName = \"" + classname+"\",\"" + str(field)+"\" \n"]
            elif isinstance(attr, Enum):
                choices = "\";\"".join(dir(type(attr))[:-4])
                print(choices)
                lines+=["let " + classname + "_"+ str(field) + " : ClassName*EnumName = \"" + classname+"\",\"" + str(field)+"\" \n"]
                lines+=["let " + classname + "_"+ str(field) + "_options  : EnumOptions = [\"" + choices + "\"] \n"]
                
            else:
                 lines+=["let " + classname + "_"+ str(field) + " : ClassName*FieldName = \"" + classname+"\",\"" + str(field)+"\" \n"]
    f = open(pathToPython,"w")
    f.writelines(lines)

def create_server(classlibrary):
    """Receives list of uiElements that handle interaction with their specified classes"""
    app = Flask(__name__)
    CORS(app)
    uiElements = []
    classnames = [type(c).__name__ for c in classlibrary]
    classlookup = dict(zip(classnames, classlibrary))
    create_type_provider(classlibrary)
    
    print(classlookup)
    @app.route("/")
    @app.route('/getTargets',methods=['PUT'])
    def get_targets(): 
        classnamescol = request.form['classname'].split('/')
        fieldnamescol = request.form['fieldname'].split('/')
        
        data = []
        for (classnames,fieldnames) in zip(classnamescol,fieldnamescol):
            subclassnames = classnames.split()
            subfieldnames = fieldnames.split()
            subdata = []
            for (classname,fieldname) in zip(subclassnames,subfieldnames):
                item = classlookup[classname].__dict__[fieldname]
                if isinstance(item, list) or isinstance(item,np.ndarray):
                    liststring = [str(el) for el in item]
                    subdata.append("@".join(liststring))
                else:
                    subdata.append(str(item))
            data.append(",".join(subdata))
        #print(data)
        return "/".join(data)
    @app.route('/updateTarget',methods=['PUT'])
    def update_target():
        classname = request.form['classname']
        fieldname = request.form['fieldname']
        valuetype = request.form['valuetype']
        value = request.form['value']
        print(value)
        if valuetype == "float":
            classlookup[classname].__dict__[fieldname] = float(value)
        if valuetype == "bool":
            value = classlookup[classname].__dict__[fieldname]
            classlookup[classname].__dict__[fieldname] = not value
        if valuetype == "string":
            classlookup[classname].__dict__[fieldname] = value
        if valuetype == "enum":
            enum = classlookup[classname].__dict__[fieldname]
            classlookup[classname].__dict__[fieldname] = type(enum)[value]  
          
        return ""
    
    @app.route('/invokeMethod',methods=['PUT'])
    def invoke_method():
        classname = request.form['classname']
        method = request.form['method']    
        getattr(classlookup[classname], method)()
        return ""
 

   
    return app




