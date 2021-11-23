## :memo: odoo_10-OCA-OCB_30100

:pushpin: **odoo_10-OCA-OCB_30100 -> 30100_db-clean**
#### Configuración:

**anubia@hp ~/odoo_10 $** vim config/odoo_10_30100.cfg
[options]
#### # Inicial con addons estandares.
**#addons_path =** /opt/odoo/odoo_10/src/OCA/OCB/odoo/addons,/opt/odoo/odoo_10/src/OCA/OCB/addons

#### # Configuración cba.

**addons_path =** /opt/odoo/odoo_10/src/OCA/OCB/odoo/addons,/opt/odoo/odoo_10/src/OCA/OCB/addons,/opt/odoo/odoo_10/src/OCA,/opt/odoo/odoo_10/src/anb,/opt/odoo/odoo_10/src/ener,/opt/odoo/odoo_10/src/external,/opt/odoo/odoo_10/src/linked,/opt/odoo/odoo_10/src/others

**db_name =** 30100_db-clean

**dbfilter =** ^30100_db-clean$

**#logfile =** /opt/odoo/odoo_10/log/odoo_10_30100.log

:pushpin: **Entorno Virtual -> virtualenv -> python2.7**
**anubia@hp ~/odoo_10 $** source odoo_10_30100-virtualenv/bin/activate
**(odoo_10_30100-virtualenv) anubia@hp ~/odoo_10 $** /opt/odoo/odoo_10/src/OCA/OCB/odoo-bin -c config/odoo_10_30100.cfg

:pushpin: **/etc/systemd/system/odoo_10_30100.service**

[Unit]

Description=Odoo 10.0 ERP server (cba) → 30100_db-clean → 30100/tcp => logs: /opt/odoo/odoo_10/log/odoo_10_30100.log
After=postgresql-12.service

[Service]
Type=simple
User=anubia
Group=anubia

ExecStart=/opt/odoo/odoo_10/odoo_10-virtualenv/bin/python2.7 /opt/odoo/odoo_10/src/OCA/OCB/odoo-bin -c  /opt/odoo/odoo_10/config/odoo_10.cfg

[Install]
WantedBy=multi-user.target


**(c) carlos briso (cba) - 2021**

