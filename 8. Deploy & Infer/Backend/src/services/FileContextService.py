import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FileContextService:
    
    def __init__(self) -> None:
        pass

    def extract_text_from_pdf(self,file):
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        combined_text = ""
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            combined_text += text

        return combined_text
    
    def separate_paragraphs(self, text):
        paragraphs = text.split("  \n")  # Split text by double line breaks

        # Remove leading and trailing whitespaces from each paragraph
        paragraphs = [paragraph.strip() for paragraph in paragraphs]
        return paragraphs
    
    def find_most_similar_text(self, sentence, text_objects):
        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

        # Fit the vectorizer on text_objects
        tfidf_matrix = vectorizer.fit_transform(text_objects)

        # Transform the input sentence using the fitted vectorizer
        sentence_vector = vectorizer.transform([sentence])

        # Calculate cosine similarities between the sentence vector and all text objects
        similarities = cosine_similarity(sentence_vector, tfidf_matrix)

        # Find the index of the most similar text object
        most_similar_index = similarities.argmax()

        # Get the most similar text object
        most_similar_text = text_objects[most_similar_index]

        # Check the length of the most similar text object
        if len(most_similar_text) < 2000:
            # Find the indices and similarities of the related text objects
            sorted_indices = similarities.argsort()[0][::-1]
            sorted_similarities = similarities[0, sorted_indices]

            # Iterate over the related text objects and add paragraphs until length exceeds 2000 characters
            for idx, similarity in zip(sorted_indices, sorted_similarities):
                if idx != most_similar_index:
                    related_text = text_objects[idx]
                    if len(most_similar_text) + len(related_text) + 2 > 2000:  # +2 for "\n\n"
                        break
                    most_similar_text += "\n\n" + related_text

        return most_similar_text