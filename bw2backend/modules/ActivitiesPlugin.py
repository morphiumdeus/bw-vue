import modules.IProcessingPlugin as IProcessingPlugin
import brightway2 as bw
import logging
from Helpers import getActivity

class ActivitiesPlugin(IProcessingPlugin.IProcessingPlugin):
    def __init__(self):
        self.name = 'activities'
        self.displayName = "My Activities"
        self.priority = 11
        self.parent = 'project'
        self.options = [{'name': {
            'type': 'process',
            'name': 'dummy name',
            'production amount': '1.0',
            'reference product': 'water',
            'unit': 'liter',
            'activity type': 'ordinary transforming activity'
            }}]
    
    def getAutocomplete(self, hierarchy):
        print(hierarchy)
        if any(item in hierarchy for item in ["base", "input"]):
            if bw.databases[hierarchy[0]]:
                return [{'label': 'db here',
'kind': 'monaco.languages.CompletionItemKind.Snippet'}]
            elif bw.databases[hierarchy[1]]:
                return [{'label': 'db2 here',
'kind': 'monaco.languages.CompletionItemKind.Snippet'}]
            else:
                return [{'label': '[${1:database id}, ${2:process id}]',
'kind': 'monaco.languages.CompletionItemKind.Snippet'}]
        else:
            return [
{'insertText': 
'''${1:identifier}:
    production amount: ${2:1.0}    
    reference product: ${3:*product}
    type: ${4:process}
    unit: ${5:*kg}
    activity type: ${6:ordinary transforming activity}
    location: ${7:2 letter country code}
    exchanges:
        - amount: ${8:1.0}
            input: [${9:db database}, ${10:process id}]
            type: ${11:technosphere}
    classifications:
        - (ISIC rev.4 ecoinvent, '${classification}')
        
    comment: ${12:this loads a database from a local file.}''',
'label': 'Full process definition [Snippet]',
'kind': 'monaco.languages.CompletionItemKind.Snippet'}]

    def process(self, input):
        ### Package "Activities"
        try:
            own_activities_db = bw.Database("own_activities")
            own_activities_obj = {}
            for act_name in input:
                if 'base' in input[act_name] :
                    print("Trying to get base Activity:")
                    print(input[act_name]['base'])
                    lca_act = getActivity(input[act_name]['base'])
                    new_act = lca_act.copy()
                    
                    for ex in input[act_name]['exchanges']:
                        print(ex)
                        try:
                            existing_ex = [e for e in new_act.exchanges() if ex['input'][1] in e['input']][0]
                            existing_ex.amount = ex['amount']
                            existing_ex.type = ex['type']
                            existing_ex.unit = ex['unit']
                        except:
                            print("Exchange not existing, adding")
                            new_ex = new_act.new_exchange(input=tuple(ex['input']), amount=ex['amount'], type=ex['type'])
                            new_ex.save()
                    own_activities_obj[("own_activities", act_name)] = new_act
                    print(new_act.as_dict())
                    for exc in new_act.exchanges():
                        print(exc.input['name'], exc['amount'], exc['unit'])
                else:
                    input[act_name]['id'] = act_name
                    for ex in input[act_name]['exchanges']:
                        ex['input'] = tuple(ex['input'])                    
                    own_activities_obj[("own_activities", act_name)] = input[act_name]
            print(own_activities_obj)    
            own_activities_db.write(own_activities_obj)
            return True
        except:
            logging.exception("message")