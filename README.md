# openstore-uploader-tool
OpenStore (open.uappexplorer.com) CLI manage tool

## Install

```
sudo ./setup.py install
```

## Usage:

usage: 'openstore-cli <command>'

This is the CLI tool for the OpenStore app store service. Manage or search
apps for your Ubuntu Touch device.

optional arguments:
  -h, --help            show this help message and exit

Commands:
    upload              Push a new package to the OpenStore server, as update
                        or new submission.

    update-info         Update remote informations of a package on the
                        OpenStore server

    search              Search an application available on the store (by its
                        id, name, keyword, or description

    info                Display information available for a single application

    add-api-key         Add your API key. Required for managing apps.
                        NOTE: You can also provide your API key by exporting the
                        'OPENSTORE_API_KEY' env.

    show-api-key        Show the API key available for this tool.

Run 'openstore-cli <command> help' to see the options available for each command.
