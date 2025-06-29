#!/bin/bash

gcc attack_tcache_poisoning.c -g -o attack_tcache_poisoning

./attack_tcache_poisoning
