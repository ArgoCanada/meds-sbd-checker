
import os
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class GoogleCredentialHelper:
    """
    Authorizing Google APIs is complex and best practices change
    quickly. This class contains the helpers needed to generate
    tokens for development (where tokens are JSON files
    generated and saved locally) and for GitHub actions
    (where tokens are JSON stored in environment variables
    set using repository secrets).
    """

    # the two scopes we need to use
    SCOPE_DRIVE_READONLY = 'https://www.googleapis.com/auth/drive.readonly'
    SCOPE_GMAIL_READONLY = 'https://www.googleapis.com/auth/gmail.readonly'

    class NoSuchCredentialError(Exception):
        pass

    @staticmethod
    def service_account_credentials(scopes=''):
        """
        Loads the service account
        credential from the GOOGLE_APPLICATION_CREDENTIALS environment variable
        (e.g., GitHub actions) or the local file 'gooogle-application-credentials.json'
        (e.g., you're developing locally).

        :param scopes: One or more scope URLs (can usually be omitted for
            publicly available information)
        """
        env_var = 'GOOGLE_APPLICATION_CREDENTIALS'
        default_file = 'google-application-credentials.json'
        content = GoogleCredentialHelper._load_json_file_or_content(env_var, default_file)
        return service_account.Credentials.from_service_account_info(content, scopes=scopes)

    @staticmethod
    def gmail_authorized_user_token(interactive=False):
        """
        Loads the authorized user token from the GMAIL_AUTHORIZED_USER_TOKEN
        environment variable (e.g., GitHub actions) or the local file
        'gmail-authorized-user-token.json'. If the credentials are invalid
        it will attempt to refresh the token and if ``interactive`` is ``True``
        it will attempt to obtain authorization using a web browser (how
        you create the credentials in the first place). A local authorization
        requires the file 'gmail-client-secret.json' (downloaded from the
        Googel Cloud Console) to exist. This authorization will choose which
        inbox is listed with a :class:`checker.source.GmailDataSource`.
        In practice this will only work for the Argo Canada account
        address because it's the only account listed under "test users"
        in the Google Cloud console. This is a good thing because you
        don't want this to accidentally have access to your personal
        email!
        """
        # https://developers.google.com/gmail/api/quickstart/python
        scopes = [GoogleCredentialHelper.SCOPE_GMAIL_READONLY]
        env_var = 'GMAIL_AUTHORIZED_USER_TOKEN'
        default_file = 'gmail-authorized-user-token.json'
        creds = None

        try:
            content = GoogleCredentialHelper._load_json_file_or_content(env_var, default_file)
            creds = Credentials.from_authorized_user_info(content, scopes)
        except GoogleCredentialHelper.NoSuchCredentialError:
            pass

        if not creds or not creds.valid:  # pragma: no cover
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif interactive:
                # pip install --upgrade google-auth-oauth
                # this literally cannot run on GitHub actions because
                # it pops up a browser window
                from google_auth_oauthlib.flow import InstalledAppFlow
                client_secret_file = 'gmail-client-secret.json'
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_file,
                    scopes
                )

                # the port number is important here because the authorized
                # redirect URL for this application (set in the Google Cloud Console
                # under 'Oauth Authorization Screen Setup') is http://localhost:53844/
                creds = flow.run_local_server(port=53844)

            # only update the credentials file interactively (no way to
            # keep this information securely up-to-date otherwise)
            if interactive:
                with open(default_file, 'w') as token:
                    token.write(creds.to_json())
            else:
                raise GoogleCredentialHelper.NoSuchCredentialError()

        return creds

    @staticmethod
    def _load_json_file_or_content(env_var, default_file):
        file_or_content = os.getenv(env_var)
        if file_or_content is None:
            file_or_content = default_file

        try:
            try:
                with open(file_or_content, 'rb') as f:
                    return json.load(f)
            except IOError:
                return json.loads(file_or_content)
        except Exception as e:
            raise GoogleCredentialHelper.NoSuchCredentialError() from e
