# script-handler
This is a python/GTK4 app for displaying and executing bash scripts that are organized in directories. Once set up, name and organize your bash scripts in directories within the "scripts" directory. The app will adopt the same names. Change the scripts directory within the script-handler.py file if you like. 

The app will display up to 12 scripts at a time, then you can cycle through more scripts using the carousel widget, which can be controlled with a mouse wheel or track pad (three fingers).

https://github.com/user-attachments/assets/4bd34217-629c-441b-9ecc-8f190a413313

## Install

Clone the repo

	git clone https://github.com/jessemcg/script-handler.git

Make sure the main script is executable:

	chmod +x $HOME/script-handler/script-handler.py
	
If using Gnome, assign a keyboard shortcut to the app by going to settings, keyboard, View and Customize Shortcuts, Custom Shortcuts:

	python $HOME/script-handler/script-handler.py
