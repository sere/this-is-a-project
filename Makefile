# Makefile for locator
# Since this is a Python project, the Makefile just
# automates the operations needed to clean the
# directory

clean:
	rm -f *{~,.pyc}

pclean: clean
	rm -f *.{orig,rej}
