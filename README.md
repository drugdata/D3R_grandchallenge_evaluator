[license]: https://github.com/drugdata/D3R_GC2_evaluation/blob/master/LICENSE

[![DOI](https://zenodo.org/badge/85742402.svg)](https://zenodo.org/badge/latestdoi/85742402)

# D3R_GC2_evaluation
Python based scripts for D3R grand challenge 2 analysis.
For more infomation about the challenge, please visit https://drugdesigndata.org

1, pose prediction:
    The script D3R_GC2_rmsd_calculation.py under folder pose_prediction_rmsd_calculation calculate the RMSDs between submitted ligand and answsers.
    Please check out the usage information by python D3R_GC2_rmsd_calculation.py -h
2, scoring and free energy predictions:
    The script D3R_GC2_ranking_calculation.py under folder ranking_calculations calculate the ranking related statistics: Kendall's Tau, Spearman's rho for both scoring and free energy submissions, and Pearson's R, RMSE for free energy submissions only. 
    Please check out the usage information by python D3R_GC2_ranking_calculation.py -h

The RMSD calculation uses similar code to what has been used in the D3R Grand Challenge 2015 and the SAMPL4 blind challenge. The author thanks for the useful advices from Dr. David Mobley in UC Irvine.

### License

[License][license]

Please feel free to contact drugdesigndata@gmail.com if you have any questions.
