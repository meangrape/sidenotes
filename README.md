---
title: Writing for the sidenote layout
author: Layout notes
date: September 2026
papersize: letter
bibliography: example/readme.bib
csl: tex/chicago-notes-bibliography.csl
---

# What this document is

This is a short article written in Markdown. It exists to show, on itself,
how notes are written so that they land in the margin, level with the mark
that calls them.[^what] The same file builds to a web page and to a PDF, and
in both the page is divided the same way: the left two thirds hold the text,
the right third holds the notes.

You write in ordinary pandoc Markdown. Headings start with `#`, emphasis uses
`*asterisks*`, and a paragraph is any run of lines separated by a blank
line.[^pandoc] Nothing about the layout is written into the text. The layout
lives in a few small files in folders beside this one, and the text only
ever says *put a note here*.

[^what]: A note like this one. Its first line sits on the line of text
    that carries its number.

[^pandoc]: Pandoc's own manual describes the full syntax. Only footnotes
    and headings matter for the layout.

# Writing a single note

A note has two halves. In the sentence, at the point where the number
should appear, you write a label in square brackets with a caret:
`[^label]`. Anywhere else in the file, usually just after the paragraph,
you write the same label followed by a colon and the text of the
note.[^label] The label is for you. It can be a word or a number and it is
never printed; the notes are numbered in the order their marks appear.

```markdown
Text with a note.[^cost] More text.

[^cost]: The text of the note.
```

A note may run to more than one paragraph. Indent every line after the
first by four spaces and separate the paragraphs with a blank line, as the
note on this sentence does.[^multi] Keep notes short where you can. A note
that runs longer than the paragraph it hangs from will push the notes below
it down the page, and in the PDF it may not fit before the page ends.

[^label]: The label here is `label`. In the source it reads `[^label]`.

[^multi]: This note has two paragraphs.

    The second paragraph is indented by four spaces in the source so that
    pandoc knows it still belongs to the note.

# Notes and page breaks

The web page has no pages, so a note is never moved. The PDF does have
pages, and a note whose mark falls near the foot of a page may not have
room below the mark. When that happens the note is pulled up the margin
just far enough to fit, so that its last line sits level with the last
line of text on the page. It is not split. Its mark stays where it is in
the text.[^break] Only a note taller than the whole margin is carried to
the next page. If you would rather the note were level with its mark,
shorten the note or move the sentence. There is no markup for forcing it.

This is the one place the two outputs differ. On the web the note on the
previous sentence sits level with its mark. In the PDF, if its mark lands
near the foot of a page, the note starts above the mark.

[^break]: This note is written to fall across a page break in the PDF. It
    is long enough not to fit in the margin left below its mark, and LaTeX
    cannot split a margin note between pages, so the marginfix package
    pulls the whole note up until it fits. The number in the text does not
    move. If you change the paper size or the font, this note may land
    somewhere else, and the paragraph that carries it may need lengthening
    or shortening to straddle a break again.

# Consecutive notes

When several marks fall close together, their notes cannot all sit level
with their marks without overlapping. The rule is that each note sits as
high as it can without touching the note above it. So the first is level
with its mark and the rest queue below it. This sentence carries three
marks in a row, one on the first clause,[^one] one on the second,[^two] and
one at the end,[^three] and the margin shows the queue.

Nothing special is written to get this. Three marks, three note bodies, and
the layout does the rest. The queue resolves itself: once the text has moved
on far enough, the next note is level with its mark again.[^again]

[^one]: The first of three notes on one sentence. It is level with its
    mark because nothing sits above it.

[^two]: The second. Its mark is on the same line as the first, so it
    waits below the first note.

[^three]: The third, queued below the second for the same reason.

[^again]: Back in step. This note's mark is far enough down the page that
    the queue above has cleared.

# Fonts

Both outputs use the same ordered list of typefaces and take the first one
that is installed on the machine doing the build. The list is written once
in each of the two style files.[^where] The order is:

1. Arbitare Sans, at weight 400
2. Serif
3. Sans Serif
4. Helvetica Neue

On the web the second and third entries are the browser's generic families,
and a generic family always matches. So a browser that lacks Arbitare Sans
will stop at *Serif* and never reach Helvetica Neue.[^generic] LaTeX has no
generic families, so the PDF build stands in Latin Modern Roman for *Serif*
and Latin Modern Sans for *Sans Serif*; both ship with every TeX
installation and so, as on the web, the fourth entry is only reached if
the TeX fonts are missing.

[^where]: `css/style.css` for the web page, `tex/preamble.tex` for the PDF.

[^generic]: If Helvetica Neue is meant as a real fallback, put it before
    the generic names in both files.

# Citing sources

References live in a BibTeX file named in the metadata block, and a
citation in the text is the entry's key in square brackets with an at
sign: `[@brandi1963]`. Pandoc reads the BibTeX file itself, turns the key
into a formatted citation and collects everything cited into a reference
list at the end. No separate bibtex or biber run is involved, and the two
outputs format their citations identically. The style
file named in the metadata decides the shape of both. This document uses
the Chicago notes style, so every citation becomes a note in the margin,
like this one.[@brandi1963] Page numbers and other locators follow the key
inside the brackets.[@munozvinas2005, 91--93] A second citation of the
same work is shortened automatically.[@brandi1963, 34]

A citation may also sit inside an ordinary note, where it is set as text
rather than as a note of its own.[^inside] Several keys separated by
semicolons make one note.[@appelbaum2007; @feller1994]

Delete the `csl` line from the metadata and pandoc falls back to its
built-in Chicago author–date style, which puts citations in the text as
parenthetical author and year and leaves the margin to your own notes.
Either way pandoc appends the reference list at the end of the document,
so end the file with a heading for it. To put the list somewhere else,
insert an empty fenced block with the id `refs` where it should go, as in
the example below. That block is pandoc-only syntax; other Markdown
readers show it as literal text, which is why this file does without it.

Give any entry whose title is not in English a `langid` field, as the
Brandi entry has. Without it the style capitalises the title as if it
were English, so *Teoria del restauro* would come out as *Teoria Del
Restauro*.[^langid]

```markdown
Brandi set out the argument.[@brandi1963, 34]

# References

::: {#refs}
:::
```

[^inside]: See @appelbaum2007 on the same point. Written as `@appelbaum2007`,
    without brackets, the citation is set as a name in running text.

[^langid]: `langid = {italian}` in the BibTeX entry. BibLaTeX uses the
    same field name, so a bibliography that already carries it needs
    nothing more.

# Building

Run the driver script on the Markdown file. It runs pandoc twice, once
for each output, and writes both into `output/`:

```sh
./build.py README.md            # output/README.html and output/README.pdf
./build.py README.md -t pdf     # one output only
./build.py README.md --papersize a4 --verbose
./build.py README.md -- --toc   # anything after -- goes straight to pandoc
./build.py --help
```

The script needs only Python and pandoc; its `uv` header lets `uv run`
start it with no setup. Every option is a pandoc option of the same name
with a default that points at the files in this folder:

```
build.py
css/style.css                      web page layout and fonts
lua/sidenotes.lua                  pandoc filter, footnotes to sidenotes
tex/preamble.tex                   PDF layout, fonts and margin notes
tex/chicago-notes-bibliography.csl citation style
example/readme.bib                 references for this document
output/                            built files
```

With the defaults filled in, the two pandoc commands it runs are:

```sh
pandoc README.md --citeproc --standalone --lua-filter=lua/sidenotes.lua \
       --css=css/style.css --embed-resources -o output/README.html
pandoc README.md --citeproc --pdf-engine=lualatex \
       --include-in-header=tex/preamble.tex -o output/README.pdf
```

The paper size of the PDF is set in the metadata block at the top of the
file. Leave the `papersize` line out and you get letter; write `a4` or
`legal` for the others.[^paper] The web page ignores it.

The Lua filter rewrites each footnote as an inline span for the web page.
The preamble sets the page geometry, the font fallback and the margin
note packages for the PDF.[^log] Neither touches the Markdown.

[^paper]: The text and note columns are sized as fractions of the page
    width, so the two-thirds split holds on any paper.

[^log]: The PDF build records which font it settled on. Run the script
    with `--verbose` and look for a line beginning `[fontfallback]`.

# References
