
from typing import BinaryIO, Iterable, Tuple
from datetime import datetime
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
        used for authentication. Not necessary if the drive is public.
    :param args: Further arguments to the /files/list endpoint.
    """

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
        sfields = 'id, name, createdTime'  # string list of fields to fetch

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
                time = datetime.strptime(item['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                yield item['name'], time, io.BytesIO(b'')

            # get more items if the user hasn't stopped iterating yet
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
