import re, logging
import urllib
import urllib.request
from urllib.parse import urlencode
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

logging.getLogger(name=__name__)


class SteamSignIn():
    _provider = 'https://steamcommunity.com/openid/login'

    def RedirectUser(self, strPostData):
        return RedirectResponse(url="{0}?{1}".format(self._provider, strPostData),
                                status_code=HTTP_303_SEE_OTHER,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def ConstructURL(self, responseURL):
        refinedScripts = re.search('(?:http)', responseURL)
        if refinedScripts == None or refinedScripts.group(0) == None:
            responseURL = "http://{0}".format(responseURL)

        authParameters = {
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.mode": "checkid_setup",
            "openid.return_to": responseURL,
            "openid.realm": responseURL,
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
        }

        return urlencode(authParameters)

    def ValidateResults(self, results):

        validationArgs = {
            'openid.assoc_handle': results['openid.assoc_handle'],
            'openid.signed': results['openid.signed'],
            'openid.sig': results['openid.sig'],
            'openid.ns': results['openid.ns']
        }

        signedArgs = results['openid.signed'].split(',')

        for item in signedArgs:
            itemArg = 'openid.{0}'.format(item)
            if results[itemArg] not in validationArgs:
                validationArgs[itemArg] = results[itemArg]

        validationArgs['openid.mode'] = 'check_authentication'
        parsedArgs = urlencode(validationArgs).encode("utf-8")

        with urllib.request.urlopen(self._provider, parsedArgs) as requestData:
            responseData = requestData.read().decode('utf-8')
        if re.search('is_valid:true', responseData):
            matched64ID = re.search('https://steamcommunity.com/openid/id/(\d+)', results['openid.claimed_id'])
            if matched64ID != None or matched64ID.group(1) != None:
                return matched64ID.group(1)
            else:
                return False
        else:
            return False
