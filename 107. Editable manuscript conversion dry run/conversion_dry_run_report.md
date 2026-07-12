# Editable manuscript conversion dry-run report

## Builder result

Generated:

`editable_manuscript_conversion_dry_run.docx`

Source:

`105. Abstract and back-matter tightening/manuscript_sensors_candidate_tightened.md`

## Structural verification

Checked with `python-docx` after generation:

- Paragraphs: 130
- Native Word tables: 4
- Inserted images: 6
- Editable equation paragraphs: 23

Interpretation:

- The 23 Markdown math blocks were converted into editable equation-text paragraphs, not images.
- The three manuscript tables plus the internal Figure File Manifest were converted into native Word tables.
- Fig. 1--6 were inserted as images.

## Render QA status

Render QA was attempted using the documents skill renderer:

`render_docx.py editable_manuscript_conversion_dry_run.docx --output_dir rendered_pages --emit_pdf`

Result:

- Render failed because the renderer could not find the LibreOffice/soffice executable (`FileNotFoundError: WinError 2`).
- Therefore, visual PNG QA is not complete.

This is acceptable only as a dry-run artifact. The DOCX should not be treated as visually approved until it is rendered and inspected on a machine with LibreOffice/soffice available.

## Known limitations

- Equations are editable text paragraphs, not final Word equation objects.
- Tables are native Word tables, but visual width and page breaks were not rendered.
- This is not a final submission DOCX.
- Human-author metadata remains unresolved.

## Next step

Run the same DOCX through visual render QA after installing or locating LibreOffice/soffice, or continue with a Word-template conversion on a system where rendering works.
