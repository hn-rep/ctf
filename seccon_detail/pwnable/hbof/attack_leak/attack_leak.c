#include <stdio.h>
#include <stdlib.h>
#include "malloc_struct.h"

#define MALLOC_SIZE 0x418

unsigned long ofs_libc_mainarena = 0x1ebb80;
int main(void){
	void *ma, *mb;
	malloc_chunk *ca;

	setbuf(stdout, NULL);

	ma = malloc(MALLOC_SIZE);
	ca = mem2chunk(ma);
	
	// glibc 2.29以降では、free直後にmain_arenaからfd/bkが上書きされないよう最初のmallocでarenaが初期化されている必要があるため、
	// ここでdummyのmalloc(0)をしておくと確実にarenaのアドレスがfd/bkに書き込まれるようになります。
	malloc(0);				// malloc(0x418)でもよい。
	//mb = malloc(0x418);
	//malloc(0);

	free(ma);
	//free(mb);

	puts("UAF");
	printf("heap base : %p\n",   (void*)ca->bk - 0x6d0);
	printf("libc base : %p\n\n", (void*)ca->fd - 0x60 - ofs_libc_mainarena);

	void *p = malloc(MALLOC_SIZE);		// 同じサイズ・順番で確保・開放すると、同じチャンクが割り当てられる
	malloc_chunk *c = mem2chunk(p);

	puts("Uninitialized");
	printf("heap base : %p\n",   (void*)c->bk - 0x6d0);
	printf("libc base : %p\n\n", (void*)c->fd - 0x60 - ofs_libc_mainarena);
}
