#!/usr/bin/env python

# Reference: http://www.linode.com/stackscripts/view/?StackScriptID=123

from fabric.api import sudo, task
from fabric.state import env

__author__ = "Michael-Keith Bernard"
__version__ = "0.0.1-alpha"

__all__ = ["create_user"]

# if not env.sudo_group:
#   env.sudo_group = "sudo"

def _create_user(username, **options):
  """Generate a `useradd` command

  username - new account name

  Keyword Arguments:
  real_name - full name of owner (default: blank)
  home - path to home directory (default: system-specific)
  shell - system shell (default: /bin/bash)
  groups - list of additional groups (default: [])
  system - create a system account (default: False)
  sudoer - add account to sudo group (default: True)

  Returns an Ubuntu-compatible `useradd` command
  """

  username = username.lower()
  real_name = options.get("real_name", "")
  home = options.get("home", None)
  shell = options.get("shell", "/bin/bash")
  groups = options.get("groups", [])
  system = options.get("system", False)
  sudoer = options.get("sudoer", True)

  cmd = ["useradd --user-group --create-home"]

  if real_name:
    cmd.append("--comment %s" % real_name)
  if home:
    cmd.append("--home %s" % home)
  if shell:
    cmd.append("--shell %s" % shell)
  if groups:
    cmd.append("--groups %s" % ",".join(groups))
  if system:
    cmd.append("--system")
  if sudoer:
    cmd.append("--groups %s" % env.sudo_group)

  cmd.append(username)

  return " ".join(cmd)

def _change_password(username, password):
  """Generate a `chpasswd` command

  username - account name
  password - new password for account

  Returns an Ubuntu-compatible `chpasswd` command
  """

  args = {"username": username, "password": password}
  return "%(username)s:%(password)s | chpasswd" % args

def _lock_user(username):
  """Generate a `passwd -l` command

  username - account name
  """
  return "passwd -l %s" % username

def _get_user_info(username):
  """Find `/etc/passwd` entry for user

  username - account name

  Returns a dict containing `passwd` information
  """

  fmt = ("username", "password", "uid", "gid", "comment", "home", "shell")
  with open("/etc/passwd", "r") as passwd:
    for user in passwd:
      info = user.strip().split(":")
      if info[0] == username:
        return dict(zip(fmt, info))
  return None

@task
def create_user(username, password, **options):
  sudo(_create_user(username, **options))
  sudo(_change_password(username, password))

@task
def lock_user(username):
  sudo(_lock_user(username))
