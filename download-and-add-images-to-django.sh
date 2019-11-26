#!/bin/bash -e

DOMAIN_NAME=https://codepoets.it
NGINX_ENDPOINT_WITH_IMAGE_PACKAGE="download-image-package"
# FIXME This need to be change after first release to support versioning
PACKAGE_NAME="project-liberation.zip"
PACKAGE_PATH="${BASH_SOURCE%/*}/$PACKAGE_NAME"

find                  \
    ${BASH_SOURCE%/*} \
    -name images      \
    -type d           \
    -exec rm -r {} +

curl                                                               \
    --connect-timeout 10                                           \
    --fail                                                         \
    --output  $PACKAGE_PATH                                        \
    $DOMAIN_NAME/$NGINX_ENDPOINT_WITH_IMAGE_PACKAGE/$PACKAGE_NAME

unzip                       \
    -oq                     \
    -d ${BASH_SOURCE%/*}/.. \
    $PACKAGE_PATH

rm $PACKAGE_PATH
