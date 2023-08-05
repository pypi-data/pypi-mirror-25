from __future__ import unicode_literals

from pre_commit.languages import helpers
from pre_commit.xargs import xargs


ENVIRONMENT_DIR = None
get_default_version = helpers.basic_get_default_version
healthy = helpers.basic_healthy
install_environment = helpers.no_install


def run_hook(repo_cmd_runner, hook, file_args):
    cmd = helpers.to_cmd(hook)
    cmd = (repo_cmd_runner.prefix_dir + cmd[0],) + cmd[1:]
    return xargs(cmd, file_args)
