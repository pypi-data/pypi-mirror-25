"""Module with friendly_sonar logic"""
# pylint: no-name-in-module

import os
import subprocess
from distutils.spawn import find_executable

import click


def _get_sonar_exec():
    sonar_home = os.environ.get('SONARLINT_HOME')
    if sonar_home:
        return os.path.join(sonar_home, "./bin/sonarlint")
    elif find_executable('sonarlint'):
        return 'sonarlint'
    click.secho(
        "Error: could not find installation of SonarLint.",
        fg='red',
        err=True
    )
    return


def _process_sonar_output(output, verbose=False):
    lower_limit = output.find(
        b"-------------  SonarLint Report  -------------"
    )
    output = output[lower_limit:]
    upper_limit = output.find(
        b"-------------------------------------------"
    )
    output = output[:upper_limit]
    if verbose:
        print(output.decode('utf-8'))
    lines = output.split(b"\n")
    results = {}
    for line in lines:
        if b"issue" in line:
            token = line.strip().split(b" ")[0]
            if token.isdigit():
                results["issues"] = int(token)
            elif token == b"No":
                results["issues"] = 0
            bracket_position = line.find(b"(")
            files_processed = line[bracket_position+1:].split(b" ")[0]
            if files_processed.isdigit():
                results["files_processed"] = int(files_processed)
        if b"critical" in line:
            results["critical_issues"] = int(line.strip().split(b" ")[0])
        if b"major" in line:
            results["major_issues"] = int(line.strip().split(b" ")[0])
        if b"minor" in line:
            results["minor_issues"] = int(line.strip().split(b" ")[0])
    return results


def run_lint(project_path="./", match_files=None, exclude=None, verbose=False):
    """Get SonarLint output."""

    sonar_exec = _get_sonar_exec()
    if sonar_exec:
        execution_cmd = sonar_exec
        if exclude:
            execution_cmd = execution_cmd + " --exclude " + exclude
        if match_files:
            execution_cmd = execution_cmd + " --src " + match_files
        try:
            output = subprocess.check_output(
                execution_cmd,
                shell=True,
                cwd=project_path
            )
        except subprocess.CalledProcessError as error:
            click.secho(
                "SonarLint failed while "
                "running on project '{}':".format(project_path),
                fg='red',
                err=True,
            )
            print(error)
            return None
        return _process_sonar_output(output, verbose)
    return None

if __name__ == "__main__":
    # results = run_lint(project_path="/Users/luiscruz/dev/autorefactor_tooldemo_exps_3/NewsBlur")
    # print(results)
    with open("test_expected.txt", "rb") as f:
        print(_process_sonar_output(f.read()))
    with open("test_expected_no_issues.txt", "rb") as f:
        print(_process_sonar_output(f.read()))
    