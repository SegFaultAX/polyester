#!/usr/bin/env python

from fabric.api import local, sudo, run, task
from fabric.state import env

from lib.ubuntu import create_user
