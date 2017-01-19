
from unittest.mock import patch
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
    segment_code = segment_batch[0]['seg_code']
    member_id = 7007


    uploader = AppnexusSegmentsUploader(
            segment_batch, segment_code, upload_string_order, separators, member_id
        )
    upload_string = uploader._get_upload_string_for_user(segment_batch[0])
    assert upload_string == '1;1278250469,,48,42,123,7007'

    upload_string = uploader._get_upload_string_for_user(segment_batch[1])
    assert upload_string == '2;1278254459,,0,0,123,7007^3'

    upload_string = uploader._get_upload_string_for_user(segment_batch[2])
    assert upload_string == '2;1278250469,,223454,0,123,7007^8\n2;1278250469,,223454,0,123,7007^3'

    upload_string = uploader._get_upload_string_for_user(segment_batch[3])
    assert upload_string == '3;1278232469,,-1,0,123,7007'

    upload_string = uploader._get_upload_string_for_user(segment_batch[4])
    assert upload_string == '4;1278211469,,12,20,123,7007'