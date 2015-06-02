# open-uapp-tool
openstore (open.uappexplorer.com) manage tool

# Install

``` 
sudo ./setup.py install
```

# Usage

Usage:
open-uapp update [app ID] [keys splited by ,] "[values splited by , (in the same order as keys)]" | Edit an app
open-uapp new | Create a new app
open-uapp delete [app ID] | Delete an App
open-uapp list | List all Apps
open-uapp info [app ID] Displays info about an App

Examples:
open-uapp update openstore.mzanetti name,version,package "testapp,0.1,build/package"
open-uapp new
open-uapp delete openstore.mzanetti
open-uapp list
open-uapp info openstore.mzanetti
