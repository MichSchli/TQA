import argparse
import tqdm
import re
import sys
import string

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return text
        #return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def handle_punc(text):
        exclude = set(string.punctuation + "".join([u"‘", u"’", u"´", u"`"]))
        return ''.join(ch if ch not in exclude else ' ' for ch in text)

    def lower(text):
        return text.lower()

    def replace_underscore(text):
        return text.replace('_', ' ')

    return white_space_fix(remove_articles(handle_punc(lower(replace_underscore(s))))).strip()


parser = argparse.ArgumentParser(description='Extracts QA pairs from JSON-formatted triviaqa data.')
parser.add_argument('--answer_file')
parser.add_argument('--evidence_file')
args = parser.parse_args()

answer_separator = " | "

evidence_file = open(args.evidence_file, 'r')

first_q = True
answerable = 0
total = 0
for answers in tqdm.tqdm(list(open(args.answer_file, 'r'))):
    total += 1
    if first_q:
        first_q = False
    else:
        print("")

    answers = answers.strip().split(answer_separator)
    answers = [re.escape(normalize_answer(a)) for a in answers]

    evidence_lines_for_question = []
    next_line = evidence_file.readline().strip()
    while next_line:
        if next_line != "":
            evidence_lines_for_question.append(next_line)
            next_line = evidence_file.readline().strip()

    first = True
    answered = False
    search_term = re.compile("\s(" + "|".join(answers) + ")\s")
    for idx, evidence_line in enumerate(evidence_lines_for_question):
        split_evidence = evidence_line.split(" ")
        lens = [len(w) for w in split_evidence]
        for m in re.finditer(search_term, str.lower(evidence_line)):
            start_letter_idx = m.start() + 1
            end_letter_idx = m.end() - 1
            acc = 0
            for word_idx, l in enumerate(lens):
                if acc <= start_letter_idx < acc + l + 1:
                    start_word = word_idx
                if acc <= end_letter_idx < acc + l + 1:
                    end_word = word_idx

                acc += l + 1

            span = [str(idx), str(start_word), str(end_word)]
            if first:
                first = False
            else:
                print("|", end="")
            print(",".join(span), end="")
            answered = True

    if answered:
        answerable += 1

print("Total: " + str(total), file=sys.stderr)
print("Answerable: " + str(answerable), file=sys.stderr)