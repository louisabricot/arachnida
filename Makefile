SPIDER = spider

SCORPIO = scorpio

LOGS =   $(SPIDER).log \
         $(SCORPIO).log \

DATA =   data

TESTS = tests

SRCS = srcs

.PHONY: all
all: install
	pip install -e .

.PHONY: clean
clean: 
	@/bin/rm -f $(LOGS)

.PHONY: fclean
fclean: clean
	@/bin/rm -rf $(DATA)
    
.PHONY: re
re: fclean all
    
.PHONY: test
test: 
	pytest $(TESTS)

.PHONY: black
black:
	black $(SRCS) $(TESTS)

.PHONY: install
install:
	pip3 install -r requirements.txt
