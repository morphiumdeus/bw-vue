import modules.IProcessingPlugin as IProcessingPlugin
import brightway2 as bw

class ProjectPlugin(IProcessingPlugin.IProcessingPlugin):
    def __init__(self):
        self.name = 'project'
        self.displayName = "Project setup"
        self.priority = 1
        self.parent = ''
        self.options = ['dummy name']
        self.autocomplete = [
            {'insertText':'name', 'label': 'name', 'kind': 'monaco.languages.CompletionItemKind.Text'},
            {'insertText':'databases', 'label': 'databases', 'kind': 'monaco.languages.CompletionItemKind.Text'},
            {'insertText':'activities', 'label': 'activities', 'kind': 'monaco.languages.CompletionItemKind.Text'},
            {'insertText':'singleLCA', 'label': 'singleLCA', 'kind': 'monaco.languages.CompletionItemKind.Text'},
            {'insertText':'thisIsMyTest', 'label': 'thisIsMyTest', 'kind': 'monaco.languages.CompletionItemKind.Text'}
        ]

    def process(self, input):
        # input is supposed to be a name
        # Activate the right project. If it doesn't exist, do the basic setup.
        if  input in [name for name, i,j in bw.projects.report()]:
            bw.projects.set_current(input)
        else:
            bw.projects.set_current(input)
            bw.bw2setup()
        return True