# Keyword Distillery
NASA Space Apps Challenge 2015 (Data Treasure Hunting)

Generates a ranked list of keywords. Each keyword can generate a ranked list of databases which relate to it, ranked by the strength of the relationship.

#Usage
TODO

#Method
Existing keywords were aggregated from the provided toolkit. These keywords were then given scaled weights by inversing the number of search results returned when searched for on a web browser.

Public data hosted on data.hawaii.gov was then crawled. Each dataset listed was downloaded and scanned for matching keywords. Keyword frequency was calculated and stored in the *relationship map*. Freqency was calculated by dividing the total number of keyword instances by the length of the document.

##Discussion
Using inverse search results to calculate word "potency" necessitates filtering of highly weighted nonsense keywords. This filtering can be done (at the cost of CPU time) at the end of the mapping, as it is unlikely that nonsense words will show up repeatedly in other datasets.

Calculating relationship strength based only on keyword frequency unfairly biases the relationship strength towards datasets with lots of words, namely, lots of the same words. There are likely instances where a keyword was used as a variable or fieldname and was over-ranked. This could suppress or hide datasets that are otherwise obviously related.