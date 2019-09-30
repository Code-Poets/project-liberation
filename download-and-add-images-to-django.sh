#!/bin/bash -e

# FIXME This need to be change after domain will be attach to new server
DOMAIN_NAME=35.246.198.141
NGINX_ENDPOINT_WITH_IMAGE_PACKAGE="download-image-package"
# FIXME This need to be change after first release to support versioning
PACKAGE_NAME="company_website_0.1.zip"
PACKAGE_PATH="${BASH_SOURCE%/*}/$PACKAGE_NAME"

find                 \
    .                \
    -name images     \
    -type d          \
    -exec rm -r {} +

curl                                                               \
    --connect-timeout 10                                           \
    --fail                                                         \
    --output  $PACKAGE_PATH                                        \
    $DOMAIN_NAME/$NGINX_ENDPOINT_WITH_IMAGE_PACKAGE/$PACKAGE_NAME

unzip -o -q $PACKAGE_PATH
rm $PACKAGE_PATH
