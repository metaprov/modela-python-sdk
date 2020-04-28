#! /usr/bin/env bash

# This script auto-generates protobuf related files. It is intended to be run manually when either
# API types are added/modified, or server gRPC calls are added. The generated files should then
# be checked into source control.

set -x
set -o errexit
set -o nounset
set -o pipefail

PROJECT_ROOT=$(cd $(dirname ${BASH_SOURCE})/..; pwd)
PATH="${PROJECT_ROOT}/dist:${PATH}"

rm -rf ${PROJECT_ROOT}/github.com
rm -rf ${PROJECT_ROOT}/github
rm -rf ${PROJECT_ROOT}/google



# Generate the grpc first, since it would be generated under github.com and not github/com

python3 -m grpc_tools.protoc \
    -I/usr/local/include \
    -I${PROJECT_ROOT} \
    -I${PROJECT_ROOT}/common-protos \
    --plugin protoc-gen-grpc-python=/usr/local/bin/grpc_python_plugin \
    --grpc-python_out=. \
    --python_out=. \
    google/api/annotations.proto \
    google/api/http.proto \
    protoc-gen-swagger/options/annotations.proto \
    ${PROJECT_ROOT}/proto/prediction_server.proto
