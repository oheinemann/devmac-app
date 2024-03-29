#!/usr/bin/env python3

import os
from git import Repo, RemoteProgress
from progress.bar import IncrementalBar as Bar


class ProgressBar(RemoteProgress):  # pragma: no cover
    '''Nice looking progress bar for long running commands'''

    def setup(self, repo_name):
        self.bar = Bar(message='Pulling from {}'.format(repo_name), suffix='')

    def update(self, op_code, cur_count, max_count=100, message=''):
        #log.info("{}, {}, {}, {}".format(op_code, cur_count, max_count, message))
        max_count = int(max_count or 100)
        if max_count != self.bar.max:
            self.bar.max = max_count
        self.bar.goto(int(cur_count))


def main():
    print("Hello world!")

    rootDir = os.path.realpath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../.."))

    print(os.path.dirname(os.path.realpath(__file__)))

    print(rootDir)

    repo = Repo(rootDir)
    if repo.is_dirty():
        print("The devmac-app has local changes!")

    o = repo.remotes.origin
    o.fetch()
    # Tags
    tags = []
    for t in repo.tags:
        tags.append({"name": t.name, "commit": str(t.commit), "date": t.commit.committed_date,
                     "committer": t.commit.committer.name, "message": t.commit.message})
    try:
        branch_name = repo.active_branch.name
        # test1
    except:
        branch_name = None

    changes = []
    commits_behind = repo.iter_commits('master..origin/master')

    for c in list(commits_behind):
        changes.append({"committer": c.committer.name, "message": c.message})

    print({"tags": tags, "headcommit": str(repo.head.commit), "branchname": branch_name,
           "master": {"changes": changes}})

    if len(changes) > 0:
        print("Updating to last changes")
        pb = ProgressBar()
        pb.setup('devmac-app')
        o.pull(progress=pb.update)


if __name__ == '__main__':
    main()
