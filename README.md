# dhtc-server

[dhtc](https://github.com/nbdy/dhtc) ui part with api endpoints

## usage

```shell
(venv) nbdy@c0:~$ python3 dhtc-server --help
usage: [-h] [--host HOST] [--port PORT]

options:
  -h, --help   show this help message and exit
  --host HOST  server address
  --port PORT  server port
```

## api routes

| method | route             | post data                                                                                                                                                                                                                              | example response                                                                                                                                                                                                                              |
|--------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POST   | /api/v1/add       | {'InfoHash': 'vB45fhNgNHZEfPDDI397UYa+g2U=', 'Name': 'Ready Player One.2O18.HDRip.28OOMB.avi', 'TotalSize': 2941046784, 'DiscoveredOn': 1657403279, 'Files': [{'size': 2941046784, 'path': 'Ready Player One.2O18.HDRip.28OOMB.avi'}]} | {"error": false}                                                                                                                                                                                                                              |
| POST   | /api/v1/search    | {'key': "Name", 'query': "Ready Player"}                                                                                                                                                                                               | [{'InfoHash': 'vB45fhNgNHZEfPDDI397UYa+g2U=', 'Name': 'Ready Player One.2O18.HDRip.28OOMB.avi', 'TotalSize': 2941046784, 'DiscoveredOn': 1657403279, 'Files': [{'size': 2941046784, 'path': 'Ready Player One.2O18.HDRip.28OOMB.avi'}]}, ...] |
| GET    | /api/v1/blacklist |                                                                                                                                                                                                                                        | {"blacklist":[{"created":"Sat, 09 Jul 2022 23:32:15 GMT","last_modified":"Sat, 09 Jul 2022 23:32:15 GMT","match_type":"0","regex":"asdfasd","table":"blacklist","uuid":"db9098de-3e3e-4085-99ab-7dddf5a4516c"}, ..]}                          |
