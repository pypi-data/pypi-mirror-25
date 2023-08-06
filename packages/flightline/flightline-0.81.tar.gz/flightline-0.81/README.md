# Flightline
Set of tools to help with Aerial Operation Projects using arcpy

Overall Logic
The overall logic is have all configs and settings stored in xml/json files to make it
easier for users to set it up for their local environment. The logic will be distributed throughout the python modules with minimal logic in the Python Toolbox tools.
When begining, a user creates a folder that defiens their project, from here the tools will generate and copy data/files into this project folder needed to run through the aerial project. A config.json file will keep track of project settings so they can be passed across toolbox tools.
The user then runs through tools to set the project up. Once setup they will run other tools whilst in the field supervising the aerial project. Then on return to the office the data from the project will be submitted to a central dataset.

## Rules
- Make the solution portable and easily implemented into any system running ArcMap.
- No hardcoding of configs/settings within python files (Instead store in json or config files)
- Usage of standard python libraries and arcpy to increase portability and remove dependencies.
- The Python Toolbox Tools should not house any major logic and should rely on the python modules.

## Pypi
This module has been loaded up into Pypi for easier distribution to users.
To build the distribution and load into Pypi run the following
(Make sure you have twine installed)
Open up cmd and change to flightline project folder
'CD ../Flightline'
'python setup.py sdist bdist_wheel'
'twine upload dist/* --skip-existing'

To install from Pypi
'pip install flightline' 


## Setup Python Toolbox
Set an environment variable Called ConfigurationPath and point it to a folder containing the ProjectSetup.json
'setx ConfigurationPath="T:\ArcGISToolboxes\Scripts\Configurations"'
From the flightline\data folder copy ProjectSetup.json to the Configurations folder and edit the path locations
within to match. The ProjectSetup.json should reference the .xml, .lyr and .json files located in the data
folder. You can copy these to a central location that users running the tool can access.
For ease of the user, copy the files out of the arctoolbox folder to an easily accessible folder,
this could be in the ArcGIS folder within the Users Documetns folder.
The tool is now all set to go.
