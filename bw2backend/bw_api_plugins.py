from flask import request, url_for, Response
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS, cross_origin
import brightway2 as bw
#from bw2io import *
from ruamel.yaml import YAML
from bw2io import BW2Package
from yapsy.PluginManager import PluginManager
from modules.IProcessingPlugin import IProcessingPlugin
import logging


app = FlaskAPI(__name__, static_folder='schema', static_url_path='/schema')
CORS(app)

yaml=YAML(typ='safe')

# Build the manager
simplePluginManager = PluginManager()
# Tell it the default place(s) where to find plugins
simplePluginManager.setPluginPlaces(["modules"])
simplePluginManager.setCategoriesFilter({
   "Processing" : IProcessingPlugin,
   })
# Load all plugins
simplePluginManager.collectPlugins()

# Activate all loaded plugins
for pluginInfo in simplePluginManager.getAllPlugins():
   simplePluginManager.activatePluginByName(pluginInfo.name)



@app.route("/run", methods=['POST'])
def runScript():
    #print(request.get_data())
    #with open("C:\\Users\\oliver.hurtig\\Downloads\\bwjoos\\example.yaml") as stream:
    project = yaml.load(request.get_data())['project']
    #print(project)    
        
    ### Execute all Plugins    
    combined_result = {}
    for module in project:
        print("------Executing module " + module + "------")
        for pluginInfo in simplePluginManager.getAllPlugins():
            if pluginInfo.plugin_object.getName() == module:
                result = pluginInfo.plugin_object.process(project[module])
                if type(result) is dict:
                    combined_result.update(result)    
    str = bw.JsonWrapper.dumps(combined_result)
    return Response(str, mimetype='application/json')

@app.route("/getAutocomplete", methods=['POST'])
def getAutocomplete():
    hierarchy = request.get_json()
    for name in hierarchy:
        #print(name)
        for pluginInfo in simplePluginManager.getAllPlugins():
            if pluginInfo.plugin_object.getName() == name:   
                autocomplete = pluginInfo.plugin_object.getAutocomplete(hierarchy)
                str = bw.JsonWrapper.dumps(autocomplete)
                return Response(str, mimetype='application/json')
    

@app.route("/getOptions", methods=['POST'])
def getOptions():
    needed_module = request.get_json()
    print(needed_module)
    results = []
    for pluginInfo in simplePluginManager.getAllPlugins():
        if pluginInfo.plugin_object.getName() == needed_module['module']:   
            options = pluginInfo.plugin_object.getOptions()
            results.extend(options)
    str = bw.JsonWrapper.dumps(results)    
    print(needed_module)
    print(results)
    print(str)
    return Response(str, mimetype='application/json')

@app.route("/getModules", methods=['GET'])
def getModules():
    results = []
    for pluginInfo in simplePluginManager.getAllPlugins():
        results.append({
            "displayName": pluginInfo.plugin_object.getDisplayName(),
            "name": pluginInfo.plugin_object.getName(),
            "pluginName": pluginInfo.name,
            "priority": pluginInfo.plugin_object.getPriority()})
    print(results)
    str = bw.JsonWrapper.dumps(results)
    return Response(str, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, port=5555, host='0.0.0.0')