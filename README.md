# POEditor exporter

This python command line script exports translations files from [POEditor](https://poeditor.com).

## Installation
To install the project with its dependencies run the following command.

```bash
pip install poeditorexporter
```

## Usage

```bash
python -m poeditorexporter api_token id languages dest filename type
```

### Arguments

#### Positional arguments

- `api_token` Your POEditor api token.
- `id` The id of your project.
- `languages` List of languages, separated by a comma.
- `dest` Destination directory of the downloaded files. It must end with a /
- `filename` Name of the file after download. The name will be suffixed by the language.
- `type` The file format. The accepted values are 'po', 'pot', 'mo', 'xls', 'xlsx', 'csv', 'ini', 'resw', 'resx',
'android_strings', 'apple_strings', 'xliff', 'properties', 'key_value_json', 'json', 'yml', 'xlf', 'xmb',
'xtb', 'arb', 'rise_360_xliff'.

Those arguments are mandatory. 

#### Optional arguments

- `-f` or `--filters` List of filters to apply on result, separated by a comma. Accepted values are 'translated',
'untranslated', 'fuzzy', 'not_fuzzy', 'automatic', 'not_automatic', 'proofread', 'not_proofread'.
- `-o` or `--order` How the terms should be ordered. Default is set to `terms`.
- `-t` or `--tags` Filter result by tags. List of tags separated by a comma.

### Print help

`python -m poeditorexporter --help`

### Example

```bash
python -m poeditorexporter 1a22cf9d548ebbdf1cb2b3bd10115a8c 12345 en,fr,de /home/user/downloads/ translation properties
```

This will download english, french and german translations file of project id 12345 in the folder `/home/user/downloads/`
with names `translation_en.properties`, `translation_fr.properties`, `translation_de.properties`.
