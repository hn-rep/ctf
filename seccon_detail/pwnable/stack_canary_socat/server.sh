#!/bin/bash

socat tcp-listen:4000,reuseaddr,fork, exec:"stdbuf -o0 ./sbof_leak_w_ssp"
