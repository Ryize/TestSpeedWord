import random

from flask import Flask, render_template, request, json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test_speed():
    if request.method == 'POST':
        words_list = request.form['word_list'].replace('\n', '').replace(' ', '').split(',')
        user_word = request.form['user_word'].split()
        select_time = int(request.form['select_time'])
        matching_elements = set(words_list) & set(user_word)
        symbols_per_second = round(len(''.join(matching_elements)) / select_time, 3)
        status_test = get_status(symbols_per_second)
        data = {
            'totalWords': len(matching_elements),
            'totalSymbols': len(''.join(matching_elements)),
            'wordsPerSecond': round(len(matching_elements)/select_time, 1),
            'symbolsPerSecond': symbols_per_second,
            'accuracy': 100/(len(user_word)/len(matching_elements)),
            'status_test': status_test,
        }
        return json.dumps(data)

    return render_template('test_speed.html', word_list=get_word_list())

def get_word_list():
    with open('word_rus.txt', encoding='utf-8') as file:
        words = file.read().split('\n')
        return ', '.join([random.choice(words) for i in range(180)])

@app.route('/get_word_list', methods=['GET', 'POST'])
def get_word_list_json():
    data = {
        'word_list': get_word_list()
    }
    return json.dumps(data)

def get_status(symbols: int | float):
    answer_test = { #How fast the print speed is, depends on the number of characters per second
        0: 'Тролль',
        2.08: 'Плохо',
        6.25: 'Нормально',
        8.33: 'Хорошо',
        15: 'БОГ'
    }

    for key, value in answer_test.items():
        if symbols <= key:
            return value

def clear_of_long_words(file_name: str = 'word_rus.txt', len_word: int = 8):
    with open(file_name, encoding='utf-8') as file:
        words = file.read().split('\n')
        clear_word = [i for i in words if len(i) <= len_word]

    with open(file_name, 'w') as file:
        file.write('\n'.join(clear_word))


if __name__ == '__main__':
    app.run(debug=True)
