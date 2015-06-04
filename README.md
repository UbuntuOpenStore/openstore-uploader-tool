# open-uapp-tool
openstore (open.uappexplorer.com) manage tool

## Install

``` 
pip install smartfile
sudo ./setup.py install
```

## Usage:

open-uapp update [app ID] [keys splited by ,] "[values splited by , (in the same order as keys)]" | Edit an app <br>
open-uapp new | Create a new app <br>
open-uapp delete [app ID] | Delete an App <br>
open-uapp list | List all Apps <br>
open-uapp info [app ID] | Displays info about an App <br>
open-uapp config | List configs <br>
open-uapp config [Config] [Value] | Edit config <br>
open-uapp keys | List repo keys 

## Examples:

open-uapp update openstore.mzanetti name,version,package "testapp,0.1,build/package" <br>
open-uapp new <br>
open-uapp delete openstore.mzanetti <br>
open-uapp list <br>
open-uapp info openstore.mzanetti 
