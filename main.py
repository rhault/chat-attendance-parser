import re
import xlsxwriter
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any

# Regular expression pattern to parse each line
LINER_PATTERN = re.compile(r"(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.*?): (.*)")
# Regular expression pattern to extract hour from message
MESSAGE_HOUR_PATTERN = re.compile(r"\b(\d{2}:\d{2})\b")


def extract_hour(text: str):
    """Extracts the first hour found in the text as a time object."""
    match = MESSAGE_HOUR_PATTERN.search(text)
    return datetime.strptime(match.group(1), "%H:%M").time() if match else None


def read_text_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads the chat file and parses each line into structured data.
    Returns a list of message dictionaries.
    """
    messages = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                match = LINER_PATTERN.match(line)
                if match:
                    date_str, time_str, sender, message = match.groups()
                    try:
                        full_datetime = datetime.strptime(
                            f"{date_str} {time_str}", "%d/%m/%Y %H:%M"
                        )
                    except ValueError as ve:
                        print(
                            f"Error converting date/time: {ve} on the line: {line}")
                        continue

                    messages.append(
                        {
                            "date": full_datetime.date(),
                            "time": full_datetime.time(),
                            "sender": sender.strip(),
                            "extracted_time": extract_hour(message.strip()),
                        }
                    )
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading the file: {e}")
    return messages


def group_messages_data(messages: List[Dict[str, Any]]):
    """
    Groups parsed messages by sender name and date.
    Returns a nested dict: sender -> date -> list of messages.
    """
    grouped_messages = defaultdict(
        lambda: defaultdict(list))

    for message in messages:
        sender = message.get("sender")
        date = str(message.get("date"))
        # Create a copy to avoid modifying the original message dictionary
        msg_copy = message.copy()
        msg_copy.pop("sender", None)  # Remove sender from message dict
        msg_copy.pop("date", None)  # Remove date from message dict
        grouped_messages[sender][date].append(msg_copy)

    return grouped_messages


def save_to_excel(grouped_data, output_file):
    """
    Saves the grouped data to an Excel file.
    """

    variance = 2  # minutes
    workbook = xlsxwriter.Workbook(output_file)
    text_styles = workbook.add_format({'bold': True, 'font_color': "red"})

    for sender, dates in grouped_data.items():
        worksheet = workbook.add_worksheet(name=sender[:31])
        worksheet.write(0, 0, "Data")
        worksheet.write(0, 1, "Entrada")
        worksheet.write(0, 3, "Saida")
        worksheet.write(0, 5, "Entrada")
        worksheet.write(0, 7, "Saida")

        row = 1

        for date, messages in dates.items():
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                print(f"Invalid date: {date}")
                continue

            worksheet.write(row, 0, date)
            col = 1

            for input in messages:
                messages_time = input.get('time')
                extracted_time = messages_time if input.get(
                    extracted_time) == "" else input.get(extracted_time)

                try:
                    date_time = datetime.combine(date, messages_time)
                    date_text = datetime.combine(date, extracted_time)
                except Exception as e:
                    print(f"Error matching date/time: {e}")
                    continue

                if (date_time > date_text):
                    delta = (date_time - date_text).total_seconds() / 60
                    set_time = extracted_time if delta >= variance else messages_time
                    worksheet.write(row, col, set_time, text_styles)
                else:
                    set_time = messages_time
                    worksheet.write(row, col, set_time)

                col += 1

            row += 1

    workbook.close()


def main():
    input_path = "./input/Controle de Jornada.txt"
    output_path = "./output/chat_attendance.xlsx"

    print("Lendo arquivo de entrada...")
    read_text = read_text_file(input_path)

    print("Agrupando mensagens...")
    group_message = group_messages_data(read_text)

    print("Salvando para Excel...")
    save_to_excel(group_message, output_path)
    print("Processo concluído.")


if __name__ == "__main__":
    main()
