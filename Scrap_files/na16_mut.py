from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt


params_folder = './params'
l5mdl = NeuronModel()
def make_hmm_wt():
    l5mdl.h.working()
    mechs = ['na16']
    dict_fn = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn, mechs)
    mechs = ['na16mut']
    update_mech_from_dict(l5mdl, dict_fn, mechs)

def plot_stim(stim_amp = 0.5,clr = 'black',fn = 'WT_Na16_Is'):
    l5mdl.init_stim(amp=stim_amp)
    Vm, I, t, stim = l5mdl.run_model(dt=0.01)
    plot_stim_volts_pair(Vm, 'Step Stim 500pA', file_path_to_save=f'./Plots/{fn}.pdf', times=t,color_str=clr)

def plot_fi_curve(start,end,nruns,wt_data = None,ax1 = None, fig = None,fn = 'ficurve.pdf'):
    fis = get_fi_curve(l5mdl,start,end,nruns,dt = 0.1,wt_data = wt_data,ax1=ax1,fig=fig,fn=fn)
    return fis

def make_hmm_het(gbar_factor = 1):
    #fig, ficurveax = plt.subplots(1, 1)
    l5mdl.h.working()
    mechs = ['na16']
    dict_fn_wt = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
    mechs = ['na16mut']
    dict_fn_mut = f'{params_folder}/na16Mut.txt'
    update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
    if gbar_factor != 1:
        update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')


def make_hmm_cultured_wt(gbar_factor = 1):
    #fig, ficurveax = plt.subplots(1, 1)
    l5mdl.h.working()
    mechs = ['na16']
    dict_fn_wt = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
    update_mod_param(l5mdl, mechs, 3, gbar_name='gbar')
    mechs = ['na16mut']
    dict_fn_mut = f'{params_folder}/na16Mut.txt'
    update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
    update_mod_param(l5mdl, mechs, 0, gbar_name='gbar')
    if gbar_factor != 1:
        update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')

def make_hmm_cultured_mut(gbar_factor = 1):
    #fig, ficurveax = plt.subplots(1, 1)
    l5mdl.h.working()
    mechs = ['na16']
    dict_fn_wt = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
    update_mod_param(l5mdl, mechs, 2, gbar_name='gbar')
    mechs = ['na16mut']
    dict_fn_mut = f'{params_folder}/na16Mut.txt'
    update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
    update_mod_param(l5mdl, mechs, 1, gbar_name='gbar')
    if gbar_factor != 1:
        update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')

def make_hmm_cultured_wt_TTX(gbar_factor = 1):
    #fig, ficurveax = plt.subplots(1, 1)
    l5mdl.h.working()
    mechs = ['na16']
    dict_fn_wt = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
    update_mod_param(l5mdl, mechs,1, gbar_name='gbar')
    mechs = ['na16mut']
    dict_fn_mut = f'{params_folder}/na16Mut.txt'
    update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
    update_mod_param(l5mdl, mechs, 0, gbar_name='gbar')
    if gbar_factor != 1:
        update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')

def make_hmm_cultured_mut_TTX(gbar_factor = 1):
    #fig, ficurveax = plt.subplots(1, 1)
    l5mdl.h.working()
    mechs = ['na16']
    dict_fn_wt = f'{params_folder}/na16WT.txt'
    update_mech_from_dict(l5mdl, dict_fn_wt, mechs)
    update_mod_param(l5mdl, mechs, 0, gbar_name='gbar')
    mechs = ['na16mut']
    dict_fn_mut = f'{params_folder}/na16Mut.txt'
    update_mech_from_dict(l5mdl, dict_fn_mut, mechs)
    update_mod_param(l5mdl, mechs, 1, gbar_name='gbar')
    if gbar_factor != 1:
        update_mod_param(l5mdl, mechs, gbar_factor, gbar_name='gbar')