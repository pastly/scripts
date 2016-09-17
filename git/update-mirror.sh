#!/usr/bin/env sh

# Super awesome script that keeps one remote repo in sync with another
# Useful when development happens on one remote repo, but you want to
# advertise your repo somewhere else too.

# Optionally takes a directory to store a temporary local copy of the repo.
# If unspecified, defaults to the current directory

[[ "$#" < 2 ]] && echo "$0 from-repo to-repo [temp-dir]" && exit 0

# Remote repository where active development happens
FROM="$1"
shift

# Remote repository which should be kept in sync with $FROM
TO="$1"
shift

[[ "$1" != "" ]] && \
	LOCAL_DIR="$1/update-mirror-${RANDOM}.git" || \
	LOCAL_DIR="./update-mirror-${RANDOM}.git"

echo "--- cloning ${FROM} locally ---"
git clone --bare "${FROM}" "${LOCAL_DIR}"
cd "${LOCAL_DIR}"

echo "--- pushing to ${TO} ---"
git push --mirror "${TO}"

cd - &> /dev/null
rm -rf "${LOCAL_DIR}"
