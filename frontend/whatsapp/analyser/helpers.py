import pandas as pd
import joblib
import os

# Adjust these paths if your notebook model files are elsewhere
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.abspath(os.path.join(
    BASE_DIR,
    '..', '..', 'backend', 'notebooks', 'flirt_model.pkl'
))
VECTORIZER_PATH = os.path.abspath(os.path.join(
    BASE_DIR,
    '..', '..', 'backend', 'notebooks', 'flirt_vectorizer.pkl'
))

def load_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def preprocess_chat_dataframe(df):
    df = df.drop(0)
    df.columns = ['Date', 'Chat']
    Message = df["Chat"].str.split("-", n=1, expand=True)
    df["Time"] = Message[0]
    Message1 = Message[1].str.split(":", n=1, expand=True)
    df["Name"] = Message1[0]
    df["Chat"] = Message1[1]
    df = df[["Date", "Time", "Name", "Chat"]]
    return df

def talkative_stats(df):
    talk_counts = df['Name'].value_counts()
    return talk_counts

def most_active_day_time(df):
    dt = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    df['datetime'] = dt
    most_active_day = df['datetime'].dt.day_name().value_counts().idxmax()
    most_active_hour = df['datetime'].dt.hour.value_counts().idxmax()
    return most_active_day, most_active_hour

def media_count_per_person(df, media_text="Media omitted"):
    media_df = df[df['Chat'].str.contains(media_text, na=False)]
    media_counts = media_df['Name'].value_counts()
    return media_counts

def missed_call_stats(df):
    missed_calls = df[df['Chat'].str.contains('Missed voice call|Missed video call', na=False)]
    missed_call_counts = missed_calls['Name'].value_counts()
    return missed_call_counts