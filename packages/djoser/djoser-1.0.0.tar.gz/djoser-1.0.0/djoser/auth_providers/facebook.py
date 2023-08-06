from requests_oauthlib.oauth2_session import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix


class FacebookOAuth2Strategy(object):
    authorization_base_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/oauth/access_token'

    def get_url(self, client_id, redirect_uri):
        session = OAuth2Session(client_id, redirect_uri=redirect_uri)
        session = facebook_compliance_fix(session)

        url, state = session.authorization_url(self.authorization_base_url)
        return url
