# Left

## CLEVR Dataset (Original)

**Step 1**: prepare the dataset. Download from [here](https://cs.stanford.edu/people/jcjohns/clevr/). We use the setup from Mao et al. 2019. See the original instruction here: [GitHub Repo](https://github.com/vacancy/NSCL-PyTorch-Release).

To replicate the experiments, you need to prepare your dataset as the following.

```
clevr
├── train
│   ├── images
│   ├── questions.json
│   ├── scenes-raw.json
│   └── scenes.json
│   └── vocab.json
└── val
    ├── images
    ├── questions.json
    ├── scenes-raw.json
    └── scenes.json
    └── vocab.json
```

You can download all images, and put them under the `images/` folders from the [official website](https://cs.stanford.edu/people/jcjohns/clevr/) of the CLEVR dataset.
The `questions.json` and `scenes-raw.json` could also been found on the website.

Next, you need to add object detection results for scenes. Here, we use the tools provided by [ns-vqa](https://github.com/kexinyi/ns-vqa).
In short, a pre-trained Mask-RCNN is used to detect all objects. We provide the json files with detected object bounding boxes at [clevr/train/scenes.json](http://nscl.csail.mit.edu/data/code-data/clevr/train/scenes.json.zip) and [clevr/val/scenes.json](http://nscl.csail.mit.edu/data/code-data/clevr/val/scenes.json.zip).

The `vocab.json` could be downloaded at [this URL](http://nscl.csail.mit.edu/data/code-data/clevr/vocab.json).


**Step 2**: generate groundtruth programs for CLEVR/train and CLEVR/val

```bash
jac-run scripts/gen-clevr-gt-program.py --input data/clevr/train/questions.json --output data/clevr/train/questions-ncprogram-gt.pkl
jac-run scripts/gen-clevr-gt-program.py --input data/clevr/val/questions.json --output data/clevr/val/questions-ncprogram-gt.pkl
```

**Step 3**: Training (10% Data Efficiency)

```bash
jac-crun 0 scripts/trainval-clevr.py --desc experiments/desc_neuro_codex_clevr_learned_belongings.py \
  --data-dir data/clevr/train \
  --data-parses data/clevr/train/questions-ncprogram-gt.pkl data/clevr/val/questions-ncprogram-gt.pkl \
  --curriculum all --expr original --validation-interval 5 --config model.learned_belong_fusion=plus --data-tvsplit 0.95 --data-retain 0.1
```

**Step 4**: Training (100% Data Efficiency)

```bash
jac-crun 0 scripts/trainval-clevr.py --desc experiments/desc_neuro_codex_clevr_learned_belongings.py \
  --data-dir data/clevr/train \
  --data-parses data/clevr/train/questions-ncprogram-gt.pkl data/clevr/val/questions-ncprogram-gt.pkl \
  --curriculum all --expr original --validation-interval 5 --config model.learned_belong_fusion=plus --data-tvsplit 0.95
```

**Step 5**: Evaluation

```bash
jac-crun 0 scripts/trainval-clevr.py --desc experiments/desc_neuro_codex_clevr_learned_belongings.py \
  --data-dir data/clevr/train \
  --data-parses data/clevr/train/questions-ncprogram-gt.pkl data/clevr/val/questions-ncprogram-gt.pkl \
  --curriculum all --expr original --validation-interval 5 --config model.learned_belong_fusion=plus --data-tvsplit 0.95 \
  --load <TRAINED_CHECKPOINT_FILE> \
  --validation-data-dir data/clevr/val --evaluate
```

## CLEVR-Humans Dataset

```bash
jac-crun 0 scripts/trainval-clevr.py --desc experiments/desc_neuro_codex_clevr_learned_belongings.py \
  --data-dir data/clevr-humans/train --data-parses promptv4-clevr-humans-trial3-round3.decomposed-full.pkl \
  --curriculum none --expr human --data-tvsplit 0.95 --validation-interval 5 --config model.learned_belong_fusion=plus \
  --load <TRAINED_CHECKPOINT_FILE>
```

Here <TRAINED_CHECKPOINT_FILE> should be replaced by the trained checkpoint file on the original CLEVR.

## CLEVR-Refs (Evaluation Only)

```bash
scripts/trainval-clevr.py --desc experiments/desc_neuro_codex_clevr_learned_belongings.py \
  --data-dir data/clevr-mini --data-parses questions-ncprogram-gt-canonize-same.json transfer-questions-ncprogram.pkl \
  --expr transfer --config model.learned_belong_fusion=plus \
  --load <TRAINED_CHECKPOINT_FILE> \
  --evaluate-custom ref --data-questions-json refexps-20230513.json
```

Note that here we need to use CLEVR-Mini dataset from [NS-VQA](https://github.com/kexinyi/ns-vqa), because we need to have the groundtruth set of objects.
You can also generate your own dataset using the code `scripts/gen-clevr-ref.py`

## CLEVR-PUZZLE (Evaluation Only)

```bash
scripts/trainval-clevr.py --desc experiments/desc_neuro_codex_clevr_learned_belongings.py \
  --data-dir data/clevr-mini --data-parses questions-ncprogram-gt-canonize-same.json transfer-questions-ncprogram.pkl \
  --expr transfer --config model.learned_belong_fusion=plus \
  --load <TRAINED_CHECKPOINT_FILE> \
  --evaluate-custom puzzle --data-questions-json puzzle-20230513.json
```

You can also generate your own dataset using the code `scripts/gen-clevr-puzzle.py`

## CLEVR-RPM (Evaluation Only)

```bash
scripts/trainval-clevr.py --desc experiments/desc_neuro_codex_clevr_learned_belongings.py \
  --data-dir data/clevr-mini --data-parses questions-ncprogram-gt-canonize-same.json transfer-questions-ncprogram.pkl \
  --expr transfer --config model.learned_belong_fusion=plus \
  --load <TRAINED_CHECKPOINT_FILE> \
  --evaluate-custom rpm --data-questions-json rpm-20230513.json
```

You can also generate your own dataset using the code `scripts/gen-clevr-rpm.py`