<p align="center">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/DiogoHMC/InfraDeComunicacao">

  <a href="https://github.com/DiogoHMC/InfraDeComunicacao/commits/main/">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/DiogoHMC/InfraDeComunicacao">
  </a>

   <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">

</p>

# InfraDeComunicacao

## Como executar o programa:

- Va para o arquivo Makefile e troque o caminho para que direcione ao aquivo InfraDeComunicacao na sua máquina

  ```bash

  
  "cd SeuCaminho/InfraDeComunicacao && python3 server/server.py"

  "cd SeuCaminho/InfraDeComunicacao && python3 client/client.py"

  ```

- Realize o seguinte comando no terminal

  ```bash
  make start
  ```

## Funcionamento do server.py:

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
