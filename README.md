Using Python to call the API ZABBIX interface, in the Baidu map shows the status of different regions of the firewall.
-------------------------------------

These code need python 2.7.9.

Operating environment in the requirement.txt in a detailed list.
        
        #pip install -r requirement.txt

Most of the settings are completed in the Config.py file. This is defined by yourself.

How to run the program?

DebugMode:

        #python manage.py runserver -t 0.0.0.0 -p 80

Production Environment:

        Flask+uWSGI+nginx, Publishing the program !
