# Data

Raw and processed data are intentionally excluded from Git.

## Primary dataset

KuaiRand-1K from the official KuaiRand release.

Official source:
- https://github.com/chongminggao/KuaiRand
- https://zenodo.org/records/10439422

Download `KuaiRand-1K.tar.gz`, extract it, and place the extracted folder under:

```text
data/raw/KuaiRand-1K/
```

Do **not** commit the raw dataset to GitHub.

## Why KuaiRand-1K?

The project needs sequential recommendation logs for session/repeat-usage analysis plus randomized exposure logs for causal/debiasing work. KuaiRand-1K keeps those capabilities while avoiding the ~46 GB footprint of the full 27K release.

## Dataset license

The dataset's official repository specifies CC BY-SA 4.0. Follow the dataset authors' license and citation requirements independently from this project's code license.
