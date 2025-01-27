from transformers import AutoTokenizer
from gitingest import ingest


def main():
    model_id = "meta-llama/Llama-3.3-70B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id, legacy=False)

    summary, tree, content = ingest("https://github.com/cyclotruc/gitingest")

    text = "hello"

    input_text = "What are we having for dinner?"
    input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")

    print(input_ids)


if __name__ == "__main__":
    main()
