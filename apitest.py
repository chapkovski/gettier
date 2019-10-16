# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# # import urllib
# url = 'https://data.stadt-zuerich.ch/api/3/action/datastore_search?resource_id=29fcecbc-e2dd-44dc-9fb2-b24edd5f8c50&limit=5&q=title:jones'
# # fileobj = urllib.urlopen(url)
# #
# import urllib.request
# #
# with urllib.request.urlopen(url) as urllink:
#     s = urllink.read()
#     # I'm guessing this would output the html source code ?
#     print(s)

import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


from urllib.request import urlopen

url = """https://data.stadt-zuerich.ch/api/3/action/datastore_search_sql?sql=SELECT * from "29fcecbc-e2dd-44dc-9fb2-b24edd5f8c50" WHERE title LIKE 'jones'"""
resp = urlopen(url,context=ctx)
print(resp.read())
