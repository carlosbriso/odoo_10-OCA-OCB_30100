#!/bin/bash

log_file="/opt/odoo/odoo_10_30103/log/odoo_10.log"
if [[ -n $1 ]]; then
    log_file="$1"
fi

if [[ ! -f "${log_file}" ]]; then
    echo "Log file does not exist: ${log_file}"
    exit 1
fi

log='s/INFO/\o033[1;34m&\o033[0m/g'
statement='s/STATEMENT/\o033[1;34;40m&\o033[0m/g'
warning='s/WARNING/\o033[1;33m&\o033[0m/g'
error='s/ERROR/\o033[1;91m&\o033[0m/g'
debug='s/DEBUG/\o033[1;33m&\o033[0m/g'
 
colorization=$log';'$statement';'$warning';'$error';'$debug
 
tail -f "${log_file}" -n 100 | sed -e "$colorization"
