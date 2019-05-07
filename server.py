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

pathToPython = "C:\\Users\\marti\\Source\\Repos\\VideoHeartbeatInterface\\src\\pythonTypes.fs"

def create_type_provider(classlibrary):
    lines = ["module PythonTypes \n"]
    lines +=["type ClassName = string \n"]
    lines +=["type FieldName = string \n"]
           
    
    for c in classlibrary:
        classname = type(c).__name__
        for field in dir(c):
            lines+=["let " + classname + "_"+ str(field) + " : ClassName*FieldName = \"" + classname+"\",\"" + str(field)+"\" \n"]
    
    f = open(pathToPython,"w")
    f.writelines(lines)

def create_server(classlibrary,createCamera):
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
        classnames = request.form['classname'].split()
        fieldnames = request.form['fieldname'].split()
        data = []
        print(fieldnames)
        for (classname,fieldname) in zip(classnames,fieldnames):
            item = classlookup[classname].__dict__[fieldname]
#            if isinstance(item, (list,)):
#                data.append(str(len(item)))
#                data += [str(val) for val in item]
#            else:
            data.append(str(item))
        print(data)
        return ",".join(data)
    @app.route('/updateTarget',methods=['PUT'])
    def update_target():
        classname_fieldname = request.form['classnamefieldname']
        splt = classname_fieldname.split(":")
        classname = splt[0]
        fieldname = splt[1]
        valuetype = request.form['valuetype']
        value = request.form['value']
        
        if valuetype == "float":
            classlookup[classname].__dict__[fieldname] = float(value)
            print(float(value))
        if valuetype == "bool":
            value = classlookup[classname].__dict__[fieldname]
            classlookup[classname].__dict__[fieldname] = not value
        if valuetype == "string":
            classlookup[classname].__dict__[fieldname] = value
            print(value)
        
        return ""
    
    @app.route('/invokeMethod',methods=['PUT'])
    def invoke_method():
        classname = request.form['classname']
        method = request.form['method']    
        getattr(classlookup[classname], method)()
        return ""
 
    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    @app.route('/video_feed')
    def video_feed():
        return Response(gen(createCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
   
    return app




