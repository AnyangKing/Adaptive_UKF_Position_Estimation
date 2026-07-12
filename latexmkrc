# latexmk configuration for the root manuscript.
# One-command build:  latexmk manuscript.tex   (runs pdflatex + bibtex + reruns)
# Clean artifacts:     latexmk -c
#
# Format convention (2026-07-12, user directive): LaTeX / IEEEtran only. No Word/DOCX.
# manuscript.tex is a living document at project root; edit it in place.

$pdf_mode = 1;          # produce PDF via pdflatex
$bibtex_use = 2;        # run bibtex when refs.bib changes; allow it to run even w/o \citation warnings
$out_dir = '.';         # keep output at root

# Extra build artifacts latexmk should also clean up with `latexmk -c` / `-C`.
$clean_ext = 'bbl fdb_latexmk fls synctex.gz';
