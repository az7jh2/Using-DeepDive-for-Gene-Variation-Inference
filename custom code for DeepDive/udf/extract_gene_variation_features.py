#!/usr/bin/env python
from deepdive import *
import ddlib

@tsv_extractor
@returns(lambda
        gene_id        = "text",
        variation_id   = "text",
        feature        = "text",
    :[])
def extract(
        gene_id          = "text",
        variation_id     = "text",
        gene_begin_index = "int",
        gene_end_index   = "int",
        var_begin_index  = "int",
        var_end_index    ="int",
        doc_id           = "text",
        sent_index       = "int",
        tokens           = "text[]",
        lemmas           = "text[]",
        pos_tags         = "text[]",
        ner_tags         = "text[]",
        dep_types        = "text[]",
        dep_parents      = "int[]",
    ):
    """
    Uses DDLIB to generate features for the spouse relation.
    """
    # Create a DDLIB sentence object, which is just a list of DDLIB Word objects
    sent = []
    for i,t in enumerate(tokens):
        sent.append(ddlib.Word(
            begin_char_offset=None,
            end_char_offset=None,
            word=t,
            lemma=lemmas[i],
            pos=pos_tags[i],
            ner=ner_tags[i],
            dep_par=dep_parents[i] - 1,  # Note that as stored from CoreNLP 0 is ROOT, but for DDLIB -1 is ROOT
            dep_label=dep_types[i]))

    # Create DDLIB Spans for the gene and variation mentions
    gene_span = ddlib.Span(begin_word_id=gene_begin_index, length=gene_end_index-gene_begin_index)
    variation_span = ddlib.Span(begin_word_id=var_begin_index, length=var_end_index-var_begin_index)

    # Generate the generic features using DDLIB
    for feature in ddlib.get_generic_features_relation(sent, gene_span, variation_span):
        yield [gene_id, variation_id, feature]
