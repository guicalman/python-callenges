import requests
import xml.etree.ElementTree as ET
import sqlite3
import os


def get_categories(db_name):
    # Define eBay configuration API url, headers, xml data
    ebay_url='https://api.sandbox.ebay.com/ws/api.dll'
    headers={
        'X-EBAY-API-CALL-NAME' : 'GetCategories',
        'X-EBAY-API-APP-NAME' : 'EchoBay62-5538-466c-b43b-662768d6841',
        'X-EBAY-API-CERT-NAME' : '00dd08ab-2082-4e3c-9518-5f4298f296db',
        'X-EBAY-API-DEV-NAME' : '16a26b1b-26cf-442d-906d-597b60c41c19',
        'X-EBAY-API-SITEID': '0',
        'X-EBAY-API-COMPATIBILITY-LEVEL': '861'
    }
    xml_data=open("api-data.xml","r")

    # Retrieves Category tree from eBay API
    response=requests.post(ebay_url, data=xml_data, headers=headers)
    resp_root=ET.fromstring(response.text)
    category_elemets=resp_root.findall('*/{urn:ebay:apis:eBLBaseComponents}Category')
    categories=[]

    # This loop iterates over all category elements and retreives a tuple with category children properties
    for category in category_elemets:
        id=category.find("{urn:ebay:apis:eBLBaseComponents}CategoryID").text
        name=category.find("{urn:ebay:apis:eBLBaseComponents}CategoryName").text
        level=category.find("{urn:ebay:apis:eBLBaseComponents}CategoryLevel").text
        parent_id=category.find("{urn:ebay:apis:eBLBaseComponents}CategoryParentID").text
        # Validations for values not present in all instances
        best_offer=category.find("{urn:ebay:apis:eBLBaseComponents}BestOfferEnabled")
        if best_offer == None:
            best_offer = 'false'
        else: best_offer = best_offer.text
        auto_pay=category.find("{urn:ebay:apis:eBLBaseComponents}AutoPayEnabled")
        if auto_pay == None:
            auto_pay = 'false'
        else:
            auto_pay = auto_pay.text
        category_tuple=(id,name, level, parent_id, best_offer, auto_pay)
        print(category_tuple, "tuple added")
        categories.append(category_tuple)

    # returns the categories list
    return categories


def create_db(name):
    # Checks if a file exists and deletes if it exists
    if os.path.isfile(name):
        os.remove(name)
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE categories (id, name, level, parent_id, best_offer, auto_pay)")


def get_subcategories(db_name, cat_id):
    sql_select="SELECT id, name, level, parent_id, best_offer, auto_pay FROM categories WHERE parent_id=? AND NOT id=?"
    conn = sqlite3.connect(db_name)
    cursor =conn.cursor()
    cursor.execute(sql_select, (cat_id,cat_id))
    subcategories=cursor.fetchall()
    sub_cat_list=[]
    if subcategories==None:
        return []
    else:
        for category in subcategories:
            temp_sub_cat={}
            temp_sub_cat['id']=category[0]
            temp_sub_cat['name']=category[1]
            temp_sub_cat['level']=category[2]
            temp_sub_cat['parent_id']=category[3]
            temp_sub_cat['best_offer']=category[4]
            temp_sub_cat['auto_pay']=category[5]
            sub_cat_list.append(temp_sub_cat)
        return sub_cat_list

def get_all_subcategories(db_name, root_cat):
    if root_cat['level'] < '6':
        #I am here
        pass


def get_category_dictionary(query_id, db_name):
    sql_select="SELECT id, name, level, parent_id, best_offer, auto_pay FROM categories WHERE id=?"
    conn = sqlite3.connect(db_name)
    cursor =conn.cursor()
    cursor.execute(sql_select, (query_id, ))
    category=cursor.fetchone()
    if(category==None):
        print("The categoy id {} doesn't exist".format(query_id))
    else:
        category_dic={}
        category_dic['id']=category[0]
        category_dic['name']=category[1]
        category_dic['level']=category[2]
        category_dic['parent_id']=category[3]
        category_dic['best_offer']=category[4]
        category_dic['auto_pay']=category[5]
        category_dic['subcategories']=get_subcategories(db_name,query_id)
        return category_dic



def db_controller(db_name, action):
    if(action=="create"):
        create_db(db_name)
    elif(action=="populate"):
        categories=get_categories(db_name)
        conn = sqlite3.connect(db_name)
        cursor =conn.cursor()
        cursor.executemany("INSERT INTO categories VALUES (?, ?, ?, ?, ?, ?)", categories)
        conn.commit()
    elif("query" in action):
        query_id=action.split(" ")[1]
        root_category = get_category_dictionary(query_id, db_name)
        hierarchy_dic = get_all_subcategories(root_category,db_name)


db_controller("example.db","query 2984")