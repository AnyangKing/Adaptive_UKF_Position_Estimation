# Warning cleanup details

## Before

The final log from folder 171 contained:

- 2 hyperref PDF-string warnings at line 159;
- 3 underfull hbox warnings at lines 79--80 and 223.

The hyperref warning came from this heading:

```tex
\subsection{Adaptive-$R$ routing}
```

Math mode in section titles is safe for print output but unsafe for PDF
bookmarks unless a plain-text alternative is provided.

## Patch

The heading was changed to:

```tex
\subsection[Adaptive-R routing]{Adaptive-$R$ routing}
```

This is a formatting-only patch. It does not alter the manuscript text visible
to the reader.

## After

After two direct `pdflatex` runs:

- hyperref warnings: 0;
- fatal errors: 0;
- output PDF produced: yes;
- PDF pages: 11;
- remaining warnings: 3 underfull hbox warnings.

## Why the remaining underfull warnings were not edited here

The remaining warnings are caused by narrow table cells with mixed English and
Korean terms such as `residual whitening`, `continuous safe boundary`, and
`lag-1 residual whitening`. Fixing them may require table layout changes, which
is a separate visual decision. This folder intentionally keeps its patch narrow.
