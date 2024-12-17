"""Provides a set of utils for oss-fuzz-gen on new python projects integration"""

import sys

sys.path.append('../../')

import logging
import os
import subprocess
from typing import Optional

from urllib3.util import parse_url

import constants, oss_fuzz_templates

logger = logging.getLogger(__name__)


# Project preparation utils
###########################
def git_clone_project(github_url: str, destination: str) -> bool:
  """Clone project from github url to destination"""
  cmd = ['git clone', github_url, destination]
  try:
    subprocess.check_call(" ".join(cmd),
                          shell=True,
                          timeout=600,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
  except subprocess.TimeoutExpired:
    return False
  except subprocess.CalledProcessError:
    return False
  return True


def get_project_name(github_url: str) -> Optional[str]:
  """Get project name by simplify github url"""
  # HTTPS Type
  # https://github.com/{user}/{proj_name} or https://github.com/{user}/{proj_name}.git
  # or
  # SSH Type
  # git@github.com:{user}/{proj_name} or git@github.com:{user}/{proj_name}.git

  # Remove the .git suffix
  if github_url.endswith('.git'):
    github_url = github_url[:-4]

  if github_url.startswith('https://'):
    # Validate url for HTTPS type
    parsed_url = parse_url(github_url)
    host = parsed_url.host
    path = parsed_url.path
    if path and host == 'github.com' and len(path.split('/')) == 3:
      return path.split('/')[2]
  elif github_url.startswith('git@github.com:'):
    # Validate url for SSH type
    path = github_url.split('/')
    if len(path) == 2:
      return path[1]

  # Malformed or invalid github url
  return None


def prepare_base_files(base_dir: str, project_name: str, url: str) -> bool:
  """Prepare OSS-Fuzz base files for python project fuzzing"""

  # Preapre build.sh and Dockerfile
  build_file = _get_build_file()
  docker_file = _get_docker_file(url, project_name)
  if not docker_file or not build_file:
    return False

  try:
    with open(os.path.join(base_dir, 'build.sh'), 'w') as f:
      f.write(build_file)

    with open(os.path.join(base_dir, 'Dockerfile'), 'w') as f:
      f.write(docker_file)

    with open(os.path.join(base_dir, 'project.yaml'), 'w') as f:
      f.write(oss_fuzz_templates.YAML_PYTHON.replace("{TARGET_REPO}", url))

    with open(os.path.join(base_dir, 'fuzz.py'), 'w') as f:
      f.write(oss_fuzz_templates.FUZZER_PYTHON)
  except:
    return False

  return True


def _get_build_file() -> str:
  """Prepare build.sh content for this project."""
  return oss_fuzz_templates.BUILD_PYTHON_BASE


def _get_docker_file(url: str, project_name: str) -> str:
  """Prepare build.sh content for this project."""
  docker_file = oss_fuzz_templates.DOCKERFILE_PYTHON
  docker_file = docker_file.replace('{TARGET_REPO}', url)
  docker_file = docker_file.replace('{PROJECT_NAME}', project_name)
  return docker_file


def _find_project_build_type(project_dir: str,
                             proj_name: str) -> tuple[str, str]:
  """Search for base project directory to detect project build type"""
  # Search for current directory first
  project_build_data = _find_dir_build_type(project_dir)
  if project_build_data:
    return project_build_data

  # Search for sub directory with name same as project name
  for subdir in os.listdir(project_dir):
    if os.path.isdir(os.path.join(project_dir, subdir)) and subdir == proj_name:
      target_dir = os.path.join(project_dir, subdir)
      project_build_data = _find_dir_build_type(target_dir)
    if project_build_data:
      return project_build_data

  # Recursively look for subdirectory that contains build property file
  for root, _, _ in os.walk(project_dir):
    project_build_data = _find_dir_build_type(root)
    if project_build_data:
      return project_build_data

  return '', ''
