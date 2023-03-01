# FairEM

Synthetic Data Generator:
Use csranking_for_em.py and compas_preprocess.py to generate datasets for EM. Based on the commented examples, you can choose change the columns, perturbation and number of samples.

Running the Experiments:
For running the experiments, first you need to get the predictions from your prefered entity matcher and export them in a CSV file with a column named "preds". Then by specfiying the "test" data in the src/run.py you reproduce the plots. Make sure to follow the directory paths based on the given examples.
