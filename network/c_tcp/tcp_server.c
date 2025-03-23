#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define	PORT	5000

int tcp_server()
{
	int sock, sock_server;
	struct sockaddr_in server;
	struct sockaddr_in client;
	char recv_buf[256];
	int len;

	/* TCPサーバ用ソケット作成 */
	sock_server = socket(AF_INET, SOCK_STREAM, 0);

	/* TCPサーバ用ソケットの設定 */
	server.sin_family		= AF_INET;
	server.sin_port			= htons(PORT);
	server.sin_addr.s_addr	= INADDR_ANY;

	bind(sock_server, (struct sockaddr *)&server, sizeof(server));

	/* TCPクライアントからの接続要求待ち */
	listen(sock_server, 5);

	/* TCPクライアントからの接続要求受け付け */
	len = sizeof(client);
	sock = accept(sock_server, (struct sockaddr *)&client, &len);

	/* TCPクライアントからデータを受信 */
	len = read(sock, recv_buf, sizeof(recv_buf));
	printf("len=%d, recv_buf=%s\n", len, recv_buf);

	close(sock);
	close(sock_server);

	return 0;
}

int main(void)
{
	tcp_server();

	return 0;
}
