#include <stdio.h>

void main(void){
	char name[0x10];
	
	printf("Input Name >> ");
	fgets(name, 0x100, stdin);
}

void win1(void){
	puts("This is win1\n");
	puts("Congratz!!");
}

void win2(unsigned key, unsigned key2, unsigned key3){
	puts("This is win2\n");
	if(key == 0xcafebabe)
		puts("Correct!");
	else
		puts("Wrong...");

	if(key2 == 0xcafebabe)
		puts("Correct!2");
	else
		puts("Wrong...2");

	if(key3 == 0xcafebabe)
		puts("Correct!3");
	else
		puts("Wrong...3");
}

void dummy(void){
	long tmp  = 0xc35f;		// 追加：ROPで利用するため（第1引数）
	long tmp2 = 0xc35e;		// 追加：ROPで利用するため（第2引数）
	long tmp3 = 0xc35a;		// 追加：ROPで利用するため（第3引数）
}
