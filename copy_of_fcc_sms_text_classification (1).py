# -*- coding: utf-8 -*-
"""Copy of fcc_sms_text_classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H1RZWzRzb-CEVPDukREX37DHJVnQNXw3
"""

!pip uninstall -y tensorflow
!pip install tensorflow --upgrade --no-cache-dir --quiet

import tensorflow as tf
print(tf.__version__)

# import libraries
try:
  # %tensorflow_version only exists in Colab.
  !pip install tf-nightly
except Exception:
  pass
import tensorflow as tf
import pandas as pd
from tensorflow import keras
!pip install tensorflow-datasets
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# get data files
!wget https://cdn.freecodecamp.org/project-data/sms/train-data.tsv
!wget https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv

train_file_path = "train-data.tsv"
test_file_path = "valid-data.tsv"

import pandas as pd

train_data = pd.read_csv(train_file_path, sep="\t", header=None)
test_data = pd.read_csv(test_file_path, sep="\t", header=None)

# Rename columns for clarity
train_data.columns = ["label", "message"]
test_data.columns = ["label", "message"]

train_data.head()

# Separate texts and convert labels to binary
train_texts = train_data['message'].tolist()
train_labels = [1 if label == 'spam' else 0 for label in train_data['label']]

test_texts = test_data['message'].tolist()
test_labels = [1 if label == 'spam' else 0 for label in test_data['label']]

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Tokenize the text
vocab_size = 5000  # number of unique words to keep
tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(train_texts)

# Convert text to sequences
train_sequences = tokenizer.texts_to_sequences(train_texts)
test_sequences = tokenizer.texts_to_sequences(test_texts)

# Pad the sequences to the same length
max_length = 100
train_padded = pad_sequences(train_sequences, maxlen=max_length, padding='post')
test_padded = pad_sequences(test_sequences, maxlen=max_length, padding='post')

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Build the model
model = keras.Sequential([
    layers.Embedding(input_dim=vocab_size, output_dim=16, input_length=max_length),  # learn word vectors
    layers.GlobalAveragePooling1D(),  # average over word embeddings
    layers.Dense(16, activation='relu'),  # hidden layer
    layers.Dense(1, activation='sigmoid')  # output layer: predicts spam/ham
])

# Compile the model
model.compile(
    loss='binary_crossentropy',      # appropriate for binary classification
    optimizer='adam',                # efficient optimizer
    metrics=['accuracy']             # track accuracy
)

# Train the model
model.fit(
    tf.convert_to_tensor(train_padded),
    tf.convert_to_tensor(train_labels),
    epochs=15,
    validation_data=(tf.convert_to_tensor(test_padded), tf.convert_to_tensor(test_labels))
)



# function to predict messages based on model
# (should return list containing prediction and label, ex. [0.008318834938108921, 'ham'])
def predict_message(text):
    # Convert to sequence and pad
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=100, padding='post', truncating='post')

    # Get prediction (returns [[value]])
    prediction = model.predict(padded, verbose=0)

    # Extract scalar value safely
    score = float(prediction[0][0])

    # Decide label
    label = "spam" if score > 0.5 else "ham"

    return [round(score, 4), label]





pred_text = "how are you doing today?"

prediction = predict_message(pred_text)
print(prediction)

test_messages = ["Free entry in 2 a wkly comp to win FA Cup", "how are you?", "Your free ringtone is waiting", "Are you coming to party?"]
for msg in test_messages:
    print(predict_message(msg))

def test_predictions():
    test_messages = [
        "how are you doing today",
        "sale today! to stop texts call 98912460324",
        "i dont want to go. can we try it a different day? available sat",
        "our new mobile video service is live. just install on your phone to start watching.",
        "you have won £1000 cash! call to claim your prize.",
        "i'll bring it tomorrow. don't forget the milk.",
        "wow, is your arm alright. that happened to me one time too"
    ]

    test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]

    for msg, ans in zip(test_messages, test_answers):
        prediction = predict_message(msg)
        print(f"Message: {msg}")
        print(f"Prediction: {prediction}")
        print(f"Expected: {ans}")
        print("✅" if prediction[1] == ans else "❌", "\n")

test_predictions()

# Run this cell to test your function and model. Do not modify contents.
def test_predictions():
  test_messages = ["how are you doing today",
                   "sale today! to stop texts call 98912460324",
                   "i dont want to go. can we try it a different day? available sat",
                   "our new mobile video service is live. just install on your phone to start watching.",
                   "you have won £1000 cash! call to claim your prize.",
                   "i'll bring it tomorrow. don't forget the milk.",
                   "wow, is your arm alright. that happened to me one time too"
                  ]

  test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]
  passed = True

  for msg, ans in zip(test_messages, test_answers):
    prediction = predict_message(msg)
    if prediction[1] != ans:
      passed = False

  if passed:
    print("You passed the challenge. Great job!")
  else:
    print("You haven't passed yet. Keep trying.")

test_predictions()