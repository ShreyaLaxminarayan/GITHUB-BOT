#!/bin/bash
set -x

BASEDIR=$(pwd)
message=()
version=""
commit_id=""
attempts=0
max_attepts=3

function clone_runtime {
	git clone --branch ${1:-main} https://github.com/dotnet/runtime
	pushd runtime
	commit_id=$(git show HEAD --pretty=format:"%h" --no-patch)
	message+=("commit id:- ${commit_id} <br>")
	popd
}

clone_runtime
