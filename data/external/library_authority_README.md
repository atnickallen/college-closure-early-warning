# Library authority notes and UNITID → OCLC crosswalk

Watch-list enrichment only. **Not a model feature.** Holdings numbers still
come from IPEDS Academic Libraries (Urban). This folder stores *cited*
identifiers and transfer notes that campus HTML and keyless OCLC APIs do not
reliably return.

## UNITID → OCLC / WorldCat Registry

`oclc_unitid_crosswalk.csv` maps IPEDS `UNITID` to:

| Column | Meaning |
| --- | --- |
| `oclc_symbol` | OCLC institution symbol used in WorldCat holdings / ILL |
| `worldcat_registry_id` | WorldCat Registry numeric ID |
| `libraries_org_id` | libraries.org profile id |
| `related_oclc_symbol` | Parent/successor symbol (do **not** treat as this UNITID's own symbol) |

**How the join is made:** libraries.org (Library Technology Guides) publishes
`NCES LIBID` on academic-library profiles. For these schools that value equals
the IPEDS UNITID. A profile is accepted only when `NCES LIBID == UNITID`.
Volume counts on libraries.org are **not** copied into `lib_physical_books`.

OCLC's [Library Profiles API](https://developer.api.oclc.org/library-profiles-api)
and the old WorldCat Registry API require a WSKey; OCLC retired developer
access to Registry data on 2025-11-30. Until a key is configured, the public
libraries.org HTML is the documented substitute. ArchiveGrid
(`https://researchworks.oclc.org/archivegrid/`) is queried when reachable
(this environment often receives HTTP 403).

## Authority notes

`library_authority_notes.csv` is a sourced overlay for the shortlist:

- **Unique (`unique_flag=true`)** only when a named collection, archive, or
  documented surviving destination exists (Finlandia FAHC → Finlandia
  Foundation National; Medaille archives → Niagara; Simmons KY digital /
  returned institutional archives; PNCA Artists Archive at Willamette;
  Chatfield/Ursuline college-history archive).
- **Not unique** when WorldCat/public sources show only generic circulating
  stock or when a “records custodian” is transcripts, not books
  (Holy Names → Dominican; Presentation → St. Ambrose; Art Institutes;
  Cardinal Stritch — no public special-collection transfer found).

Finlandia: the Finnish-American collection claim is the **FAHC historical
archive**, not an invented IPEDS holdings figure. FAHC’s own page is the
item-level source (including the 1642 Christina Bibles). The closed Maki
Library is a separate circulating collection on libraries.org.

Re-run: `python3 scripts/07_report.py` (uses cached libraries.org HTML when
present, then this overlay).
