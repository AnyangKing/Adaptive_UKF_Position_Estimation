# Next step: 142. Journal-neutral front/back matter audit

## Why

The manuscript is now long enough and the major LaTeX hbox warnings are gone. The next visible issue
is no longer scientific depth; it is submission framing.

Current likely issues:

1. Header/title area may mention a specific journal draft state.
2. Author names and affiliations may still be placeholders.
3. Author Contributions, Funding, Data Availability, Acknowledgments, and Conflicts sections still
   need final author decisions.
4. If the target journal is not fixed, the manuscript should stay journal-neutral.

## Proposed 132 task

Audit the front matter and back matter without inventing author information.

Actions:

- Identify all placeholder strings.
- Decide which placeholders can be made journal-neutral.
- Do not fabricate author/funding/conflict statements.
- Record what must be supplied by the user/professor before final submission.
