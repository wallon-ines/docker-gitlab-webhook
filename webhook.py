#!/usr/bin/env python3
#
# Requirement:
# python3-yaml
# python3-flask
#


import os
import subprocess
import yaml
import sys

from flask import Flask
from flask import g, jsonify, request, abort

app = Flask(__name__)
app.config['DEBUG'] = False



repository = os.getenv("REPOSITORY")
token = os.getenv("TOKEN")
repo_dir = "/app"
branch = os.getenv("BRANCH", "master")
pre_script = os.getenv("PRE_SCRIPT")
post_script = os.getenv("POST_SCRIPT")


def run_it(cmd):
  try:
      output = subprocess.check_output(
          cmd, executable='/bin/bash', shell=True,
          stderr=subprocess.STDOUT, universal_newlines=True)
  except subprocess.CalledProcessError as er:
      print(er.output, file=sys.stderr)
      return False, er.output
  else:
      print(output, file=sys.stderr)
      return True, output


@app.route('/', methods=['POST'])
def receive():
  global repository, token, branch, pre_script, post_script

  token_gitlab = request.headers.get('X-Gitlab-Token', False)
  data = request.json or {}


  if not token_gitlab:
    abort(403, 'No X-Gitlab-Token header given')

  if ('repository' in data and 'name' in data['repository'] and
      data['repository']['name'] == repository):
    print("Matching repo: {}".format(data['repository']), file=sys.stderr)

    if token_gitlab != token:
      print('Token invalid, expected: {}, got: {}'.format(token, token), file=sys.stderr)
    url = data['repository']['url']


    # clean up git workdir, reset changes, fetch updates
    os.chdir(repo_dir)
    if pre_script:
      ok, pre_script_output = run_it(pre_script)
    ok, output = run_it('git checkout -- . && git pull && git checkout {}'.format(branch))
    print(output, file=sys.stderr)
    if post_script:
      ok, post_script_output = run_it(post_script)
    if not ok:
      print("Script error", file=sys.stderr)

  return 'success: {}'.format(request.json)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
