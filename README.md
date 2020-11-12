# web-library

[![Build Status](https://travis-ci.com/vnkrtv/web-library.svg?branch=master)](https://travis-ci.com/vnkrtv/web-library)
![Docker](https://github.com/vnkrtv/web-library/workflows/Docker/badge.svg)
![Ubuntu](https://github.com/vnkrtv/web-library/workflows/Ubuntu/badge.svg)


### Description  

App for adding and storing translations of various compositions.  
System features:
- adding various authors
- adding various authors' composition
- adding compositions' translations

All data stored in PostgreSQL, web app implemented in Django.

### Deploying

- ```git clone https://github.com/vnkrtv/web-library.git```
- ```cd web-library```
- ```./deploy/deploy_containers```

Collects container with app, configure it and configure docker-compose. If allowed will be added as a service in systemd as ```translation-lib.service```.

### Testing    
Run all tests with coverage by running (venv must be activated):   
- ```coverage run library/manage.py test main```

```
Name                         Stmts   Miss  Cover
------------------------------------------------
library/main/decorators.py       8      0   100%
library/main/forms.py           28      1    96%
library/main/models.py          44      5    89%
library/main/views.py           86      1    99%
------------------------------------------------
TOTAL                          166      7    96%
```
For detailed report run:
- ```coverage report```  
- ```coverage html```  
- ```x-www-browser ./htmlcov/index.html``` for Linux or ```Invoke-Expression .\htmlcov\index.html``` for Windows

### Code inspection

Run ```pylint library/main/*.py```:  
- ```Your code has been rated at 10.00/10```
