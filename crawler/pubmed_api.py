import requests
from xml.etree import ElementTree as ET
from nltk.tokenize import sent_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def find_sentences_with_keywords(keywords, sentences):
    result = []
    seen = set()
    for i, sentence in enumerate(sentences):
        for keyword in keywords:
            if keyword in sentence and sentence not in seen:
                result.append(i)
                seen.add(sentence)
                break
    return result

def excute_pubmed_api(base_url,api_key,db,retmax,query):
    word_tokens = word_tokenize(query.translate(str.maketrans('', '', string.punctuation)))
    keywords = [w for w in word_tokens if not w.lower() in stop_words]
    # Perform the ESearch request to get the WebEnv and QueryKey parameters
    esearch_url = f"{base_url}esearch.fcgi?db={db}&term={query}&sort=relevance&retmax={retmax}&usehistory=y&api_key={api_key}"
    response = requests.get(esearch_url, timeout=20)
    esearch_xml = response.content.decode("utf-8")
    # Parse the WebEnv and QueryKey parameters from the ESearch response
    root = ET.fromstring(esearch_xml)
    if root.find(".//WebEnv") is None:
        external_contexts = []
    else:
        webenv = root.find(".//WebEnv").text
        query_key = root.find(".//QueryKey").text
        # Perform the EFetch request to retrieve the full records for the PubMed IDs
        efetch_url = f"{base_url}efetch.fcgi?db={db}&query_key={query_key}&WebEnv={webenv}&api_key={api_key}&retmax={retmax}&usehistory=y&retmode=xml"
        response = requests.get(efetch_url, timeout=20)
        efetch_xml = response.content.decode("utf-8")
        # Parse the full records from the EFetch response
        root = ET.fromstring(efetch_xml)
        external_contexts = []
        for pubmed_article in root.findall(".//PubmedArticle"):
            # Get the title from the full record
            title = pubmed_article.find(".//ArticleTitle").text
            # Get the description (abstract) from the full record, if available
            description_elem = pubmed_article.find(".//AbstractText")
            if description_elem is not None:
                if description_elem.text is not None:
                    description = description_elem.text
                    copy_description = description
                    copy_description_segmented = sent_tokenize(copy_description)
                    description_segmented = sent_tokenize(description)
                    result = find_sentences_with_keywords(keywords, copy_description_segmented)
                    for item in result:
                        external_contexts.append(description_segmented[item])
                else:
                    if title is not None:
                        external_contexts.append(title)
            else:
                if title is not None:
                    external_contexts.append(title)
            if len(external_contexts)>3:
                break
    return word_tokenize(" ".join(external_contexts))


# if __name__=='__main__':
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
#     my_api_key = "27af1ec10cd5d499b43225ebf7f669d90b09"
#     # Set the query parameters
#     db = "pubmed"
#     retmax = 20
#     query = str("""We think that a prospective study would be useful .""")
#     print(excute_pubmed_api(base_url=base_url,api_key=my_api_key,db=db,retmax=retmax,query=query))