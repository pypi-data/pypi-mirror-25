from configutator import ConfigMap, ArgMap, EnvMap, loadConfig
import sys

def test(param1: int, param2: str):
    """
    This is a test
    :param param1: An integer
    :param param2: A string
    :return: Print the params
    """
    print(param1, param2)

if __name__ == '__main__':
    for argMap in loadConfig(sys.argv, (test,), "Test"):
        test(**argMap[test])

