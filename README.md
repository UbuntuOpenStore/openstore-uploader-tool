# open-uapp-tool
openstore (open.uappexplorer.com) manage tool

## Install

```
sudo ./setup.py install
```

## Usage:

open-uapp update [Click file] [Args] | Edit an app <br>
open-uapp new [Click file] [Args] | Create a new app <br>
open-uapp delete [app ID] | Delete an App <br>
open-uapp list | List all Apps <br>
open-uapp info [app ID] | Displays info about an App <br>
open-uapp config | List configs <br>
open-uapp config [Config] [Value] | Edit config <br>

## Args:

--changelog, -m
--license, -l
--source, -s
--description, -d
--category, -c
--tagline, -t

## Examples:

open-uapp update myawesomeapp.click <br>
open-uapp update myawesomeapp.click -l "GPL" -s http://github.com/myawesomeapp <br>
open-uapp new myawesomeapp.click <br>
open-uapp delete openstore.mzanetti <br>
open-uapp list <br>
open-uapp info openstore.mzanetti
