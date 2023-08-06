tinyj2
======
{%- if env.__description__ is defined %}
{%- set description = env.__description__ %}
{%- elif description is not defined %}
{%- set description = 'tiny renderer for jinja templates' %}
{%- endif %} 
{{ description }}

Examples
--------

This README.md was rendered using tinyj2. There are several ways to render it:

#### Using environment variables
```bash
$ __description__="{{ description }}" tinyj2
```

#### Using params supplied via python dict formatted string:
```bash
$ tinyj2 -p "{'description':'{{ description }}'}"
```
{%- set types = {
  'json': '{"description": "%s"}' % description,
  'yaml': 'description: %s' % description,
} %}
{%- for type, sample_content in types.items() %}
#### Supplying params via {{ type }} file
```bash
$ echo '{{ sample_content }}' > params.{{ type }}
$ tinyj2 --{{ type }} params.{{ type }}
```
{%- endfor %}