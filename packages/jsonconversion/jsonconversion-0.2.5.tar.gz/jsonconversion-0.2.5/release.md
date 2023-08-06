# Releasing on GitHub

After applying changes to the `master`, do the following steps:

1. `git checkout public_master`
2. `git merge master`
3. `git push github HEAD:master`
4. `git tag -a [version] -m "[version message]"`
5. `git push github [version]`

This assumes that there is a remote `github` with the following URL: `it@github.com:DLR-RM/python-jsonconversion.git`.
