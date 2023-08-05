- The program logic has been reworked to work much more generally.  You are no
  longer limited to just sections and subsections.  You can nest however deep
  you like.  This change is *backwards-incompatible* for your configuration
  file and your date files.

  - "header" → "h1"

  - "section_header" → "h2"

  - "subsection_header" → "h3"

  - "[sub]section_name" → "name"

  - "section_date" → "date"

  - And the "date" files must be renamed to "_date".
