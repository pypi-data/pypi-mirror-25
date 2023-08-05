===========
Test SIM
===========

TEST SIM in sorted order

-----------

It fetches CNAME from hosted zone in Route53 and sorts them according to CNAME.
Generates a html page and update it onto the confluence page.

Pre-requisite
===============

Please get the below details and replace in the script:

* hosted-zone-id:  You can get this from AWS account

* CONFURL: This is the rest url of your confluence page

* CONFPAGEID:  This is the confluence pageid

* CONFUSERNAME, CONFPASSWORD: Confluence username and password

Execution & Output
-------------------

arjun$ python aws_cname.py

INFO:aws_cname.py:Fetching CNAME records from AWS account. This may take few minutes.

INFO:aws_cname.py:Fetching data succesful.

INFO:aws_cname.py:Proceeding data scrubbing.

INFO:aws_cname.py:Updating confluence page: https://CONFURL/AWS+Route+53+CNAME

INFO:aws_cname.py:Finish updating records
