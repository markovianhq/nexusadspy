
from gzip import GzipFile
from nexusadspy.segment import AppnexusSegmentsUploader


def test_segment_upload_string_creation(segment_batch):

    upload_string_order = [
        'timestamp',
        'seg_id',
        'expiration',
        'value',
        'seg_code',
        'member_id'
    ]

    separators = [';', ':', ',', '~', '^']
    member_id = 7007


    uploader = AppnexusSegmentsUploader(
            segment_batch, upload_string_order, separators, member_id
        )
    compressed_buffer = uploader._get_buffer_for_upload()
    with GzipFile(fileobj=compressed_buffer, mode='rb') as compressor:
        upload_string = compressor.read().decode('UTF-8')

    expected_user_1 = '1;1278250469,,48,42,123,7007'
    expected_user_2 = '2;1278254459,,0,0,555,7007:1278250469,,223454,0,444,7007^3'
    expected_user_3 = '3;1278232469,,-1,0,321,7007^8\n3;1278232469,,-1,0,321,7007^3'
    expected_user_4 = '4;1278211469,,12,20,456,7007:1278431469,,21,10,777,7007'

    assert upload_string == '\n'.join([expected_user_1, expected_user_2, expected_user_3, expected_user_4])