from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import numpy as np
class NaMut:
    def __init__(self,mut_name = 'na12WT3',wt_file = 'na12WT3', wt_mec = 'na12',mut_mec = 'na12mut', params_folder = './params/',nav12=1,nav16=1,plots_folder = f'./Plots/'):
        self.l5mdl = NeuronModel(nav12=nav12, nav16=nav16)
        #mechs = ['na12']
        #update_mod_param(self.l5mdl, mechs, 2, gbar_name='gbar')
        #mechs = ['na12mut']
        #update_mod_param(self.l5mdl, mechs, 0, gbar_name='gbar')
        
        self.mut_mech = [mut_mec]
        self.wt_mech = [wt_mec]
        self.plot_folder = plots_folder 
        if wt_file:
            print(f'using wt_file {wt_file}')
            p_fn = f'{params_folder}{wt_file}.txt'
            self.wt_p = update_mech_from_dict(self.l5mdl, p_fn, self.wt_mech) 
        if mut_name:#to generate a full WT call it with na12WT as mut name
            print(f'using mut_file {mut_name}')
            self.mut_name = mut_name
            self.plot_folder = f'{plots_folder}{self.mut_name}/'
            Path(self.plot_folder).mkdir(parents=True, exist_ok=True)
            p_fn = f'{params_folder}{self.mut_name}.txt'
            self.mut_p = update_mech_from_dict(self.l5mdl, p_fn, self.mut_mech) 
    def make_het(self):
        self.l5mdl.h.working()
        #updating the WT 
        update_mech_from_dict(self.l5mdl, self.wt_p, self.wt_mech,input_dict = True)
        #updating the Mut 
        update_mech_from_dict(self.l5mdl, self.mut_p, self.mut_mech,input_dict = True)

    def make_wt(self):
        self.l5mdl.h.working()
        #update_mech_from_dict(self.l5mdl, self.wt_p, self.wt_mech,input_dict = True)
        #updating the Mut 
        update_mech_from_dict(self.l5mdl, self.wt_p, self.mut_mech,input_dict = True)

    def update_gfactor(self,gbar_factor = 1):
        update_mod_param(self.l5mdl, self.mut_mech, gbar_factor, gbar_name='gbar')

    def plot_stim(self,stim_amp = 0.3,dt = 0.01,clr = 'black',plot_fn = 'step',axs = None,rec_extra = False):
        self.dt = dt
        if not axs:
            fig,axs = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        self.l5mdl.init_stim(amp=stim_amp)
        if rec_extra:
            Vm, I, t, stim,extra_vms = self.l5mdl.run_model(dt=dt,rec_extra = rec_extra)
            self.extra_vms = extra_vms
        else:
            Vm, I, t, stim = self.l5mdl.run_model(dt=dt)
            
        self.volt_soma = Vm
        self.I = I
        self.t = t
        self.stim = stim
        
        axs.plot(t,Vm, label='Vm', color=clr,linewidth=1)
        axs.locator_params(axis='x', nbins=5)
        axs.locator_params(axis='y', nbins=8)
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}{self.mut_name}_{plot_fn}1.pdf'
        plt.show()
        plt.savefig(file_path_to_save, format='pdf', dpi=my_dpi, bbox_inches="tight")
        return axs

    def plot_currents(self,stim_amp = 0.3,dt = 0.01,clr = 'black',plot_fn = 'step',axs = None):
        if not axs:
            fig,axs = plt.subplots(4,figsize=(cm_to_in(8),cm_to_in(30)))
        self.l5mdl.init_stim(amp=stim_amp)
        Vm, I, t, stim = self.l5mdl.run_model(dt=dt)
        axs[0].plot(t,Vm, label='Vm', color=clr,linewidth=1)
        axs[0].locator_params(axis='x', nbins=5)
        axs[0].locator_params(axis='y', nbins=8)
        
        axs[1].plot(t,I['Na'],label = 'Na',color = 'red')
        axs[2].plot(t,I['K'],label = 'K',color = 'black')
        axs[3].plot(t,I['Ca'],label = 'Ca',color = 'green')
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}{self.mut_name}_{plot_fn}.pdf'
        plt.savefig(file_path_to_save+'.pdf', format='pdf', dpi=my_dpi, bbox_inches="tight")
        return axs


        
    def plot_fi_curve(self,start,end,nruns,wt_data = None,ax1 = None, fig = None,fn = 'ficurve'):
        fis = get_fi_curve(self.l5mdl,start,end,nruns,dt = 0.1,wt_data = wt_data,ax1=ax1,fig=fig,fn=f'{self.plot_folder}{fn}.pdf')
        return fis
    
    def plot_wt_mut_vs(self,stim_amp = 0.3):
        self.make_wt()
        axs = self.plot_stim()
        self.make_het()
        axs = self.plot_stim(clr = 'red',axs = axs)
    
    def plot_wt_mut_fi(self,st_fi = 0,end_fi = 1,n_fi = 11):
        fis = []
        x_axis = np.linspace(st_fi,end_fi,n_fi)
        self.make_wt()
        wt_fis = self.plot_fi_curve(st_fi,end_fi,n_fi)
        fis.append([x_axis,wt_fis,'WT'])
        self.make_het()
        mut_fis = self.plot_fi_curve(st_fi,end_fi,n_fi)
        fis.append([x_axis,mut_fis,self.mut_name])
        return fis

    def plot_volts_dvdt(self,stim_amp = 0.3):
        fig_volts,axs_volts = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        fig_dvdt,axs_dvdt = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        self.make_wt()
        self.plot_stim(axs = axs_volts,dt=0.005)
        plot_dvdt_from_volts(self.volt_soma,self.dt,axs_dvdt)
        self.make_het()
        self.plot_stim(clr = 'red',axs = axs_volts,dt=0.005)
        file_path_to_save=f'{self.plot_folder}{self.mut_name}_step_{stim_amp}.pdf'
        fig_volts.savefig(file_path_to_save, format='pdf', dpi=my_dpi)
        plot_dvdt_from_volts(self.volt_soma,self.dt,axs = axs_dvdt,clr = 'red')
        file_path_to_save=f'{self.plot_folder}{self.mut_name}_volts_dvdt_{stim_amp}.pdf'
        fig_dvdt.savefig(file_path_to_save, format='pdf', dpi=my_dpi)


    

    
    

sim = NaMut()
sim.plot_volts_dvdt()

    

"""
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
"""
