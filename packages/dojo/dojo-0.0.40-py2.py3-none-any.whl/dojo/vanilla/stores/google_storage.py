from __future__ import absolute_import, print_function, unicode_literals

import os
import io
import json
import tempfile
import googleapiclient
import contextmanager

from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from ..storage import Storage
from dojo.transforms import ConvertTo


@contextmanager
def authed_service(auth):
    with tempfile.NamedTemporaryFile() as auth_file:
        auth_file.write(json.dumps(auth))
        auth_file.flush()
        os.fsync(auth_file.fileno())
        scopes = ['https://www.googleapis.com/auth/devstorage.full_control']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_file.name, scopes)
        yield discovery.build('storage', 'v1', credentials=credentials)


class VanillaGoogleStorage(Storage):

    def read(self, path):
        rows = []
        if path.endswith('*'):
            path = path[:-1]
        keys = self.list_keys(path)
        for key in keys:
            rows += self._read_rows(key)
        return rows

    def read_file(self, path, file=None):
        if file is None:
            return self._read_rows(path)
        elif isinstance(file, io.BytesIO):
            return self._read_file(path, file)
        else:
            raise ValueError('unsupported type to read file from storage', type(file))

    def write(self, path, rows, format='json'):
        if len(rows) == 0:
            print('Skipped writing of empty output to %s' % (path, ))
            return
        sample_rows = rows[:100]
        max_per_file = 2000000
        avg_line_length = sum([len(json.dumps(row)) for row in sample_rows]) / len(sample_rows)
        lines_per_file = max_per_file / avg_line_length
        num_files = (len(rows) / lines_per_file) + 1
        for i in range(num_files):
            output_path = path + '-%05d-of-%05d' % (i, num_files)
            start_index = i * lines_per_file
            end_index = (i + 1) * lines_per_file
            self._write_rows(output_path, rows[start_index:end_index], format=format)

    def write_file(self, path, file_or_rows, format='json'):
        if isinstance(file_or_rows, (list, tuple)):
            self._write_rows(path, file_or_rows, format=format)
        elif isinstance(file_or_rows, io.BytesIO):
            self._write_file(path, file_or_rows)
        else:
            raise ValueError('unsupported type to write file to storage', type(file_or_rows))

    def list_keys(self, prefix):
        with authed_service(self.secrets['connection']) as service:
            req = service.objects().list(bucket=self.config['bucket'], prefix=prefix, delimiter='/')
            keys = []
            while req:
                resp = req.execute()
                keys += resp.get('prefixes', [])
                keys += [key['name'] for key in resp.get('items', [])]
                req = service.objects().list_next(req, resp)
            return keys

    def as_uri(self, path):
        return '%s://%s/%s' % (self.config['protocol'], self.config['bucket'], path)

    def _read_rows(self, key):
        with authed_service(self.secrets['connection']) as service:
            file = io.BytesIO()
            req = service.objects().get_media(bucket=self.config['bucket'], object=key)
            downloader = googleapiclient.http.MediaIoBaseDownload(file, req)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print("Download {}%.".format(int(status.progress() * 100)))
            file.seek(0)
            rows = file.read().decode('utf-8').split('\n')
            file.close()
            return rows

    def _read_file(self, key, to_file):
        with authed_service(self.secrets['connection']) as service:
            req = service.objects().get_media(bucket=self.config['bucket'], object=key)
            downloader = googleapiclient.http.MediaIoBaseDownload(to_file, req)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print("Download {}%.".format(int(status.progress() * 100)))
            to_file.seek(0)
            return to_file

    def _write_file(self, path, file):
        with authed_service(self.secrets['connection']) as service:
            req = service.objects()\
                         .insert(bucket=self.config['bucket'],
                                 body={'name': path},
                                 media_body=googleapiclient.http.MediaIoBaseUpload(file, 'text/plain'))
            req.execute()

    def _write_rows(self, path, rows, format='json'):
        with authed_service(self.secrets['connection']) as service:
            rows = [ConvertTo(format).process(row) for row in rows]
            f = io.BytesIO('\n'.join(rows).encode('utf-8'))
            req = service.objects()\
                .insert(bucket=self.config['bucket'],
                        body={'name': path},
                        media_body=googleapiclient.http.MediaIoBaseUpload(f, 'text/plain'))
            req.execute()
