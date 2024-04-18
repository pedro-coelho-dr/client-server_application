<p align="center">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/DiogoHMC/InfraDeComunicacao">
  <a href="https://github.com/DiogoHMC/InfraDeComunicacao/commits/main/">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/DiogoHMC/InfraDeComunicacao">
  </a>
   <img alt="License" src="https://img.shields.io/github/license/DiogoHMC/InfraDeComunicacao">
</p>



# Aplicação Cliente-Servidor

Trabalho de Infraestrutura de Comunicação<br>
Orientador: Petrônio Gomes <br>
Ciência da Computação - CESAR School<br>

<b>Objetivo geral:</b> Desenvolver uma aplicação cliente-servidor capaz de, na camada de
aplicação, fornecer um transporte confiável de dados considerando um canal com
perdas de dados e erros.


## Como executar

- No diretório 'src'

  ```
  python server.py
  python client.py
  ```
## Descrição

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

### verify_checksum(data, sequence_number, rcv_checksum)
Calcula o checksum dos dados e do número de sequência e verifica se é igual ao checksum recebido. Retorna verdadeiro se forem iguais.

### parse_pkt(packet)
Recebe um pacote e extrai os dados, o número de sequência e o checksum recebido.


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

### make_pkt(data, sequence_number)
Cria um pacote com os dados, número de sequência, um checksum.

### parse_pkt(packet)
Analisa um pacote recebido para extrair os dados, números de sequência e checksum.

### verify_checksum(data, sequence_number, last_sequence_number, rcv_checksum)
Verifica o checksum de um pacote recebido.


# Colaboradores

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/111138996?v=4" width=115><br><sub>Pedro Coelho</sub>](https://github.com/pedro-coelho-dr) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/103130662?v=4" width=115><br><sub>Yara Rodrigues</sub>](https://github.com/Yara-R) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/117921412?v=4" width=115><br><sub>Estela Lacerda</sub>](https://github.com/EstelaLacerda) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/116087739?v=4" width=115><br><sub>Diogo Henrique</sub>](https://github.com/DiogoHMC) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/117746778?v=4" width=115><br><sub>Matheus Gomes</sub>](https://github.com/MatheusGom) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/116605416?v=4" width=115><br><sub>Kaique Alves</sub>](https://github.com/Kaiquegb) |
| :---: | :---: | :---: | :---: | :---: | :---: |

