# codeChallenge
Application to manage certs

*******************************************
To install dependencies and environment run:
source installation.sh
*******************************************

*******************************************
Place the files inside the attached codeChallenge package inside cloudflare virtual environemnt
The directory structure needs to be like
--cd cloudflare/
      app/
	__init__.py
	createCert.py
	database.py
	scripts.sh
	tabledef.py
      run.py
      config.py


To start the server execute teh following environemnt inside the 
activated environemnt (souce bin/activate is part of the installation.sh script):
 python run.py
*******************************************

CURL Commands:

-Signup 
curl -H "Content-Type: application/json" -X POST -d '{"customer_name":"xyz","password":"xyz","customer_email":"xyz@mail.com"}' http://localhost:5000/signup-customer


-customer-signin
curl -H "Content-Type: application/json" -X POST -d '{"customer_email":"xyz@mail.com","password":"xyz"}' http://localhost:5000/customer-signin

-Delete customer 
curl -H "Content-Type: application/json" -X POST -d '{"customer_email":"xyz@mail.com","password":"xyz"}' http://localhost:5000/delete-customer


-/create-certificate
curl -H "Content-Type: application/json" -X POST -d '{"customer_email":"xyz@mail.com","password":"xyz","domain":"cloudflare","country":"USA"}' http://localhost:5000/create-certificate


-show-all-Certificates
curl -H "Content-Type: application/json" -X POST -d '{"customer_email":"xyz@mail.com","password":"xyz"}' http://localhost:5000/show-all-Certificates


-deactivate-certificate
curl -H "Content-Type: application/json" -X POST -d '{"customer_email":"xyz@mail.com","password":"xyz"}' http://localhost:5000/deactivate-certificate


-show-certificate
curl -H "Content-Type: application/json" -X POST -d '{"customer_email":"xyz@mail.com","password":"xyz","certificate_name":"102016_1131.key.org"}' http://localhost:5000/show-certificate
*******************************************

