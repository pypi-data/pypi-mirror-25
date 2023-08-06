from sh import git
import os, pickle, logging

logger = logging.getLogger(__name__)
logger2 = logging.getLogger('sh')
logging.basicConfig(level=logging.INFO)
logger2.setLevel(logging.WARN)  # turn down sh logging

std_files = ['classifier.pkl', 'testing.pkl', 'training.pkl']


class ActiveGit():
    """ Uses a git repo to keep track of active learning data and classifier.

    The standard set of files is: 'training.pkl', 'testing.pkl', and 'classifier.pkl'.
    First two each contain a dictionary with features as keys and target labels (e.g., 0/1) as values.
    The third file contains the classifier (e.g., from sklearn).

    Tags are central to tracking classifier and data. A new repo starts with empty files and a tag "initial".
    Branch 'master' keeps latest and branch 'working' is used for active session.
    After committing a new version, the working is merged to master, deleted, and a new working branch checked out.

    Setting bare=True creates a bare git repo that can be shared (cloned) by a group locally or via git daemon sharing.
    """

    def __init__(self, repopath, bare=False, shared='group'):
        """ Set up activegit for repo at repopath. Checks out master branch (lastest commit) by default. """

        self.repo = git.bake(_cwd=repopath)
        self.repopath = repopath
        self.bare = bare
        self.shared = shared

        if os.path.exists(repopath):
            try:
                contents = [gf.rstrip('\n') for gf in self.repo.bake('ls-files')()]
                if all([sf in contents for sf in std_files]):
                    logger.info('ActiveGit initializing from repo at {0}'.format(repopath))
                    logger.info('Available versions: {0}'.format(','.join(self.versions)))
                    if 'working' in self.repo.branch().stdout:
                        logger.info('Found working branch on initialization. Removing...')
                        cmd = self.repo.checkout('master')
                        cmd = self.repo.branch('working', D=True)
                    self.set_version(self.repo.describe(abbrev=0, tags=True).stdout.rstrip('\n'))
                else:
                    raise
            except:
                logger.warn('{0} does not include standard set of files {1}. Initializing...'.format(repopath, std_files))
                self.initializerepo()
        else:
            logger.info('Creating repo at {0}'.format(repopath))
            self.initializerepo()

    def initializerepo(self):
        """ Fill empty directory with products and make first commit """

        try:
            os.mkdir(self.repopath)
        except OSError:
            pass

        cmd = self.repo.init(bare=self.bare, shared=self.shared)

        if not self.bare:
            self.write_testing_data([], [])
            self.write_training_data([], [])
            self.write_classifier(None)

            cmd = self.repo.add('training.pkl')
            cmd = self.repo.add('testing.pkl')
            cmd = self.repo.add('classifier.pkl')

            cmd = self.repo.commit(m='initial commit')
            cmd = self.repo.tag('initial')
            cmd = self.set_version('initial')


    # version/tag management
    @property
    def version(self):
        """ Current version checked out. """

        if hasattr(self, '_version'):
            return self._version
        else:
            logger.info('No version defined yet.')


    @property
    def versions(self):
        """ Sorted list of versions committed thus far. """

        return sorted(self.repo.tag().stdout.rstrip('\n').split('\n'))


    @property
    def isvalid(self):
        """ Checks whether contents of repo are consistent with standard set. """

        gcontents = [gf.rstrip('\n') for gf in self.repo.bake('ls-files')()]
        fcontents = os.listdir(self.repopath)
        return all([sf in gcontents for sf in std_files]) and all([sf in fcontents for sf in std_files])
        

    def set_version(self, version, force=True):
        """ Sets the version name for the current state of repo """

        if version in self.versions:
            self._version = version
            if 'working' in self.repo.branch().stdout:
                if force:
                    logger.info('Found working branch. Removing...')
                    cmd = self.repo.checkout('master')
                    cmd = self.repo.branch('working', d=True)                    
                else:
                    logger.info('Found working branch from previous session. Use force=True to remove it and start anew.')
                    return

            stdout = self.repo.checkout(version, b='working').stdout  # active version set in 'working' branch
            logger.info('Version {0} set'.format(version))
        else:
            raise AttributeError('Version {0} not found'.format(version))


    def show_version_info(self, version):
        """ Summarizes info of a particular version (a la "git show version") """

        if version in self.versions:
            stdout = self.repo.show(version, '--summary').stdout
            logger.info(stdout)
        else:
            logger.info('Version {0} not found'.format(version))


    # data and classifier as properties
    @property
    def training_data(self):
        """ Returns data dictionary from training.pkl """

        data = pickle.load(open(os.path.join(self.repopath, 'training.pkl')))
        return data.keys(), data.values()


    @property
    def testing_data(self):
        """ Returns data dictionary from testing.pkl """

        data = pickle.load(open(os.path.join(self.repopath, 'testing.pkl')))
        return data.keys(), data.values()


    @property
    def classifier(self):
        """ Returns classifier from classifier.pkl """        

        clf = pickle.load(open(os.path.join(self.repopath, 'classifier.pkl')))
        return clf


    # methods to update data/classifier
    def write_training_data(self, features, targets):
        """ Writes data dictionary to filename """

        assert len(features) == len(targets)

        data = dict(zip(features, targets))

        with open(os.path.join(self.repopath, 'training.pkl'), 'w') as fp:
            pickle.dump(data, fp)


    def write_testing_data(self, features, targets):
        """ Writes data dictionary to filename """

        assert len(features) == len(targets)

        data = dict(zip(features, targets))

        with open(os.path.join(self.repopath, 'testing.pkl'), 'w') as fp:
            pickle.dump(data, fp)


    def write_classifier(self, clf):
        """ Writes classifier object to pickle file """

        with open(os.path.join(self.repopath, 'classifier.pkl'), 'w') as fp:
            pickle.dump(clf, fp)


    # methods to commit, pull, push
    def commit_version(self, version, msg=None):
        """ Add tag, commit, and push changes """

        assert version not in self.versions, 'Will not overwrite a version name.'

        if not msg:
            feat, targ = self.training_data
            msg = 'Training set has {0} examples. '.format(len(feat))
            feat, targ = self.testing_data
            msg += 'Testing set has {0} examples.'.format(len(feat))

        cmd = self.repo.commit(m=msg, a=True)
        cmd = self.repo.tag(version)
        cmd = self.repo.checkout('master')
        self.update()
        cmd = self.repo.merge('working')
        cmd = self.repo.branch('working', d=True)
        self.set_version(version)

        try:
            stdout = self.repo.push('origin', 'master', '--tags').stdout
            logger.info(stdout)
        except:
            logger.info('Push not working. Remote not defined?')


    def update(self):
        """ Pull latest versions/tags, if linked to a remote (e.g., github). """

        try:
            stdout = self.repo.pull().stdout
            logger.info(stdout)
        except:
            logger.info('Pull not working. Remote not defined?')
