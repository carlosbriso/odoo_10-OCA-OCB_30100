#!/bin/bash

links_path="/opt/odoo/odoo_10_30103/src/linked"
links_path="$(readlink -f ${links_path})"
src_path='/opt/odoo/odoo_10_30103/src'  # './OCA'
mkdir -p ${links_path}
dir_skip1="__unported__"
dir_skip2="__unreviewed__"
dir_skip3="tests"
declare -i modules_total=0
declare -i modules_linked=0
declare -i modules_skipped=0

echo "---> START LINKING!"
echo "Odoo modules source path: ${src_path}"
echo "Odoo linked modules path: ${links_path}"
cd "${src_path}"
pwd

declare -a modules=$(find -type f -name "__manifest__.py" | sort -r)
for manifest in ${modules[@]}; do
    module_path="$(dirname $(readlink -f ${manifest}))"
    echo "PATH: ${module_path}"
    unported=`echo ${module_path} | grep -c "${dir_skip1}"`
    unreviewed=`echo ${module_path} | grep -c "${dir_skip2}"`
    tests=`echo ${module_path} | grep -c "${dir_skip3}"`
#     echo "A> ${unported}"
#     echo "B> ${unreviewed}"
#     echo "C> ${tests}"
    modules_total+=1
    module_name="$(basename ${module_path})"
    if [[ "${unported}" != "0" || "${unreviewed}" != "0" || "${tests}" != "0" ]] ; then
        echo "-- > Skipped: ${module_name}"
        modules_skipped+=1
        continue
    else
        echo "OK > LINKING: ${module_name}"
        ln -s "${module_path}" "${links_path}"
        modules_linked+=1
    fi
    echo "L/S (T): ${modules_linked}/${modules_skipped} (${modules_total})"
done

# Remove specific modules
# rm "${links_path}/"
rm "${links_path}/account_invoice_insulation"
rm "${links_path}/procurement_insulation"
rm "${links_path}/product_insulation"
rm "${links_path}/sale_insulation"
rm "${links_path}/stock_picking_delivery_insulation"
rm "${links_path}/exportsage50"

# For italian localization, you need to install:
# sudo pip install codicefiscale
# Otherwise, remove:
# rm "${links_path}/account_invoice_entry_date"
# rm "${links_path}/l10n_it_ateco"
# rm "${links_path}/l10n_it_base"
# rm "${links_path}/l10n_it_base_location_geonames_import"
# rm "${links_path}/l10n_it_fiscalcode"
# rm "${links_path}/l10n_it_pec"

# So far, module ./OCA/connector-ecommerce/__unported__/connector_ecommerce
# is not ported yet, so:
rm "${links_path}/prestashoperpconnect"
rm "${links_path}/prestashoperpconnect_catalog_manager"
rm "${links_path}/prestashoperpconnect_customize_example"

# If not specifically needed, remove magento connector,
# as it has magento itself as a required depend.
rm "${links_path}/customize_example"
rm "${links_path}/magentoerpconnect"

# Reove except needed, it has many depends
rm "${links_path}/base_external_dbsource"


# Not a real modules, but test  modules:
# OCA/OCB/addons/base_import_module/tests/test_module
rm "${links_path}/test_module"

rm "${links_path}/account_banking_tests"
rm "${links_path}/test_translation_import"
rm "${links_path}/test_module"
rm "${links_path}/web_tests_demo"
rm "${links_path}/runbot_skip_tests"
rm "${links_path}/test_module"
rm "${links_path}/broken_module"
rm "${links_path}/second_module"

# para que linke el l10n_es adecuado
rm "${links_path}/l10n_es"
ln -s "${src_path}/OCA/l10n-spain/l10n_es" "${links_path}/l10n_es"

echo "---"
echo "Odoo modules source path: ${src_path}"
echo "Odoo linked modules path: ${links_path}"
echo "---"
echo "Linked modules : ${modules_skipped}"
echo "Skipped modules: ${modules_linked}"
echo "Total modules  : ${modules_total}"
echo "---"
echo "---> ENDED LINKING!"

