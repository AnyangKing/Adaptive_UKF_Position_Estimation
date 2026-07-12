# 106. Editable equation and table conversion plan

## Purpose

This folder prepares the next practical conversion step: turning Markdown math blocks and Markdown tables into journal-template-ready editable equations and native tables.

Folder 105 produced the current manuscript candidate. It is scientifically coherent, but it still contains fenced Markdown math and wide Markdown tables that will not survive final Word/LaTeX formatting unchanged.

## Inputs

- `105. Abstract and back-matter tightening/manuscript_sensors_candidate_tightened.md`
- `100. Manuscript formatting prep/equation_numbering_plan.md`
- `103. Sensors free-format dry run/conversion_breakage_log.md`

## Outputs

- `equation_conversion_plan.md`
- `table_conversion_plan.md`
- `word_latex_conversion_decisions.md`
- `conversion_order.md`
- `precommit_verification.md`

## Current counts

- Fenced math blocks: 23
- Markdown table lines: 37
- Manuscript-facing tables: Table 1, Table 2, Table 3
- Internal table-like manifest: Figure File Manifest

## Decision

Do not convert to a final template in this folder. First define the conversion units and risk points so the actual Word/LaTeX conversion does not silently break equations, table layout, or claim boundaries.
