import re
import xlsxwriter
from datetime import datetime
from collections import defaultdict

# Regular expression pattern to parse each line
LINER_PATTERN = re.compile(r"(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.*?): (.*)")

MESSAGE_HOUR_PATTERN = re.compile(r"\b(\d{2}:\d{2})\b")


def extract_hour(text):
    match = MESSAGE_HOUR_PATTERN.search(text)
    return match.group(1) if match else ""


def read_text_file(file_path):
    """
    Reads the chat file and parses each line into structured data.
    """
    messages = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = LINER_PATTERN.match(line)
            if match:
                date_str, time_str, sender, message = match.groups()
                full_datetime = datetime.strptime(
                    f"{date_str} {time_str}", "%d/%m/%Y %H:%M"
                )

                messages.append(
                    {
                        "date": full_datetime.date(),
                        "time": full_datetime.time(),
                        "sender": sender.strip(),
                        "text": extract_hour(message.strip()),
                    }
                )
        return messages


def group_messages_data(messages):
    """
    Groups parsed messages by sender name and date.
    """
    grouped_messages = defaultdict(lambda: defaultdict(list))

    for message in messages:
        sender = message["sender"]
        date = str(message["date"])
        del message["sender"]  # Remove sender from message dict
        del message["date"]  # Remove date from message dict
        grouped_messages[sender][date].append(message)

    return grouped_messages


def save_to_excel(grouped_data, output_file):
    """
    Saves the grouped data to an Excel file.
    """

    workbook = xlsxwriter.Workbook(output_file)

    for sender, dates in grouped_data.items():
        worksheet = workbook.add_worksheet(name=sender[:31])

        worksheet.write(0, 0, "Data")
        worksheet.write(0, 1, "Entrada")
        worksheet.write(0, 2, "Entrada t")
        worksheet.write(0, 3, "Saida")
        worksheet.write(0, 4, "Saida t")
        worksheet.write(0, 5, "Entrada")
        worksheet.write(0, 6, "Entrada t")
        worksheet.write(0, 7, "Saida")
        worksheet.write(0, 8, "Saida t")

        row = 1

        for date, messages in dates.items():
            worksheet.write(row, 0, date)
            col = 1
            for input in messages:
                time = input["time"]
                text = input["text"]

                worksheet.write(row, col, time.strftime("%H:%M"))
                worksheet.write(row, col + 1, text)
                col += 2

            row += 1

    workbook.close()


read_text = read_text_file("./input/Controle de Jornada.txt")
group_message = group_messages_data(read_text)
save_to_excel(group_message, "./output/chat_attendance.xlsx")
