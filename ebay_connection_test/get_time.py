import requests
import xml.etree.ElementTree as ET
# eBay configuration API
ebay_url='https://api.sandbox.ebay.com/ws/api.dll'
headers={
            'X-EBAY-API-CALL-NAME' : 'GeteBayOfficialTime',
            'X-EBAY-API-APP-NAME' : 'EchoBay62-5538-466c-b43b-662768d6841',
            'X-EBAY-API-CERT-NAME' : '00dd08ab-2082-4e3c-9518-5f4298f296db',
            'X-EBAY-API-DEV-NAME' : '16a26b1b-26cf-442d-906d-597b60c41c19',
            'X-EBAY-API-SITEID': '0',
            'X-EBAY-API-COMPATIBILITY-LEVEL': '861'
        }
xml_data=open("api-data.xml","r")



response=requests.post(ebay_url, headers=headers, data=xml_data)
response_tree=ET.fromstring(response.text)
for child in response_tree:
    print(child.tag, child.text)
