# Pra executar: no terminal execute 'make'

CC = g++
PROJECT = output
SRC = highGui.cpp
LIBS = `pkg-config --cflags  --libs opencv4`
$(PROJECT) : $(SRC) 
	$(CC) $(SRC) -o $(PROJECT) $(LIBS)