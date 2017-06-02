import pytest


@pytest.fixture()
def segment_batch():

    segment_batch = [
        {'uid': 1, 'timestamp': 1278250469, 'expiration': 48, 'value': 42,
         'type': None, 'member_id': 7007, 'seg_id': 123, 'seg_code': '123'},
        {'uid': 2, 'timestamp': 1278254459, 'expiration': 0, 'value': 0,
         'type': 'idfa', 'member_id': 7007, 'seg_id': 234, 'seg_code': '555'},
        {'uid': 2, 'timestamp': 1278250469, 'expiration': 223454,
         'seg_id': 234, 'seg_code': '444'},
        {'uid': 3, 'timestamp': 1278232469, 'expiration': -1, 'type': 'aaid',
         'member_id': 7007, 'seg_id': 567, 'seg_code': '321'},
        {'uid': 4, 'timestamp': 1278211469, 'expiration': 12, 'value': 20,
         'type': None, 'member_id': 7007, 'seg_id': 890, 'seg_code': '456'},
        {'uid': 4, 'timestamp': 1278431469, 'expiration': 21, 'value': 10,
         'type': None, 'member_id': 7007, 'seg_id': 890, 'seg_code': '777'}
    ]
    return segment_batch
