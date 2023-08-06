from sandstone.lib.handlers.base import BaseHandler
from sandstone import settings
import requests
import os

class JupyterHubLoginHandler(BaseHandler):

    def verify_token(self, cookie_name, encrypted_cookie, verify):
        """method for token verification"""
        # adapted from
        # https://github.com/jupyterhub/jupyterhub/blob/30469710648e4a94b6a200fd470d9746bbda24dc/scripts/jupyterhub-singleuser#L52

        api_token = os.environ['JUPYTERHUB_API_TOKEN']
        hub_api_url = os.environ['JUPYTERHUB_API_URL']

        url = '{hub_url}/authorizations/cookie/{cookie_name}/{cookie_value}'.format(
            hub_url=hub_api_url,
            cookie_name=cookie_name,
            cookie_value=encrypted_cookie,
        )

        r = requests.get(
            url,
            headers = {'Authorization' : 'token %s' % api_token},
            verify = verify
        )

        if r.status_code == 404:
            data = None
        elif r.status_code == 403:
            self.log.error("I don't have permission to verify cookies, my auth token may have expired: [%i] %s", r.status_code, r.reason)
            raise HTTPError(500, "Permission failure checking authorization, I may need to be restarted")
        elif r.status_code >= 500:
            self.log.error("Upstream failure verifying auth token: [%i] %s", r.status_code, r.reason)
            raise HTTPError(502, "Failed to check authorization (upstream problem)")
        elif r.status_code >= 400:
            self.log.warn("Failed to check authorization: [%i] %s", r.status_code, r.reason)
            raise HTTPError(500, "Failed to check authorization")
        else:
            data = r.json()
        return data


    def get(self):
        # The XSRF token must be manually set in the absence of
        # a web form. Accessing the property is enough to set it.
        self.xsrf_token

        api_token = os.environ['JUPYTERHUB_API_TOKEN']
        hub_api_url = os.environ['JUPYTERHUB_API_URL']
        cookie_name = os.environ['JUPYTERHUB_COOKIE_NAME']

        # Has user deconfigured certificate verification?
        verify = getattr(settings,'VERIFY_JH_CERT',True)

        encrypted_cookie = self.get_cookie(cookie_name)

        if encrypted_cookie:
            auth_data = self.verify_token(cookie_name, encrypted_cookie, verify)
            if auth_data:
                username = auth_data['name']
            else:
                username = None
        else:
            username = None

        if username:
            self.set_secure_cookie('user', username)
            self.redirect('/user/{}'.format(username))
        else:
            self.set_status(403)
            self.finish()


class JupyterHubLogoutHandler(BaseHandler):
    def get(self):
        # clear the user cookie
        self.clear_cookie('user')
        self.clear_cookie('_xsrf')

        # redirect to hub home
        self.set_status(302)
        self.redirect('/hub/home')
