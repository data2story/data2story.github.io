## Story Spine
**Core claim**: Stanford is the closest thing the tech economy has to a factory — a single university that, by deliberate design, has seeded the companies that built Silicon Valley — but the data that proves it is also a lesson in how loosely we define "founder" and "Stanford."

**Tension**: The popular story is clean (Stanford produces tech giants). The data is messy: the #1 "Stanford founder" barely attended Stanford, more than half the records have no industry at all, and the same list that contains Google also contains a PAC and a Belgian relief commission.

**Payoff**: The reader comes away believing the founder-factory thesis — but believing it for the right reasons, having seen exactly where the evidence is strong, where it is a floor, and where a famous number is mostly an artifact of how Wikidata defines its words.

## Sections

### edt_01: Hook — The factory and its asterisk
**Evidence**: ana_02, ana_00 | **Context**: det_06, det_07, det_01

[ana_02, det_06] The most prolific founder to come out of Stanford is Elon Musk, with fifteen organizations to his name. He also attended Stanford for about two days, in 1995, before walking out of a physics PhD to go chase the internet.

[editorial] That single fact is the whole story of this dataset in miniature. Stanford really is a founder factory — but the records that prove it are built on words like "founded" and "educated" that turn out to be far looser than they sound.

[ana_00, det_01] The raw material is 545 founder→organization links pulled from Wikidata: 394 distinct Stanford-educated people credited with starting 509 different organizations across 149 industries. It is the spine of Silicon Valley, captured as a spreadsheet.

[CHART: ana_02]
[MEDIA: image]

### edt_02: The boom — a curve shaped like Silicon Valley
**Evidence**: ana_01 | **Context**: det_02, det_05

[ana_01] Lay the foundings out by decade and you get the rise of Silicon Valley as a single line. A trickle before the war — three organizations in the 1910s — climbs to eighteen in the 1960s, fifty in the 1980s, seventy-three in the 1990s, and peaks at a hundred and twenty in the 2000s.

[det_02] None of this was an accident. In the 1930s Stanford's engineering dean, Frederick Terman, started pushing his students to build companies near campus instead of leaving for the East Coast. He leased university land to high-tech firms and earned the title "father of Silicon Valley." The curve is the shape of his strategy paying off.

[det_05] By 2011, a Stanford survey counted nearly forty thousand active alumni-founded companies generating $2.7 trillion a year — output on the scale of the world's tenth-largest economy. This dataset is a tiny, famous slice of that machine.

[CHART: ana_01]

### edt_03: The canon — from a garage to Palantir
**Evidence**: ana_07, ana_08 | **Context**: det_03, det_04

[ana_07, det_03] The list reads like the table of contents of a Silicon Valley history. It opens with Hewlett-Packard in 1939 — two Stanford students, a rented Palo Alto garage, the building now stamped "Birthplace of Silicon Valley."

[ana_07, det_04] Then the 1980s wave: Silicon Graphics and Logitech in 1981, Sun Microsystems in 1982, Cisco in 1984. Sun's name was literally a pun on "Stanford University Network," and its first machine was built from spare parts in the campus computer lab. Cisco's router software descended from code written at Stanford. These companies weren't founded by alumni who happened to study there — they were spun straight out of the labs.

[ana_07] From there it runs through Nvidia in 1993 and the dot-com duo of PayPal and Google in 1998, into LinkedIn and Palantir in the 2000s. Every name a household word, every one a single row in the same file.

[ana_08, det_04] And Stanford rarely supplies just one founder per company. Thirty organizations here have more than one Stanford-educated founder — four at OpenAI, three apiece at Sun, Palantir, and PayPal. The factory ships teams, not just individuals.

[CHART: ana_07]
[MEDIA: interactive]

### edt_04: The fog — most of the records can't tell you what they are
**Evidence**: ana_05, ana_06 | **Context**: det_08

[ana_05, det_08] Here is where the clean story gets honest. The dataset has a tidy "is technology" flag — but it is built on Wikidata's industry field, and 323 of the 545 records, fifty-nine percent, have no industry recorded at all. Only 104 links carry the tech flag. The flag is a floor, not a count: the famous tech firms sitting in that 59% fog are simply invisible to it.

[ana_06] That fog distorts everything downstream. The tech share per decade looks like it collapses to zero in the 1960s and 1970s — not because Stanford stopped making tech companies, but because almost none of those older records have an industry filled in. Where the data exists, tech holds a steady twenty to thirty-five percent.

[CHART: ana_05]

### edt_05: The signal under the fog
**Evidence**: ana_09, ana_04 | **Context**: det_08

[ana_09] So clear the fog. Look only at the 202 organizations that actually have an industry recorded, and technology becomes the single largest bloc: eighty-eight of them, almost forty-four percent, are tech — more than every other industry combined.

[ana_04] And when you list those named industries, they read like Silicon Valley's own glossary: software, computer hardware, artificial intelligence, information technology, the Internet, semiconductors. The founder-factory thesis survives contact with the messy data — you just have to know which numbers are a floor and which are the signal.

[CHART: ana_04]

### edt_06: Where the factory sits
**Evidence**: ana_03 | **Context**: det_09, det_02

[ana_03, det_09] Map the headquarters and Terman's strategy is still visible on the ground. Of the companies with a known location, they pile up within a few miles of campus: San Francisco, Mountain View, Palo Alto, Menlo Park, Sunnyvale, San Jose. New York and Washington trail far behind — and Washington's count is mostly Herbert Hoover's relief commissions, not startups.

[editorial] Eighty-odd years after a dean told his students to stay close to home, the map of what they built still clusters around the same handful of Peninsula towns. The factory has an address.

[CHART: ana_03]
[MEDIA: map]

## Editorial Notes
- The "about two days" / 15-orgs framing for Musk (ana_02, det_06) is the load-bearing hook — keep it up front and exact.
- The 59% / 323-of-545 missing-industry figure (ana_05) must stay visible; it is the honesty pivot of the whole piece. Do not bury it.
- ana_06 is weak evidence (coverage artifact) — present it explicitly as a distortion, never as a real trend.
- Keep the "PAC and a Belgian relief commission" juxtaposition (det_07) — it makes the "founded by is broad" caveat felt, not footnoted.
- ana_03 percentages: 338 known-HQ companies, 125 in core Bay Area cities. Frame as "of companies with a known location."
