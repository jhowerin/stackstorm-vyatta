himport requests
import warnings
import json

from st2client.client import Client
from st2client.models import KeyValuePair

from st2actions.runners.pythonrunner import Action

class showIpRouteSubnet(Action):
    def run(self, deviceIP, subnet):
        
        # Fetching device credentials based on keys derived from deviceIP 
        #################################################################
        user_key_name = deviceIP + "_user"
        pswd_key_name = deviceIP + "_pswd"
        print("\n")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Looking for credentials: Fetching values for keys " + user_key_name + " and " + pswd_key_name)
        client = Client()
        keys = client.keys.get_all()
        try:
            user = (client.keys.get_by_name(user_key_name)).value
            pswd = (client.keys.get_by_name(pswd_key_name)).value
            print("     Obtained from KV store: user = " + user)
            print("     Obtained from KV store: pswd = " + pswd)
        except:
            return (False, "No credentials for : " + deviceIP)

        # Preapring the URL request 
        #################################################################
        headers = {
            "accept": "application/json",
            "content-length": "0"
        }

        subnet = subnet.replace("/", "%2F")
        url_base = "https://" + deviceIP + "/rest/op/"
        url = url_base + "show/ip/route/" + subnet

        # Sending the URL call(s)
        #################################################################
        print("Sending REST call(s):")
        print("     POST            " + url)
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cmd_response = requests.post(url, auth=(user, pswd), headers=headers, verify=False)
            cmd_response_code = str(cmd_response.status_code)
            print("     Response code:   " + cmd_response_code)
            cmd_response_code = int(cmd_response.status_code)
            if cmd_response_code != 201:
                return (False, cmd_response_code)
            else:
                cmd_path = cmd_response.headers["Location"]
                url = "https://" + deviceIP + "/" + cmd_path
                print("     GET             " + url)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    output_response = requests.get(url, auth=(user, pswd), headers=headers, verify=False)
                    output_response_code = str(output_response.status_code)
                    print("     Response code:   " + output_response_code)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    output_response_code = int(output_response.status_code)
                    if output_response_code != 200:
                        return (False, output_response_code)
                    else:
                        try:
                            print("\n")
                            print output_response.text
                        except:
                            print ("     Response body: empty")