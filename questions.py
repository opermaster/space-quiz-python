class Answer:
    def __init__(self,text,isCorrect):
        self.text       = text
        self.isCorrect  = isCorrect
    def _print(self):
        print(f"{self.text} {self.isCorrect}")

class Question:
    def __init__(self,text,image_path=""):
        self.text       = text
        self.image_path = image_path
        self.answers    = []

    def _print(self):
        print(f"{self.text} {self.image_path}")
        for ans in self.answers:
            ans._print()


def process_answers(answers_string):
    answers_str = answers_string.split(',')

    if len(answers_str) != 4:
        raise ValueError(f"Expected 4 answers, got {len(answers_str)}")

    correct_count = sum(1 for ans in answers_str if ans.strip().endswith('!'))
    if correct_count == 0:
        raise ValueError("No correct answer marked with '!'")
    if correct_count > 1:
        raise ValueError(f"Multiple correct answers marked: {correct_count}")

    answers = []
    for ans in answers_str:
        ans = ans.strip()
        if not ans:
            raise ValueError("Answer text cannot be empty")
        answers.append(Answer(ans[:-1] if ans[-1] == '!' else ans, ans[-1] == '!'))

    return answers


def process_question(question_string):
    parts = question_string.split(',')

    text = parts[0].strip()
    if not text:
        raise ValueError("Question text cannot be empty")

    image_path = parts[1].strip() if len(parts) == 2 else ""
    return Question(text, image_path)


def process_line(line, line_number):
    parts = line.split(':')

    if len(parts) != 2:
        raise ValueError(f"Line {line_number}: invalid format, expected 'question:answers'")

    question = process_question(parts[0])
    question.answers = process_answers(parts[1])
    return question


def load_questions(filepath="questions.txt"):
    questions = []

    with open(filepath, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                question = process_line(line, line_number)
                questions.append(question)
            except ValueError as e:
                raise ValueError(f"Line {line_number}: {e}") from e

    if not questions:
        raise ValueError("Question file is empty")

    return questions
