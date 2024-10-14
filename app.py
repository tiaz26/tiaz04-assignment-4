from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)


# TODO: Fetch dataset, initialize vectorizer and LSA here
categories = None  # You can specify categories or leave it as None for all categories
newsgroups = fetch_20newsgroups(subset='all', categories=categories, remove=('headers', 'footers', 'quotes'))

# Initialize TfidfVectorizer and fit-transform the dataset
stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=0.5, max_features=10000)
X_tfidf = vectorizer.fit_transform(newsgroups.data)

# Apply TruncatedSVD for LSA
n_components = 100  # Number of dimensions to reduce to
lsa = TruncatedSVD(n_components=n_components, random_state=42)
X_lsa = lsa.fit_transform(X_tfidf)


def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # TODO: Implement search engine here
    # return documents, similarities, indices 
    query_tfidf = vectorizer.transform([query])
    query_lsa = lsa.transform(query_tfidf)

    # Compute cosine similarities between the query and all documents
    similarities = cosine_similarity(query_lsa, X_lsa)[0]

    # Get the top 5 most similar documents
    top_indices = similarities.argsort()[::-1][:5]  # Indices of top 5 most similar documents
    top_similarities = similarities[top_indices]  # Cosine similarities of the top 5
    top_documents = [newsgroups.data[i] for i in top_indices]  # Retrieve the documents

    return top_documents, top_similarities.tolist(), top_indices.tolist()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices}) 

if __name__ == '__main__':
    app.run(debug=True)
