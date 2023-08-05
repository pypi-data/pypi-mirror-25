import pickle
import json
import base64

test_data = {}
pickled_data = pickle.dumps(test_data)
pickled_data_64 = base64.b64encode(pickled_data)
pickled_data_64_ascii = pickled_data_64.decode('ascii')
json_dumped = json.dumps(pickled_data_64_ascii)

json_loaded_64_ascii = json.loads(json_dumped)
json_loaded_64 = json_loaded_64_ascii.encode('ascii')
json_loaded = base64.b64decode(json_loaded_64)

loaded_data = pickle.loads(json_loaded)

print(type(pickled_data))
print(type(pickled_data_64))
print(type(json_loaded_64_ascii))
print(type(json_loaded_64))
print(type(json_loaded))
