import joblib

from .models import *


class Extractor:
    def __init__(self, model="en_core_web_md") -> None:
        self.classifier = joblib.load('model/intent_classifier.joblib')

    def extract(self, text: str) -> list[ExtractedItem]:
        """
        Extract todos, tasks, reminders, and events from natural language.
        """
        # Predict the category without any hardcoded rules
        prediction = self.classifier.predict([text])[0]

        item = []
        if prediction == "todo":
            item.append(Todo(title=text))
        elif prediction == "reminder":
            item.append(Reminder(title=text))
        elif prediction == "event":
            item.append(Event(title=text, start_at=datetime.now()))
        elif prediction == "task":
            item.append(Task(title=text))

        print(item, prediction)

        return item
