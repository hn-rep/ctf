# 概要
  - スタックバッファーオーバーフローを利用したローカル変数の書き換え

### 実行方法
    $ stdbuf -o0 -e0 python3 ./sbof_lv.py

# 脆弱性
  - 標準入力で、ローカル変数 name に書き込みするとき、スタックバッファーオーバーフローが発生する。

### 対象ソースコード
  - sbof_lv.c
  - code 32-9～32-11

### スタックメモリ配置（書き換え前）
  -0x30 - -0x21 : name  
  -0x20 - -0x11 : select  
  -0x10 - -0x0D : reserved  
  -0x0C - -0x09 : key  
  -0x08 - -0x01 : priv  
  +0x00 - +0x07 : saved rbp  
  +0x08 - +0x0F : return address  

### スタックメモリ配置（書き換え後）
  -0x30 - -0x21 : 'a' * 0x10  
  -0x20 - -0x11 : 'H4cked!' + '\x00'* 9  
  -0x10 - -0x0D : 0x00000000  
  -0x0C - -0x09 : 0xdeadbeef  
  -0x08 - -0x01 : 0x000000000040204b  
  +0x00 - +0x07 : saved rbp  
  +0x08 - +0x0F : return address  
