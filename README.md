<p align="center">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/DiogoHMC/InfraDeComunicacao">
  <a href="https://github.com/DiogoHMC/InfraDeComunicacao/commits/main/">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/DiogoHMC/InfraDeComunicacao">
  </a>
   <img alt="License" src="https://img.shields.io/github/license/DiogoHMC/InfraDeComunicacao">
</p>



# Aplicação Cliente-Servidor

<b>Cadeira:</b> Infraestrutura de Comunicação - Ciência da Computação<br>
<b>Faculdade:</b> CESAR School<br>
<b>Orientador:</b> Petrônio Gomes

<b>Alunos:</b> Diogo Henrique, Estela de Lacerda, Kaique Alves, Matheus Gomes, Pedro Coelho, Yara Rodrigues

<b>Objetivo geral:</b> Desenvolver uma aplicação cliente-servidor capaz de, na camada de
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

## Client.py

### Funcionamento do client.py:
### make_pkt(data, sequence_number):
Essa função cria um pacote que será enviado ao servidor, juntando os dados a serem transmitidos e o número de sequência do pacote.
Ela também calcula um checksum para garantir que os dados não sejam corrompidos durante a transmissão.

### parse_pkt(packet):
Esta função analisa o pacote recebido do servidor, separando os dados, o número de sequência e o checksum para que possam ser verificados individualmente.
Ela verifica se o pacote está no formato correto e, em caso afirmativo, extrai as informações essenciais para processamento adicional.

### verify_checksum(data, sequence_number, rcv_checksum):
Aqui, verificamos se o checksum recebido do servidor corresponde ao checksum calculado localmente.
O checksum é uma medida de verificação de integridade que nos ajuda a garantir que os dados não tenham sido alterados durante a transmissão.

### isNAK(client_socket, data, sequence_number):
Esta função é acionada quando o servidor envia um NAK (Negative Acknowledgement), indicando que ocorreu um erro na transmissão do pacote.
Ela é responsável por lidar com a situação de reenvio do pacote para garantir que os dados sejam entregues corretamente.

### isACK(client_socket, sequence_number):
Aqui, verificamos se recebemos um ACK (Acknowledgement) do servidor em resposta ao pacote enviado.
Se recebermos um ACK com o número de sequência esperado, isso indica que o pacote foi entregue com sucesso.
Se um NAK for recebido ou se não houver resposta do servidor dentro do tempo limite, consideramos que ocorreu um erro na transmissão.

### send(client_socket, data, sequence_number):
Essa função é responsável por enviar um pacote ao servidor contendo os dados a serem transmitidos e o número de sequência do pacote.
Ela utiliza a função make_pkt para criar o pacote e o envia através do socket do cliente.

### interface(client_socket):
Aqui, implementamos a interface interativa do cliente, que permite ao usuário enviar mensagens para o servidor.
O usuário tem a opção de enviar uma mensagem ou sair do programa, tornando a interação mais amigável e intuitiva.

### handshake(client_socket):
O handshake é uma etapa crucial na inicialização da comunicação entre cliente e servidor.
Nesta função, o cliente envia um SYN (synchronize) ao servidor, aguarda um SYN-ACK em resposta e envia um ACK de confirmação.
Se o handshake for bem-sucedido, podemos prosseguir com a comunicação; caso contrário, é necessário investigar e corrigir qualquer problema encontrado.

### connection(server_host='localhost', server_port=65432):
Esta função é responsável por estabelecer a conexão com o servidor.
Ela cria um socket e o conecta ao servidor especificado.
Após a conexão bem-sucedida, o handshake é realizado e, se for bem-sucedido, a interface do cliente é iniciada para interação com o usuário.


### Server.py
Funcionamento do server.py:

### start_server:
Inicialização do servidor TCP/IP:

Aqui é onde o servidor TCP/IP é iniciado, definindo o host como "localhost" e a porta como "65432".
Um objeto socket é criado para comunicação TCP usando endereços IPv4.
Vinculação do endereço e porta:

O socket é vinculado ao endereço do servidor e à porta especificada.
O servidor é configurado para escutar por conexões de clientes.
Loop infinito para aceitar conexões:

O código entra em um loop infinito, aguardando e aceitando conexões com clientes.
Após aceitar uma conexão, o handshake é realizado.
Se o handshake for bem-sucedido, a interface do servidor é executada; caso contrário, a conexão é fechada.
handshake:
### Controle de tentativas:

Variáveis attempts e max_attempts são utilizadas para controlar as tentativas de handshake.
Recebimento do SYN:

O servidor aguarda a chegada do SYN do cliente. Se recebido, passa para a próxima etapa.
Envio do SYN-ACK e espera pelo ACK:

O servidor envia SYN-ACK para o cliente e aguarda o recebimento de um ACK em resposta.
Se o ACK for recebido dentro do tempo limite, o handshake é concluído com sucesso.
Tratamento de timeouts e falhas:

Se ocorrer um timeout ou se o cliente enviar uma resposta diferente de ACK, o servidor pode tentar novamente até atingir o número máximo de tentativas.

### server_interface:
Menu interativo:
Um menu é exibido no terminal do servidor, permitindo que o usuário escolha entre as opções de escutar e aguardar resposta de um único cliente ou múltiplos clientes.

### listening:
Recepção de pacotes:

O servidor continua aguardando pacotes enviados pelo cliente.
Os pacotes são decodificados em uma string e verificados quanto à integridade e número de sequência.
Verificação de checksum:

O checksum do pacote recebido é verificado para garantir a integridade dos dados.
Envio de ACK ou NACK:

Se os dados estiverem íntegros, um ACK é enviado ao cliente. Caso contrário, um NACK é enviado para solicitar a retransmissão do pacote.
Reconstrução da mensagem:

Os dados recebidos são adicionados à mensagem completa e, se for recebido um pacote com o número de sequência esperado, a mensagem completa é impressa e resetada para receber uma nova string.

### listening_group:
Recepção de pacotes em grupo:

Este método lida com a recepção de pacotes quando múltiplos clientes estão enviando dados simultaneamente.
Ele acumula pacotes em um buffer até que possa confirmar a integridade de um grupo de pacotes.
Envio de ACK ou NACK em grupo:

Após receber um grupo de pacotes, o servidor envia um ACK em grupo se todos os pacotes estiverem íntegros, ou um NACK em grupo se algum pacote estiver corrompido.
Reconstrução da mensagem completa:

Após o envio do ACK ou NACK em grupo, a mensagem completa é impressa e resetada para receber uma nova string.
Outras funções:

### make_pkt(data, sequence_number):

Esta função cria um pacote a ser enviado, incluindo os dados e o número de sequência.
Um checksum é calculado e anexado ao pacote para garantir a integridade dos dados durante a transmissão.

### send_ack_nak(client_connection, is_ack):

Esta função envia um ACK (Acknowledgement) se is_ack for verdadeiro, ou um NAK (Negative Acknowledgement) caso contrário.
É utilizada para fornecer feedback ao cliente sobre a integridade dos dados recebidos.

### parse_pkt(packet):

Esta função analisa o pacote recebido do cliente e extrai os dados, número de sequência e checksum.
Os componentes essenciais do pacote são separados para posterior verificação.

verify_checksum(data, sequence_number, rcv_checksum):

Esta função verifica se o checksum recebido corresponde ao esperado para garantir a integridade dos dados.
O checksum é recalculado com base nos dados e número de sequência recebidos e comparado com o checksum recebido do cliente.


# Colaboradores

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/111138996?v=4" width=115><br><sub>Pedro Coelho</sub>](https://github.com/Dricalucia) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/103130662?v=4" width=115><br><sub>Yara Rodrigues</sub>](https://github.com/Yara-R) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/117921412?v=4" width=115><br><sub>Estela Lacerda</sub>](https://github.com/EstelaLacerda) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/116087739?v=4" width=115><br><sub>Diogo Henrique</sub>](https://github.com/DiogoHMC) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/117746778?v=4" width=115><br><sub>Matheus Gomes</sub>](https://github.com/MatheusGom) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/116605416?v=4" width=115><br><sub>Kaique Alves</sub>](https://github.com/Kaiquegb) |
| :---: | :---: | :---: | :---: | :---: | :---: |

