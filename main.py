import decouple
import random
import docx2txt as docx
import time
import os
import re


PATH_DIR: str = decouple.config('PATH_DIR')

def parse_title(text: str) -> str:
    """Get title of quiz from string."""
    title: str = text.splitlines()[0].strip()
    return title


def parse_questions(text: str) -> list[str]:
    """Get all questions from string."""
    questions_pattern = r'\d+\. ([^\n]+)'
    questions: list[str] = re.findall(questions_pattern, text)
    return questions


def parse_answers(text: str) -> list[list[str]]:
    """Get all answers from string."""
    answers_pattern = r'([a-zA-Zа-яА-ЯёЁ]\) [^\n]+)'
    answers: list[str] = re.findall(answers_pattern, text)
    return answers


def parse_correct_answers(text: str) -> list[str]:
    """Get all correct answers from string."""
    correct_answers_pattern = r'\d+\) ([a-zA-Zа-яА-ЯёЁ])'
    correct_answers: list[str] = re.findall(correct_answers_pattern, text)
    return correct_answers


def shuffle(*args, repeat: int = 30) -> None:
    """Shuffle all quiz data in random order."""
    for _ in range(repeat):
        a: int = random.randrange(len(args[0]))
        b: int = random.randrange(len(args[0]))

        for collection in args:
            collection[a], collection[b] = collection[b], collection[a]


def get_data_from_quiz(text: str) -> tuple[str, list[str], list[list[str]]]:
    """Get all data for quiz from string."""
    title: str = parse_title(text)

    questions: list[str] = parse_questions(text)

    answers: list[str] = parse_answers(text)
    answers_count = len(answers) // len(questions)
    answers = [
        answers[i:i+answers_count]
        for i in range(0, len(answers), answers_count)
    ]

    correct_answers: list[str] = parse_correct_answers(text)

    shuffle(questions, answers, correct_answers)
    return title, questions, answers, correct_answers


def textfile_parse(filepath: str) -> tuple[str, list[str], list[list[str]]]:
    """Parse ``.txt`` files."""
    with open(filepath, 'r', encoding='utf-8') as file:
        quiz_data: str = file.read()

    return get_data_from_quiz(quiz_data)


def docxfile_parse(filepath: str) -> tuple[str, list[str], list[list[str]]]:
    """Parse ``.docx`` files."""
    quiz_data: str = docx.process(filepath)

    return get_data_from_quiz(quiz_data)


def main() -> None:
    directories: list[str] = os.listdir(PATH_DIR)
    quiz_filename: str = random.choice(directories)
    quiz_path = os.path.join(PATH_DIR, quiz_filename)
    extension = quiz_path.split('.')[-1]

    title: str = ''
    questions: list[str] = []
    answers: list[list[str]] = []
    correct_answers: list[str] = []

    if extension == 'txt':
        title, questions, answers, correct_answers = textfile_parse(quiz_path)
    elif extension == 'docx':
        title, questions, answers, correct_answers = docxfile_parse(quiz_path)
    else:
        return

    print('Добро пожаловать на викторину')
    print('Тема сегодняшней викторины: "%s"' % title)
    print('\nУдачи!\n')

    score: int = 0
    max_score: int = len(questions)

    for idx in range(len(questions)):
        print('%d.' % (idx+1), questions[idx])
        print('\nВарианты ответа:', *answers[idx], sep='\n  ')

        user_answer: str = input('\nВаш ответ (введите букву варинта ответа): ')

        if user_answer.lower() == correct_answers[idx].lower():
            score += 1
            print('\n  [V] Правильно!\n')

        else:
            correct_answer: str = [
                answer for answer in answers[idx]
                if answer[0] == correct_answers[idx]
            ]
            if correct_answer:
                correct_answer = correct_answer[0]
            else:
                correct_answer = correct_answers[idx]

            print('\n  [X] Неверно! Правильный ответ: %s\n' % correct_answer)

        time.sleep(0.6)

    print('Вот и подошла викторина к концу. Ваш результат:')
    print('%s / %s' % (score, max_score))

    time.sleep(5)

if __name__ == '__main__':
    main()
