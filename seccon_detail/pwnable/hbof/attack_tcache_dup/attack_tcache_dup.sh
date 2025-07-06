#!/bin/bash

gcc attack_tcache_dup.c -g -o attack_tcache_dup

setarch -R ./attack_tcache_dup
