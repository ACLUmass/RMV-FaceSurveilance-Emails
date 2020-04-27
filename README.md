# RMV-FaceSurveilance-Emails
NLP analysis of emails received from the RMV about facial surveillance

## Folder Structure
```
├── README.md
├── environment.yaml                - structured file containing all required Python packages and versions
├── *.txt                           - other files of random notes
├── exploration/                 
│   └── email_exploration.ipynb     - preliminary Jupyter notebook for email exploration
├── pdf_processing/
│   ├── pdf2json.py                 - program to convert all email pdf sources to one json object
│   ├── csv2json.py                 - program to convert facial recognition csv log sources to one json object
│   └── rmvDups.py                  - program to remove duplicate emails from json of all emails
└── data/        
    ├── json_structs.txt            - description of the json objects created from RMV sources
    ├── allMails.json               - output of pdf2json.py
    ├── allLogs.json                - output of csv2json.py
    ├── nodupsMail.json             - version of allMails.json with duplicates removed 
    └── src                         
        ├── mailList.json           - paths to all all the RMV pdfs in src to convert
        ├── logList.json            - paths to all all the RMV csv in src to convert
        ├── *.pdf                   - all the email pdf sources from the RMV
        └── *.csv                   - all the sheets from the Facial Recognition logs in csv form
```

## Architecture Considerations
Since the original data sources from the RMV are not saved on github, the json generating programs cannot be cloned and run on any machine. 
Only people with permission to download  those data sources from the ACLU's google drive (Lauren, Kade, Aaron and maybe others) can do that.

The json objects produced are described in data/src/json_structs.txt and should be usable by both pandas and tinyDB. 

## Development Environment

This project requires the following Python packages to run:

|Package          |Min. Version |
|-----------------|---------|
|chardet          |3.0.4    |   
|ipython          |7.11.1   |  
|jupyter          |1.0.0    |
|notebook         |6.0.1    |  
|pandas           |0.25.3   |
|pdfminer.six     |20181108 |
|pdfplumber       |0.5.14   |  
|Pillow           |6.2.1    |
|pycryptodome     |3.9.4    |   
|six              |1.13.0   |
|sortedcontainers |2.1.0    |   
|tabulate         |0.8.6    |
|unicodecsv       |0.14.1   |  
|Wand             |0.5.8    |

If you are managing virtual environments using ``conda``, these packages can be installed in a **Python 3** environment named "rmv_emails" with the following command:
```
    conda create -f environment.yaml
```
    
Or, if you want to update your environment due to changes to the environment::
```
    conda update -f environment.yaml 
```
