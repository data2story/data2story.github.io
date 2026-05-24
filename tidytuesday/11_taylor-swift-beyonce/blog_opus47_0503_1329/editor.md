## Story Spine

**Core claim**: When you treat Beyoncé and Taylor Swift as two text corpora and two chart-position tables, the popular framing of who-writes-what flips: Beyoncé says "love" more, Taylor's catalog stays net-positive across thirteen years and then breaks in 2020.

**Tension**: The dataset was published as a Beyoncé-vs-Taylor comparison and the culture has been trained to read Taylor as the love-and-breakup songwriter. The data says the opposite, twice over — Beyoncé's lyrics are *more* love-saturated per word, and Taylor's eight-album sentiment line stays positive until folklore.

**Payoff**: Two artists who get treated as parallel turn out to be doing very different things. One builds songs by repeating a single phrase 48 times. The other writes in landscapes — woods, daylight, wonderland — and then, in lockdown, goes net-negative for the first time in her career.

## Sections

### edt_01: Hook — Two corpora, one comparison
**Evidence**: ana_01 | **Context**: det_01, det_04

[ana_01] In September 2020, the TidyTuesday community was handed two artists' catalogs as four CSV files. Beyoncé's lyric file: 22,616 lines, 391 song entries. Taylor Swift's: 132 songs, eight studio albums. The size gap is real, but it's an accident of how the two corpora were built — Beyoncé's includes every remix, live cut and a Lemonade film script; Taylor's is one canonical version per studio track.

[det_04] The two artists are paired here for the same reason they have been paired for a decade: the 2009 VMAs, where Kanye interrupted Taylor to argue that Beyoncé deserved the award, then Beyoncé returned the moment to her on stage during her own win. The dataset's cover image is a backstage photo from that night.

[editorial] Strip the catalog down to numbers and the popular framing of who writes what about love starts to give way.

[INSTANCE: inst_02]

### edt_02: The lyric size gap is structural, not real
**Evidence**: ana_01, ana_03 | **Context**: det_03

[ana_01] Compare the two artists at the song level: Beyoncé averages 57.8 lines per song across 391 entries, Taylor 52.7 lines across her 132 studio recordings. On a per-song basis the volume is almost identical.

[ana_03] But six of the ten longest entries in Beyoncé's lyric file are not pop songs at all. The longest is the 336-line script of the Lemonade film. Three of the next four are different live and remix versions of "Get Me Bodied" (245, 195, and 195 lines). The first canonical solo studio track to crack the top 10 by line count is "That's How You Like It" with Jay-Z, at 122 lines.

[det_03] The asymmetry is built into the source: Beyoncé's data came from Genius's per-line table (one row per lyric line, including remixes and live transcripts); Taylor's came from a per-song scrape (one row per song, eight studio albums, no remixes). The headline "Beyoncé has 3.3 times as many lyric lines" is a fact about the dataset, not the music.

[CHART: ana_03]

### edt_03: 48 chants vs 12 hooks
**Evidence**: ana_04 | **Context**: 

[ana_04] When you ask each artist's lyric file the same simple question — what is the most-repeated single line within one song? — the answers describe two different songwriting modes. Beyoncé's top within-song repeat is "That's how you like it, huh", sung 48 times in a single track. The next is "Who run the world? Girls!" at 38 repetitions in one club remix, then 25, then 23.

[ana_04] Taylor Swift's top within-song repeat is 12. Six of her songs are tied at that number — "Look what you just made me do", "Come back, be here", "I'd never walk Cornelia Street again", "Welcome to New York", "All you had to do was stay", "In a getaway car". She caps her hooks because there is always another verse to come. Beyoncé builds songs out of a single chant.

[CHART: ana_04]

### edt_04: Beyoncé says "love" more than Taylor does
**Evidence**: ana_06, ana_05 | **Context**: det_05

[ana_06] Here is the result that contradicts the popular framing the most directly. Beyoncé's lyrics are denser with love-words (love, loved, loving, heart, baby, kiss) than Taylor Swift's. After stripping stop-words, 3.50% of Beyoncé's content vocabulary is love-words. For Taylor, it is 2.36%. Beyoncé's rate is 1.5 times Taylor's.

[ana_05] Look at the raw counts and the picture sharpens. "Love" appears 1,362 times in Beyoncé's catalog, 248 in Taylor's. "Baby" — 1,024 vs 153. "Kiss" and "heart" follow the same pattern. Taylor Swift writes a lot about relationships, but the inside of the relationship — the words for the body, the closeness, the moment — belongs to Beyoncé. "Halo" alone is sung 383 times across her dataset.

[det_05] This is the lexicon-level signal that Rosie Baillie's tidytext-style analysis was set up to find: words count, in aggregate, even when the intuition cuts the other way.

[CHART: ana_06]
[INSTANCE: inst_01]

### edt_05: Words that uniquely belong to each artist
**Evidence**: ana_15

[ana_15] If you compute a log-likelihood ratio over the two artists' shared vocabulary, the words that uniquely belong to each tell their own story. Beyoncé's most-distinctive words are "bodied" (205 vs 0), "halo" (383 vs 1), "slay" (148 vs 0), "diva" (110 vs 0), "ladies" (269 vs 2), "upgrade" (86 vs 0). Her vocabulary names the body and the room.

[ana_15] Taylor's most-distinctive words are "starlight" (0 vs 22), "wonderland" (0 vs 21), "getaway" (0 vs 21), "woods" (1 vs 38), "daylight" (2 vs 40), "darling" (5 vs 30), "york" (3 vs 38). Her vocabulary names landscapes and times of day. One songwriter is in the room with you. The other is describing where you both are.

[CHART: ana_15]

### edt_06: Folklore — the only sad Taylor album
**Evidence**: ana_13 | **Context**: det_05

[ana_13] Score every Taylor Swift studio album by its sentiment ratio — positive words minus negative, divided by total — and you get a steady arc. The self-titled debut: +0.88. Fearless: +0.99. Speak Now: +1.02 (the most positive album she has made). Red, 1989, reputation, Lover all stay net-positive but trend down: +0.92, +0.77, +0.45, +0.41.

[ana_13] In 2020, the line crosses zero for the first time. Folklore — written and recorded in lockdown — is the only Taylor Swift studio album that scores net-negative: 140 positive words against 150 negative, in 4,856 total. Speak Now is the most hopeful album she has made; folklore, ten years and one pandemic later, is the first sad one.

[ana_14] Beyoncé's full catalog scores +1.63 on the same scale. Above every Taylor Swift album except Speak Now, Fearless and Red. The "breakup album" framing of Lemonade, viewed at the catalog level, doesn't outweigh the love-and-celebration density of the rest.

[CHART: ana_13]

### edt_07: Different markets, different #1s
**Evidence**: ana_10, ana_11 | **Context**: det_07

[ana_10] On the album charts, the two artists own different territory. In the US, Beyoncé hits #1 with every one of her six studio albums (100%); Taylor with seven of her eight (87.5%, the lone miss being her 2006 debut). In Australia, the order flips: Taylor goes 75% to Beyoncé's 33%. New Zealand: Taylor 87.5%, Beyoncé 17%. Canada: Taylor 87.5%, Beyoncé 50%. France is no one's country — both at 0%.

[ana_11] At the album level, Beyoncé's median peak position across ten national charts traces a U-shape: she opens at 1.5 with Dangerously in Love, dips to 4.5 with I Am... Sasha Fierce in 2008, then climbs back to a perfect 1.0 with Lemonade. Taylor's line is the opposite — it falls steadily from a median peak of 38 on the debut, hits 1.0 with Red in 2012, and stays at 1.0 for every album since.

[CHART: ana_10]
[MEDIA: map]

### edt_08: Per album, the sales gap nearly disappears
**Evidence**: ana_12, ana_07 | **Context**: det_06

[ana_12] The popular framing — "Taylor outsells Beyoncé worldwide" — is technically true. Taylor's six worldwide-row albums total 40.8 million units; Beyoncé's five total 34.5 million. But on a per-release basis, the gap nearly vanishes. Taylor averages 6.80 million worldwide units per album. Beyoncé averages 6.90 million.

[ana_07] The single largest-selling album in either catalog is Taylor's Fearless (2008) at 12.0 million worldwide. Right behind it: Beyoncé's debut Dangerously in Love (2003) at 11.0 million. Taylor's 1989 (10.1M), Beyoncé's B'Day (8.0M), Beyoncé's I Am... Sasha Fierce (8.0M), Taylor's Red (6.0M). Every blockbuster album in the dataset belongs to one of these two artists.

[CHART: ana_07]

### edt_09: Close — what the corpus says back
**Evidence**: | **Context**: det_05, det_08

[editorial] The two artists were paired here, in 2020, on the assumption that they were doing comparable things. The data says they are doing different things, in different vocabularies, with different shapes of repetition, in different markets. Beyoncé says love more often per word; Taylor stays positive across thirteen years and then writes folklore.

[det_05] The tidytext approach has a tendency to flatten that difference into a single sentiment number. The lexicons it ships with were trained on standard English, and they systematically misread Black Vernacular English ("bad" meaning "good"). So the +1.63 on Beyoncé's catalog is, almost certainly, an undercount.

[editorial] The honest move is to take the lyrics as the lyrics and let the per-album lines tell their own story. Speak Now is the brightest. Folklore is the first one that goes dark. And every blockbuster album in either catalog still belongs to one of these two women.

## Editorial Notes
- 12 (Taylor's max within-song repeat) and 48 (Beyoncé's) must be exact — they're the central comparison in edt_03.
- folklore's −0.21 score and its position as the first Taylor album to go net-negative is the load-bearing finding of the second half of the piece.
- 1.5x (Beyoncé's love-word rate over Taylor's) must be exact in edt_04 — this is the headline-flipping number.
- Caveat that Beyoncé's catalog includes remixes/live/film scripts must stay visible in edt_02; the 3.3x line-count gap is structural, not artistic.
- Sentiment lexicon caveat (BVE misread) must be visible somewhere — placed in edt_09.
- Spotify embeds: Single Ladies in edt_01, Halo in edt_04. Both verified.
