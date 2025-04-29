# 概要
  - スタックバッファーオーバーフローを利用したローカル変数の書き換え
  - code 32-9～32-11

### 実行方法
    $ stdbuf -o0 -e0 python3 ./sbof_lv.py


# 脆弱性
  - 標準入力で、ローカル変数 name に書き込みするとき、スタックバッファーオーバーフローが発生する。

### 対象ソースコード
  - sbof_lv.c

### スタックのメモリ配置
  -0x2F - -0x20 : name  
  -0x1F - -0x10 : select  
  -0x0F - -0x0C : reserved  
  -0x0B - -0x08 : key  
  -0x07 - -0x00 : priv  
  +0x00 - +0x07 : saved rbp  
  +0x08 - +0x0F : return address  

### スタックのメモリ書き換え
  -0x2F - -0x20 : 'a' * 0x10  
  -0x1F - -0x10 : 'H4cked!' + '\x00'* 9  
  -0x0F - -0x0C : 0x00000000  
  -0x0B - -0x08 : 0xdeadbeef  
  -0x07 - -0x00 : 0x000000000040204b  
  +0x00 - +0x07 : saved rbp  
  +0x08 - +0x0F : return address  
