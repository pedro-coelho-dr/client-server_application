# Variável para verificar o sistema operacional
ifeq ($(OS),Windows_NT) # Comandos para Windows
	
	RM = del /Q
	RUN_SERVER = start cmd /c "cd Documentos\InfraDeComunicacao && python server\server.py"
	RUN_CLIENT = start cmd /c "cd Documentos\InfraDeComunicacao && python client\client.py"
	
else

	UNAME_S := $(shell uname -s)

	ifeq ($(UNAME_S),Darwin) # Comandos para macOS
		
		RM = rm -f
		RUN_SERVER = osascript -e 'tell app "Terminal" to do script "cd Documents/InfraDeComunicacao && python3 server/server.py"'
		RUN_CLIENT = osascript -e 'tell app "Terminal" to do script "cd Documents/InfraDeComunicacao && python3 client/client.py"'

	else # Comandos para outros sistemas Unix-like
		
		RM = rm -f
		RUN_SERVER = xterm -e "cd Documents/InfraDeComunicacao && python3 server/server.py"
		RUN_CLIENT = xterm -e "cd Documents/InfraDeComunicacao && python3 client/client.py"
	endif
endif

all: redes

CC = clang
override CFLAGS += -g -Wno-everything -pthread -lm

SRCS = $(shell find . -name '*.c')
HEADERS = $(shell find . -name '*.h')

redes: $(SRCS) $(HEADERS)
	$(CC) $(CFLAGS) $(SRCS) -o "$@"

redes-debug: $(SRCS) $(HEADERS)
	$(CC) $(CFLAGS) -O0 $(SRCS) -o "$@"

clean:
	$(RM) redes redes-debug

run-server:
	$(RUN_SERVER)

run-client:
	$(RUN_CLIENT)

start:
	$(MAKE) run-server & $(MAKE) run-client
