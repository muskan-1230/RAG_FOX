import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")
nltk.download("punkt_tab")

text = """
Reflection occurs when light strikes a surface. The angle of incidence equals the angle of reflection.
Mirrors can form real or virtual images. Concave mirrors converge light rays.
Convex mirrors diverge light rays.
"""

sentences = sent_tokenize(text)

for i, sentence in enumerate(sentences):
    print(f"\nSentence {i+1}:")
    print(sentence)