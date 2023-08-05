#!/usr/bin/env python
"""Setup configuration for the python grr modules."""

# pylint: disable=unused-variable
# pylint: disable=g-multiple-import
# pylint: disable=g-import-not-at-top
import ConfigParser
import os
import subprocess

from setuptools import find_packages, setup, Extension
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.sdist import sdist

IGNORE_GUI_DIRS = ["node_modules", "bower_components", "tmp"]


def find_data_files(source, ignore_dirs=None):
  ignore_dirs = ignore_dirs or []
  result = []
  for directory, dirnames, files in os.walk(source):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

    files = [os.path.join(directory, x) for x in files]
    result.append((directory, files))

  return result


def run_make_files(make_docs=False,
                   make_ui_files=True,
                   force_compile_protos=False,
                   sync_artifacts=True):
  """Builds necessary assets from sources."""

  if force_compile_protos:
    # Clean and recompile the protobufs.
    subprocess.check_call(["python", "makefile.py", "--clean"])
  else:
    subprocess.check_call(["python", "makefile.py"])

  if sync_artifacts:
    # Sync the artifact repo with upstream for distribution.
    subprocess.check_call(["python", "makefile.py"], cwd="grr/artifacts")

  if make_docs:
    # Download the docs so they are available offline.
    subprocess.check_call(["python", "makefile.py"], cwd="docs")

  if make_ui_files:
    subprocess.check_call(["npm", "install"], cwd="grr/gui/static")
    subprocess.check_call(
        ["npm", "install", "-g", "bower", "gulp"], cwd="grr/gui/static")
    subprocess.check_call(["bower", "update"], cwd="grr/gui/static")
    subprocess.check_call(["gulp", "compile"], cwd="grr/gui/static")


def get_version():
  config = ConfigParser.SafeConfigParser()
  config.read(
      os.path.join(os.path.dirname(os.path.realpath(__file__)), "version.ini"))
  return config.get("Version", "packageversion")


class Develop(develop):

  def run(self):
    run_make_files()
    develop.run(self)


class Sdist(sdist):
  """Build sdist."""

  user_options = sdist.user_options + [
      ("no-make-docs", None, "Don't build ascii docs when building the sdist."),
      ("no-make-ui-files", None, "Don't build UI JS/CSS bundles (AdminUI "
       "won't work without them)."),
      ("no-compile-protos", None, "Don't clean protos, use existing _pb2's."),
      ("no-sync-artifacts", None,
       "Don't sync the artifact repo. This is unnecessary for "
       "clients and old client build OSes can't make the SSL connection."),
  ]

  def initialize_options(self):
    self.no_make_docs = None
    self.no_sync_artifacts = None
    self.no_make_ui_files = None
    self.no_compile_protos = None
    sdist.initialize_options(self)

  def run(self):
    run_make_files(
        make_docs=not self.no_make_docs,
        make_ui_files=not self.no_make_ui_files,
        force_compile_protos=not self.no_compile_protos,
        sync_artifacts=not self.no_sync_artifacts)
    sdist.run(self)


data_files = (
    find_data_files("docs") + find_data_files("executables") +
    find_data_files("install_data") + find_data_files("scripts") +
    find_data_files("grr/artifacts") + find_data_files("grr/checks") +
    find_data_files("grr/gui/static", ignore_dirs=IGNORE_GUI_DIRS) +
    find_data_files("grr/gui/local/static",
                    ignore_dirs=IGNORE_GUI_DIRS) + ["version.ini"])

if "VIRTUAL_ENV" not in os.environ:
  print "*****************************************************"
  print "  WARNING: You are not installing in a virtual"
  print "  environment. This configuration is not supported!!!"
  print "  Expect breakage."
  print "*****************************************************"

setup_args = dict(
    name="grr-response-core",
    version=get_version(),
    description="GRR Rapid Response",
    license="Apache License, Version 2.0",
    url="https://github.com/google/grr",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    ext_modules=[Extension(
        "grr._semantic",
        ["accelerated/accelerated.c"],)],
    cmdclass={
        "develop": Develop,
        "install": install,
        "sdist": Sdist,
    },
    install_requires=[
        "cryptography==2.0.3",
        "PyYAML==3.11",
        "binplist==0.1.4",
        "ipaddr==2.1.11",
        "ipython==5.0.0",
        "pip>=8.1.1",
        "psutil==4.3.0",
        "python-dateutil==2.5.3",
        "pytsk3==20160721",
        "pytz==2016.4",
        "requests==2.9.1",
        "protobuf==3.3.0",
        "Werkzeug==0.11.3",
        "wheel==0.29",
        "virtualenv==15.0.3",
    ],
    extras_require={
        # The following requirements are needed in Windows.
        ':sys_platform=="win32"': [
            "WMI==1.4.9",
            "pypiwin32==219",
        ],
    },

    # Data files used by GRR. Access these via the config_lib "resource" filter.
    data_files=data_files)

setup(**setup_args)
