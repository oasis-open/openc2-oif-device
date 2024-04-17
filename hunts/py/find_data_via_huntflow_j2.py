import toml
import logging
from kestrel.session import Session
from typing import List

from jinja2 import Template


def __hunt_returns(huntflow_file):
    returns = []
    with open(huntflow_file) as f:
        huntflow = f.readlines()
    for i in range(0, len(huntflow)):
        if "returns:" in huntflow[i]:
            k = i+1
            while "#" in huntflow[k]:
                returns.append(huntflow[k].split('- ')[1].split(" ")[0])
                k = k + 1
            break
    return returns

#def __hunt_params(huntflow_file):
#    params = []
#    with open(huntflow_file) as f:
#        huntflow = f.read()
#    for i in range(0, len(huntflow)):
#        if "params:" in huntflow[i]:
#            k = i+1
#            while "returns" not in huntflow[k]:
#                params.append(huntflow[k].split('-')[1].split(" ")[0])
#                k = k + 1
#    return params

def __template(huntflow, huntargs):
    #huntflow = '/home/mvle/git/github.com/screambun/openc2-oif-device/' + huntflow
    with open(huntflow) as f:
        huntflow = f.read()
    j2_template = Template(huntflow)
    return j2_template.render(huntargs)

def hunt_via_file_j2(huntflow_file: str, huntflow_args: List[str]):

    config_data = toml.load("config.toml")
    is_sample_data = config_data["KESTREL"]["is_sample_data"]

    #args = {}
    #params = __hunt_params(huntflow_file)
    #for x in zip(params, huntflow_args):
    #    args[x[0]] = x[1]

    returns = __hunt_returns(huntflow_file)

    args = {}
    for a in huntflow_args:
        j = a.split(":")[0]
        v = a.split(":")[1]
        args[j] = v
    huntflow = __template(huntflow_file, args)

    with Session() as session:
        #with open(huntflow_file) as hff:
        #    huntflow = hff.read()
        session.execute(huntflow)
        return_data = {}
        for v in returns:
            return_data[v] = session.get_variable(v)

        rsp = {}
        if is_sample_data:
            for k,data_item in return_data.items():
                for d in data_item:
                    rsp[k] = d
                    break
        else:
            rsp = return_data
    return rsp