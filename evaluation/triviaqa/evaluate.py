import argparse
import tqdm

from official_triviaqa_evaluation_script import metric_max_over_ground_truths, f1_score, exact_match_score

parser = argparse.ArgumentParser(description='Evaluate predictions using the official evaluation scrip.')
parser.add_argument('--predictions')
parser.add_argument('--gold')
args = parser.parse_args()

answer_separator = " | "

f1 = 0
em = 0
count = 0

pred_file = open(args.predictions, 'r')
gold_file = open(args.gold, 'r')

combined_list = list(zip(pred_file, gold_file))
for pred, gold in tqdm.tqdm(combined_list):
    preds = pred.strip().split(answer_separator)
    golds = gold.strip().split(answer_separator)

    # Use only first pred:

    used_pred = preds[0]

    f1 += metric_max_over_ground_truths(f1_score, used_pred, golds)
    em += metric_max_over_ground_truths(exact_match_score, used_pred, golds)
    count += 1

print("F1: "+str(f1 / count))
print("EM: "+str(em / count))