import argparse
import json
import nltk
import tqdm

parser = argparse.ArgumentParser(description='Extracts QA pairs from JSON-formatted triviaqa data.')
parser.add_argument('--json_document')
parser.add_argument('--evidence_folder')
parser.add_argument('--target_folder')
args = parser.parse_args()

json_data=open(args.json_document).read()
data = json.loads(json_data)

answer_separator = " | "

question_out_file = open(args.target_folder + "/questions.txt", "w")
answer_out_file = open(args.target_folder + "/answers.txt", "w")
evidence_out_file = open(args.target_folder + "/evidence.txt", "w")

def format(string):
    tokens = nltk.word_tokenize(string.strip())
    return " ".join(tokens)

first = True
for line in tqdm.tqdm(data["Data"]):
    if first:
        first = False
    else:
        print("\n", file=evidence_out_file)
        print("", file=answer_out_file)
        print("", file=question_out_file)

    text = line["Question"]
    print(text, file=question_out_file, end="")

    answers = line["Answer"]["Aliases"]
    answer_string = answer_separator.join(answers)
    print(answer_string, file=answer_out_file, end="")

    for entity_page in line["EntityPages"]:
        filename = entity_page["Filename"]
        complete_name = args.evidence_folder + "/" + filename

        evidence_lines = []
        with open(complete_name, 'r') as evidence_file:
            for evidence_line in evidence_file:
                evidence_line = format(evidence_line)
                if evidence_line:
                    evidence_lines.append(evidence_line)

        print("\n".join(evidence_lines), file=evidence_out_file, end="")