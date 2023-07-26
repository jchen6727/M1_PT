from NaMut import *
import matplotlib.pyplot as plt
import numpy as np
import NrnHelper as NH
from neuron import h
import time
import efel
efel.api.setDoubleSetting('Threshold', 15)
import pandas as pd
import math
from scipy.signal import find_peaks

def get_sim_volt_values(mutant_name,rec_extra = False,dt = 0.005,stim_amp = 0.3):

    sim = NaMut(mutant_name)
    sim.dt= dt
    sim.make_het()
    rec_extra = True
    sim.l5mdl.init_stim(amp=stim_amp)
    if rec_extra:
        Vm, I, t, stim,extra_vms = sim.l5mdl.run_model(dt=dt,rec_extra = rec_extra)
        sim.extra_vms = extra_vms
    else:
        Vm, I, t, stim = sim.l5mdl.run_model(dt=dt)
        extra_vms = {}

    return Vm,t,extra_vms,I,stim

def get_features(mutant_name = 'na12WT2',rec_extra=True):
    print("running routine")
    dt=0.005
    Vm,t,extra_vms,_,__ = get_sim_volt_values(mutant_name,rec_extra=rec_extra)
    #creating the trace file
    stim_start = 100
    stim_end = 600
    trace={}
    trace = {'T':t,'V':Vm,'stim_start':[stim_start],'stim_end':[stim_end]}
    trace['T']= trace['T'] * 1000
    #for neu
    feature_list= ['AP_height','AP_width','AP1_peak','AP1_width','Spikecount','all_ISI_values']
    traces = [trace]
    features = efel.getFeatureValues(traces,feature_list)
    try:
        features[0]['ISI mean'] =features[0]['all_ISI_values'].mean()
    except Exception as e:
        features[0]['ISI mean'] = 0
    features[0]['AP_height'] =features[0]['AP_height'].mean()
    features[0]['AP_width'] =features[0]['AP_width'][0].mean()
    features[0]['AP1_peak'] =features[0]['AP1_peak'][0]
    features[0]['AP1_width'] =features[0]['AP1_width'][0]
    features[0]['Spikecount'] =features[0]['Spikecount'][0]
    #import pdb; pdb.set_trace()
    #for dv/dt Peak 1 and Peak 2 and sum
    spike_count= features[0]['Spikecount']
    isi_values = features[0]['all_ISI_values']
    median_spike = int(math.ceil(spike_count/2)) + 1
    #median spike location
    start = int((stim_start + isi_values[0:median_spike-1].sum())/dt)    #dividing by dt to get into same unit
    end = start + int(isi_values[median_spike]/dt)
    volt_segment = Vm[start:end]
    dvdt = np.gradient(volt_segment)/dt
    curr_peaks_indices,curr_peaks_values= find_peaks(dvdt,height = 100)
    features[0]['dvdt Peak1 Height'] = curr_peaks_values['peak_heights'][0]
    features[0]['dvdt Peak1 Voltage'] = volt_segment[curr_peaks_indices[0]]
    features[0]['dvdt Peak2 Height'] = curr_peaks_values['peak_heights'][-1]
    features[0]['dvdt Peak2 Voltage'] = volt_segment[curr_peaks_indices[-1]]
    features[0]['dvdt Threshold'] = volt_segment[np.where(dvdt>1)[0][0]]
    if rec_extra:
    #for ais
        trace['V'] = extra_vms['ais']
        feat_list = ['Spikecount']
        traces = [trace]
        feature_ais = efel.getFeatureValues(traces,feat_list)
        features[0]['ais spikecount'] =feature_ais[0]['Spikecount']
        features[0]['ais spikecount'] =features[0]['ais spikecount'][0]
        
        #for nexus
        trace['V'] = extra_vms['nexus']
        feat_list = ['Spikecount']
        traces = [trace]
        feature_nex = efel.getFeatureValues(traces,feat_list)
        features[0]['nex spikecount'] =feature_nex[0]['Spikecount']
        features[0]['nex spikecount'] =features[0]['nex spikecount'][0]
        
        #for dist_dend
        trace['V'] = extra_vms['dist_dend']
        feat_list = ['Spikecount']
        traces = [trace]
        feature_disdend = efel.getFeatureValues(traces,feat_list)
        features[0]['disdend spikecount'] =feature_disdend[0]['Spikecount']
        features[0]['disdend spikecount'] =features[0]['disdend spikecount'][0]
    
    features = pd.DataFrame(features)
    features = features.drop(columns =['all_ISI_values'])
    features.insert(0,'Type',mutant_name)
    
    return features
    




# mut_names = ['R853Q','E1211K','A1773T','G879R','A880S','A427D','E430A','E999K','E1211K','E1880K','G879R',
#            'K1260E','K1260Q','M1879T','R571H','R850P','R1319L','R1626Q','R1882L','R1882Q','S1780I','Y816F','na12WT2']

mut_names = ['R853Q','E1211K']
mut_not_found = {}
feature_row=None
for mut_name in mut_names:
    try:
        feature_row = get_features(mutant_name=mut_name)
        with open('efel_features.csv', 'a') as f:
            feature_row.to_csv(f, header=f.tell()==0,index=False) #bug needs an existing file

    except Exception as e:
        print(e)
        mut_not_found[mut_name] = e


