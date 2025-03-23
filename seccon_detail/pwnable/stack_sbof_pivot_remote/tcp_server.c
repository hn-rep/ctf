#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int tcp_server(int port, char *buf, int len)
{
	int sock, sock_server;
	struct sockaddr_in server;
	struct sockaddr_in client;

	/* TCPサーバ用ソケット作成 */
	sock_server = socket(AF_INET, SOCK_STREAM, 0);

	/* TCPサーバ用ソケットの設定 */
	server.sin_family		= AF_INET;
	server.sin_port			= htons(port);
	server.sin_addr.s_addr	= INADDR_ANY;

	bind(sock_server, (struct sockaddr *)&server, sizeof(server));

	/* TCPクライアントからの接続要求待ち */
	listen(sock_server, 5);

	/* TCPクライアントからの接続要求受け付け */
	len = sizeof(client);
	sock = accept(sock_server, (struct sockaddr *)&client, &len);

	/* TCPクライアントからデータを受信 */
	len = read(sock, buf, sizeof(buf));
	printf("len=%d, buf=%s\n", len, buf);

	close(sock);
	close(sock_server);

	return 0;
}
