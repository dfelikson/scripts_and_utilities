#!/bin/bash

perl -pi -e 's/\r\n|\n|\r/\r\n/g' $1

