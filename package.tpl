\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{sanskrit-hyphenation}

\RequirePackage{ifluatex}
\ifluatex
$CODE
\fi
\newenvironment{hyphenatesanskrit}{\language=\mysanskrit}{}
