1. sample_articles_rev_ids.json- This file contains the timestamps and corresponding revision ID referring to the revisions of articles. We have shown the data for sample articles only.
2. sample_articles_ores_preds.json - This file lists the prediction of quality classes (i.e, SS, BC, AGA or FA) by ORES for all the revisions of articles.
3. sample_articles_ores_timeseries_permonth.json - It filters out the latest revision timestamp and its quality as predicted by ORES on every month for a given article. If the quality remains same as that of the previous 
   month it is marked as 0, otherwise 1.
4. ORES_Predictor.py - This code extracts the ORES predictions for all the revisions of the articles using the ORES API.
5. ORES_Evaluation.py - This code computes the precision, recall and coverage for the time series based on ORES predictions.

#### To compare ORES results with our CPD algorithm settings ####
1. The code **ORES_Predictor.py** will be run. It will generate the file **sample_articles_ores_preds.json**.
2. The code **ORES_Evaluation.py** needs to be run for comparison.
