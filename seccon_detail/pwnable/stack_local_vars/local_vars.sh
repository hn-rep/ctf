#!/bin/bash

gcc local_vars.c -fno-stack-protector -no-pie -g -o local_vars
objdump --no-show-raw-insn -M intel -d local_vars | grep "<main>:" -A 10
