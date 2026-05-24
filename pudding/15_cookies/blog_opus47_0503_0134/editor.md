## Story Spine

**Core claim**: Across 209 chocolate chip cookie recipes scraped from the internet, the "average cookie" turns out to contain 68 ingredients — including bourbon, zucchini, and coriander — and that joke is a small, edible parable about what averaging does to anything humans actually make.

**Tension**: We treat "the average" as if it points at the typical thing. It doesn't. It points at a Frankenstein superset that includes every minority taste at trace amounts. The mathematical mean of 209 cookies is a recipe with white pepper in it.

**Payoff**: After reading, the reader should understand why "average" is rarely the right word for what algorithms recommend, generate, or summarize — and should also have a working recipe for a cookie that, for what it's worth, is genuinely chewy.

## Sections

### edt_01: The most-average cookie has bourbon in it
**Evidence**: ana_07, ana_04 | **Context**: det_04, det_03

[ana_07, det_04] In May 2018, Elle O'Brien and Amber Thomas at The Pudding scraped 209 chocolate chip cookie recipes off the internet, scaled them all to a 48-cookie yield, and computed the strict arithmetic mean of every ingredient. The resulting average cookie contains 68 distinct ingredients. Ten of them appear in substantial quantities. Forty-six are visible. Nineteen are pure trace.

[ana_04] In there, in microscopic but mathematically real amounts, are bourbon (0.019 tablespoons, from a single recipe), zucchini, applesauce, coriander, white pepper, and a thing labeled simply "nestle." 23 distinct ingredients show up in exactly one recipe out of 209, and the average keeps every one of them.

[det_03, det_04] O'Brien actually baked the result. Her verdict: *"Chewy and very chocolatey, no one would suspect these cookies were made with everything in your pantry."* The average cookie tastes fine. It also has trace marshmallows in it.

[MEDIA: image]

### edt_02: But the average cookie is also boringly normal
**Evidence**: ana_06, ana_03 | **Context**: det_02, det_07

[ana_06, det_07] If you only look at the top of the list, the average cookie is unsurprisingly Toll House. Per 48 cookies: 3.5 cups all-purpose flour, 2.9 eggs, 1.8 cups semisweet chips, 1.4 teaspoons baking soda, 1.2 cups light brown sugar, 1.1 teaspoons salt, 1.1 cups butter, and 1 cup white sugar. Vanilla, three teaspoons of it. That's the cookie Ruth Wakefield invented at her Toll House Inn in 1938, after eight decades of distributed amateur engineering by anonymous home bakers.

[ana_03, det_02] Nine ingredients appear in three quarters or more of the 209 recipes — egg (97.6%), vanilla (93.8%), all-purpose flour (92.3%), baking soda (89.5%), white sugar (83.3%), light brown sugar (81.3%), salt (79.9%), butter (76.1%), and semisweet chocolate chip (74.6%). After this group, there's a cliff: the next ingredient, baking powder, appears in only 23.9% of recipes. There is no middle. An ingredient is either canonical or a one-baker quirk.

[CHART: ana_03]
[MEDIA: image]

### edt_03: A close look at the ingredient vector
**Evidence**: ana_17, ana_05 | **Context**: det_04

[ana_17, ana_05] Lay out all 68 ingredients on a single chart and the shape of the corpus is almost geological. A small cliff face on the left — the universal staples, packed tight at three-quarters or more of recipes. Then nothing. A wide, shallow tail running across the rest of the page: walnuts (18.7%), milk chocolate chips (14.8%), shortening (13.9%), oats (9.1%), bittersweet chips (8.1%) — and then a long fade into one-baker curiosities. 49 of the 68 ingredients show up in fewer than 5% of recipes.

[editorial] This is the structure that makes "the average" misleading. The arithmetic mean treats each of those rare ingredients as a tiny, real number — not as zero, not as missing, not as an outlier — and rolls them all into the recipe. White pepper, in microscopic doses, becomes part of the cookie.

[CHART: ana_17]

### edt_04: Where the bakers actually disagree
**Evidence**: ana_08, ana_09, ana_11, ana_10 | **Context**: det_07

[ana_08] The standardized form of the cookie hides a wider disagreement underneath. Among the 192 recipes that include all-purpose flour, the median is 3.3 cups (per 48 cookies) but the spread runs from 1.5 cups at the 5th percentile to 8 cups at the 95th. The widest recipe lists 16 cups. The narrowest, 0.32. Flour is the ingredient where bakers seem least sure how much is enough.

[ana_11] Chocolate chips, by contrast, are simpler: 93.8% of recipes use at least one variety, the median is 2.3 cups per 48 cookies, and 74.6% of bakers reach for semisweet specifically. Bittersweet bakers are a small but devoted club: only 17 recipes use bittersweet chips, but when they do, they use *4.4 cups* on average — twice as much as the semisweet crowd.

[ana_10, det_07] The interesting micro-finding is in the sugars. Among recipes that use both white and brown sugar (152 of 209), 36.8% use *more brown sugar than white*. Just 15.8% lean the other way. The Nestle Toll House recipe, the canonical one, calls for equal amounts. The internet has voted, by a clear margin, for chewier.

[CHART: ana_11]
[MEDIA: interactive]

### edt_05: The oven hasn't moved in 80 years
**Evidence**: ana_16, ana_15 | **Context**: det_02

[ana_16, det_02] Dump every recipe's directions into one corpus and grep for oven temperatures. 350 degrees Fahrenheit gets 74 mentions. 375 gets 46. Everything else — 325, 300, 385 — combined accounts for fewer than 11. About 60% of all temperature mentions land on 350F, the temperature Wakefield's original Toll House recipe specified in 1938.

[ana_15] The instructional vocabulary is just as canonical. The most common content phrases in 1,110 lines of cookie instructions are "baking soda" (191 mentions), "chocolate chips" (191), "stir in" (166), "preheat oven" (123), and "drop by spoonfuls". This is the shared liturgy of cookie-making.

### edt_06: What averaging is actually for
**Evidence**: ana_07 | **Context**: det_05, det_03

[det_05, ana_07] Beyond the cookie itself, this is a small argument about what we ask "the average" to do. Recommendation algorithms, predictive text, neural networks — they all promise to summarize a population and return a representative output. O'Brien's three experiments tested this on cookies. The mathematical mean produced an edible 68-ingredient Frankenstein. The 4-gram predictive text model fell into an infinite loop the moment it encountered cannelini beans. The character-level neural network output "1.904 cups seconds" and listed white sugar five separate times.

[det_05] Average is not typical. Average is not preferred. Average is what you get when you let the union of every minority taste have a vote. Sometimes — as with the cookies — the result is fine. Sometimes — as with the neural net — it's nonsense. The cookie experiment is a small, tactile demonstration of a thing that is harder to feel when the topic is news feeds or movie recommendations: the algorithm is summing all of us, including the one person who put zucchini in their cookies, and pretending that's what the population wanted.

## Editorial Notes
- All ingredient quantities and counts must be quoted exactly from the analyst.json data tables (e.g., 209 recipes, 68 ingredients, 0.019 tablespoons of bourbon).
- The Wakefield/Toll House origin story is editorial color but is grounded in det_02; do not embellish.
- The "Chewy and very chocolatey..." quote in edt_01 is verbatim from O'Brien's essay (det_04). Do not paraphrase.
- The neural-network and n-gram failure stories in edt_06 come from det_03 — keep the cannelini-beans detail; it's load-bearing.
- The interactive in edt_04 should let the reader explore the brown:white sugar ratio or the flour distribution — pick one finding the user should *guess* before seeing the answer.
- Do not invent a chocolate-chip ratio for the "average recipe" beyond what's in ana_06 (1.833 cups semisweet).
