Standalone CLI command
++++++++++++++++++++++

::

  Usage: najdisi-sms -u username -p password  reciever_NUM  MESSAGE

  Options:
    -h, --help            show this help message and exit
    -u USERNAME, --username=USERNAME
                          Username
    -p PASSWORD, --password=PASSWORD
                          Password
    -A USERAGENT, --useragent=USERAGENT
                          HTTP User Agent

Example::

  najdisi-sms -u brodul -p FUBAR_PASS 031123456 "Pikica, rad te mam. (sent from cronjob)"
