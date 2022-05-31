#!/usr/bin/bash

cd || exit

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.0-linux-x86_64.tar.gz
tar xvzf elasticsearch-8.2.0-linux-x86_64.tar.gz

# shellcheck disable=SC2164
cd elasticsearch-8.2.0/

./bin/elasticsearch -d