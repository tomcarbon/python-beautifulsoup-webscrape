##############################################
# Beautiful Soup HTML to JSON converter
##############################################
import sys
import urllib
from bs4 import BeautifulSoup
import json


#########################################
# syntax_text ():
# display generic instructions
#########################################
def syntax_text (): 
    print "SYNTAX: python bsoup.py inputfile.html [outputfile.json]"
    print "The output file parameter is optional. If no outputfile is specified, output.json will be used."
    print "On success, this program creates the specified output file."
    return

########################
# Here's the main event.
# What's expected:
# customer (name, phone)
# customer_order_id (8d-7d)
# menu_items (id, item_name, price, quantity)
# restaurant (restaurant_name)
########################
print "PROGRAM: Perform BeautifulSoup parsing on given html file."

arguments = len(sys.argv) - 1
if arguments == 0:
    syntax_text() 
    print "ERROR: You must provide at least an input file."
    print "Exiting."
    sys.exit()

fin = sys.argv[1]
if arguments == 1:
    fout = "output.json"
else: 
    fout = sys.argv[2]

soup = BeautifulSoup(open(fin), 'html.parser')
order = list()

c1 = soup.find(id="cust_service_info")
c2 = c1.text.strip()
cust_order_id = c2[6:]

restaurant_name = soup.find(attrs={"data-field": "restaurant-name"})

phone = soup.find(attrs={"data-field": "phone"})

# get the customer name, do some validation here
table = soup.find(lambda tag: tag.name=='table')
rows = list()
for row in table.findAll(lambda tag: tag.name=='tr'):
    rows.append(row)
d1 = rows[0].text.strip() #this value is expected to be = 'Deliver to:'
if "Deliver to:" not in d1:
    syntax_text()
    print("ERROR: customer name not found. Expecting 'Deliver to:'. Found %s" % d1)
    sys.exit()
cust_name = rows[1].text.strip()        #The field after "Deliver To:" contains the name

#get all the ordering data
orderinfo = list()
for dat in soup.findAll(lambda tag: tag.name == 'div', {"data-section":"menu-item"}):
    menu_item_name = dat.find(attrs={"data-field": "menu-item-name"})
    quantity = dat.find(attrs={"data-field": "quantity"})
    p1 = dat.find(attrs={"data-field": "price"})
    p2 = p1.text.strip()
    price = p2[1:]
    menu_item_id = dat.find(attrs={"data-field": "menu-item-name"})['menu-item-id']
    orderinfo.append({"id":int(menu_item_id), "item_name": menu_item_name.text.strip(), "price": float(price), "quantity": int(quantity.text.strip())})
orderinfo_sorted = sorted(orderinfo)

order = {"restaurant":{"restaurant_name":restaurant_name.text.strip()},"customer": {"name": cust_name, "phone": phone.text.strip()},"customer_order_id": cust_order_id,"menu_items":orderinfo_sorted}

with open(fout, 'w') as outfile:
    json.dump(order, outfile, indent=4, sort_keys=True)


print ("The file %s has been created" % fout)
print "The bsoup program has completed successfully."
print "Exiting."
