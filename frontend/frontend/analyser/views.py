from django.shortcuts import render
from .forms import ChatUploadForm
from .helpers import (
    preprocess_chat_dataframe, talkative_stats, most_active_day_time,
    media_count_per_person, missed_call_stats, load_model
)
import pandas as pd

def dashboard(request):
    results = {}
    if request.method == 'POST':
        form = ChatUploadForm(request.POST, request.FILES)
        if form.is_valid():
            chat_file = request.FILES['chat_file']
            lines = pd.read_csv(chat_file, header=None, encoding='utf8', on_bad_lines='skip')
            df = preprocess_chat_dataframe(lines)
            model, vectorizer = load_model()
            df['flirt_prediction'] = model.predict(vectorizer.transform(df['Chat'].fillna('')))
            df['flirt_label'] = df['flirt_prediction'].map({1: 'Flirt', 0: 'Not Flirt'})
            results['messages'] = df[['Date', 'Time', 'Name', 'Chat', 'flirt_label']].to_dict('records')
            results['talkative'] = talkative_stats(df)
            results['active_day'], results['active_hour'] = most_active_day_time(df)
            results['media_count'] = media_count_per_person(df)
            results['missed_calls'] = missed_call_stats(df)
    else:
        form = ChatUploadForm()
    return render(request, 'analyser/dashboard.html', {'form': form, 'results': results})