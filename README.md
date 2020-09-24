# Motivation
Currently available tools for LCA lack one or more of the following:
* Reproducability, Verifiability, Peer review
* Interactivity
* Possibility to reuse blocks or whole LCAs (modularity of LCA)
* Batch processing, scenario analysis
* Possibility to extend functions (via plugins)

Further, an online tool has several advantages:
* No need for installing
* Easier publication, sharing and collaboration
* Distribution of tasks
* Division of backend and frontend (users can decide on how to input/visualize data)

There are several ongoing projects in that area. I am aware of:
* Antelope / LCA-tools / uo-lca by brandon.kuczenski@301south.net
* LCOPT by pjjoyce@kth.se
* brightway2-ui by Tomas Navarrete Gutierrez
* brightway2-restapi by Chris Mutel
* Activity Browser by Bernhard Steubing
* OpenLCA (especially https://github.com/GreenDelta/olca-schema and https://github.com/GreenDelta/olca-ipc.py)

They all address some of the problems and should be analyzed and maybe integrated into any new effort. But none gives a user the flexibility yet usability of current LCA software and often extending proves complicated.

The ideal tool would present an API that is capable of returning entities the same way as e.g. Antelope, Brightway-UI and LCOPT. But it would allow for a relatively easy plugin mechanism to do e.g. sensitivity analyses, data quality checks, LCI blocks and much more, as well as result visualizations adapted to the use case.

# The idea
One way to ensure all of the above would be to use a "recipe" file for the whole LCA. This would describe the databases used, the user-defined processes, the LCIs and LCIAs as well as the result visualization. This file could then be versioned, shared, split as well as reused and reviewed. Comments and workflows could be integrated into that document. Scripts could use the document to generate reports, create html or pdf reports and so on.

An efficient way to create such a file could be an interactive web interface with a code editor, coupled with auto-complete options, buttons to insert/edit whole blocks of template text, and live result visualizations. But this front-end would be mostly decoupled from the backend, so that visual (click-and-drop) interfaces would be possible. Existing LCA software exports could also be translated to the file format.

# Proof of concept
Currently, a PoC has been programmed using a python backend based on brightway2 and a javascript frontend based on vue. The file was written in YAML as it is more human readable than JSON or XML, but could be easily switched to any other language. Very simple plugins to load databases, define processes and do LCI / LCIA calculations have been implemented.

# Next steps
The next step is to really define a format for:
* the plugin schemas and interactions
* the file structure and schema
* a standardized way to expose auto-complete and other user support for plugins from the plugin schema
* the general API
* the plugin API
It would be good to re-use as much as possible from LCOPT, Antelope and brightway2 (plus ui, web, api, etc.) while keeping the possibility to adress all points described above.