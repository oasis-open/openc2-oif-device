# Serializations
## Currently implemented:
- [Binn](https://github.com/liteserver/binn)
- [Bencode](https://wiki.theory.org/index.php/BitTorrentSpecification#Bencoding)
- [BSON](http://bsonspec.org/)
- [CBOR](https://tools.ietf.org/html/rfc7049)
- [Extensible Data Notation (EDN)](http://edn-format.org/)
- [JSON](https://tools.ietf.org/html/rfc8259) - Official
- [MessagePack (msgpack)](https://msgpack.org)
- [S-expressions](https://people.csail.mit.edu/rivest/Sexp.txt)
- [Smile](https://github.com/FasterXML/smile-format-specification)
- [Toml](https://github.com/toml-lang/toml)
- [XML](https://w3.org/TR/2008/REC-xml-20081126/)
- [ubjson](http://ubjson.org/)
- [VelocityPack (VPack)](https://github.com/arangodb/velocypack)
	- Requires velocity pack to be installed, no python module currently
- [YAML](https://yaml.org/spec/1.2/spec.html)

## Adding Additional Serializations
##### Note: Python is the default language used within the OIF, all python modules can be found on [PyPi](https://pypi.org/) or searching for 'SERIALIZATION python3' on google
1. Open the `modules/utils/root/sb_utils/message/serialize.py` file
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
	
	- Wrapped Serializations, multiple functions - YAML
	
	```python
    import yaml
 
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper
	...
	serializations = dict(
	    encode=dict(
             yaml=lambda m: yaml.dump(m, Dumper=Dumper)
	    ),
		decode=dict(
             yaml=lambda m: yaml.load(m, Loader=Loader)
	   	)
	)
	```

3. Add the non standard packages used for the encoding to the `modules/utils/root/setup.cfg` under the options/install_requires section
	- Note: A package version is not required, but recomended 
	- For BSON, bson
	- For YAML, pyyaml

	```cfg
	...
	[options]
	  packages = find:
	  python_requires= >=2.7, !=3.[1-5], <4
	  setup_requires = setuptools_scm
	  install_requires =
	    bson==0.5.9
	    pyyaml==5.3.1
	...
	```

### Adding serializations to the GUI
#### Option 1
###### This is preferred as it is persistant across multiple instances derived from a single source
1. Open the `orchestrator/core/orc_server/data/fixtures/orchestrator.json` file
2. Add an entry for the new serialization to the file, incrementing the pk field
	- Note: The name field can be any combination of uppercase or lowercase with numbers and special characters, it however __must match__ the serialization key, from above, when all characters are lowercase
	- BSON
		
	```json
	...
	{
   	"model": "orchestrator.serialization",
  		"pk": X,
		"fields": {
			"name": "BSON"
   		}
	},
	...
	```
			
- YAML

	```json
	...
	{
   		"model": "orchestrator.serialization",
  			"pk": X,
		"fields": {
			"name": "YAML"
   		}
	},
	...
	``` 
	
3. Rerun the `configure.py` script to add the additional serializations

#### Option 2
###### This is not preferred as it is not persistant across multiple instances derived from a single source. This options is better oriented for serialization testing
1. Rerun the `configure.py` script to add the additional serializations
2. Open a web browser to the admin page of the Orchestrator
	- This is the same log/pass as the user page
3. From the list on the page, click 'Serializations' under 'Orchestrator'
4. Shown are the currently enabled/usable serializations, click 'ADD SERIALIZATION' in the upper right of the page
5. Add the serialization name as used in the code, then save to add/enable the serialization
	- Note: The name field can be any combination of uppercase or lowercase with numbers and special characters, it however __must match__ the serialization key, from above, when all characters are lowercase