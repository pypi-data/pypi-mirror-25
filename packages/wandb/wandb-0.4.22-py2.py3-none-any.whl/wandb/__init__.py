# -*- coding: utf-8 -*-

__author__ = """Chris Van Pelt"""
__email__ = 'vanpelt@wandb.com'
__version__ = '0.4.22'

import types
import six
import sys
import logging
import os
import traceback

# We use the hidden version if it already exists, otherwise non-hidden.
if os.path.exists('.wandb'):
    __stage_dir__ = '.wandb/'
elif os.path.exists('wandb'):
    __stage_dir__ = "wandb/"
else:
    __stage_dir__ = None


def get_stage_dir():
    return __stage_dir__

# Used when initing a new project with "wandb init"


def _set_stage_dir(stage_dir):
    global __stage_dir__
    __stage_dir__ = stage_dir


from .git_repo import GitRepo
from .api import Api, Error
from .sync import Sync
from .config import Config
from .results import Results
from .summary import Summary
from .history import History
from wandb import wandb_run

# Three possible modes:
#     'cli': running from "wandb" command
#     'run': we're a script launched by "wandb run"
#     'dryrun': we're a script not launched by "wandb run"

# Hmmm....
stack_frame0 = traceback.extract_stack()[0]
try:
    launched_file = stack_frame0.filename
except AttributeError:
    launched_file = stack_frame0[0]

if launched_file.endswith('bin/wandb'):
    MODE = 'cli'
else:
    MODE = os.environ.get('WANDB_MODE', 'dryrun')


# called by cli.py
# Even when running the wandb cli, __init__.py is imported before main() runs, so we set
# cli mode afterward. This means there's a period of time before this call when MODE will
# be dryrun
def _set_cli_mode():
    global MODE, run
    MODE = 'cli'
    run = None


if __stage_dir__ is not None:
    log_fname = __stage_dir__ + 'debug.log'
else:
    log_fname = './wandb-debug.log'
logging.basicConfig(
    filemode="w",
    filename=log_fname,
    level=logging.DEBUG)


def push(*args, **kwargs):
    Api().push(*args, **kwargs)


def pull(*args, **kwargs):
    Api().pull(*args, **kwargs)


def _do_sync(dir, extra_config=None):
    if MODE == 'run':
        api = Api()
        if api.api_key is None:
            raise Error(
                "No API key found, run `wandb login` or set WANDB_API_KEY")
        api.set_current_run_id(run.id)
        if extra_config is not None:
            run.config.update(extra_config)
        sync = Sync(api, run.id, config=run.config, dir=dir)
        sync.watch(files='*')
        return sync
    elif MODE == 'dryrun':
        print('wandb dryrun mode. Use "wandb run <script>" to save results to wandb.\n'
              'Run directory: %s' % run.dir)


# The current run (a Run object)
run = None

if __stage_dir__ and MODE != 'cli':
    _run_id = os.getenv('WANDB_RUN_ID')
    if _run_id is None:
        _run_id = wandb_run.generate_id()
    _run_dir = os.getenv('WANDB_RUN_DIR')
    if _run_dir is None:
        _run_dir = wandb_run.run_dir_path(_run_id, dry=MODE == 'dryrun')
    _conf_paths = os.getenv('WANDB_CONFIG_PATHS', '')
    if _conf_paths:
        _conf_paths = _conf_paths.split(',')

    syncer = None

    def persist_config_callback():
        if syncer:
            syncer.update_config(_config)
    _config = Config(config_paths=_conf_paths,
                     wandb_dir=__stage_dir__, run_dir=_run_dir,
                     persist_callback=persist_config_callback)
    run = wandb_run.Run(_run_id, _run_dir, _config)
    syncer = _do_sync(run.dir)

__all__ = ["Api", "Error", "Config", "Results", "History", "Summary",
           "WandBKerasCallback"]
