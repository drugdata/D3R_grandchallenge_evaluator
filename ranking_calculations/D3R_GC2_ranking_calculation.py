#!/usr/bin/env python
__author__ = "Shuai Liu"
__email__ = "shuailiu25@gmail.com"

import sys
import os
import numpy as np
from random import shuffle
import scipy.stats as sp
import math
import logging 
import pickle
import argparse

def rms(predictions, targets):
    #calculate the centered rms
    diff = predictions - targets
    mean_diff = np.mean(diff)
    translated_diff = diff - mean_diff
    return np.sqrt((translated_diff**2).mean())
def bootstrap_exptnoise( calc1, expt1, exptunc1 = 0):
    #using bootstrap to generate new data 
    calc = np.array(calc1)
    expt = np.array(expt1)
    exptunc = np.array(exptunc1)
    npoints = len(calc)
    idx = np.random.randint( 0, npoints, npoints)
    newcalc = calc[idx]
    newexpt = expt[idx]                                             
    newexptunc = exptunc[idx]
    print "Check the new list 111", newcalc
    print "Check the new list 222", newexpt
    print "Check the new list 333", newexptunc, npoints
    if exptunc == []:
        noise = np.zeros( npoints)
    else:
        noise = np.random.normal( 0., exptunc, npoints)             
    print "Noise nnnnnn", noise
    newexpt += noise                                                
    print "Check the new list 444", newexpt
    return newcalc, newexpt 
def calculate_kendalls (template_value, submitted_value, exp_unc, boot_bins = 10000):
    #calculating kendalls tau etc using bootstrapping resampling method
    if len(template_value)> 2:
        taus = np.zeros(boot_bins)
        spearmans = np.zeros(boot_bins)
        rms_errors = np.zeros(boot_bins)
        Pearsons = np.zeros(boot_bins)
        for i in range (boot_bins):
            new_template_value, new_submitted_value = bootstrap_exptnoise(template_value, submitted_value, exp_unc)
            rms_errors[i] = rms(new_template_value, new_submitted_value)
            taus[i] = sp.kendalltau(new_template_value, new_submitted_value)[0]
            if math.isnan(taus[i]):
                    taus[i] = 0
            spearmans[i] = sp.spearmanr(new_template_value, new_submitted_value)[0]
            Pearsons[i] = sp.pearsonr(new_template_value, new_submitted_value)[0]
        rms_error = rms(np.asarray(template_value), np.asarray(submitted_value))
        tau = sp.kendalltau(template_value, submitted_value)[0]
        spearman = sp.spearmanr(template_value, submitted_value)[0]
        Pearson = sp.pearsonr(template_value, submitted_value)[0]
        return (rms_error, rms_errors.std(), tau, taus.std(), spearman, spearmans.std(), Pearson, Pearsons.std())
    else:
        return False

def uM_to_kcal(ic50):
    #convert the ic50 values to binding affinity
    return math.log(ic50 * 1e-6) * 0.5961

def ic50_ratio_to_kcal(ic50_ratio):                                 
    #convert the ic50 uncertainty(ratio) to binding affinity uncertainty
    return math.log(ic50_ratio) * 0.5961

def extract_ranking_list(template_csv, submitted_csv, template_error_csv, system_name = "FXR_"):
    #extract the template and submission values 
    template_f = open(template_csv, "r")
    template_lines = template_f.readlines()
    template_dic= {}
    for template_line in template_lines:
        template_title = template_line.split(",")[0].strip()
        template_value = uM_to_kcal(float(template_line.split(",")[1]))
        if template_title not in template_dic:
            template_dic[template_title] = template_value
    template_error = open(template_error_csv, "r")
    template_error_lines = template_error.readlines()         
    template_error_dic = {}
    for template_error_line in template_error_lines:
        template_error_title = template_error_line.split(",")[0].strip()
        template_error_value = ic50_ratio_to_kcal(float(template_error_line.split(",")[1]))
        if template_error_title not in template_error_dic:
            template_error_dic[template_error_title] = template_error_value
    submitted_f = open(submitted_csv, "r")
    submitted_lines = submitted_f.readlines()
    title_list = []
    template_value_list = []
    template_error_value_list = []
    submitted_value_list = []
    for submitted_line in submitted_lines:
        if system_name in submitted_line: 
            submitted_title = submitted_line.split(",")[0].strip()
            if submitted_title in template_dic:
                try:
                    submitted_value = float(submitted_line.split(",")[1])
                    title_list.append(submitted_title)
                    template_value_list.append(template_dic[submitted_title])
                    template_error_value_list.append(template_error_dic[submitted_title])
                    submitted_value_list.append(submitted_value)
                except:
                    pass
    return (len(title_list), template_value_list, submitted_value_list, template_error_value_list)   
   

def main_ranking (submitted_folder_path, template_affinity_file, template_error_file, bootstrap = 10000, free_energy = True):
    if free_energy:
        out_ranking_csv = open("%s/Free_energy_rankings.csv"%submitted_folder_path, "w")
        submitted_csv = "%s/FreeEnergies.csv"%submitted_folder_path
        try:
            num_bins, template_value_list, submitted_value_list, template_error_value_list = extract_ranking_list(template_affinity_file, submitted_csv, template_error_file, system_name = "FXR_")
            logging.info("Got %s of submitted ligand in this submission"%num_bins)
            rms_error, rms_errors_std, tau, taus_std, spearman, spearmans_std, Pearson, Pearsons_std = calculate_kendalls (template_value_list, submitted_value_list, template_error_value_list, boot_bins = bootstrap)
            logging.info("The Kendall's Tau value for this submission is %s"%tau)
            data = ["type, num_bins, kendall, kendall_err, spearman, spearman_err, Pearson, Pearson_err, RMSD, RMSD_err\n"]
            data.append("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%("Free_energy", num_bins, tau, taus_std, spearman, spearmans_std, Pearson, Pearsons_std, rms_error, rms_errors_std))
            logging.info("Successfully calculate the ranking statistics...")
        except:
            logging.info("Fatal Error: The calculation didn't finish...")
            data = ["N/A\n"]
    else:
        out_ranking_csv = open("%s/Scoring_rankings.csv"%submitted_folder_path, "w")
        try:
            submitted_csv = "%s/LigandScores.csv"%submitted_folder_path
            num_bins, template_value_list, submitted_value_list, template_error_value_list = extract_ranking_list(template_affinity_file, submitted_csv, template_error_file, system_name = "FXR_")
            logging.info("Got %s of submitted ligand in this submission"%num_bins)
            rms_error, rms_errors_std, tau, taus_std, spearman, spearmans_std, Pearson, Pearsons_std = calculate_kendalls (template_value_list, submitted_value_list, template_error_value_list, boot_bins = bootstrap)
            logging.info("The Kendall's Tau value for this submission is %s"%tau)
            data = ["type, num_bins, kendall, kendall_err, spearman, spearman_err\n"]
            data.append("%s,%s,%s,%s,%s,%s\n"%("Scoring", num_bins, tau, taus_std, spearman, spearmans_std))
            logging.info("Successfully calculate the ranking statistics...")
        except:
            logging.info("Fatal Error: The calculation didn't finish...")
            data = ["N/A\n"]
    out_ranking_csv.writelines(data)
    

if ("__main__") == (__name__):
    desc = """
This code was design to evaluate the scoring and free energy of D3R Grand Challenge 2
For more infomation about the challenge, please visit https://drugdesigndata.org/

######Usage exmaple######
### Use the freeenergy option to analyze the free energy type of submissions###
# python D3R_GC2_ranking_calculation.py --submitdir ./example_free_energy_submission_folder --templatefile ./experimental_data/experimental_affinity.csv --errorfile ./experimental_data/experimental_uncertainty.csv --freeenergy  

### Do not use freeenergy option to calculate the scoring type of submissions ###
# python D3R_GC2_ranking_calculation.py --submitdir ./example_scoring_submission_folder --templatefile ./experimental_data/experimental_affinity.csv --errorfile ./experimental_data/experimental_uncertainty.csv 
#########################

######Output#######
### Scoring_rankings.csv for scoring submissions 
### Free_energy_rankings.csv for free energy submissions 
### Output files are under example_submission_folder
###################

######Dependencies######
#numpy 
#scipy
########################
    """
    help_formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=desc,
                            formatter_class=help_formatter)
    parser.add_argument("-s", "--submitdir", metavar="PATH",
                      help="PATH where we could find the submission files")

    parser.add_argument("-t", "--templatefile", metavar="PATH",
                      help="PATH where we could find the template affinity")
    parser.add_argument("-e", "--errorfile", metavar="PATH",  
                      help="PATH where we could find the uncertainty of the template affinity")
    parser.add_argument("-f", "--freeenergy", action="store_true",
                      help="Free energy type of submission")
    parser.add_argument("-b", "--bootstrap", type=int, default =10000, 
                      help="Bootstrapping resampling times")
    parser.add_argument("-l", "--logfilename", default= "ranking_calculation.log", metavar="FILENAME",
                      help="Log file name")
    opt = parser.parse_args()
    submitDir = opt.submitdir
    tempfile = opt.templatefile
    temperrfile = opt.errorfile
    logfilename = opt.logfilename
    bootstrap_bins = opt.bootstrap
    free_energy_option = opt.freeenergy
    logger = logging.getLogger()
    logging.basicConfig( format  = '%(asctime)s: %(message)s', datefmt = '%m/%d/%y %I:%M:%S', filename = logfilename, filemode = 'w', level   = logging.INFO )
    logging.info("Working on submission :%s and the template file is %s"%(submitDir, tempfile))
    main_ranking (submitDir, tempfile,temperrfile, bootstrap = bootstrap_bins , free_energy = free_energy_option)
