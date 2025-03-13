import json
import os
import math

# Mapping answer choices to Greek letter groups
ANSWER_OPTIONS = ["A", "B", "C", "D", "E"]


def quiz():
    questions = load_questions()
    answers = run_quiz(questions)

    personalities = load_personalities()
    personality_matches = get_personality_matches(personalities, answers)
    best_personality_match = get_personality(personality_matches)
    print_result(best_personality_match, personalities)


def load_questions():
    # Questions and answer choices
    with open("config/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    return questions


def load_personalities():
    with open("config/personalities.json", "r", encoding="utf-8") as f:
        personalities = json.load(f)
    return personalities


def run_quiz(questions):
    # Store answers
    answers = []

    # Run the quiz
    print("\nWelcome to the 'Which Greek Letter Are You?' Quiz!\n")
    for i, (question, choices) in enumerate(questions.items(), 1):
        clear()
        print(f"\n{i}. {question}")
        for choice in choices:
            print(choice)

        while True:
            answer = (
                input(f"\nEnter your choice ({', '.join(ANSWER_OPTIONS)}): ")
                .strip()
                .upper()
            )
            if answer in ANSWER_OPTIONS:
                answers.append(answer)
                break
            else:
                print(
                    f"Invalid input. Please enter {', '.join(ANSWER_OPTIONS)}."
                )

    return answers

def clear():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux/macOS)
        os.system('clear')

def get_personality_matches(personalities, answers):
    # Determine the most frequent answer
    answer_distribution = {
        option: answers.count(option) / len(answers)
        for option in ANSWER_OPTIONS
    }

    personality_matches = {}
    for letter, letter_dict in personalities.items():
        distance = math.sqrt(
            sum(
                (letter_dict["answers"][opt] - answer_distribution[opt]) ** 2
                for opt in ANSWER_OPTIONS
            )
        )
        personality_matches[letter] = distance

    return personality_matches


def get_personality(personality_matches):
    best_personality_match = min(
        personality_matches, key=personality_matches.get
    )
    return best_personality_match


def print_result(best_personality_match, personalities):
    result = personalities[best_personality_match]
    # Display the result
    print("\nQuiz Complete! Your Greek Letter personality is:")
    print(f"\n{best_personality_match} - {result['title']}")
    print(f"{result['personality']}\n")


if __name__ == "__main__":
    quiz()
