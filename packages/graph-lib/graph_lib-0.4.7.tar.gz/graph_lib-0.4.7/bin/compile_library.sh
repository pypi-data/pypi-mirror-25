#!/bin/bash
cd "graph_lib/lib/graph_lib_test"
set -e
make clean
make -f Makefile

cp libgraph.dylib ../../../build/lib/graph_lib/lib/graph_lib_test/
cp libgraph.so ../../../build/lib/graph_lib/lib/graph_lib_test/
