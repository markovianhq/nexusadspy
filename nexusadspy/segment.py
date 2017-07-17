
from __future__ import (
    print_function, division, generators,
    absolute_import, unicode_literals
)

from gzip import GzipFile
from io import BytesIO
from itertools import groupby
import time
import logging

from nexusadspy.client import AppnexusClient


class AppnexusSegmentsUploader:

    def __init__(self, batch_file, upload_string_order, separators, member_id,
                 credentials_path='.appnexus_auth.json'):
        """
        Batch-upload API wrapper for AppNexus.
        :param batch_file: list, List of dictionaries representing AppNexus users. Every member should have fields
            - uid: AppNexus user ID. AAID/IDFS in case of mobile. Always first in upload string.
            - timestamp: POSIX timestamp when user entered the segment.
            - expiration (optional): Expiration timestamp for the user. A POSIX timestamp. Defaults to 0.
            - value (optional): Numerical value for the segment. Defaults to 0.
            - mobile_os (optional): OS used by the user. Considered internally by AppNexus to be desktop if absent.
        :param upload_string_order: list, List specifying the order of inputs behind uid for the upload string.
            Possible values are seg_id, timestamp, expiration, value, member_id, seg_code.
        :param separators: list, List of five field separators. As documented in
        https://wiki.appnexus.com/display/api/Batch+Segment+Service+-+File+Format
        :param member_id: str, Member ID for AppNexus account.
        :param credentials_path: str (optional), Credentials path for AppnexusClient. Defaults to '.appnexus_auth.json'.
        :return:
        """
        self._credentials_path = credentials_path
        self._batch_file = batch_file
        self._upload_string_order = upload_string_order
        self._separators = separators
        self._member_id = member_id
        self._logger = logging.getLogger('nexusadspy.segment')

    def upload(self, polling_duration_sec=2, max_retries=10):
        """
        Initiate segment upload task
        :param polling_duration_sec: int (optional), Time to sleep while polling for status. Defaults to 2.
        :param max_retries: int (optional), Max number of polling retries to be done. Defaults to 10.
        :return: tuple, Tuple with two values, number of valid users and invalid users.
        """
        valid_user_count = invalid_user_count = 0
        api_client = AppnexusClient(self._credentials_path)
        job_id, upload_url = self._initialize_job(api_client)
        self._upload_batch_to_url(api_client, upload_url)
        for attempt in range(max_retries):
            time.sleep(polling_duration_sec)
            job_status = self._get_job_status_response(api_client, job_id)
            if job_status[0].get('phase') == 'completed':
                valid_user_count = job_status[0].get('num_valid_user')
                invalid_user_count = job_status[0].get('num_invalid_user')
                break
        return valid_user_count, invalid_user_count

    def _initialize_job(self, api_client):
        service_endpoint = 'batch-segment?member_id={}'.format(self._member_id)
        response = api_client.request(service_endpoint, 'POST')
        job_id = response[0]['batch_segment_upload_job']['job_id']
        upload_url = response[0]['batch_segment_upload_job']['upload_url']
        return job_id, upload_url

    def _upload_batch_to_url(self, api_client, upload_url):
        upload_buffer = self._get_buffer_for_upload()
        headers = {'Content-Type': 'application/octet-stream'}
        api_client.request(upload_url, 'POST', data=upload_buffer.read(), prepend_endpoint=False, headers=headers)

    def _get_job_status_response(self, api_client, job_id):
        status_endpoint = 'batch-segment?member_id={}&job_id={}'.format(self._member_id, job_id)
        headers = {'Content-Type': 'application/octet-stream'}
        return api_client.request(status_endpoint, 'GET', headers=headers)

    def _get_buffer_for_upload(self):
        upload_string = '\n'.join(
            self._get_upload_string(uid, batch) for uid, batch in self._get_segment_batches(self._batch_file))
        self._logger.debug("Attempting to upload \n" + upload_string)
        compressed_buffer = BytesIO()
        with GzipFile(fileobj=compressed_buffer, mode='wb') as compressor:
            compressor.write(upload_string.encode('UTF-8'))
        compressed_buffer.seek(0)
        return compressed_buffer

    @staticmethod
    def _get_segment_batches(batch_file):
        sorted_batch_file = sorted(batch_file, key=lambda row: row['uid'])
        for uid, batch in groupby(sorted_batch_file, key=lambda row: row['uid']):
            yield uid, batch

    def _get_upload_string(self, uid, batch):
        upload_string = str(uid) + self._separators[0]
        for line in batch:
            upload_string += self._get_upload_string_for_segments(line)
            device_id_field = self._get_mobile_device_id_field(line)
        upload_string = upload_string.strip(self._separators[1])
        if device_id_field:
            upload_string += self._separators[4] + device_id_field
        if device_id_field == '8':
            upload_string += '\n' + upload_string.strip('8') + '3'
            # Appnexus bug: AAID should be uploaded as both IDFA and AAID. Otherwise it cannot be used in mopub.
        return upload_string

    def _get_upload_string_for_segments(self, line):
        line['member_id'] = self._member_id
        segment_string = ''
        for item in self._upload_string_order:
            segment_string += str(line.get(item, '0'))
            segment_string += self._separators[2]
        segment_string = segment_string.strip(self._separators[2])
        segment_string += self._separators[1]
        return segment_string

    @staticmethod
    def _get_mobile_device_id_field(line):
        device_id_type = line['type']
        if device_id_type == 'idfa':
            return '3'
        elif device_id_type == 'sha1udid':
            return '4'
        elif device_id_type == 'md5udid':
            return '5'
        elif device_id_type == 'sha1mac':
            return '6'
        elif device_id_type == 'openudid':
            return '7'
        elif device_id_type == 'aaid':
            return '8'
        elif device_id_type == 'windowsadid':
            return '9'
