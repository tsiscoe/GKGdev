# Legacy Content Review

This import is a preservation pass, not a semantic rewrite. The legacy repository was not a fork of `safishamsi/graphify`; it was a small knowledge-graph/content project with 32 tracked files and no shared git ancestry with upstream.

What is useful:

- The `knowledge_graph/intake/AI Dev/` corpus contains AI development notes that are suitable for a Graphify worked example or internal knowledge corpus.
- The folder layout documents the earlier intended taxonomy: intake, analysis, assessments, debriefs, archive, governance, and toolkit.

Known limitations:

- The imported files have not been regenerated with current `graphifyy`.
- Some placeholder README files are skeletal.
- Generated legacy graph artifacts were excluded because current Graphify should rebuild fresh outputs.

Suggested next step:

Run `graphify extract worked/graphify-dev-legacy/raw --force` and commit the resulting `graphify-out` or curated outputs if this becomes an official worked example.

Additional note:

- The
aw/00_Inbox/ batch is a direct source-file import from Google Drive and has not been curated beyond exact-file selection.

Additional project-source note:

- The
aw/01_Projects/ batch is a direct source-file import from Google Drive, preserving MilTech, AI Dev, and NEKOnet grouping.

Additional document-source note:

- The latest batch includes PDFs and a NotebookLM briefing from Google Drive plus local Downloads, preserved as raw source material for future Graphify extraction.

Full NEKOnet import note:

- The full NEKOnet project-folder import skipped duplicate names and duplicate file hashes; see NEKOnet-import-manifest.md for the copied/skipped breakdown.

Document/style prompt note:

- This batch imports Tools for Thought plus Style Prompts assets and removes the two previously committed large NEKOnet videos from the active tree; see document-style-import-manifest.md for copied/skipped details.

Claude/NotebookLM note:

- This batch imports GitYana project notes and de-duplicates NotebookLM AI Dev notes against existing migrated content; see claude-notebooklm-import-manifest.md.
