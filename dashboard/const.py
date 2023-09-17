


SQL_1_GET_CLIENT_CONTACT = "SELECT dashboard_client.name, dashboard_contract.title FROM dashboard_client_contractss LEFT JOIN dashboard_client ON dashboard_client_contractss.client_id=dashboard_client.id LEFT JOIN dashboard_contract ON dashboard_client_contractss.contract_id=dashboard_contract.id"
SQL_2_GET_NAME_LIKE_EMAIL = "SELECT name FROM dashboard_client WHERE email LIKE '%{}%'"
SQL_2_GET_TITLE_LIKE_PART = "select title FROM dashboard_contract WHERE needed LIKE '%%s%%'"   # strip %
SQL_3_GET_PAYMENTS_BETWEEN_DATE = "SELECT * FROM dashboard_payment WHERE date BETWEEN '{}' AND '{}'"  # '2019-10-01' AND '2019-10-30';"
SQL_3_GET_ACCOUNT_BETWEEN_DATE = "select accounts_myuser.name, dashboard_workboard.hoursamount, dashboard_workboard.id FROM accounts_myuser INNER JOIN dashboard_workboard ON accounts_myuser.id=dashboard_workboard.userId_id WHERE dashboard_workboard.date BETWEEN '{}' AND '{}'" # '2019-12-01' AND '2019-12-03'"
SQL_4_SUM_DRAFT_PRICE = "SELECT dashboard_draft.title, SUM(dashboard_draftitem.price), dashboard_draft.id FROM dashboard_draft LEFT JOIN dashboard_draftitem ON dashboard_draft.id=dashboard_draftitem.draftId_id WHERE draftId_id={}"
SQL_4_AVG_USER_HOUR_AMOUNT = "select accounts_myuser.name, AVG(dashboard_workboard.hoursamount) FROM dashboard_workboard LEFT JOIN accounts_myuser ON accounts_myuser.id=dashboard_workboard.userId_id where userId_id={}"
SQL_5_SUM_GROUP_PAYED_CONTRACT = "SELECT dashboard_client.name, dashboard_contract.title, SUM(dashboard_payment.amount) FROM dashboard_client_contractss LEFT JOIN dashboard_contract ON dashboard_client_contractss.contract_id=dashboard_contract.id LEFT JOIN dashboard_payment ON dashboard_payment.contractId_id=dashboard_client_contractss.contract_id LEFT JOIN dashboard_client ON dashboard_client_contractss.client_id=dashboard_client.id GROUP BY dashboard_contract.id"
SQL_5_AVG_GROUP_USER_HOUR_AMOUNT = "select accounts_myuser.name, AVG(dashboard_workboard.hoursamount) FROM dashboard_workboard LEFT JOIN accounts_myuser ON accounts_myuser.id=dashboard_workboard.userId_id group by accounts_myuser.id;"
SQL_8_SELECT_LEFT_NOT_IN_CLIENT_NOT_PAYED = "SELECT dashboard_client.name FROM dashboard_client LEFT JOIN (select client_id as cl FROM dashboard_client_contractss where contract_id not in (select contractId_id from dashboard_payment)) ss ON ss.cl=dashboard_client.id WHERE dashboard_client.id=ss.cl;"
SQL_8_SELECT_USER_NOT_PRESENT = "select accounts_myuser.name from accounts_myuser where accounts_myuser.id not in (select userId_id from dashboard_workboard)"
SQL_9_CORRELATED = "select userId_id from dashboard_workboard d where hoursamount = ( SELECT AVG(hoursamount) FROM dashboard_workboard) GROUP BY userId_id;"
SQL_9_CORR = "select contractId_id from dashboard_payment where amount = (select MAX(amount) from dashboard_payment);"
SQL_10_1 = "UPDATE dashboard_draftitem SET price=%s, supplierId_id=%s WHERE draftId_id IN (SELECT id from dashboard_draft where done=0)"
SQL_10_2 = "update dashboard_contract set done=0 where id in (select contractId from dashboard_draft where done=0)"
SQL_11_1 = 'SELECT id, "Done" as comment from dashboard_draft where done =1 UNION Select id, "Not done" as comment from dashboard_draft where done=0'
SQL_11_2 = 'SELECT id, "Done" as comment from dashboard_contract where done =1 UNION Select id, "Not done" as comment from dashboard_contract where done=0;'


SQL_UPDATE_SATISFIED = "UPDATE dashboard_draftitem SET satisfied = 1 WHERE id=%s"               # 10
SQL_UPDATE_QUANTITY = "UPDATE dashboard_item SET quantity=%s WHERE id=%s"
SQL_UPDATE_FINISH_DRAFT = "UPDATE dashboard_draft SET done = 1 WHERE id=%s"
SQL_UPDATE_RESTORE_DRAFT = "UPDATE dashboard_draft SET done = 0 WHERE id=%s"
SQL_UPDATE_FINISH_CONTRACT = "update dashboard_contract set done=1 where id=%s"
SQL_UPDATE_RESTORE_CONTRACT = "update dashboard_contract set done=0 where id=%s"
SQL_GET_ITEM_SUPPLIER_PRICE = "select id, price from dashboard_itemsupplier where item_id=%s and supplier_id=%s"
SQL_UPDATE_ITEM_DRAFT = " UPDATE dashboard_draftitem SET price=%s, supplierId_id=%s WHERE draftId_id=%s and itemId_id=%s" # 10
SQL_UPDATE_ITEM_DRAFT_SATISFIED = "UPDATE dashboard_draftitem SET satisfied = 1 WHERE id=%s"
SQL_GET_DRAFT_STATUS = "SELECT id, done, contractId_id as contractid FROM dashboard_draft WHERE id=%s"
SQL_SATISFY_ALL_POSSIBLE = "SELECT id, itemId_id as itemid from dashboard_draftitem where draftId_id = %s"




DRAFTS_DETAIL_REDIRECT = "/dashboard/drafts/{}"
DRAFTS_MANAGEMENT_DETAIL_REDIRECT = "/management/drafts/{}"
MANAGEMENT_REDIRECT = "/management/stats/"
HISTORY_STRING = "User - {} - {} {}"
SQL_SELECT_SUPPLIERS_BY_ITEM = "SELECT * from dashboard_supplier WHERE id IN (SELECT supplier_id FROM dashboard_itemsupplier WHERE item_id=%s)"           # 7
SQL_GET_DRAFTS_BY_USER = "SELECT * FROM dashboard_draft d WHERE d.contractId_id IN (SELECT id FROM dashboard_contract c WHERE c.userId_id=%s)"            # 7
SQL_GET_SUPPLIER_ITEM = "SELECT dashboard_supplier.id, dashboard_supplier.name, dashboard_supplier.email, dashboard_supplier.company_name, dashboard_itemsupplier.id as itemsupid, dashboard_itemsupplier.price FROM dashboard_supplier INNER JOIN dashboard_itemsupplier ON dashboard_supplier.id=dashboard_itemsupplier.supplier_id WHERE dashboard_itemsupplier.item_id=%s"
SQL_GET_CONTRACT_BY_USER = "select * from dashboard_contract where taken=0 or (taken=1 and done=1 and userId_id=%s)"








