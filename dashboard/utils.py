from accounts.models import MyUser
from .models import Contract, Supplier, Payment, WorkBoard, Client, Item, DraftItem, Draft, ItemSupplier, History
from datetime import datetime, timedelta
from random import randint, random
from time import time
from django.db import connection
from .const import SQL_UPDATE_SATISFIED, SQL_UPDATE_QUANTITY, SQL_UPDATE_FINISH_DRAFT, SQL_UPDATE_RESTORE_DRAFT, SQL_UPDATE_FINISH_CONTRACT, SQL_UPDATE_RESTORE_CONTRACT, SQL_GET_ITEM_SUPPLIER_PRICE, SQL_UPDATE_ITEM_DRAFT,SQL_UPDATE_ITEM_DRAFT_SATISFIED, SQL_GET_DRAFT_STATUS, SQL_SATISFY_ALL_POSSIBLE


def populate_db():
    populate_users()
    populate_contracts_and_client()
    populate_workboard()
    populate_payments()
    populate_supplier()
    populate_item()


def just_get_from_file(f_name):
    f = open(f_name, 'r', encoding='latin1')
    content = [i.rstrip("\n") for i in f.readlines()]
    f.close()
    return content


def get_supplier(i):
    suppliers = list()
    indexes = list()
    if i < 60:
        suppliers.append(Supplier.objects.get(pk=i + 1))
        indexes.append(i)
    k = randint(1,4)
    for d in range(k):
        u = randint(1,60)
        if u not in indexes:
            suppliers.append(Supplier.objects.get(pk=u))
            indexes.append(u)
    return suppliers


def populate_users():
    names = ['John Doll', 'Jane Smith', 'Jack Walter', 'Christian Drell', 'Ukima Dwell','Tim Toder', 'Samuel Spyce', 'Qween Treen', 'Dimitrij Shells', 'Katom Quell', 'Drigit Smith', 'Max Dell', 'Ibraghim Quanton']
    for i in range(1, 11):
        username = 'user{}'.format(i)
        name = names[i]
        if i == 1:                                            # 12345Qwerty#
            MyUser.objects.create(username=username, password='pbkdf2_sha256$150000$M8eDfHgRGYtc$Ax/1T4SXcpyq7GrQW46As80HpqKSIZhtTsNfO6v3/Ls=', email='email@some.com', name=name, status='Manager')
        else:
            MyUser.objects.create(username=username, password='pbkdf2_sha256$150000$M8eDfHgRGYtc$Ax/1T4SXcpyq7GrQW46As80HpqKSIZhtTsNfO6v3/Ls=', email='email@some.com', name=name, status='Agent')


def populate_workboard():
    for i in range(5):
        date = datetime.today() - timedelta(days=i)
        for k in range(1, 11):
            hours_amount = randint(0, 11)
            user = MyUser.objects.get(pk=k)
            WorkBoard.objects.create(userId=user, date=date, hoursamount=hours_amount)


def populate_contracts_and_client():
    names = ['Drigit Smith', 'Max Dell', 'Ibraghim Quanton', 'Idgit Queen', 'Sandor Duel']
    parts = just_get_from_file("parts.txt")
    for i in range(5):
        budget = randint(1000, 20000000)
        title = "Contract {}".format(i)
        content = "\nLorem ipsum dolor sit amet, consectetur adipiscing elit,\n sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris\n nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in\n voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint\n occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"*randint(1, 10)
        needed = generate_requirements()
        Contract.objects.create(content=content, budget=budget, title=title, needed=needed)
        Client.objects.create(name=names[i], phone="125551044{}".format(i), email="some{}@mail.com".format(i))
        client = Client.objects.get(pk=i+1)
        contract = Contract.objects.get(pk=i+1)
        client.contractss.add(contract)


def generate_requirements():
    content = "\n We need:"
    parts = just_get_from_file("parts.txt")
    parts_count = randint(1, len(parts)-1)
    for i in range(parts_count):
        index = randint(1, len(parts)-1)
        content += "\n{} {} \tprice {}$".format(i, parts[index], randint(1, 100))
        del parts[index]
    return content

def populate_payments():
    for i in range(10):
        payment = randint(100, 20000000)
        obj_id = randint(1, 5)
        date = datetime.now() - timedelta(days=randint(0, 100))
        contract = Contract.objects.get(pk=obj_id)
        if contract.budget - payment < 0:
            payment = payment - contract.budget
        if payment == 0:
            continue
        else:
            Payment.objects.create(contractId=contract, amount=payment, date=date)


def populate_supplier():
    companies = just_get_from_file("companies.txt")
    names = just_get_from_file("names.txt")
    for i in range(len(companies)):
        phone = "1114422{0:02d}".format(i)
        email = "email{0:02d}@corp.co".format(i)
        Supplier.objects.create(name=names[i], company_name=companies[i], phone=phone, email=email)


def populate_item():
    parts = just_get_from_file("parts.txt")
    print(parts)
    description = "This is a very long description of an automobile part: {}"
    supplier_len = len(Supplier.objects.all())
    for i in range(len(parts)):
        description.format(parts[i].upper())
        quantity = randint(0, 500)
        if 200 < quantity < 300:
            quantity = 0
        Item.objects.create(type=parts[i], description=description.format(parts[i]), quantity=quantity)
        item = Item.objects.get(pk=i+1)
        suppliers = get_supplier(i)
        for supplier in suppliers:
            ItemSupplier.objects.create(item=item, supplier=supplier, price=randint(50, 900000))


def analyse(text):
    p = text.split(':')[1].split("\n")[1:]
    s = [(p[i].split('\tprice ')[0].split("{}".format(i))[1].strip(), int(p[i].split('\tprice ')[1].rstrip("$").strip())) for i in range(len(p))]
    print(s)
    return s


def add_needed_items_to_draft(text, draft):
    print(text)
    items = analyse(text)
    print(items)
    for i,k in items:
        print("item here")
        print(i.rstrip())
        print(Item.objects.raw('SELECT id from dashboard_item WHERE type=%s',[i.rstrip()])[0])
        item = Item.objects.raw("SELECT id from dashboard_item WHERE type=%s",[i.rstrip()])[0]
        print("kkkk")
        DraftItem.objects.create(amount_needed=k, price=0, satisfied=False, draftId=draft, itemId=item)
    print("end")


def get_needed_items(pk):
    return DraftItem.objects.raw("SELECT dashboard_item.id, dashboard_draftitem.id as draftid, dashboard_draftitem.satisfied, dashboard_item.type FROM dashboard_draftitem INNER JOIN dashboard_item ON dashboard_draftitem.itemId_id=dashboard_item.id WHERE dashboard_draftitem.draftId_id=%s", [pk])


def check_item(did, ipk):
    print('check')
    d = Item.objects.raw(" SELECT dashboard_item.id, dashboard_draftitem.id as draftid, dashboard_draftitem.amount_needed, dashboard_draftitem.satisfied, dashboard_item.type, dashboard_item.quantity FROM dashboard_item INNER JOIN dashboard_draftitem ON dashboard_item.id=dashboard_draftitem.itemId_id WHERE dashboard_draftitem.draftId_id=%s AND dashboard_draftitem.id=%s AND dashboard_draftitem.satisfied=0", [did, ipk])[0]
    print(d.type)
    if d.amount_needed < d.quantity:
        return True, (d.amount_needed, d.quantity, d.draftid)
    return False, (0, 0, 0)


def satisfy_item(did, ipk):
    try:
        condition, values = check_item(did, ipk)
        if condition:
            val = values[1] - values[0]
            cursor_exec(SQL_UPDATE_SATISFIED % values[2])
            cursor_exec(SQL_UPDATE_QUANTITY % [val, values[2]])
            return True
    except Exception as e:
        print(e)
        return False
    return False


def finish_draft(ddd):
    #try:
    d = Draft.objects.raw(SQL_GET_DRAFT_STATUS % ddd)[0]
    print(d.done)
    if d.done:
        cursor_exec(SQL_UPDATE_RESTORE_DRAFT % ddd)
    else:
        cursor_exec(SQL_UPDATE_FINISH_DRAFT % ddd)
    finish_contract(d.contractid)
    return True
    #except Exception as e:
    #    print(e)
    return False


def finish_contract(contractId):
    c = Contract.objects.get(pk=contractId)
    if c.done:
        cursor_exec(SQL_UPDATE_RESTORE_CONTRACT % contractId)
    else:
        cursor_exec(SQL_UPDATE_FINISH_CONTRACT % contractId)
    return True

def satisfy_all_possible_items(did):
    items = DraftItem.objects.raw(SQL_SATISFY_ALL_POSSIBLE, [did])
    print(items)
    print('asf')
    for item in items:
        print(len(items))
        print(item.id)
        satisfy_item(did, item.id)


def cursor_exec(sql):
    with connection.cursor() as cur:
        cur.execute(sql)


def cursor_exec_get(sql):
    with connection.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()



def get_item_id(ipk):
    print('item')
    d = (DraftItem.objects.get(pk=ipk)).itemId_id
    print('utem')
    return d


def order_write(select, did, sid, ipk):
    p = ItemSupplier.objects.raw(SQL_GET_ITEM_SUPPLIER_PRICE, [get_item_id(ipk), sid])[0]
    price = p.price
    if random() < 0.5:
        price = (price + select) / 2
    print(p.price)
    print('uhi')
    cursor_exec(SQL_UPDATE_ITEM_DRAFT % (price, sid, did, get_item_id(ipk)))
    cursor_exec(SQL_UPDATE_ITEM_DRAFT_SATISFIED % ipk)


def update_text(pk, text):
    Draft.objects.filter(pk=pk).update(text=text)


def insert_history(text):
    History.objects.create(time=time(), message=text)








