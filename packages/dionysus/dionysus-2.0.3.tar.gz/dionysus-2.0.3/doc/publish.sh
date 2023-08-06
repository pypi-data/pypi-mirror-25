#!/bin/sh

rsync -r --delete --progress _build/html/ cole:www/mrzv/software/dionysus2
