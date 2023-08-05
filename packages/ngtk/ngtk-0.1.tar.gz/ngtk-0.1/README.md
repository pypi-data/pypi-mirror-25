# NGTK 🔧🔨

NGrok ToolKit

## current installation (w/in the package directory)
`pip3 install --editable .`


## Printing urls:

```bash
$ ngtk url
https://<...>.ngrok.io
http://<...>.ngrok.io
```

#### Pretty print urls:
```bash
$ ngtk url --pretty
------------------------
Port number of web service: 4040
https://<...>.ngrok.io
------------------------
Port number of web service: 4040
http://<...>.ngrok.io
```

#### Configure a different port for the webservice:
```bash
$ ngtk url -p <port_number>
------------------------
Port number of webservice: <port_number>
https://<...>.ngrok.io
------------------------
Port number of webservice: <port_number>
http://<...>.ngrok.io
```

#### Only print a single url from default
```bash
$ ngtk url --one
http://<...>.ngrok.io
```

----

### TODO
- [ ] Build python API for the click app to use
- [ ] Use nested subcommands
- [ ] Test using a config file with ngrok to utilize other API endpoints
- [ ] More features