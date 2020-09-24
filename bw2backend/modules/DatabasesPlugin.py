import modules.IProcessingPlugin as IProcessingPlugin
from bw2io import BW2Package
import brightway2 as bw

class DatabasePlugin(IProcessingPlugin.IProcessingPlugin):
    def __init__(self):
        self.name = 'databases'
        self.displayName = "Databases"
        self.priority = 10
        self.parent = 'project'
        self.import_db_dispatcher = {
            'SingleOutputEcospold1Importer' : bw.SingleOutputEcospold1Importer,
            'SingleOutputEcospold2Importer' : bw.SingleOutputEcospold2Importer,
            'BW2package' : self.import_bw2package
        }
        self.options = [{'!needed name': {
                'type': importer,
                'location': '!needed path/to/local/file',
                'name': 'descriptive name',
                'source': 'URL.of.database',
                'comment': 'this loads a database from a local file.'
            },
            'comment': 'Import a database in a format compatible with the BW ' + importer + ' importer',
            'inputType': 'button'} for importer in list(self.import_db_dispatcher.keys())]

    def getAutocomplete(self, hierarchy):
        if hierarchy[0] == "type":
            return [{'label': importer,
'kind': 'monaco.languages.CompletionItemKind.Text'} for importer in list(self.import_db_dispatcher.keys())]
        else:
            return [
{'insertText': 
'''${1:identifier}:
    type: ${2:*type}    
    location: ${3:*path to database file, e.g. /Users/yourname/Documents/db.db}
    name: ${4:name}
    source: ${5:link to database webpage or readme}
    comment: ${6:this loads a database from a local file.}''',
'label': 'Full database definition [Snippet]',
'kind': 'monaco.languages.CompletionItemKind.Snippet'}]

    def process(self, input):           
        try:
            databases
        except:
            databases = {}
        for db_name in input:
            print(db_name)
            if db_name not in bw.databases:
                db = input[db_name]
                print("Adding " + db_name)
                databases[db_name] = {}
                databases[db_name]['importer'] = self.import_db(db_name, db['location'], db['type'])
                try:
                    databases[db_name]['importer'].apply_strategies()
                    databases[db_name]['importer'].statistics()
                    databases[db_name]['importer'].write_database()
                except:
                    print("Skipped strategies, statistics, write")
                databases[db_name]['db'] = bw.Database(db_name)
        return True

    def import_bw2package(self, location, name):
        BW2Package.import_file(location)

    def import_db(self, name, location, importer):
        try:
            return self.import_db_dispatcher[importer](location, name)
        except:
            return "Invalid function"
