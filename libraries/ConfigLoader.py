from ruamel.yaml import YAML
import ruamel.yaml
from pathlib import Path

CWD = str(Path(__file__).parent.parent)

def load_file(file):
    dics =None
    with open(file) as f:
        yaml = YAML(typ='safe')
        docs = yaml.load_all(f)
        for doc in docs:
            dics = doc
    if dics is None:
        return load_file(file)
    return dics


def write_key(file,key,value):
    with open(file) as f:
        yaml = YAML(typ='safe')  # defaults to round-trip if no parameters given
        code = yaml.load(f)

    with open(file, 'w') as f:
        code[f'{key}'] = value
        # Use ruamel.yaml.dump to store yaml file as original (block style)
        ruamel.yaml.RoundTripDumper.ignore_aliases = lambda *args: True
        ruamel.yaml.dump(code, f, Dumper=ruamel.yaml.RoundTripDumper, indent=2)

def load_robot_config():
    return load_file('configurations/RobotCoordinates.yaml')

def load_system_config():
    return load_file('configurations/SystemConfig.yaml')

def load_operation_config():
    return load_file('configurations/OperationConfig.yaml')

def load_motor_config():
    return load_file('configurations/MotorConfig.yaml')

def write_robot_config(key,value):
    write_key('configurations/RobotCoordinates.yaml',key,value)

def write_operation_config(key,value):
    write_key('configurations/OperationConfig.yaml',key,value)

def write_system_config(key,value):
    write_key('configurations/SystemConfig.yaml',key,value)

def write_motor_config(key,value):
    write_key('configurations/MotorConfig.yaml',key,value)

