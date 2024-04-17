import json
import os
import toml
from kestrel.session import Session

# Ref
# https://kestrel.readthedocs.io/en/stable/source/kestrel.session.html


default_get_cmd = "process"
default_from_cmd = "stixshifter://bh22-linux"
default_where_cmd = "name = 'bash' AND pid LIKE '13333'"
default_start_cmd = "2022-07-01T00:00:00Z"
default_stop_cmd = "2022-08-01T00:00:00Z"

def hunt_via_variables(get_cmd: str = None, 
                       from_cmd: str = None, 
                       where_cmd: str = None,
                       start_cmd: str = None,
                       stop_cmd: str = None):
    
    config_data = toml.load("config.toml")
    is_sample_data = config_data["KESTREL"]["is_sample_data"]
    
    if get_cmd is None:
        get_cmd = default_get_cmd

    if from_cmd is None:
        from_cmd = default_from_cmd
        if start_cmd is None:
            start_cmd = default_start_cmd
            stop_cmd = default_stop_cmd

    if where_cmd is None:
        where_cmd = default_where_cmd                   

    if start_cmd and stop_cmd:
        hunt = f"results = GET {get_cmd} FROM {from_cmd} WHERE {where_cmd} START {start_cmd} STOP {stop_cmd}"
    else:
        hunt = f"results = GET {get_cmd} FROM {from_cmd} WHERE {where_cmd}"

    with Session() as session:
        session.execute(hunt)
        return_data = session.get_variable("results")

        rsp = {}
        if is_sample_data:
            for data_item in return_data:
                rsp = data_item
                break
        else:
            rsp = return_data

    print(rsp) 
    return rsp
