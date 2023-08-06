Vapps CLI
=============================
This product allows users to use the command line to call VA master API functions by using simple commands. 

Installation
=============================

``
pip install vapps
``

Usage
============================
The first time you use the command, it will prompt you for a username, password and the URL of Your VA master. ::


    # vapps providers list
    Could not find a va_master configuration - either the --load-conf path is incorrect, or a configuration has not been generated yet. Please answer the following prompts : 
    Enter the va_master username : admin
    Enter the va_master password : admin
    Enter the VA master url. Include the http:// and the port, example : https://127.0.0.1:443
    VA master url : https://127.0.0.1:443

    [   {   'driver_name': u'vmware',
            'location': u'va_master',
            'provider_name': u'va-vmware'}]



After this, a config file is generated which will use the entered credentials. ::


    # vapps apps list available

    [   {   u'location': u'va_master',
            u'provider_name': u'va-vmware',
            u'provider_usage': {   u'used_cpus': 95.0,
                                   u'used_disk': 134.41,
                                   u'used_ram': 0.01,
                                   u'used_servers': 9},
            u'servers': [   {   u'hostname': u'server_hostname',
                                u'icon': u'fa-server',
                                u'ip': None,
                                u'provider': u'va-vmware',
                                u'size': u'va-small',
                                ...
                            }
                        ]
        }
    ]



Available Commands
=================================
providers
    list - Prints a list of all providers and their name, location and driver name. 

apps
    list 
        available - Prints a list of all apps. 
        running - Prints a list of all running apps. #Not yet implemented, also returns all apps. 

    directory #Not yet implemented

services
    list - Prints all consul services
        ok - Prints all services which returned with status "passing"
        critical - Prints all services which returned with status "critical"

vpn
    list - Lists all VPN users
    status - Returns the status of VPN users
    add - Creates a new VPN user
        --username The user will be created with this username. Example ``vapps vpn add --username new_vpn_user``
    get-cert - Prints the VPN certificate for the user
        --username The user for which the certificate is retrieved. Example ``vapps vpn get-cert --username some_vpn_user``
        


