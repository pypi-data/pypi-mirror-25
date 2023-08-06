
# activegit

Active learning is a machine learning technique to iteratively train a classifier. `activegit` uses git to create shareable, distributable repositories of data and classifiers for active learning. `activegit` runs in python.

[![Build Status](https://travis-ci.org/caseyjlaw/activegit.svg?branch=master)](https://travis-ci.org/caseyjlaw/activegit) [![codecov](https://codecov.io/gh/caseyjlaw/activegit/branch/master/graph/badge.svg)](https://codecov.io/gh/caseyjlaw/activegit)
[![Documentation Status](https://readthedocs.org/projects/activegit/badge/?version=latest)](http://activegit.readthedocs.io/en/latest/?badge=latest)

# Usage
    ag = activegit.ActiveGit('repopath')
    ActiveGit initializing from repo at repopath
    Available versions: initial

(Build up targets for features. Update classifier.)

    ag.write_training_data(features, targets)
    ag.write_classifier(clf)
    ag.commit_version('newversion')
    ag.versions
    ['initial', 'newversion']
    ag.set_version('newversion')

# Install
    pip install activegit
