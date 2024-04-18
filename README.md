# Aplicação Cliente-Servidor

Infraestrutura de Comunicação

Ciência da Computação

Cesar School

Prof.: Petrônio Gomes

Alunos:
	Diogo
 	Estela
 	Kaique Alves
 	Matheus Gomes
 	Pedro Coelho
 	Yara
  
Objetivo geral: Desenvolver uma aplicação cliente-servidor capaz de, na camada de
aplicação, fornecer um transporte confiável de dados considerando um canal com
perdas de dados e erros.


## Como executar:

- No diretório 'src'

  ```
  python server.py
  python client.py
  ```

## Descrição:

![arq2](https://github.com/DiogoHMC/InfraDeComunicacao/assets/111138996/58c568b5-1453-4dfd-b4b5-cb646bd34da9)

## Cliente

### connection(server_host, server_port)
Estabelece a conexão com o servidor e inicia a interface após um handshake bem-sucedido.

### handshake(client_socket)
Realiza o handshake inicial com o servidor para estabelecer a conexão. Envia "SYN" e espera por "SYN-ACK".

### interface(client_socket)
Fornece uma interface interativa ao usuário para enviar pacotes individualmente ou em grupo e simular erros de transmissão.

### send_batch(client_socket, corrupt, drop)
Envia uma sequência de mensagens em lotes. Cada mensagem é dividida em pacotes de até 5 caracteres. Permite simular a corrupção e perda de pacotes.

### send_batch_group(client_socket, corrupt, drop)
Envia uma sequência de mensagens usando confirmação em grupo. Utiliza uma janela deslizante e também permite simular corrupção e perda de pacotes.

### send(client_socket, data, sequence_number, last_sequence_number, corrupt)
Envia um pacote de dados pelo socket do cliente. Se corrupt for verdadeiro, o pacote é enviado com um checksum adulterado.

### make_pkt(data, sequence_number, last_sequence_number, corrupt)
Cria um pacote com os dados, número de sequência, último número de sequência e um checksum. Se corrupt for verdadeiro, o checksum é adulterado.

### receive_ack_nak(client_socket, timeout)
Aguarda o recebimento de um ACK ou NAK dentro de um tempo limite. Se um pacote for recebido, é verificado e o tipo de resposta é retornado juntamente com o número de sequência.

### parse_pkt(packet)
Recebe um pacote e extrai os dados, o número de sequência e o checksum recebido. Levanta um erro se o pacote tiver tamanho inválido.

### verify_checksum(data, sequence_number, rcv_checksum)
Calcula o checksum dos dados e do número de sequência e verifica se é igual ao checksum recebido. Retorna verdadeiro se forem iguais.


## Servidor

### start_server(host, port)
Inicia o servidor, aguarda conexões e processa os handshakes.

### handshake(client_connection)
Realiza o handshake do lado do servidor.

### server_interface(client_connection)
Fornece uma interface para o servidor escolher entre confirmação individual ou em grupo.

### listening(client_connection)
Escuta pacotes individuais e envia confirmações individuais.

### listening_group(client_connection)
Escuta pacotes em uma janela deslizante e envia confirmações em grupo.

### send_ack_nak(client_connection, ack_nak, sequence_number)
Envia um ACK ou NAK como resposta para o cliente.

### parse_pkt(packet)
Analisa um pacote recebido para extrair os dados, números de sequência e checksum.

### verify_checksum(data, sequence_number, last_sequence_number, rcv_checksum)
Verifica o checksum de um pacote recebido.

### make_pkt(data, sequence_number)
Prepara um pacote com os dados e o número de sequência recebidos, adicionando um checksum para verificação de integridade. É usada para responder ao cliente com um ACK (confirmação) ou NAK (negação) após receber e processar um pacote.











- **start_server:**
	- Criação do servidor TCP/IP, onde o host é estabelecido como "localhost" e o port como "65432".
	- Um objeto socket é criado, especificando que foi utilizado o TCP para comunicação, além de estar sendo usando endereços IPv4.
 	- O socket vincula o endereço do servidor e a porta, além do servidor ser colocado para escutar por envios do cliente.
  	- O código entra em um loop infinito, onde ele espera e aceita conexões com um cliente.
  	- A verificação do Handshake é feita, caso sucedida, a interface é executada ou caso falha, a conexão é fechada.
 
- **handshake:**
	- Criação de variáveis de controle "attempts" e "max_attempts".
	- O servidor decodifica dados recebidos pelo servidor e caso a string recebida for "SYN", a primeira etapa foi sucedida.
 	- O servidor codifica e envia uma string "SYN-ACK" para o cliente, aguardando receber a resposta "ACK", concluindo a segunda etapa.
  	- O servidor ao receber de volta a resposta "ACK", o handshake de três vias é concluído e a conexão será feita.
  	- Caso o servidor espere mais de um segundo ou o cliente enviar uma resposta que não seja "ACK", o handshake é considerado falho.
  	- Caso falho, ocorre outras tentativas de serem feitas o handshake até ser concluída ou atingir o quantidade de "max_attempts".

- **server_interface:**
	- Impressão do menu no terminal do servidor, em loop infinito, que aceitará apenas os inputs indicados:
 		- 1 - Escutar e esperar resposta de um cliente.
   		- 2 - Escutar e esperar resposta de multíplos clientes.

- **listening:**
	- Criação de uma variável de armazenamento da mensagem completa mandada pelo usuário "full_message".
 	- O servidor aguarda continuamente por pacotes, os decodificando para uma string.
  	- O servidor apenas irá aguardar por pacotes não vazios e caso receba um vazio, a conexão terminará.
  	- Uma análise usando parse_pkt é feita no pacote recebido para extrair os componentes essenciais do pacote.
  	- O verify_checksum é chamado para verificar se a quantidade de dados recebidos corresponde com o pacote.
  	- Caso a verificação seja bem sucedida, os dados serão adicionados para "full_message" e será enviado um ACK.
  	- Caso a verificação seja falha, será enviado um NACK para solicitar a retransmissão do pacote.
  	- Uma verificação do número de sequência do pacote recebido ser igual ao último número de sequência esperado é feita.
  	- Caso o resultado da verificação anterior for verdadeira, a "full_message" é impressa e resetada para receber uma nova string.
  	- O except é utilizado para capturar mensagens de erro recebidas e será impressa no terminal.

- **listening_group:**
	- Criação de uma variável de armazenamento da mensagem completa mandada pelo usuário "full_message".
  	- Criação de uma variável de armazenamento dos dados até que possam ser processados em pacotes completos "buffer".
	- Criação de uma lista para armazenar tuplas de informações sobre os pacotes recebidos para posterior confirmação "packets_to_ack".
 	- O servidor aguarda continuamente por dados do cliente, os decodificando para uma string.
  	- O servidor apenas irá aguardar por um conjunto de dados não vazios e caso receba um vazio, a conexão terminará e sairá do loop.
  	- Uma análise é feita no buffer para extrair pacotes de comprimento 17 caracteres, os removendo do buffer.
	- Uma análise usando parse_pkt é feita no pacote para extrair os componentes essenciais do pacote.
   	- Caso um erro ocorra na etapa anterior, o except irá capturar o erro e será posteriormente impresso.
  	- O verify_checksum é chamado para verificar se a quantidade de dados recebidos corresponde com o pacote.
  	- Caso a verificação seja bem sucedida, o seqnum e um sinal ACK = TRUE serão adicionados para "packets_to_ack".
  	- Após isso, os dados recebidos pela variável "data" é concatenado para a variável "full_message"
  	- Caso a verificação seja falha, o seqnum e um sinal NACK = FALSE serão adicionados para "packets_to_ack".
	- Ocorre a verificação se o número de pacotes enviado é igual ao esperado.
  	- Ocorre a verificação se o número de sequência do pacote atual é igual ao número de sequência esperado.
   	- Ocorre a verificação se todos os ACKS recebidos recebeream o valor "TRUE".
   	- Caso o resultado seja que todos receberam "TRUE", o servidor envia um ACK em grupo para o último pacote recebido e é impresso.
   	- Caso o resultado seja que ocorreu um NACK, o servidor envia um NACK em grupo para o último pacote recebido e é impresso.
   	- Após o envio do ACK ou NACK em grupo, o "packets_to_ack" é resetado e a string "full_message" é impressa e resetada.
   	- O except é utilizado para capturar mensagens de erro recebidas e será impressa no terminal.


