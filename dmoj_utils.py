import sys
from dmoj import judgeenv


# Sussy baka code right here
def init_with_config_file(path: str, testsuite=False):
    old_argv = sys.argv[:]
    sys.argv = [old_argv[0], '-c', path]
    judgeenv.load_env(True, testsuite)
    sys.argv = old_argv
