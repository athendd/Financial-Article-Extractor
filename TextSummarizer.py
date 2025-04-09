import TextCleaner
import numpy as np 
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from nltk.tokenize import sent_tokenize


def textrank(matrix, iterations, damping_factor):
    N = len(matrix)
    
    # Get vector from the given matrix and assign each sentence an equal probability
    vector = [1/N] * N
    
    # Normalize the vector
    vector = vector/np.linalg.norm(vector, 1)
    
    previous_vector = 0
    
    dampened_matrix = damping_factor * matrix + (1 - damping_factor) / N
    
    for _ in range(iterations):
        
        # Perform matrix and vector multiplication to update similarity scores
        vector = np.dot(dampened_matrix, vector)
        
        # Check for convergence
        if abs(previous_vector - sum(vector)) < min_threshold:
            print("reached it baby")
            break
        
        previous_vector = sum(vector)
    
    return vector

def perform_textrank(data):
    separated_data = sent_tokenize(data)

    cleaned_data = TextCleaner.clean_text(separated_data)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    min_threshold = 1e-5
    
    n = len(cleaned_data)

    # Matrix that represents similarities between each text
    similarity_scores = np.zeros((n,n))

    sentence_embeddings = model.encode(cleaned_data)


    for row in range(n):
        for column in range(n):
            sim_score = cosine_similarity([sentence_embeddings[row]], [sentence_embeddings[column]]).item()
            similarity_scores[row][column] = sim_score
            similarity_scores[column][row] = sim_score

    # Normalize the similarity scores 
    similarity_scores /= np.sum(similarity_scores, axis = 1, keepdims = True) + 1e-10

    rankings_vector = textrank(similarity_scores, 350, 0.85)

    sorted_indices = np.argsort(rankings_vector)[::-1]
    
    summarized_text = "".join(map(str, sorted_indices[:5]))
    
    return summarized_text
