#include <stdio.h>

#define	PORT	4001

extern int tcp_server(int port, char *buf, int len);

char msg[0x100];

void main(void){
	char name[0x10];
	
	puts("Hello!");

	printf("Input Name >> ");
	//fgets(name, 0x20, stdin);
	tcp_server(PORT, name, 0x20);

	printf("Input Message >> ");
	//fgets(msg, sizeof(msg), stdin);
	tcp_server(PORT, msg, sizeof(msg));
}

void win(unsigned key1, unsigned key2){
	puts("This is win\n");
	if(key1 == 0xcafebabe && key2 == 0xc0bebeef)
		puts("Correct!");
	else
		puts("Wrong...");
}

void dummy(void){
	long tmp  = 0xc35f;				// pop rdi ; ret  ;
	long tmp2 = 0xc35f415e;			// pop rsi ; pop r15 ; ret  ;
}
