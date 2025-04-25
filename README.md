# ForbiddenFrUIT

Here, we introduce the annotations we made on the FrUIT corpus (see [here](https://github.com/JulienBez/FrUIT)) for Multiword Expression (MWEs) and Puns in Multiword Expressions (PMWEs) detection. We annotated a total of 600 tweets between 3 experts. Each tweet has been tagged according to whether it contains a MWE, a PMWE or neither. This repository contains the results of this annotation process as well as the begining of a new annotation phase, in which we aim to annotate at token-level the PMWEs within those 600 tweets. 

## Data structure

- **data/all** - contains all the annotations made during several annotations phases between 3 experts (A1, A2 and A3) ;
- **data/csv** - contains the generated **csv** files for the new annotation phase. Only contains PMWEs ;
- **data/json** - contains the converted **csv** files from **data/csv** to **json** format for later use ;
- **guide** - contains the annotation guidelines for the new annotation phase ;
- **output** - contains some graphs regarding the results of the first annotation phase.

## How to use

First, run this command to install all the prerequisites:

```
pip install -r requirements.txt
```

There is a total of 3 commands, which can be executed as follows:

```
python main.py -Mmc
```

- **M (metadata)** - gives some metadata regarding the first annotation phase ;
- **m (make)** - create the ready-to-annotate **csv** files for the second annotation phase ;
- **c (convert)** - convert the ready-to-annotate **csv** files to **json** for later use.
