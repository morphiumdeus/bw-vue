from flask import request, url_for, Response
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS, cross_origin
import brightway2 as bw
from bw2io import *
from ruamel.yaml import YAML
from bw2io import BW2Package

app = FlaskAPI(__name__)
CORS(app)

@app.route("/run", methods=['POST'])
def runScript():
    print(request.get_data())

    yaml=YAML(typ='safe')

    #with open("C:\\Users\\oliver.hurtig\\Downloads\\bwjoos\\example.yaml") as stream:
    project = yaml.load(request.get_data())['project']
    #print(project)
    # Activate the right project. If it doesn't exist, do the basic setup.
    if  project['name'] in [name for name, i,j in bw.projects.report()]:
        bw.projects.set_current(project['name'])
    else:
        bw.projects.set_current(project['name'])
        bw.bw2setup()
        
    ### Package "databases"
    # Load the databases if not already done.
    def import_bw2package(location, name):
        BW2Package.import_file(location)
    import_db_dispatcher = {
        'SingleOutputEcospold1Importer' : bw.SingleOutputEcospold1Importer,
        'SingleOutputEcospold2Importer' : bw.SingleOutputEcospold2Importer,
        'BW2package' : import_bw2package
    }
    def import_db(name, location, importer):
        try:
            return import_db_dispatcher[importer](location, name)
        except:
            return "Invalid function"

    try:
        databases
    except:
        databases = {}
    for db_name in project['databases']:
        if db_name not in bw.databases:
            db = project['databases'][db_name]
            print("Adding " + db_name)
            databases[db_name] = {}
            databases[db_name]['importer'] = import_db(db_name, db['location'], db['type'])
            try:
                databases[db_name]['importer'].apply_strategies()
                databases[db_name]['importer'].statistics()
                databases[db_name]['importer'].write_database()
            except:
                print("Skipped strategies, statistics, write")
            databases[db_name]['db'] = bw.Database(db_name)
            
    ### Package "Activities"
    own_activities_db = bw.Database("own_activities")
    own_activities_obj = {}
    for act_name in project['activities']:
        project['activities'][act_name]['id'] = act_name
        for ex in project['activities'][act_name]['exchanges']:
            ex['input'] = tuple(ex['input'])
            print(ex)
        own_activities_obj[("own_activities", act_name)] = project['activities'][act_name]
    own_activities_db.write(own_activities_obj)

    ### Package "SingleLCA"
    result = {'singleLCA': {}}
    for lca_name in project['singleLCA']:
        lca_info = project['singleLCA'][lca_name]
        lca_act = own_activities_db.get(lca_info['activity'])
        print(lca_info['lcia'])
        for n, m in enumerate(lca_info['lcia']):
            method = tuple(m)
            if n == 0:
                lca = bw.LCA({lca_act: lca_info['amount']}, method)
                lca.lci()
                lca.lcia()
                result['singleLCA'][lca_name] = {
                    'inputs': {
                        'name': lca_act['name'],
                        'amount': lca_info['amount'],
                        'unit': lca_act['unit']
                    },
                    'results': []
                }
            else:                
                print("lcia")
                print(method)
                lca.switch_method(method)
                lca.redo_lcia()
            result['singleLCA'][lca_name]['results'].append({
                'name': bw.Method(method).name,
                'amount': lca.score,
                'unit': bw.Method(method).metadata['unit']
            })
            print(result['singleLCA'][lca_name]['results'])
    str = bw.JsonWrapper.dumps(result)
    return Response(str, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, port=5555, host='0.0.0.0')