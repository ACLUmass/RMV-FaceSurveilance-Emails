# Aaron's Files

Files that Aaron alone contributes to live here.

## Folder Structure
```
├── README.md
├── pdf2json.py           - program to convert all email pdf sources to one json object
├── mailList.json         - paths to all all the RMV pds in src to convert
├── allMails.json         - output of pdf2json.py because the sources to generate it are not
├── csv2json.py           - program to convert facial recognition csv log sources to one json object
├── logList.json          - paths to all all the RMV csv in src to convert
├── allLogs.json          - output of csv2json.py because the sources to generate it are not
├── src                   - not saved on github because they are confidential documents
│   ├── *.pdf             - all the email pdf sources from the RMV
│   └── *.csv             - all the sheets from the Facial Recognition logs in csv form
└── int_docs              - internal documents
    ├── json_structs.txt  - description of the json objects created from RMV sources
    └── *.txt             - other files of random notes
```
## Architecture Considerations
Since the original data sources from the RMV are not saved on github, the json generating programs cannot be cloned and run on any machine. Only people with permission to download  those data srouces from the ACLU's google drive (Lauren, Kade, me and maybe others) can do that.

The json objects produced are described in int_docs/json_structs.txt and should be usable by both pandas and tinyDB. 

### Deveopment Environment
I am using a python 3 virtual environment because my other projects use python 2.7. These are the packages and I have no idea if this code works in any other environment 
Package            Version 
------------------ --------
* python           3.7.0
* chardet          3.0.4   
* pdfminer.six     20181108
* pdfplumber       0.5.14  
* Pillow           6.2.1   
* pip              19.3.1  
* pycryptodome     3.9.4   
* setuptools       43.0.0  
* six              1.13.0  
* sortedcontainers 2.1.0   
* tabulate         0.8.6   
* unicodecsv       0.14.1  
* Wand             0.5.8   
* wheel            0.33.6  

