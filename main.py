
import os
import re
from datetime import datetime
import pandas as pd
from collections import defaultdict

# Regular expression pattern to parse each line
LINER_PATTERN = re.compile(r"\[(\d{2}/\d{2}), (\d{2}:\d{2})\] (.*?): (.*)")

MESSAGE_HOUR_PATTERN = re.compile(r"\b(\d{2}:\d{2})\b")


def read_text_file(file_path):
    """
    Reads the chat file and parses each line into structured data.
    """
    messages = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = LINER_PATTERN.match(line)
            if match:
                date_str, time_str, sender, message = match.groups()
                full_datetime = datetime.strptime(
                    f"{date_str}/2025 {time_str}", "%d/%m/%Y %H:%M")

                messages.append({
                    'date': full_datetime.date(),
                    'time': full_datetime.time(),
                    'sender': sender.strip(),
                    'message': message.strip()
                })
        return messages


def group_messages_sender(messages):
    """
    Groups parsed messages by sender name.
    """
    grouped = defaultdict(list)

    for message in messages:
        sender = message['sender']
        del message['sender']  # Remove sender from message dict
        grouped[sender].append(message)

    return grouped


def group_messages_date(messages):
    """
    Groups parsed messages by date.
    """

    grouped = defaultdict(list)
    senders = list(messages.keys())

    for sender in senders:
        grouped[sender] = defaultdict(list)  # type: ignore
        for message in messages[sender]:
            date = message['date']
            del message['date']  # Remove date from message dict
            grouped[sender][date].append(message)

    return grouped


text = read_text_file('./input/chat.txt')
group_message = group_messages_sender(text)
group_date = group_messages_date(group_message)
