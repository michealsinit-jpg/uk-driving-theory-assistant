import json
import random

with open("theory_data.json", "r") as file:

    theory_data = json.load(file)

with open("quiz_data.json", "r") as file:
    quiz_data=json.load(file)

print("\nAvailable questions:")

for key in theory_data:

    print("-", key)

print()
from difflib import get_close_matches
def start_quiz():

    score = 0

    wrong_answers = []

    questions = random.sample(quiz_data, 5)

    for i, q in enumerate(questions, start=1):

        print(f"\nQuestion {i}/5")

        print(q["question"])

        for letter, option in q["options"].items():

            print(f"{letter}. {option}")

        answer = input("\nYour answer (A, B, C, D): ").upper().strip()

        if answer == q["correct"]:

            print("✅ Correct!")

            score += 1

        else:

             print("❌ Wrong!")

             print(

                 f"Correct answer: "

                 f"{q['correct']} - {q['options'][q['correct']]}"

             )

             wrong_answers.append({

                "question": q["question"],

                "correct_letter": q["correct"],

                "correct_text": q["options"][q["correct"]]

            })

    print(f"\nQuiz finished! Your score: {score}/5")

    with open("scores.txt", "a") as file:

        file.write(f"{score}\n")

    if score >= 4:

        print("🎉 Pass!")

    else:

        print("❌ Fail. Try again!")

    if wrong_answers:

        print("\nQuestions to review:")

        for item in wrong_answers:

            print("-", item["question"])

            print(

                f"  Correct answer: "

                f"{item['correct_letter']} - {item['correct_text']}"

            )
def show_category(category):

    print(f"\nQuestions in category '{category}':")

    for key in theory_data:

        if isinstance(theory_data[key], dict):

            if theory_data[key]["category"] == category:

                print("-", key)  

def search_question(question):

    found = False

    for key in theory_data:

        if question in key or key in question:

            print(theory_data[key]["answer"])

            found = True

            break

    if not found:

        matches = get_close_matches(

            question,

            theory_data.keys(),

            n=1,

            cutoff=0.6

        )

        if matches:

            print("Did you mean:", matches[0])

            print(theory_data[matches[0]]["answer"])

        else:

            print("Sorry, I don't know that answer yet.")   

def show_scores():

    try:

        with open("scores.txt", "r") as file:

            scores = [int(line.strip()) for line in file]

        print("\nQuiz History")

        for i, score in enumerate(scores, start=1):

            print(f"Quiz {i}: {score}/5")

        average = sum(scores) / len(scores)

        print(f"\nAverage score: {average:.1f}/5")

        print(f"Best score: {max(scores)}/5")
        print(f"Total quizzes taken: {len(scores)}")

        if max(scores) == 5:

           print("🏆 Perfect score achieved!")

    except FileNotFoundError:

        print("No quiz history yet.")   
while True:

    question = input("Ask a driving theory question: ").lower()

    if question == "quiz":

        start_quiz()

        continue


    if question == "scores":

        show_scores()

        continue

    if question.startswith("show "):

       category = question.replace("show ", "")
     
       show_category(category)

       continue

    if question == "quit":
        print("Goodbye!")
        break

search_question(question)