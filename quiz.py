import json
import os


def quiz():
    questions, answer_options = load_questions()
    answers = run_quiz(questions, answer_options)

    personalities = load_personalities()
    personality_matches = get_personality_matches(personalities, answers)
    best_personality_match = get_personality(personality_matches)
    print_result(best_personality_match, personalities)


def load_questions():
    # Questions and answer choices
    with open("config/questions.json", "r") as f:
        questions = json.load(f)

    # Mapping answer choices to Greek letter groups
    answer_options = ["A", "B", "C", "D", "E"]

    return questions, answer_options


def load_personalities():
    with open("config/personalities.json", "r") as f:
        personalities = json.load(f)
    return personalities


def run_quiz(questions, answer_options):
    # Store answers
    answers = []

    # Run the quiz
    print("\nWelcome to the 'Which Greek Letter Are You?' Quiz!\n")
    for i, (question, choices) in enumerate(questions.items(), 1):
        os.system("clear")
        print(f"\n{i}. {question}")
        for choice in choices:
            print(choice)

        while True:
            answer = (
                input("\nEnter your choice (A, B, C, D, or E): ")
                .strip()
                .upper()
            )
            if answer in answer_options:
                answers.append(answer)
                break
            else:
                print("Invalid input. Please enter A, B, C, D, or E.")

    return answers


def get_personality_matches(personalities, answers):
    # Determine the most frequent answer
    personality_matches = {}
    for letter, letter_dict in personalities.items():
        matches = sum(
            1 for a, b in zip(letter_dict["answers"], answers) if a == b
        )
        personality_matches[letter] = matches

    return personality_matches


def get_personality(personality_matches):
    best_personality_match = max(
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
