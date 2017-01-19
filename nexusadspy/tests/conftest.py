import pytest

@pytest.fixture()
def segment_batch():

    segment_batch = [
        {'uid': 1, 'timestamp': 1278250469, 'expiration': 48, 'value': 42,
         'mobile_os': None, 'member_id': 7007, 'seg_id': 123, 'seg_code': '123'},
        {'uid': 2, 'timestamp': 1278254459, 'expiration': 0, 'value': 0,
         'mobile_os': 'ios', 'member_id': 7007, 'seg_id': 234, 'seg_code': '123'},
        {'uid': 2, 'timestamp': 1278250469, 'expiration':223454,
         'mobile_os': 'android' , 'seg_id': 234, 'seg_code': '123'},
        {'uid': 3, 'timestamp': 1278232469, 'expiration': -1,
         'member_id': 7007, 'seg_id': 567, 'seg_code': '123'},
        {'uid': 4, 'timestamp': 1278211469, 'expiration': 12, 'value': 20,
         'mobile_os': None, 'member_id': 7007, 'seg_id': 890, 'seg_code': '456'}
    ]
    return segment_batch
