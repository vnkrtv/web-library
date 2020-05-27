# web-library

### Description  

App for adding and storing translations of various compositions.  
System features:
- adding various authors
- adding various authors' composition
- adding compositions' translations

All data stored in PostgreSQL, web app implemented in Django.

### Deploying

- ```git clone https://github.com/LeadNess/web-library.git```
- ```cd web-library```
- ```./deploy/deploy_containers```

Collects container with app, configure it and configure docker-composite. If allowed will be added as a service in systemd as ```translation-lib.service```.