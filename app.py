from flask import Flask, render_template, request
import os

app = Flask(__name__)

match_history = [] 
image_dir = 'static/images/'

def get_image_list(directory):
    image_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_list.append(filename)
    return image_list

from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_profile = request.form['user_profile']
        opponent_profile = request.form['opponent_profile']
        choice = request.form['choice']
        result = request.form['result']
        
        current_datetime = datetime.now()
        
        match_history.append({
            'datetime': current_datetime,  # 日時を記録（datetimeオブジェクト）
            'user_profile': user_profile,
            'opponent_profile': opponent_profile,
            'choice': choice,
            'result': result
        })

    user_profiles = get_image_list(image_dir)
    opponent_profiles = get_image_list(image_dir)

    return render_template('index.html', user_profiles=user_profiles, opponent_profiles=opponent_profiles, match_history=match_history)

@app.route('/history')
def history():
    total_matches = len(match_history)
    wins = sum(1 for match in match_history if match['result'] == '勝')
    losses = total_matches - wins
    win_rate = (wins / total_matches) * 100 if total_matches > 0 else 0

    return render_template('history.html', match_history=match_history, total_matches=total_matches, wins=wins, losses=losses, win_rate=win_rate)

@app.template_filter('percent')
def percent_filter(value):
    return f"{value:.2f}%"

if __name__ == '__main__':
    app.run(debug=True)
