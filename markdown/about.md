# About
Semantic Shakespeare allows users to leverage transformer models (AI) to semantically search the entire Shakespeare Corpus. Unlike a traditional search engine, semantic searching does not rely strictly on keywords. Instead, it allows users to search the entire Shakespeare Corpus purely from the semantic meaning of the search.

The application is written in Python with Streamlit, a Python library for developing web-based applications. The vectorization of the texts, indexing of them, and querying of the index is built upon txtAI.

On the Homepage of this application, type your query, select the number of results you want to see populated (limit is 2000) and then run your search. Depending on the number of results you hava selected, it may take several seconds for your search to complete. When done, your results will populate in the main page.

If you want to ignore the words of your query from the results, select the checkbox "Ignore Search Words".

## How to Read Results
The populated the results are a DataFrame (spreadsheet) with 6 columns.
- Play => The name of the play
- PlayerLinenumber => The line number for that particular speaker
- ActSceneLine => the Act, Scene, and Line numbers
- Player => The speaker of the line
- PlayerLine => The line that returned the results
- similarity => The degree to which the line matches your query. This is a float (decimal) between 0 and 1. The higher the percentage, the more similar the text is.


The results have syntax highlighting. The more relevant the word, the darker the highlighting.



## Version History
### Current Version: 0.0.2
Added syntax highlighting with the explain function and added an About page

### Version 0.0.1
App loaded onto UKY servers and allows users to run basic searches
