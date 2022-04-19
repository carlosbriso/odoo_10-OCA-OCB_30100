## :memo: odoo_10-OCA-OCB_30200

:pushpin: **odoo_10-OCA-OCB_30200 -> 30200_db-clean**
#### Configuración:

**odoo@hp ~/odoo_10 $** vim config/odoo_10_30200.cfg

**[options]**

#### # Inicial con addons estandares.
**#addons_path =** /opt/odoo/odoo_10/src/OCA/OCB/odoo/addons,/opt/odoo/odoo_10/src/OCA/OCB/addons

#### # Configuración cba.

**addons_path =** /opt/odoo/odoo_10/src/OCA/OCB/odoo/addons,/opt/odoo/odoo_10/src/OCA/OCB/addons,/opt/odoo/odoo_10/src/OCA,/opt/odoo/odoo_10/src/anb,/opt/odoo/odoo_10/src/ener,/opt/odoo/odoo_10/src/external,/opt/odoo/odoo_10/src/linked,/opt/odoo/odoo_10/src/others,/opt/odoo/odoo_10/src/muk

**db_name =** 30200_db-clean

**db_user =** odoo

**db_password =** odoo

**dbfilter =** ^30200_db-clean$

## cba -> por motivos de tails directos -> Debe COMENTARSE esta línea, para el debug. Despues debe DESCOMENTARSE de nuevo !!!.
## Debe crearse el archivo log asociado tambien => odoo_10_30200.log

**#logfile =** /opt/odoo/odoo_10/log/odoo_10_30200.log

**logrotate =** True

...

:pushpin: **Entorno Virtual -> virtualenv -> python2.7**

**odoo@hp ~/odoo_10 $** source odoo_10_30200-virtualenv/bin/activate

**(odoo_10_30200-virtualenv) odoo@hp ~/odoo_10 $** /opt/odoo/odoo_10/src/OCA/OCB/odoo-bin -c config/odoo_10_30200.cfg

:pushpin: **/etc/systemd/system/odoo_10_30200.service**

[Unit]

Description=Odoo 10.0 ERP server (cba) → 30200_db-clean → 30200/tcp => logs: /opt/odoo/odoo_10/log/odoo_10_30200.log

After=postgresql-12.service

[Service]

Type=simple

User=odoo

Group=odoo

ExecStart=/opt/odoo/odoo_10/odoo_10_30200-virtualenv/bin/python2.7 /opt/odoo/odoo_10/src/OCA/OCB/odoo-bin -c  /opt/odoo/odoo_10/config/odoo_10_30200.cfg

[Install]

WantedBy=multi-user.target


**(c) carlos briso (cba) - 2022**

