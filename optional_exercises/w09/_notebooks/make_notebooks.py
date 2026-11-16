"""Build the solution notebooks for Exercises 7-9 of ../exercises_w09.qmd.

The code cells are copied from the ```python blocks of the qmd, so after editing
those exercises, rebuild and re-execute the notebooks with

    python make_notebooks.py

from any environment with torch, nbformat, nbclient and ipykernel. Each code cell
is located by the opening line of its block (an "anchor") within its exercise; the
script fails if an anchor matches no block or more than one.
"""

import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
QMD = HERE.parent / "exercises_w09.qmd"
PAGE_URL = "https://utm-csc413.github.io/2026F-website/optional_exercises/w09/exercises_w09.html"


def exercise_blocks(text, number):
    match = re.search(rf"^## Exercise {number} - .*?(?=^## Exercise |\Z)", text, re.S | re.M)
    if match is None:
        raise ValueError(f"Exercise {number} not found in {QMD.name}")
    return [b.strip("\n") for b in re.findall(r"```python\n(.*?)```", match.group(0), re.S)]


def find_block(blocks, number, anchor):
    hits = [b for b in blocks if b.lstrip().startswith(anchor)]
    if len(hits) != 1:
        raise ValueError(f"Exercise {number}: anchor {anchor!r} matches {len(hits)} blocks")
    return hits[0]


def up_to(code, marker):
    if marker not in code:
        raise ValueError(f"marker {marker!r} not found")
    return code[:code.index(marker)].rstrip("\n")


def header(number, title, summary):
    return (f"# Week 9, Exercise {number}: {title}\n\n{summary}\n\n"
            f"This notebook contains the full solution of Exercise {number} from the "
            f"[Week 9 optional exercises]({PAGE_URL}). The saved outputs come from a run on a CPU; "
            "your numbers may differ slightly on Colab or with other PyTorch versions. "
            "Each training run takes a few seconds to about half a minute on a CPU.")


NOTEBOOKS = {
    "ex7_decoder_only_transformer.ipynb": (7, [
        ("md", header(7, "Coding a Decoder-Only Transformer",
                      "We implement a small GPT-style language model from scratch and train it to "
                      "predict the next character of a short text.")),
        ("md", "## (a)-(c) Multi-head attention, the causal mask, the Transformer block, and the model\n\n"
               "`MultiHeadAttention` takes separate query and key/value inputs, so that the same module "
               "can be used for cross-attention in Exercise 9. `Block` follows the encoder layer from the "
               "lecture: self-attention, Add & Norm, FFN, Add & Norm. The `use_mask` argument of "
               "`DecoderOnlyLM` is only there for part (e)."),
        ("code", 7, "import torch", None),
        ("md", "## (d) Training data\n\nEach training example is a window of 32 characters `x`, and the "
               "targets `y` are the same window shifted by one character."),
        ("code", 7, "text = (", None),
        ("md", "Every position in a window is trained to predict the next character at once. This is "
               "teacher forcing: the model always sees the true previous characters, never its own "
               "predictions. To generate, we repeatedly append the most likely next character."),
        ("code", 7, "def train(use_mask", None),
        ("md", "The training text is only about 100 characters long, so the model has essentially "
               "memorized it rather than learned English. Because greedy decoding is deterministic, "
               "it can also get stuck repeating the same phrase."),
        ("md", "## (e) Training without the causal mask"),
        ("code", 7, "model_nomask = train(", None),
        ("md", "The training loss is even lower than with the mask, but generation produces garbage. "
               "Without the mask, position $i$ can attend to position $i+1$, which holds exactly the "
               "character it is supposed to predict, so the model learns to copy it from the input. At "
               "generation time, the next character is not in the input yet, so the copying strategy has "
               "nothing to copy. The causal mask makes training match generation: each position only "
               "sees the characters before it."),
    ]),
    "ex8_encoder_only_transformer.ipynb": (8, [
        ("md", header(8, "Coding an Encoder-Only Transformer",
                      "We implement a small BERT-style classifier, which prepends a `[CLS]` token and uses "
                      "unmasked self-attention, and train it to decide whether a sequence of 8 digits is "
                      "sorted.")),
        ("md", "## Building blocks from Exercise 7\n\n`MultiHeadAttention`, `causal_mask`, and `Block`, "
               "copied from Exercise 7."),
        ("code", 7, "import torch", "class DecoderOnlyLM"),
        ("md", "## Data\n\nOnly about 0.02% of random digit sequences are sorted, so `make_batch` builds a "
               "balanced dataset: each positive is a sorted random sequence, and each negative is a shuffle "
               "of random digits that is not sorted."),
        ("code", 8, "def make_batch(", None),
        ("md", "## (a) The encoder-only classifier"),
        ("code", 8, "class EncoderClassifier", None),
        ("md", "## (b) Training with position embeddings"),
        ("code", 8, "def train(use_pos", None),
        ("md", "## (c) Training without position embeddings"),
        ("code", 8, "train(use_pos=False)", None),
        ("md", "Without position embeddings, the model does no better than chance, and the loss stays at "
               "$\\log 2 \\approx 0.693$. By Exercise 5, unmasked self-attention without positional "
               "information is permutation equivariant, and the FFN, residual connections, and LayerNorm "
               "all act on each token separately. Shuffling the 8 digit tokens therefore only shuffles "
               "their outputs, and the `[CLS]` output (which attends to all of them) does not change at "
               "all. The model only sees the *multiset* of digits. Any multiset of digits can appear both "
               "sorted (as a positive) and shuffled (as a negative), so the multiset carries essentially "
               "no information about the label. With position embeddings, each token knows where it is, "
               "and the task becomes easy."),
    ]),
    "ex9_seq2seq_transformer.ipynb": (9, [
        ("md", header(9, "Coding a Sequence-to-Sequence Transformer",
                      "We implement an encoder-decoder Transformer, whose decoder attends to the encoder "
                      "outputs through cross-attention, and train it to reverse a sequence of 8 digits.")),
        ("md", "## Building blocks from Exercise 7\n\n`MultiHeadAttention`, `causal_mask`, and `Block`, "
               "copied from Exercise 7."),
        ("code", 7, "import torch", "class DecoderOnlyLM"),
        ("md", "## Data\n\nThe decoder input is the target shifted right, starting with `<BOS>`, and the "
               "decoder target ends with `<EOS>`. All sequences have the same length, so we need no padding "
               "mask."),
        ("code", 9, "BOS, EOS", None),
        ("md", "## (a)-(b) The decoder block and the encoder-decoder model\n\nIn cross-attention, the "
               "queries come from the decoder and the keys and values come from the encoder outputs `z`."),
        ("code", 9, "class DecoderBlock", None),
        ("md", "## (c) Training with teacher forcing, and greedy decoding"),
        ("code", 9, "torch.manual_seed(0)", None),
        ("md", "The model reverses essentially every test sequence and ends each one with `<EOS>` "
               "(token 11).\n\n## (d)\n\nThe encoder reads an input sequence that is entirely known in "
               "advance, so every input token can use context from both sides. The decoder is trained with "
               "teacher forcing to predict token $i+1$ from tokens $1, \\dots, i$. Without the mask, it "
               "could read the answer from position $i+1$ of its input (see Exercise 7(e)), and at "
               "generation time the future tokens don't exist yet. In cross-attention, the queries come "
               "from the decoder (the output of its masked self-attention sublayer), and the keys and "
               "values come from the final encoder outputs $Z$. This is how each output position looks up "
               "the relevant input tokens; for reversal, output position $i$ learns to attend to input "
               "position $n + 1 - i$."),
    ]),
}


def build(cells, qmd_text):
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        "colab": {"provenance": []},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
    }
    for cell in cells:
        if cell[0] == "md":
            nb.cells.append(nbformat.v4.new_markdown_cell(cell[1]))
        else:
            _, number, anchor, stop = cell
            code = find_block(exercise_blocks(qmd_text, number), number, anchor)
            if stop is not None:
                code = up_to(code, stop)
            nb.cells.append(nbformat.v4.new_code_cell(code))
    return nb


def main():
    qmd_text = QMD.read_text()
    for name, (number, cells) in NOTEBOOKS.items():
        nb = build(cells, qmd_text)
        NotebookClient(nb, timeout=600, kernel_name="python3", record_timing=False,
                       resources={"metadata": {"path": str(HERE)}}).execute()
        nb.metadata["language_info"] = {"name": "python"}
        for i, cell in enumerate(nb.cells):
            cell.id = f"cell-{i}"
        nbformat.write(nb, HERE / name)
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
