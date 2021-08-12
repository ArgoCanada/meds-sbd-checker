
from typing import BinaryIO, Iterable, Tuple
from datetime import datetime
import base64
import io
import googleapiclient.discovery


class RawFloatDataSource:
    """
    An abstract class representing some source of new float
    data, iterating over the latest files from a source
    in the order newest to oldest. This should be an iterable of
    tuples in the form ``(filename, datetime, file-like object)``
    so that callers can iterate over the structure like this:

    >>> for name, time, file in obj:
    >>>    # process files until finished
    >>>    break
    """

    def __iter__(self) -> Iterable[Tuple[str, datetime, BinaryIO]]:
        raise NotImplementedError()  # pragma: no cover


class TestRawFloatDataSource(RawFloatDataSource):
    """A test source containing two dummy sbd files."""

    def __iter__(self) -> Iterable[Tuple[str, datetime, BinaryIO]]:
        yield '123_abc.sbd', datetime(2021, 1, 2), io.BytesIO(b'123')
        yield '456_def.sbd', datetime(2021, 1, 1), io.BytesIO(b'456')


class GoogleDriveDataSource(RawFloatDataSource):
    """
    Data source based on a Google Drive folder. This class is a wrapper
    around the Google Drive v3 API /files/list and /files/get endpoints.

    :param folder_id: The shared folder identifier. Should look
        like this: 2bhGbTy9G7HJnSEAsHS3p9CNwYGwvYdAX.
    :param credentials: A ``from oauth2client.service_account.ServiceAccountCredentials``
        used for authentication. Not necessary if the GOOGLE_APPLICATION_CREDENTIALS
        environment variable has been set.
    :param args: Further arguments to the /files/list endpoint.
    """

    class LazyDriveFile:
        """Lazy wrapper that doesn't download unless :meth:`read` is called"""

        def __init__(self, service, file_id) -> None:
            self._service = service
            self._file_id = file_id
            self._buffer = None
        
        def read(self, size=None):
            if self._buffer is None:
                # this will download the file all at once which is OK for now
                req = self._service.files().get_media(fileId=self._file_id)
                self._buffer = io.BytesIO(req.execute())
            return self._buffer.read(size)
        
        def __enter__(self):
            return self
        
        def __exit__(self, *execinfo):
            pass
                

    def __init__(self, folder_id, credentials=None, args=None) -> None:
        self._service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
        self._args = {} if args is None else {}

        # the folder_id is a query param that we might need to combine with others
        q_folder_id = f"'{folder_id}' in parents"
        if 'q' not in self._args:
            q = q_folder_id
        else:
            q = f"({q_folder_id}) and ({self._args['q']})"
        
        self._args['q'] = q
    
    def __iter__(self) -> Iterable[Tuple[str, datetime, BinaryIO]]:    
        page_token = None  # says whether or not we have reached the last page

        # get all files in folder, break when last page is reached, but page_token
        # is None to start and end so can't build condition on that
        while True:
            # get files
            results = self._service.files().list(
                fields='nextPageToken, files(id, name, createdTime)',
                orderBy='createdTime desc',
                **self._args,
                pageToken=page_token
            ).execute()

            # iterate through items
            for item in results.get('files', []):
                # TODO: specify UTC?
                time = datetime.strptime(item['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                with GoogleDriveDataSource.LazyDriveFile(self._service, item['id']) as file:
                    yield item['name'], time, file

            # get more items if the user hasn't stopped iterating yet
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break


class GmailDataSource(RawFloatDataSource):

    def __init__(self, credentials, max_messages=1000, args=None):
        self._service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)
        self._args = {} if args is None else {}
        self._max_messages = max_messages

    def __iter__(self) -> Iterable[Tuple[str, datetime, BinaryIO]]:
        page_token = None
        n_messages = 0

        while True:
            # get messages
            messages = self._service.users().messages().list(
                userId='me',
                **self._args,
                pageToken=page_token
            ).execute()

            for msg_item in messages['messages']:
                message = self._service.users().messages().get(
                    userId='me',
                    id=msg_item['id']
                ).execute()

                n_messages += 1

                time = datetime.fromtimestamp(int(message['internalDate']) / 1000)
                for part in message['payload']['parts']:
                    if 'attachmentId' in part['body']:
                        name = part['filename']
                        attachment = self._service.users().messages().attachments().get(
                            userId='me',
                            messageId=msg_item['id'],
                            id=part['body']['attachmentId']
                        ).execute()

                        data_base64 = attachment['data']
                        data_bytes = base64.urlsafe_b64decode(data_base64)
                        yield name, time, io.BytesIO(data_bytes)

            # get more messages if we're not done iterating
            page_token = messages.get('nextPageToken', None)
            if page_token is None or n_messages >= self._max_messages:
                break
