#!/bin/sh

ogrinfo -so -al $1 | grep Extent

