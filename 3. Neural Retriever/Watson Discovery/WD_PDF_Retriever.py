import json
import os
import time
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

dwKey = os.getenv('WD_KEY')
# Discovery Setup
url = os.getenv('WD_URL')
project_name = 'SuperKnowa-extenstion'
collection_name = 'Whitepaper-1'
project_id = 'e32d0542-cccd-430b-9146-dd14dd687ea1'
collection_id = '9ed78dd6-bb73-dc82-0000-0188c5b1c0c9'

# Discovery Service Handling
authenticator = IAMAuthenticator(dwKey)
discovery = DiscoveryV2(
    version='2020-08-30',
    authenticator=authenticator
)
discovery.set_service_url(url)

# Add a document
filename = '1_55661.pdf'
path_element = ''
with open(os.path.join(os.getcwd(), path_element, filename),'rb') as fileinfo:
  response = discovery.add_document(
    project_id=project_id,
    collection_id=collection_id,
    file=fileinfo,
    filename='1_55661.pdf',
    file_content_type='application/pdf'
  ).get_result()
  print(json.dumps(response, indent=2))
  document_id = response.get("document_id")



# # Get document details
# response = discovery.get_document(
#     project_id=project_id,
#     collection_id=collection_id,
#     document_id="19272caf-e397-411c-9154-49869349c05e"
#     ).get_result()
# print(json.dumps(response, indent=2))


while True:
    # Get document details
    response = discovery.get_document(
        project_id=project_id,
        collection_id=collection_id,
        document_id=document_id
    ).get_result()

    # Check the status
    status = response.get("status")
    if status == "available":
        #Print the response and exit the loop
        print("Document is available. Now you can start asking the questions.")
        #print(json.dumps(response, indent=2))
        break
    else:
      print("Document still in process")

    #Wait for 15 seconds before making the next request
    time.sleep(15)