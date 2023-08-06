#!/bin/bash

rsync -avP build-ns /media/psf/stash --exclude "*.js" --exclude "*.css" --exclude "*.map.js" --exclude platforms --exclude node_modules

rsync -avP build-ns/hooks /media/psf/stash/build-ns/


