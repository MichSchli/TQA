import argparse
import tqdm
import sys

parser = argparse.ArgumentParser(description='Convert spans to textual answers based on a reference document')
parser.add_argument('--document')
parser.add_argument('--spans')
args = parser.parse_args()

document_lines = open(args.document, 'r')
span_lines = list(open(args.spans, 'r'))

answer_separator = " | "

first = True
for span in tqdm.tqdm(span_lines):
    if first:
        first = False
    else:
        print("")
    evidence_lines_for_question = []
    next_line = document_lines.readline().strip()
    while next_line:
        if next_line != "":
            evidence_lines_for_question.append(next_line.split(" "))
            next_line = document_lines.readline().strip()

    span_parts = span.strip().split(";")
    has_printed = False
    for span_part in span_parts:
        if not span_part:
            continue

        span_data = span_part.split(",")

        paragraph = int(span_data[0])
        start = int(span_data[1])
        end = int(span_data[2])

        if has_printed:
            print(answer_separator, end="")
        print(" ".join(evidence_lines_for_question[paragraph][start:end+1]), end="")
        has_printed = True