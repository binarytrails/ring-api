
from libcpp.string cimport string
from libcpp.map cimport map as map

# python callbacks
global py_cbs
py_cbs = dict.fromkeys(['account_message'])

# python callbacks context
global py_cbs_ctx

cdef public void incoming_account_message(
        const string& raw_account_id,
        const string& raw_from_ring_id,
        const map[string, string]& raw_content):

    account_id = bytes(raw_account_id).decode()
    from_ring_id = bytes(raw_from_ring_id).decode()

    content = dict()
    raw_content_dict = dict(raw_content)
    for raw_key in raw_content_dict:
        key = raw_key.decode()
        content[key] = raw_content_dict[raw_key].decode()

    global py_cbs_ctx
    global py_cbs
    callback = py_cbs['account_message']

    if (callback and py_cbs_ctx):
        callback(py_cbs_ctx, str(account_id), str(from_ring_id), content)
    elif (callback):
        callback(str(account_id), str(from_ring_id), content)
