#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <image-name>"
  exit 1
fi

IMAGE_NAME="$1"

SOURCE_REGISTRY="registry.hamdocker.ir/the-atid"
DEST_REGISTRY="192.168.36.2:8182/ctf"

SOURCE_IMAGE="${SOURCE_REGISTRY}/${IMAGE_NAME}"
DEST_IMAGE="${DEST_REGISTRY}/${IMAGE_NAME}"

echo "Pulling image from ${SOURCE_IMAGE}..."
docker pull "${SOURCE_IMAGE}"

echo "Tagging image as ${DEST_IMAGE}..."
docker tag "${SOURCE_IMAGE}" "${DEST_IMAGE}"

echo "Pushing image to ${DEST_IMAGE}..."
docker push "${DEST_IMAGE}"

echo "Done."

