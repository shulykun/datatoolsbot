
from logic.smalltalk import Smalltalk
from service.feedback import FeedbackChat

class FunctionLoader:
    """
        Набор функций для генерации динамических ответов 
    """
    
    def __init__(self, medium):
        self.medium = medium
        self.smalltalk = Smalltalk(medium=self.medium)
        self.feedback = FeedbackChat(medium=self.medium)


    def make_functions_dict(self):
        functions = {
            'drop':self.smalltalk.drop,
            'help':self.smalltalk.help,
            'feedback':self.feedback.feedback_start,
            'feedback_text':self.feedback.text_add

        }
        return functions
