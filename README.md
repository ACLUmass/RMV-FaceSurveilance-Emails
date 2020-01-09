# RMV-FaceSurveilance-Emails
NLP analysis of emails received from the RMV about facial surveillance

## Folder Structure
```
├── README.md
└── environment.yaml      - structured file containing all required Python packages and versions
```

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
