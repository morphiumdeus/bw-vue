import modules.IProcessingPlugin as IProcessingPlugin
import brightway2 as bw
import logging
from Helpers import getActivity

class SingleLCAPlugin(IProcessingPlugin.IProcessingPlugin):
    def __init__(self):
        self.name = 'singleLCA'
        self.displayName = "Single LCA"
        self.priority = 100
        self.parent = 'project'
        self.options = [{'name': {
            'activity': '[database, activity]',
            'amount': '1.0',
            'lcia': [['IPCC 2013', 'climate change', 'GWP 100a'], ['IPCC 2013', 'climate change', 'GTP 100a']]
            }}]
        self.autocomplete = []

    def process(self, input):                   
        ### Package "SingleLCA"
        try:
            result = {'singleLCA': {}}
            for lca_name in input:
                lca_info = input[lca_name]
                print("---SingleLCA started with:")
                print(lca_info['activity'])
                lca_act = getActivity(lca_info['activity'])
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
                        lca.switch_method(method)
                        lca.redo_lcia()
                    result['singleLCA'][lca_name]['results'].append({
                        'name': bw.Method(method).name,
                        'amount': lca.score,
                        'unit': bw.Method(method).metadata['unit']
                    })
            return result
        except:
            logging.exception("message")