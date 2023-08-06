tinyj2
====== 
tiny renderer for jinja templates

Examples
--------

This README.md was rendered using tinyj2. There are several ways to render it:

#### Using environment variables
```bash
$ __description__="tiny renderer for jinja templates" tinyj2
```

#### Using params supplied via python dict formatted string:
```bash
$ tinyj2 -p "{'description':'tiny renderer for jinja templates'}"
```
#### Supplying params via json file
```bash
$ echo '{"description": "tiny renderer for jinja templates"}' > params.json
$ tinyj2 --json params.json
```
#### Supplying params via yaml file
```bash
$ echo 'description: tiny renderer for jinja templates' > params.yaml
$ tinyj2 --yaml params.yaml
```