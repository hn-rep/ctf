#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define	ADDR		"127.0.0.1"
#define	PORT		5000
#define	SEND_MSG	"test"

int tcp_client()
{
	struct sockaddr_in server;
	int sock;

	/* ソケット作成 */
	sock = socket(AF_INET, SOCK_STREAM, 0);

	/* 接続先の情報を設定 */
	server.sin_family		= AF_INET;
	server.sin_port			= htons(PORT);
	server.sin_addr.s_addr	= inet_addr(ADDR);

	/* TCPサーバに接続 */
	connect(sock, (struct sockaddr *)&server, sizeof(server));

	/* TCPサーバにデータ送信 */
	write(sock, SEND_MSG, sizeof(SEND_MSG));

	close(sock);

	return 0;
}

int main(void)
{
	tcp_client();

	return 0;
}
