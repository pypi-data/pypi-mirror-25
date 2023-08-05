MULATOR = ../../../simulator/

.SECONDEXPANSION:

all: $(wildcard *.c) 
	$(CC) -Wall -O0 -g -std=c99 \
		-DM_PROFILE -DDEBUG1 -DDEBUG2 -DNO_PIPELINE \
		-I$(MULATOR) \
		$(MULATOR)/core/isa/decode_helpers.c \
		$(MULATOR)/core/isa/decompile.c \
		$(MULATOR)/cpu/misc.c \
		$(MULATOR)/core/opcodes.c \
        $(MULATOR)/core/pipeline.c \
		$(wildcard $(MULATOR)/core/isa/arm-thumb/*.c) \
		$(wildcard $(MULATOR)/core/operations/*.c) \
		$^

clean:
	rm -rf a.out a.out.*
