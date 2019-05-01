## Serializations
- Currently implemented:
	- CBOR
	- JSON
	- XML
	- YAML

- Adding Additional

##### Note: Python is the default language used within the OIF, all python modules can be found on [PyPi](https://pypi.org/)
1. Open the `modules/utils/sb_utils/message.py` file
2. Add the serialization to the serializations dictionary
	- Note: The key should be lowercase and not begin with a number or special character for all serializations added
	- Simple Serializations, single function - BSON
	
	```python
	import bson
	...
	serializations = dict(
		encode=dict(
			bson=bson.dumps
	   ),
		decode=dict(
			bson=bson.loads
	   	)
	)
	```
	
	- Wrapped Serializations, multiple functions - CBOR
	
	```python
	import base64
	import cbor2
	...
	serializations = dict(
		encode=dict(
			cbor=lambda x: base64.b64encode(cbor2.dumps(x)).decode('utf-8'),
	   ),
		decode=dict(
			cbor=lambda x: base64.b64decode(cbor2.loads(x)),
	   	)
	)
	```

3. Add the non standard packages used for the encoding to the `modules/utils/requirements.txt`
	- For BSON, bson
	- For CBOR, cbor2

	```text
	...
	bson
	cbor2
	...
	```

4. Rerun the `configure.py` script to add the additional serializations