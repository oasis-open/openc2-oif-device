import os
from hunts.py.find_data_via_huntflow import hunt_via_file
from hunts.py.find_data_via_jinja_hunt import hunt_jinja_via_variables 
from hunts.py.find_data_via_variables import hunt_via_variables
import unittest  

class Test_Hunts(unittest.TestCase):

    def test_query_data_via_stixshifter(self):

        working_directory = os.getcwd()
        huntflow_file = working_directory + '/hunts/huntflow/query_data_via_stixshifter.hf'

        hunt_data = hunt_via_file(huntflow_file)
        search_for = "pid"
        is_found = search_for in hunt_data.keys()

        self.assertIsNotNone(hunt_data)    
        self.assertEqual(True, is_found)     

    def test_helloworld(self):

        working_directory = os.getcwd()
        huntflow_file = working_directory + '/hunts/huntflow/helloworld.hf'

        hunt_data = hunt_via_file(huntflow_file, 'browsers')
        search_for = "pid"
        is_found = search_for in hunt_data.keys()

        self.assertIsNotNone(hunt_data)    
        self.assertEqual(True, is_found) 

    def test_find_data_via_variables(self):

        get_cmd = "process"
        from_cmd = "file://./data/test_stixbundle.json"
        where_cmd = "[process:name='compattelrunner.exe']"

        hunt_data = hunt_via_variables(True, get_cmd, from_cmd, where_cmd)

        # Might be safer to test on keys, if data changes..
        search_for = "MYORGIDX-01aac66c-00000820-00000000-1d70c280e79cd04"
        is_found = search_for in hunt_data.values()

        self.assertIsNotNone(hunt_data)    
        self.assertEqual(True, is_found) 

    def test_jijna_hunt(self):

        get_cmd = "process"
        from_cmd = "file://./data/test_stixbundle.json"
        where_cmd = "[process:name='compattelrunner.exe']"

        hunt_data = hunt_jinja_via_variables(True, get_cmd, from_cmd, where_cmd)

        search_for = "MYORGIDX-01aac66c-00000820-00000000-1d70c280e79cd04"
        is_found = search_for in hunt_data.values()

        self.assertIsNotNone(hunt_data)    
        self.assertEqual(True, is_found)         

    def test_query_net_traffic_stixdata(self):

        working_directory = os.getcwd()
        huntflow_file = working_directory + '/hunts/huntflow/query_net_traffic_stixdata.hf'

        hunt_data = hunt_via_file(huntflow_file)
        search_for = "network-traffic--0446320c-6ad1-5a1a-86e7-9b0bb4998282"
        is_found = search_for in hunt_data.values()

        self.assertIsNotNone(hunt_data)    
        self.assertEqual(True, is_found)    

    def test_query_web_stixdata(self):

        working_directory = os.getcwd()
        huntflow_file = working_directory + '/hunts/huntflow/query_web_stixdata.hf'

        hunt_data = hunt_via_file(huntflow_file)
        search_for = "MYORGIDX-01aac66c-00000820-00000000-1d70c280e79cd04"
        is_found = search_for in hunt_data.values()

        self.assertIsNotNone(hunt_data)    
        self.assertEqual(True, is_found)     

    def test_query_local_stixdata(self):

        working_directory = os.getcwd()
        huntflow_file = working_directory + '/hunts/huntflow/query_local_stixdata.hf'

        hunt_data = hunt_via_file(huntflow_file)
        search_for = "MYORGIDX-01aac66c-00000820-00000000-1d70c280e79cd04"
        is_found = search_for in hunt_data.values()

        self.assertIsNotNone(hunt_data)    
        self.assertEqual(True, is_found)    

if __name__ == '__main__':
    unittest.main()
