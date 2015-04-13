# Keyword Distillery
NASA Space Apps Challenge 2015 (Data Treasure Hunting)

Generates a ranked list of keywords. Each keyword can generate a ranked list of databases which relate to it, ranked by the strength of the relationship.

#Usage
* Generate a list of keywords you would like to map, save this file as `keywords.json`
* Download a `data.json` file from:
 * http://data.ny.gov/data.json
 * http://data.hawaii.gov/data.json
 * http://data.oregon.gov/data.json
* Run distill.py:
 * `python distill.py weigh`
 * `python distill.py filter`
* After the filtering is finished (will take some time) a `filtered_keyword_relationship_map.json` will be created.

The `filtered_keyword_relationship_map.json` contains a list of keywords and any datasets related to it. The datasets are ranked in order of `relation_score`. This value, calculated by multiplying keyword weight and relation_weight is a reasonable approximation of the strength of a keyword-to-dataset relation.

#Method
Existing keywords were aggregated from the provided toolkit. These keywords were then given scaled weights by inversing the number of search results returned when searched for on a web browser.

Public data hosted on data.hawaii.gov was then crawled. Each dataset listed was downloaded and scanned for matching keywords. Keyword frequency was calculated and stored in the *relationship map*. Freqency was calculated by dividing the total number of keyword instances by the length of the document.

##Discussion
Using inverse search results to calculate word "potency" necessitates filtering of highly weighted, but nonsense, keywords (because the work is done in lowercase, it might not be immediately obvious that the keyword is an acronym). This filtering is done at the end of the mapping, as it is unlikely that nonsense words will show up repeatedly in other datasets. In some cases a human generated keyword list might be the best choice when using the tool. Based on preference or use-case keywords can be generated and assigned automatically to a dataset by setting a threshold for the `relation_score` and tagging the dataset when it is exceeded.

The tool also can be improved with how it calculates `relation_weight`. Searching for word roots instead of exact matches (or synonyms) and throwing out `relation_weight`s that are well outside a normal distribution. Calculating relationship strength based only on keyword frequency unfairly biases the relationship strength towards datasets with lots of words, namely, lots of the same words. There are likely instances where a keyword was used as a variable or fieldname and was over-ranked. This could suppress or hide datasets that are otherwise obviously related.

Currently the program throws away three letter words, this can be changed to include potentially useful three letter acronyms that would have otherwise been discarded.