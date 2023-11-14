import csv

from transformers import AutoTokenizer, BertForSequenceClassification


# Get model
tokenizer = AutoTokenizer.from_pretrained(
    "Emran/ClinicalBERT_description_full_ICD10_Code"
)
model = BertForSequenceClassification.from_pretrained(
    "Emran/ClinicalBERT_description_full_ICD10_Code"
)
config = model.config


def get_code(text, top_n=3):
    encoded_input = tokenizer(text, return_tensors="pt")
    output = model(**encoded_input)
    codes = [
        config.id2label[ids]
        for ids in output.logits.detach().cpu().numpy()[0].argsort()[::-1][:top_n]
    ]
    return codes


text = "IRON DEFICIENCY ANAEMIA"


def top_level_term(term: str) -> str:
    return term.split(".")[0]


def run_test(test_file: str) -> list[dict[str, str]]:
    print(
        "SATERM,ICD-10 Code,ICD-10 Predicted,MatchInTopTerms,ExactMatch,MatchInTopLevelTerms,ExactMatchTopLevel"
    )
    with open(test_file) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            model_terms = get_code(row["SATERM"])
            actual_term = row["ICD-10 Code"]
            actual_top_level = top_level_term(actual_term)
            model_top_level_terms = list(map(top_level_term, model_terms))
            print(
                ",".join(
                    [
                        row["SATERM"],
                        row["ICD-10 Code"],
                        ";".join(model_terms),
                        str(int(actual_term in model_terms)),
                        str(int(actual_term == model_terms[0])),
                        str(int(actual_top_level in model_top_level_terms)),
                        str(int(actual_top_level == model_top_level_terms[0])),
                    ]
                )
            )

run_test("terms_training.csv")
