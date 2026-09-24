import dateparser
import joblib
import spacy

from datetime import datetime, timedelta
from spacy.matcher import Matcher

from .models import *


class Extractor:
    def __init__(self, model="en_core_web_md", timezone="PST") -> None:
        self.classifier = joblib.load("model/intent_classifier.joblib")
        self.nlp = spacy.load(model)
        self.matcher = Matcher(self.nlp.vocab)
        self.timezone = timezone

        todo_pattern = [
            {"POS": "VERB"},
            {"POS": "DET", "OP": "?"},
            {"POS": "ADJ", "OP": "*"},
            {"POS": "NOUN", "OP": "*"},
            {"POS": "NOUN"},
        ]

        task_pattern = [
            {"POS": "VERB"},
            {"POS": {"IN": ["DET", "ADJ", "NOUN", "PROPN", "NUM"]}, "OP": "*"},
            {"POS": "NOUN"},
        ]

        reminder_pattern = [
            {"LOWER": "remind"},
            {"POS": {"IN": ["PRON", "PROPN"]}},
            {"LOWER": "to"},
            {"POS": "VERB"},
            {"OP": "{1,4}"},  # Captures the next 1-4 words
        ]

        event_pattern = [
            {"POS": {"IN": ["NOUN", "ADJ", "PROPN"]}, "OP": "*"},
            {"LEMMA": {"IN": ["appointment", "meeting", "lunch", "event", "session"]}},
        ]

        self.matcher.add("TODO", [todo_pattern])
        self.matcher.add("TASK", [task_pattern])
        self.matcher.add("REMINDER", [reminder_pattern])
        self.matcher.add("EVENT", [event_pattern])

    def parse_command(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)

        if not matches:
            return {"title": "Could not extract a pattern."}

        longest_match = None
        max_length = 0

        for match_id, start, end in matches:
            match_length = end - start
            if match_length > max_length:
                max_length = match_length
                longest_match = (match_id, start, end)

        match_id, start, end = longest_match  # type: ignore
        intent_label = self.nlp.vocab.strings[match_id]

        if intent_label == "REMINDER":
            match_span = doc[start:end]
            to_index = start + 2

            for token in match_span:
                if token.lower_ == "to":
                    to_index = token.i
                    break

            extracted_phrase = doc[to_index + 1 : end].text
        else:
            extracted_phrase = doc[start:end].text

        date: str = ""
        time: str = ""
        location: str | None = None

        for ent in doc.ents:
            if ent.label_ == "DATE":
                date = ent.text
            if ent.label_ == "TIME":
                time = ent.text
            if ent.label_ in ["GPE", "LOC"]:
                location = ent.text

        date_time: datetime | None = dateparser.parse(
            date + time, settings={"TIMEZONE": self.timezone}
        )

        data = {"title": extracted_phrase, "datetime": date_time, "location": location}
        return data

    def extract(self, text: str) -> list[ExtractedItem]:
        """
        Extract todos, tasks, reminders, and events from natural language.
        """
        # Predict the category without any hardcoded rules
        prediction = self.classifier.predict([text])[0]

        item = []

        data = self.parse_command(text)

        print(data)
        if prediction == "todo":
            item.append(Todo(title=data["title"]))
        elif prediction == "reminder":
            item.append(Reminder(title=data["title"]))
        elif prediction == "event":
            item.append(
                Event(
                    title=data["title"],
                    start_at=data["datetime"], # type: ignore
                    end_at=data["datetime"] + timedelta(hours=1), # type: ignore
                    location=data["location"]
                )
            )
        elif prediction == "task":
            item.append(Task(title=data["title"], due_at=data["datetime"])) # type: ignore

        print(item, prediction)

        return item
