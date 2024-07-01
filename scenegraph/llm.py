import fire
from llama import Llama

from pathlib import Path
import json
import os

BASEBATH = Path(__file__).resolve().parent
PROMPTS_DIRECTORY = BASEBATH / "prompts"
RESULTS_DIRECTORY = BASEBATH / "results" / "raw"

def load_text_files(directory):
    text_list = []
    filenames = []
    for filepath in directory.glob("*.txt"):
        with filepath.open('r') as file:
            text_list.append(file.read())
            filenames.append(filepath.name)
    return text_list, filenames

def write_text_files(text_list, filenames, directory):
    for text, filename in zip(text_list, filenames):
        output_path = directory / filename
        with output_path.open('w') as file:
            file.write(text)

class Llama3Parser:
    def __init__(self, ckpt_dir, tokenizer_path, max_seq_len, max_batch_size):
        
        # instantiate llama
        self.generator = Llama.build(
            ckpt_dir=ckpt_dir,
            tokenizer_path=tokenizer_path,
            max_seq_len=max_seq_len,
            max_batch_size=max_batch_size,
        )


    def batch_parse_n_save(self, prompts, filenames, max_gen_len, temperature, top_p):
        results = self.batch_parse(prompts, max_gen_len, temperature, top_p)
        results = [json.dumps(result) for result in results]
        write_text_files(results, filenames, RESULTS_DIRECTORY)
        


    def batch_parse(self, prompts, max_gen_len=64, temperature=0.6,top_p=0.9):
        results = self.generator.text_completion(
            prompts,
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
        return results


def main(ckpt_dir, tokenizer_path, max_seq_len, max_batch_size, max_gen_len, temperature, top_p):
    prompts, filenames = load_text_files(PROMPTS_DIRECTORY)
    llm = Llama3Parser(
        ckpt_dir=ckpt_dir, 
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    llm.batch_parse_n_save(prompts, filenames, max_gen_len=max_gen_len, temperature=temperature,top_p=top_p)


if __name__ == "__main__":
    fire.Fire(main)
