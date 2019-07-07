# Sanskrit-Hyphenation

This is a package for hyphenating transliterated Sanskrit texts in LaTeX.

I wrote it because there is no support for Sanskrit in babel, and because
polyglossia, which does include [Sanskrit hyphenation
patterns](https://github.com/hyphenation/tex-hyphen/blob/47a97a7db314f5774120925d92a51b0eeae4f799/hyph-utf8/tex/generic/hyph-utf8/patterns/tex/hyph-sa.tex),
cannot currently hyphenate Sanskrit texts in LuaTeX, [for technical
reasons](https://tex.stackexchange.com/questions/283567/error-polyglossia-for-sanskrit-and-hindi-with-lualatex-but-not-with-xelatex).
Compared to the polyglossia Sanskrit patterns---which were originally written by
Yves Codet---, mine introduce two novelties.

Firstly, they work correctly with all precomposed characters. By contrast, some
precomposed characters---liquids, for instance---are missing from the
polyglossia patterns, such that _kṛtvam_ with 'ṛ' = U+1E5B (LATIN SMALL LETTER R
WITH DOT BELOW) is not hyphenated as _kṛ-tvam_, as it should be, but rather as
_kṛtvam_, without any hyphen. I made sure that my patterns work with both
composed and decomposed characters. However, they are designed to deal correctly
_only_ with text that is encoded in one of the four [Unicode normalization
forms](https://unicode.org/reports/tr15). Mixing several normalization forms
might yield incorrect results. Since (correct) texts are supposed to be encoded
in a single given normalization form, this shouldn't be an issue.

Furthermore, the hyphenation policy is different. Patterns in polyglossia
systematically keep together clusters of consonants, such that _vikṣiptam_ is
hyphenated as _vi-kṣi-ptam_. By contrast, I allow breaks inside runs of
consonants in certain circumstances. The term _vikṣiptam_, for instance, is
hyphenated as _vi-kṣip-tam_. To determine acceptable break points inside
consonants clusters, I used [Elisa Freschi's
heuristic](http://elisafreschi.com/2014/06/17/hyphenation-in-transliterated-sanskrit-texts/),
which is to treat as syllable starters runs of consonants followed by a vowel
that can occur at the beginning of a word. I used Monier-William's dictionary,
as distributed by the [University of
Cologne](https://www.sanskrit-lexicon.uni-koeln.de), to extract the necessary
data.

The result is far from being satisfactory enough, but is still preferable, I
believe, to the way polyglossia segments Sanskrit texts. Much improvements are
still needed.

## Installation

### For XeLaTeX

Copy `sanskrit-hyphenation.fmt`and `sanskrit-hyphenation.sty` to the directory
your document resides in (or in some other appropriate location). Then, to
compile a document named `my_document.tex`, use a command like the following:

	xelatex -fmt sanskrit-hyphenation.fmt my_document.tex

### For LuaLaTeX

Like for XeLaTeX, except that the file `sanskrit-hyphenation.fmt` should not be
used. Just copy the file `sanskrit-hyphenation.sty` in an appropriate location,
and compile your document as usual.

## Usage

The package defines a single environment `hyphenatesanskrit`. Use it like so:

	\documentclass{article}

	\usepackage{sanskrit-hyphenation}

	\begin{document}
	\begin{hyphenatesanskrit}
	kṛtvam
	\end{hyphenatesanskrit}
	\end{document}

To save some typing, you might want to define a command in the document preamble:

	\newcommand\sanskritword[1]{\begin{hyphenatesanskrit}#1\end{hyphenatesanskrit}}

Then, somewhere in the document:

	\sanskritword{kṛtvam}
