all: sanskrit-hyphenation.sty sanskrit-hyphenation.fmt

test: test_codet.hyp test_this.hyp

clean:
	rm -f *.log *.aux *.pdf *.hyp

.PHONY: all test clean

sanskrit-hyphenation.tex: mkpatterns.py monier.txt patterns.tpl
	python3 $< > $@

sanskrit-hyphenation.fmt: wrap-fmt.tex sanskrit-hyphenation.tex
	xelatex -etex -ini -jobname sanskrit-hyphenation $<

sanskrit-hyphenation.sty: mkpackage.py package.tpl sanskrit-hyphenation.tex
	python3 $< > $@

test_codet.pdf: test_codet.tex test_text.tex
	xelatex $<

test_this.pdf: test_this.tex test_text.tex sanskrit-hyphenation.sty
	lualatex $<

%.hyp: %.pdf
	pdftotext $< $@
