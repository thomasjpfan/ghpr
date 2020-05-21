import argparse
import os
import sys

from github import Github
from git import Repo


def main():
    parser = argparse.ArgumentParser(description="Easily checkout prs")
    parser.add_argument("pr", help="pr number to checkout", type=int)
    parser.add_argument("--upstream",
                        default="upstream",
                        help="remote name for upstream")
    parser.add_argument("--github-token",
                        default=os.environ.get("GPPR_GITHUB_API_TOKEN", None),
                        help="github personal token")
    parser.add_argument("--prefix",
                        default="pr/",
                        help="prefix for local branch")

    args = parser.parse_args()

    if args.github_token is None:
        print("GPPR_GITHUB_API_TOKEN or --github_token must be set")
        sys.exit(1)

    local_branch = "{}{}".format(args.prefix, args.pr)

    local_repo = Repo(".")

    try:
        remote = local_repo.remotes[args.upstream]
        remote_url = remote.url
    except IndexError:
        print("Must run in a git repo with a {} remote".format(args.upstream))
        sys.exit(1)

    if remote_url.startswith("https://github.com/"):
        repo_string = "/".join(remote_url.split("/")[-2:])
        html_repo = True
    elif remote_url.startswith("git@github.com:"):
        repo_string = remote_url.split(":")[-1][:-4]
        html_repo = False
    else:
        print("Remote url: {} on {} must be from github".format(
            remote_url, args.upstream))
        sys.exit(1)

    github_api = Github(args.github_token)
    remote_repo = github_api.get_repo(repo_string)
    pr = remote_repo.get_pull(args.pr)

    remote_url = pr.head.repo.html_url if html_repo else pr.head.repo.ssh_url
    remote_branch = pr.head.ref
    user = pr.user.login

    try:
        remote = local_repo.remotes[user]
    except IndexError:
        remote = local_repo.create_remote(user, remote_url)

    print("fetching from remote: {}, url: {}".format(user, remote_url))
    remote.fetch()

    try:
        branch_ref = local_repo.branches[local_branch]
        print("checkout local branch {}, tracking: {}".format(
            local_branch, remote_branch, remote.refs[remote_branch]))
        branch_ref.checkout()
        print("pulling changes to local branch {}".format(local_branch))
        print(remote_branch)
        remote.pull(remote_branch)
    except IndexError:
        print("creating local branch {}, tracking: {}".format(
            local_branch, remote.refs[remote_branch]))
        local_repo.create_head(local_branch,
                               remote.refs[remote_branch]).set_tracking_branch(
                                   remote.refs[remote_branch]).checkout()
