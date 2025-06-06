from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load BLIP model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def describe_image(image):
    """
    Uses the BLIP model to generate a caption from the image.
    :param image: PIL Image object
    :return: string caption
    """
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def calculate_similarity(user_text, ai_caption):
    """
    Calculates the cosine similarity between user input and AI caption using TF-IDF.
    :param user_text: string
    :param ai_caption: string
    :return: float similarity percentage
    """
    if not user_text.strip() or not ai_caption.strip():
        return 0.0

    texts = [user_text.lower(), ai_caption.lower()]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = similarity_matrix[0][0]  # Value between 0 and 1

    return round(score * 100, 2)