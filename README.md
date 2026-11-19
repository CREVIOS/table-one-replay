# Table One Replay

Can someone outside a research group check a published table cell on a laptop? This pilot starts with calibration error. It includes a working scorer, six synthetic predictions and a plan to check one result from Guo et al. Anyone with Python 3.9 or later can run it on CPU, offline, with no account or package installation.

## Replay the example

From the repository root, run

```sh
python3 replay.py > bins.csv
python3 -m unittest -v
```

The first command writes 15 rows to `bins.csv` and prints **23.33%** for expected calibration error (ECE) and **3.33%** for the pooled gap. Two occupied bins explain the difference.

| Confidence | Predictions | Correct | Sum of confidences | Correct minus sum of confidences |
| --- | ---: | ---: | ---: | ---: |
| 60% | 2 | 2 | 1.2 | +0.8 |
| 90% | 4 | 3 | 3.6 | −0.6 |

ECE adds the absolute gaps within bins and divides by six, giving (0.8 + 0.6) / 6. Pooling lets opposite errors cancel, giving |0.8 − 0.6| / 6. Publishing the counts, correct totals and sums lets a reader check that arithmetic without receiving individual predictions.

To score another export, run `python3 replay.py predictions.csv > bins.csv`. The required columns are `confidence` (probability assigned to the predicted class) and `correct` (0 or 1). Bins are equal width with inclusive upper edges. Bin 1 includes zero. The output uses exact fractions for confidence sums.

## First replication target

Guo et al. report **16.53%** uncalibrated ECE and **1.26%** after temperature scaling in Table 1, CIFAR-100, ResNet-110, using 15 bins. These two paper values are **awaiting independent replay**. The results above come from the six-row synthetic fixture. [Paper, Table 1](https://arxiv.org/html/1706.04599v2) · [Author’s demonstration code](https://github.com/gpleiss/temperature_scaling)

The proposed Devin Bot pilot has three steps.

1. Before allocating a GPU, check for the original test outputs, labels and split identifiers. Fitting the temperature also needs validation logits and labels. Record the available input hashes and code revision. Stop the access check after five CPU minutes and mark a missing input by name.
2. Fit the temperature on the validation split only. Export and score the held-out test predictions before and after scaling. Record the fitted temperature, 15-bin summaries, replay commands, environment and actual credit usage.
3. Give a second researcher the permitted artifacts and ask them to replay the row on a clean machine without Devin. Compare the values at the paper’s printed precision and publish any difference, including the first bin that diverges when both bin summaries are available.

If the artifacts are private, the lab can run the scorer locally and choose whether to share its aggregate bins. Those bins let outsiders check how the metric was calculated. Independently verifying the model predictions still requires access to the underlying artifacts. A blocked row stays visible with its missing input and cost. Independent public rows can continue.

To report a discrepancy, open an issue with the commit, replay command and first differing bin. Share only artifacts you have permission to publish.
