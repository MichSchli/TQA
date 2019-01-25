#!/bin/bash

PRED_FILE=$1
DATASET=$2

PRED_ANSWER_FILE=$PRED_FILE'.predictions.txt'
rm -rf $PRED_ANSWER_FILE

pipenv run python evaluation/triviaqa/span_to_text.py --document $DATASET'/evidence.txt' --spans $PRED_FILE > $PRED_ANSWER_FILE

pipenv run python evaluation/triviaqa/evaluate.py --predictions $PRED_ANSWER_FILE --gold $DATASET/answers.txt
