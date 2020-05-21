# Github PR Puller

Simple tool for pulling PRs locally.

## Usage

0. Generate API key on github to have access to repos and set as the env variable `GPPR_GITHUB_API_TOKEN`.
1. Fork project on github.
2. Clone fork

```
git clone https://github.com/thomasjpfan/scikit-learn
```

3. Set original repo as upstream

```
git remote add upstream https://github.com/scikit-learn/scikit-learn
```

4. Get pull request locally by PR #:

```
ghpr $PR_NUMBER
```

## License

MIT
