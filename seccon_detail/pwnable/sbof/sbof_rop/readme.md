# 概要
  - スタックバッファーオーバーフローを利用したローカル変数の書き換え

### 実行方法
    $ stdbuf -o0 -e0 python3 ./sbof_ret.py

# 脆弱性
  - 標準入力で、ローカル変数 name に書き込みするとき、スタックバッファーオーバーフローが発生する。

### 対象ソースコード
  - sbof_ret.c
  - code 32-27

### スタックメモリ配置（書き換え前）
  -0x10 - -0x01 : name  
  +0x00 - +0x07 : saved rbp (rbp)  
  +0x08 - +0x0F : return address  

### スタックメモリ配置（書き換え後）
  -0x18 - -0x09 : 'a' * 0x10  
  -0x08 - -0x01 : 0x00000000deadbeef ←何でもよい  
  +0x00 - +0x07 : pop rdi; ret (rsp) ←第一引数書き換えのためのROPガジェット  
  +0x08 - +0x0F : 0x00000000cafebabe (return address) ←win2()の第一引数key  
  +0x10 - +0x17 : win2  

