# friendly_sonar

[![Build Status](https://travis-ci.org/luiscruz/friendly_sonar.svg?branch=master)](https://travis-ci.org/luiscruz/friendly_sonar)

Python3 library to statically analyze software using [SonarLint](http://www.sonarlint.org/) and collect data in a Python Object, CSV, or JSON data format.

## Install

1. Download [SonarQube CLI](https://bintray.com/sonarsource/Distribution/org.sonarsource.sonarlint-cli/_latestVersion)

2. A) Add environment variable `$SONARLINT_HOME` with  directory of your sonar lint installation:

```
export SONARLINT_HOME='~/sonarlint-cli-2.1.0.566'
```
**OR**

2. B) Add environment variable `$SONARLINT_HOME` with  directory of your sonar lint installation:

```
export PATH=~/sonarlint-cli-2.1.0.566/bin:$PATH
```

3. Install Python library

```
$pip install friendly_sonar
```

## Usage

```
import friendly_sonar.lint

# run sonar on current directory
results = friendly_sonar("./") 
print results

```

## Contributing

Feel free to create pull requests.
Be sure that your code passes our checkers:

```
$tox -e py36
```
### Tests

Tests are still not being made properly.
So far you can check whether it is working by running:

```
$python -m friendly_sonar.lint
```



