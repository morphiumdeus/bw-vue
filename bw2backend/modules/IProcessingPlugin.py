from yapsy.IPlugin import IPlugin

class IProcessingPlugin(IPlugin):

    def __init__(self):
        self.parent = 'project'
        self.priority = 10000
        self.options = []
        self.autocomplete = []
        self.name = 'dummy'
        self.displayName = "dummy"
        IPlugin.__init__(self)

    def activate(self):
        """
		On activation tell that this has been successfull.
		"""
		# get the automatic procedure from IPlugin
        IPlugin.activate(self)
        return

    def deactivate(self):
    	"""
    	On deactivation check that the 'activated' flag was on then
    	tell everything's ok to the test procedure.
    	"""
    	IPlugin.deactivate(self)

    def process(self, input):
        pass

    def getOptions(self):
        return self.options

    def getAutocomplete(self, hierarchy):
        return self.autocomplete

    def getName(self):
        return self.name

    def getDisplayName(self):
        return self.displayName

    def getPriority(self):
        return self.priority