import utils
from chatbot import ChatBot


class DialogueManager(object):
    def __init__(self):
        print("Loading resources...")

        self.chatbot = ChatBot()
       
    def generate_answer(self, question):
        question = utils.text_prepare(question)
        response = self.chatbot.get_response(question)

        return response
