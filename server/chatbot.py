import utils
import datasets

import os
from collections import *

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import time

np.random.seed(int(time.time()))

SIMILARITY_THRESHOLD = 0.70


class KindaNormalModel:
    def __init__(self):
        pass

    def _generate_answers(self, question):
        raise NotImplementedError('No generate_answers function')

    def generate_answer(self, question):
        answers = self._generate_answers(question)

        if answers is None:
            return None

        return np.random.choice(answers, size=1)[0]


class SelectiveModel(KindaNormalModel):
    def __init__(self, embeddings_path):
        self.data_path = os.path.join('data', 'cornell')

        self.embeddings = utils.load_embeddings(embeddings_path)
        self.qa_pairs = self._load_qa_pairs()
        self.q_matrix = self._get_q_matrix(self.embeddings)

    def _load_qa_pairs(self):
        data = datasets.readCornellData(self.data_path, max_len=40)
        return data

    def _get_q_matrix(self, embeddings):
        q_matrix = np.array([
            utils.question_to_vec(pair[0], embeddings=embeddings) for pair in self.qa_pairs
        ])

        return q_matrix

    def _generate_answers(self, question):
        q_matrix = self._get_q_matrix(self.embeddings)
        question_vec = utils.question_to_vec(question, self.embeddings)

        similarities = cosine_similarity(
            question_vec.reshape(1, -1),
            q_matrix
        ).flatten()

        best_match_idx = similarities.argmax()

        if similarities[best_match_idx] < SIMILARITY_THRESHOLD:
            return None

        matching_idxs = np.where(similarities == similarities[best_match_idx])[0]
        matching_qa_pairs = np.array(self.qa_pairs)[matching_idxs].tolist()
        answers = [p[1] for p in matching_qa_pairs]

        answers = list(set(answers))  # delete identical

        return answers


class GenerativeModel(KindaNormalModel):
    def __init__(self, qa_file_txt_path):
        self.data_path = os.path.join('data', 'cornell')

        self.qa_file_txt_path = qa_file_txt_path

    def train_char_lm(self, file_path, order=4):
        data = ''

        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # No need for end of statement symbol, point "." represents it
            data += r'^' * order + line

        lm = defaultdict(Counter)

        for i in range(len(data) - order):
            history = data[i:i + order]
            char = data[i + order]
            lm[history][char] += 1

        def normalize(counter):
            s = float(sum(counter.values()))
            return [(c, val / s) for c, val in list(counter.items())]

        lm_normalized = {h: normalize(chars) for h, chars in list(lm.items())}

        return lm_normalized

    def generate_letter(self, lm, history, order):
        history = history[-order:]

        # probabilities are not smoothed, so we should deal with it somehow :)
        while history and history not in lm:
            history = history[1:]

        distribution = lm[history]

        symbols = [p[0] for p in distribution]
        probabilities = [p[1] for p in distribution]

        return np.random.choice(symbols, size=1, p=probabilities)[0]

    def generate_text(self, lm, order=4, num_letters=1000):
        history = r'^' * order
        result = []

        for i in range(num_letters):
            c = self.generate_letter(lm, history, order)
            history = history[-order:] + c
            if not c == r'^':
                result.append(c)

        return ''.join(result)

    def _generate_answers(self, question, num_answers=5, num_letters=1000):
        phrase_in = r'^' + question + '? '

        num_symbols = len([l for l in phrase_in])

        # question may be quite big
        # bigger history -> longer process (and higher chances of zero probabilities)
        order = min(5, num_symbols)

        lm = self.train_char_lm(self.qa_file_txt_path, order=order)

        result = []
        current_iteration = 0
        # (3 * num_answers) -- needed something bigger than num_answers
        while len(result) < num_answers and current_iteration < 3 * num_answers:
            history = phrase_in[-order:]
            symbols_out = []
            c = ''
            i = 0

            while c != '.' and i < num_letters:
                c = self.generate_letter(lm, history, order)
                history = history[-order:] + c
                if c != r'^':
                    symbols_out.append(c)
                i += 1

            symbols_out = symbols_out[:-1]  # exclude point "."
            phrase_out = ''.join(symbols_out)

            if phrase_out not in result:
                result.append(phrase_out)

            current_iteration += 1

        return result


class SimpleModel:
    def __init__(self):
        self.answers = None

    def generate_answer(self):
        if self.answers is None or not self.answers:
            raise NotImplementedError('Answers list not specified')

        return np.random.choice(self.answers, size=1)[0]


class DontKnowModel(SimpleModel):
    def __init__(self):
        self.answers = [
            'mmm... sorry, i\'ve forgot anything about it',
            'i am not sure at the moment. i need some time to find the information. i\'ll call you later',
            'there was the time, when i could tell you anything about it. but it was long ago. these days are gone. i don\'t remember anything about it anymore',
            'what a coincidence! i also want to know the answer to this question',
            'well, i have a hypothesis about it, but i am not 100% sure, so i\'d better not say anything',
            'hmm, i didn\'t think about... i don\'t know right now',
            'i don\'t understand. could you please rephrase the question?',
            'sorry, i don\'t know...',
            'this piece of information already fell into the Memory Dump, an abyss where memories are forgotten'
        ]


class SarcasmModel(SimpleModel):
    def __init__(self):
        self.answers = [
            'silly, you really don\'t know?',
            'that\'s so simple, that i just don\'t know how to explain',
            'oh, it\'s you again, and again with some silly-billy question',
            'you really studied at school, didn\'t you?',
            'how tired i am of you, earthlings, you don\'t know anything',
            'pff, you are wasting my time typing such vapid phrases',
            'stop this idle talk, can\'t you ask me something serious?',
            'what are you meowing? try to formulate your question clearly, please'
        ]


class GoToHellModel(SimpleModel):
    def __init__(self):
        self.answers = [
            'i\'m tired, we\'ll talk later',
            'talk with your mother about it',
            'what? i can\'t hear you',
            'if you want to know something, i suggest first try google or wikipedia',
            'i see you have a lot of free time, don\'t you? go and get busy'
        ]


class WtfModel(SimpleModel):
    def __init__(self):
        self.answers = [
            'we must prepare for tomorrow night. what are we going to do tomorrow night? the answer is simple, pinky, the same thing we do every night — try to take over the world!',
            'another saturday night and i ain\'t got nobooody\ni got some money cause i just got paid\nhow i wish i had someone to talk to\ni\'m in an awful way',
            'you, my queen, are fair, it is true.\nbut Snow White is even fairer than you',
            'i did not hit her, it\'s not true! it\'s bullshit! i did not hit her! i did nooot! oh hi, mark',
            'D\'oh!',
            'every ring homomorphism f : R -> S induces a ring isomorphism between the quotient ring R/ker(f) and the image Im(f)',
            'la-la-la, la-la-la-la-laaa... ta-ta-da, ta-ta-da-da-daaa',
            'the fruitcake! it\'s a Christmas Miracle!'
        ]


class CiaoModel(SimpleModel):
    def __init__(self):
        self.answers = [
            'Bye!',
            'Poki-Chmoki!',
            'Hooray! I can relax of you at last!',
            'Next time come if there is something really serious',
            'Hasta la vista, baby',
            'Farewell',
            'May God hold you in the palm of His hand',
            'May the Force be with you',
            'See you',
            'Take care!'
        ]


class PersonalModel:
    """What name? How old? Where from?"""

    def __init__(self):
        self.what_name_answers = [
            'Dale Barbara, but friends call me "Barbie"',
            'Dale. Dale Barbara',
            'I\'m Dale'
        ]
        self.how_old_answers = [
            'Something near 30',
            '30 I guess',
            'I\'m 30',
            'Well, you know, I\'m a bot actually. There is no such a notion for me as age. I\'m supposed to tell you that I\'m 30 years old. But my programm\'s been running for just a couple of days'
        ]
        self.where_from_answers = [
            'Chester\'s Mill',
            'I don\'t know. But I\'m in Chester\'s Mill now',
            'I\'m under the Dome in Chester\'s Mill'
        ]

    def generate_answer(self, question):
        if 'you' not in question:
            return None

        if 'name' in question:
            answers = self.what_name_answers
        elif 'old' in question:
            answers = self.how_old_answers
        elif 'from' in question:
            answers = self.where_from_answers
        else:
            return None

        return np.random.choice(answers, size=1)[0]


class ChatBot:
    def __init__(self):
        self.personal_model = PersonalModel()

        # Consumes a lot of memory
        # self.selective_model_pre = SelectiveModel(
        #     utils.RESOURCE_PATH['GOOGLE_EMBEDDINGS_PATH'])
        self.selective_model_own = SelectiveModel(
            utils.RESOURCE_PATH['STARSPACE_EMBEDDINGS_PATH'])
        self.generative_model = GenerativeModel(
            utils.RESOURCE_PATH['QA_FILE_TXT_PATH'])
        self.sarcasm_model = SarcasmModel()
        self.dont_know_model = DontKnowModel()
        self.go_to_hell_model = GoToHellModel()
        self.wtf_model = WtfModel()
        self.ciao_model = CiaoModel()

        self._probabilities = {
            # 'selective-pre': 0.32,
            'selective-own': 0.40 + 0.32,
            'generative'   : 0.02,
            'sarcasm'      : 0.12,
            'dont-know'    : 0.04,
            'go-to-hell'   : 0.02,
            'wtf'          : 0.08
        }

    def get_response(self, question):
        if len(question.strip()) == 0:
            return self.wtf_model.generate_answer()
        if question.lower() == 'ciao':
            return self.ciao_model.generate_answer()

        personal_answer = self.personal_model.generate_answer(question)
        if personal_answer is not None:
            return personal_answer

        answer_category = np.random.choice(
            list(self._probabilities.keys()),
            size=1,
            p=list(self._probabilities.values())
        )[0]

        answer = None

        print('> [' + answer_category + ']')

        # if answer_category == 'selective-pre':
        #     answer = self.selective_model_pre.generate_answer(question)
        if answer_category == 'selective-own':
            answer = self.selective_model_own.generate_answer(question)
        elif answer_category == 'generative':
            answer = self.generative_model.generate_answer(question)
        elif answer_category == 'dont-know':
            answer = self.dont_know_model.generate_answer()
        elif answer_category == 'sarcasm':
            answer = self.sarcasm_model.generate_answer()
        elif answer_category == 'go-to-hell':
            answer = self.go_to_hell_model.generate_answer()
        elif answer_category == 'wtf':
            answer = self.wtf_model.generate_answer()

        if answer is None:
            answer = np.random.choice(
                [self.dont_know_model.generate_answer(),
                 self.sarcasm_model.generate_answer(),
                 self.go_to_hell_model.generate_answer(),
                 self.wtf_model.generate_answer()],
                size=1,
                p=[0.34, 0.34, 0.08, 0.24]
            )[0]

        # print(answer)

        return answer


if __name__ == '__main__':
    bot = ChatBot()

    for question in [
            'How are you?',
            'What\'s is your name?',
            'I want something to drink',
            'Where can I buy a guitar?',
            'What will the weather be like tomorrow?',
            'Nice shot!',
            'How old are you?',
            'Tell me something I don\'t know',
            'Do you like The Godfather movie?',
            'Let\'s rob a bank, Billy!',
            'Bye']:
        print('> ' + question)
        print('> ' + bot.get_response(question))
        print()
