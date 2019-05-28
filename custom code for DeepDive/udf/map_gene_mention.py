#!/usr/bin/env python
from deepdive import *
import json

@tsv_extractor
@returns(lambda
        mention_id       = "text",
        mention_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        gene_begin_index = "int",
        gene_end_index   = "int",
    :[])
def extract(
        doc_id         = "text",
        sentence_index = "int",
        tokens         = "text[]",
        ner_tags       = "text[]",
    ):
    """
    Finds genes that are words tagged with GENE or in gene_list.
    """
    with open("/home/hill103/nips_2017/input/gene_list.json", "r") as f:
        gene_list = set(json.load(f))
    num_tokens = len(ner_tags)
    # find all indexes of series of tokens tagged as GENE
    for index in range(num_tokens):
        if ner_tags[index] == "GENE" or tokens[index] in gene_list:
            # generate a mention identifier
            mention_id = "%s_%d_%d" % (doc_id, sentence_index, index)
            mention_text = tokens[index]
            # Output a tuple for each PERSON phrase
            yield [
                mention_id,
                mention_text,
                doc_id,
                sentence_index,
                index,
                index+1,
            ]
