
import ndex.client as nc
import time


ndex_network_resource = "/v2/network/"


def set_provenance_and_profile():

        ndex_server = "http://dev2.ndexbio.org"

        network_UUID = "e144cc43-5797-11e7-a2e2-0660b7976219"

        ndex = nc.Ndex(host=ndex_server, username="aaa", password="aaa", debug=True)

        update_start_time = int(round(time.time() * 1000))

        #update your network here
        #ndex.update_cx_network(...)
        #sleep(..)
        #update version
        #ndex.update_network_profile(...)

        networkURI = ndex_server + ndex_network_resource + network_UUID + "/summary"
        new_provenance =  {
            "uri": networkURI,
            "creationEvent": {
                "eventType": "Update Network",
                "startedAtTime": update_start_time,
                "endAtTime": int(round(time.time() * 1000)),
                "inputs": [
                    { "uri": networkURI,
                      "properties": [],
                      "creationEvent":{
                          "eventType": "Create Network",
                          # "startedAtTime": network_creation_time,
                          # "endAtTime": network_creation_time,
                          "inputs": []
                      }
                    }
                    ]
            },
            "properties": [ {
                "name": "update_count",
                "value": "400"
            }]
        }


        ndex.set_provenance(network_UUID, new_provenance)

if __name__ == '__main__':
    set_provenance_and_profile ()
