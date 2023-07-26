from NeuronModelClass import NeuronModel
from NrnHelper import *
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import csv
import numpy as np
from currentscape.currentscape import plot_currentscape

class Na1612Model:
    #def __init__(self,na12name = 'na12_orig1', na12mechs = ['na12','na12mut'],na16name = 'na16_orig2', na16mechs = ['na16','na16mut'], params_folder = './params/',nav12=1,nav16=1,K=1,KT=1,KP=1,somaK=1,ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,plots_folder = f'./Plots/'):
    def __init__(self,na12name = 'na12_orig1', na12mechs = ['na12','na12mut'],na16name = 'na16_orig2', na16mechs = ['na16','na16mut'], params_folder = './params/',nav12=1,nav16=1,K=1,KT=1,KP=1,somaK=1,ais_ca = 1,ais_Kca = 1,soma_na16=1,soma_na12 = 1,node_na = 1,plots_folder = f'./Plots/'):
        ais_Kca = 0.5
        #K = 0.6
        #update_param_value(self.l5mdl,['SKv3_1'],'vtau',25)
        #ais_ca = 2
        #soma_na16 = 0.7
        #soma_na12 = 0.7
        nav12 = 4.5
        nav16 = 1.1 * nav16 #the wt should be 1.1 and then add to that what we get from the input
        #KP = 0.1
        #somaK = 2
        #KP=3
        #K=3
        #KT = 0.5
        #nav12 = 1.2
        #nav16 = 1.2



        nav12 = 3.5
        nav16 = 1.2
        ais_Kca = 0.03*ais_Kca
        ais_ca = 0.04*ais_ca
        KP = 1*KP
        somaK = somaK
        KP=1.1*KP
        K = 4.8*K
        KT = 0.025*0.5*KT
        """
        ais_Kca = 0.03*ais_Kca
        #K = 0.6
        #update_param_value(self.l5mdl,['SKv3_1'],'vtau',25)
        ais_ca = 0.04*ais_ca
        #soma_na16 = 0.7
        #soma_na12 = 0.7
        nav12 = 1.8 *nav12
        nav16 = 1.8 *nav16#the wt should be 1.1 and then add to that what we get from the input
        KP = 1.2*KP
        somaK = 0.5 * somaK
        KP=0.95*KP
        K = 4.8*K
        KT = 0.025*0.5*KT
        """
        self.l5mdl = NeuronModel(nav12=nav12, nav16=nav16,axon_K = K,axon_Kp = KP,axon_Kt = KT,soma_K = somaK,ais_ca = ais_ca,ais_KCa=ais_Kca,soma_nav16=soma_na16,soma_nav12 = soma_na12,node_na = node_na)
        #update_param_value(self.l5mdl,['SKv3_1'],'mtaumul',6)
        
        update_param_value(self.l5mdl,['SKv3_1'],'vtau',25)
        self.params_folder = params_folder
        self.na12mechs = na12mechs
        self.na16mechs = na16mechs
        self.plot_folder = plots_folder 
        self.plot_folder = f'{plots_folder}/Na16G1625R/v2_full/'
        Path(self.plot_folder).mkdir(parents=True, exist_ok=True)
        """
        print(f'using na12_file {na12name}')
        p_fn_na12 = f'{params_folder}{na12name}.txt'
        self.na12_p = update_mech_from_dict(self.l5mdl, p_fn_na12, self.na12mechs) 
        """
        print(f'using na16_file {na16name}')
        p_fn_na16 = f'{params_folder}{na16name}.txt'
        self.na16_p = update_mech_from_dict(self.l5mdl, p_fn_na16, self.na16mechs) 
        
    def make_mut(self,mut_mech,mut_params_fn):
        print(f'updating mut {mut_mech} with {mut_params_fn}')
        self.na16_p_mut = update_mech_from_dict(self.l5mdl, self.params_folder + mut_params_fn, mut_mech) 

    def update_gfactor(self,gbar_factor = 1):
        update_mod_param(self.l5mdl, self.mut_mech, gbar_factor, gbar_name='gbar')

    def plot_stim(self,stim_amp = 0.5,dt = 0.02,clr = 'black',plot_fn = 'step',axs = None,rec_extra = False):
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
        #plt.show()
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}{plot_fn}.pdf'
        plt.savefig(file_path_to_save, format='pdf')
        return axs

    def plot_currents(self,stim_amp = 0.5,dt = 0.01,clr = 'black',plot_fn = 'step',axs = None):
        if not axs:
            fig,axs = plt.subplots(4,figsize=(cm_to_in(8),cm_to_in(30)))
        self.l5mdl.init_stim(amp=stim_amp,sweep_len = 200)
        Vm, I, t, stim = self.l5mdl.run_model(dt=dt)
        axs[0].plot(t,Vm, label='Vm', color=clr,linewidth=1)
        axs[0].locator_params(axis='x', nbins=5)
        axs[0].locator_params(axis='y', nbins=8)
        
        axs[1].plot(t,I['Na'],label = 'Na',color = 'red')
        axs[2].plot(t,I['K'],label = 'K',color = 'black')
        axs[3].plot(t,I['Ca'],label = 'Ca',color = 'green')
        #add_scalebar(axs)
        file_path_to_save=f'{self.plot_folder}Ktrials2_{plot_fn}.pdf'
        plt.savefig(file_path_to_save+'.pdf', format='pdf', dpi=my_dpi)
        return axs
    def get_axonal_ks(self, start_Vm = -72, dt= 0.1,rec_extra = False):
        h.dt=dt
        self.dt = dt
        h.finitialize(start_Vm)
        timesteps = int(h.tstop/h.dt)

        Vm = np.zeros(timesteps)
        I = {}
        I['Na'] = np.zeros(timesteps)
        I['K'] = np.zeros(timesteps)
        I['K31'] = np.zeros(timesteps)
        I['KT'] = np.zeros(timesteps)
        I['KCa'] = np.zeros(timesteps)
        I['KP'] = np.zeros(timesteps)
        stim = np.zeros(timesteps)
        t = np.zeros(timesteps)

        for i in range(timesteps):
            Vm[i] = h.cell.soma[0].v
            I['Na'][i] = self.l5mdl.ais(0.5).ina
            I['K'][i] = self.l5mdl.ais(0.5).ik
            I['K31'][i] = self.l5mdl.ais.gSKv3_1_SKv3_1
            I['KP'][i] = self.l5mdl.ais.gK_Pst_K_Pst
            I['KT'][i] = self.l5mdl.ais.gK_Tst_K_Tst
            I['KCa'][i] = self.l5mdl.ais.gSK_E2_SK_E2
            t[i] = i*h.dt / 1000
            stim[i] = h.st.amp
            h.fadvance()
        return Vm, I, t, stim


    def plot_axonal_ks(self,stim_amp = 0.5,dt = 0.01,clr = 'black',plot_fn = 'step_axon_ks',axs = None):
        if not axs:
            fig,axs = plt.subplots(7,2,figsize=(cm_to_in(16),cm_to_in(70)))
        self.l5mdl.init_stim(amp=stim_amp,sweep_len = 500)
        Vm, I, t, stim = self.get_axonal_ks(dt=dt)
        axs[0][0].plot(t,Vm, label='Vm', color=clr,linewidth=1)
        plot_dvdt_from_volts(Vm,self.dt,axs[0][1])
        axs[0][0].locator_params(axis='x', nbins=5)
        axs[0][0].locator_params(axis='y', nbins=8)
        
        axs[1][0].plot(t,I['Na'],label = 'Na',color = 'red')
        axs[1][0].legend()
        plot_dg_dt(I['Na'],Vm,self.dt,axs[1][1])
        axs[2][0].plot(t,I['K'],label = 'K',color = 'black')
        plot_dg_dt(I['K'],Vm,self.dt,axs[2][1])
        axs[2][0].legend()
        axs[3][0].plot(t,I['K31'],label = 'K31',color = 'green')
        plot_dg_dt(I['K31'],Vm,self.dt,axs[3][1])
        axs[3][0].legend()
        axs[4][0].plot(t,I['KP'],label = 'KP',color = 'orange')
        plot_dg_dt(I['KP'],Vm,self.dt,axs[4][1])
        axs[4][0].legend()
        axs[5][0].plot(t,I['KT'],label = 'KT',color = 'yellow')
        plot_dg_dt(I['KT'],Vm,self.dt,axs[5][1])
        axs[5][0].legend()
        axs[6][0].plot(t,I['KCa'],label = 'KCa',color = 'grey')
        plot_dg_dt(I['KCa'],Vm,self.dt,axs[6][1])
        axs[6][0].legend()
        



        #add_scalebar(axs)
        file_path_to_save=plot_fn
        plt.savefig(file_path_to_save, format='pdf', dpi=my_dpi)
        return axs
        
    def plot_fi_curve(self,start=0,end=1,nruns=11,wt_data = None,ax1 = None, fig = None,fn = 'ficurve'):
        fis = get_fi_curve(self.l5mdl,start,end,nruns,dt = 0.01,wt_data = wt_data,ax1=ax1,fig=fig,fn=f'{self.plot_folder}{fn}.pdf')
        return fis
    

    def plot_volts_dvdt(self,stim_amp = 0.5):
        fig_volts,axs_volts = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        fig_dvdt,axs_dvdt = plt.subplots(1,figsize=(cm_to_in(8),cm_to_in(7.8)))
        self.plot_stim(axs = axs_volts,dt=0.02)
        plot_dvdt_from_volts(self.volt_soma,self.dt,axs_dvdt)
        file_path_to_save=f'{self.plot_folder}AnnaModel_volts_dvdt_{stim_amp}.pdf'
        fig_dvdt.savefig(file_path_to_save, format='pdf', dpi=my_dpi)
        file_path_to_save=f'{self.plot_folder}AnnaModel_volts_{stim_amp}.pdf'
        fig_volts.savefig(file_path_to_save, format='pdf', dpi=my_dpi)


    def get_ap_init_site(self):
        self.plot_stim(stim_amp = 0.7,rec_extra=True)
        soma_spikes = get_spike_times(self.volt_soma,self.t)
        axon_spikes = get_spike_times(self.extra_vms['axon'],self.t)
        ais_spikes = get_spike_times(self.extra_vms['ais'],self.t)
        for i in range(len(soma_spikes)):
            print(f'spike #{i} soma - {soma_spikes[i]}, ais - {ais_spikes[i]}, axon - {axon_spikes[i]}')
    
    
    def plot_model_FI_Vs_dvdt(self,vs_amp,fnpre = '',wt_fi = None, start=0,end=2,nruns=21):
        #wt_fi = [0, 0, 0, 0, 3, 5, 7, 9, 10, 12, 13]
        for curr_amp in vs_amp:
            fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(3),cm_to_in(3.5)))
            axs[0] = self.plot_stim(axs = axs[0],stim_amp = curr_amp,dt=0.005)
            #axs[0] = self.plot_stim(axs = axs[0],stim_amp = curr_amp,dt=0.05)
            axs[1] = plot_dvdt_from_volts(self.volt_soma,self.dt,axs[1])
            add_scalebar(axs[0])
            add_scalebar(axs[1])
            fn = f'{self.plot_folder}/{fnpre}dvdt_vs_{curr_amp}.pdf'
            fig_volts.savefig(fn)
            csv_volts = f'{self.plot_folder}/{fnpre}vs_{curr_amp}.csv'
            with open(csv_volts, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Voltage'])  # Write header row
                writer.writerows(zip(self.volt_soma))
        fi_ans = self.plot_fi_curve(start,end,nruns,wt_data = wt_fi,fn = fnpre + '_fi')
        with open(f'{self.plot_folder}/{fnpre}.csv', 'w+', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(fi_ans)
        return fi_ans

        
def scan_sec_na():
    for fac in np.arange(0.1,1,0.1):
        sim = Na1612Model(soma_na16=fac,soma_na12=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Na16_{fac}_Na12_{fac}.pdf'
        fig_volts.savefig(fn)
        """
        sim = Na1612Model(soma_na12=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Na12_{fac}.pdf'
        fig_volts.savefig(fn)

        sim = Na1612Model(node_na=fac)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/node_na_{fac}.pdf'
        fig_volts.savefig(fn)
        """
def scan12_16():
    for i12 in np.arange(2,0.4,-0.5):
        for i16 in np.arange(2,0.4,-0.5):
            sim = Na1612Model(nav12=i12, nav16=i16)
            #sim.make_wt()
            fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(8),cm_to_in(15)))
            sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
            plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
            fn = f'{sim.plot_folder}/vs_dvdt12_{i12}_16_{i16}.pdf'
            fig_volts.savefig(fn)

def scanK():
    for i in np.arange(0.1,5,0.5):

        

        sim = Na1612Model(ais_ca=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/ais_CA_{i}_.pdf'
        fig_volts.savefig(fn)
        
        sim = Na1612Model(ais_Kca=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/ais_Kca_{i}_.pdf'
        fig_volts.savefig(fn)
        """
        sim = Na1612Model(K=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/K_{i}_.pdf'
        fig_volts.savefig(fn)
        
        sim = Na1612Model(somaK=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/somaK_{i}_.pdf'
        fig_volts.savefig(fn)


        sim = Na1612Model(KP=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Kp_{i}_.pdf'
        fig_volts.savefig(fn)


        
        """
        sim = Na1612Model(KT=i)
        #sim.make_wt()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(10),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/Kt_{i}_.pdf'
        fig_volts.savefig(fn)





def scanKv31():
    
    vtau_orig = 18.700
    vinf_orig = -46.560
    for i in np.arange(0,21,5):
        sim = Na1612Model()
        update_param_value(sim.l5mdl,['SKv3_1'],'vtau',vtau_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kv31_shift_vtau_{i}_.pdf'
        fig_volts.savefig(fn)
        update_param_value(sim.l5mdl,['SKv3_1'],'vtau',vtau_orig)

        
        sim = Na1612Model()
        update_param_value(sim.l5mdl,['SKv3_1'],'vinf',vinf_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kv31_shift_vinf_{i}_.pdf'
        fig_volts.savefig(fn)
        update_param_value(sim.l5mdl,['SKv3_1'],'vinf',vinf_orig)
    mtaumul_orig = 4
    for i in np.arange(0.1,1,0.2):
        sim = Na1612Model()
        update_param_value(sim.l5mdl,['SKv3_1'],'mtaumul',mtaumul_orig +i)
        fn = f'{sim.plot_folder}/kv31_shift_mtaumul_{i}_.pdf'
        sim.plot_axonal_ks(plot_fn = fn)
    update_param_value(sim.l5mdl,['SKv3_1'],'mtaumul',mtaumul_orig)
        

def scanKT():
    vshift_orig = -10
    for i in np.arange(10,31,10):
        sim = Na1612Model()
        update_param_value(sim.l5mdl,['K_Tst'],'vshift',vshift_orig+i)
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/kT_vshift_{i}_.pdf'
        fig_volts.savefig(fn)
    update_param_value(sim.l5mdl,['K_Tst'],'vshift',vshift_orig)
def test_params():
    for i in range(1,9):
        na16_name = f'na16WT{i}'
        sim = Na1612Model(na16name = na16_name)
        sim.plot_currents()
        fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
        sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
        plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
        fn = f'{sim.plot_folder}/default_na16_{i}.pdf'
        fig_volts.savefig(fn)
def default_model():
    sim = Na1612Model()
    sim.plot_currents()
    fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
    sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
    plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
    fn = f'{sim.plot_folder}/default_na12HMM.pdf'
    fig_volts.savefig(fn)

def plot_mutant():
    sim = Na1612Model()
    sim.make_mut('na16mut','na16_G1625R.txt')
    sim.plot_currents()
    fig_volts,axs = plt.subplots(2,figsize=(cm_to_in(9.5),cm_to_in(15)))
    sim.plot_stim(axs = axs[0],stim_amp = 0.7,dt=0.005)
    plot_dvdt_from_volts(sim.volt_soma,sim.dt,axs[1])
    fn = f'{sim.plot_folder}/na16_G1625R.pdf'
    fig_volts.savefig(fn)

def overexp(wt_fac = 1,mut_fac = None,plot_wt=True,fnpre = '',axon_KP = 1):
    sim = Na1612Model(nav16 = wt_fac,KP=axon_KP)
    if plot_wt:
        wt_fi = sim.plot_model_FI_Vs_dvdt([0.8,0.85,0.9,0.95],fnpre=f'{fnpre}_FI_')
        #wt_fi = sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],fnpre=f'{fnpre}_FI_')
    else:
        wt_fi = []
    print(f'wt_fi is {wt_fi}')
    if mut_fac:
        sim.make_mut(['na16mut'],'na16_G1625R.txt')
        update_mod_param(sim.l5mdl,['na16mut'],mut_fac)
        sim.l5mdl.h.finitialize()
        if plot_wt:
            sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],wt_fi = wt_fi,fnpre=f'{fnpre}mutX{mut_fac}_')
        else:
            sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],fnpre=f'{fnpre}mutX{mut_fac}_')
    else:
        sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],fnpre=f'{fnpre}_{mut_fac}_')
def mut_ttx(g_factor,fnpre = 'mut_TTX',axon_KP = 1):
    sim = Na1612Model(KP=axon_KP)
    sim.make_mut(['na16mut'],'na16_G1625R.txt')
    update_mod_param(sim.l5mdl,['na16'],0)
    update_mod_param(sim.l5mdl,['na16mut'],g_factor)
    sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2],fnpre=f'{fnpre}{g_factor*100}_')
def plot_het(fnpre = 'het_wtX1_mutX1_',axon_KP = 1):
    sim = Na1612Model(KP=axon_KP)
    sim.make_mut(['na16mut'],'na16_G1625R.txt')
    sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],fnpre=f'{fnpre}')
    #sim.plot_model_FI_Vs_dvdt([0.4,0.5],fnpre=f'{fnpre}',start = 0.45, end = 0.55,nruns= 3)


def make_currentscape_plot(sim_config = {
                'section' : 'soma',
                'segment' : 0.5,
                'section_num': 0,
                'currents'  : ['na12.ina_ina','na12mut.ina_ina','na16.ina_ina','na16mut.ina_ina','ica_Ca_HVA','ica_Ca_LVAst','ihcn_Ih','ik_SK_E2','ik_SKv3_1'],
                'ionic_concentrations' :["cai", "ki", "nai"]
                
            }):
    sim_obj = NeuronModel()   #TO DO : send in different parameters???
    sim_obj.init_stim(amp=0.5,sweep_len = 200)
    Vm, I, t, stim,ionic = sim_obj.run_sim_model(dt=0.01,sim_config=sim_config)
    current_names = sim_config['currents']
    plot_config = {
        "output": {
            "savefig": True,
            "dir": "./Plots/Currentscape/",
            "fname": "test_plot",
            "extension": "pdf",
            "dpi": 600,
            "transparent": False
        },
        "current": {"names": current_names},
        "ions":{"names": ["ca", "k", "na"]},
        "voltage": {"ylim": [-90, 50]},
        "legendtextsize": 5,
        "adjust": {
            "left": 0.15,
            "right": 0.8,
            "top": 1.0,
            "bottom": 0.0
            }
        }
    fig = plot_currentscape(Vm, [I[x] for x in I.keys()], plot_config,[ionic[x] for x in ionic.keys()])

"""   
1. TTX_10.0_axonKP_0.7
2. TTX_10.0_axonKP_0.8
3.TTX_2.0_axonKP_0.5 (3rd best)
4.TTX_5.0_axonKP_0.75 (2nd best) 
5. TTX_5.0_axonKP_0.7(best)

i=0.05
j=0.7
overexp(wt_fac = i,fnpre=f'Task_3/WT_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
mut_ttx(i,fnpre=f'Task_4/mut_TTX_{i*100}_axonKP_{j}_',axon_KP = j)

i=0.1
j=0.7
overexp(wt_fac = i,fnpre=f'Task_3/WT_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
mut_ttx(i,fnpre=f'Task_4/mut_TTX_{i*100}_axonKP_{j}_',axon_KP = j)

i=0.1
j=0.8
overexp(wt_fac = i,fnpre=f'Task_3/WT_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
mut_ttx(i,fnpre=f'Task_4/mut_TTX_{i*100}_axonKP_{j}_',axon_KP = j)

i=0.02
j=0.5
overexp(wt_fac = i,fnpre=f'Task_3/WT_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
mut_ttx(i,fnpre=f'Task_4/mut_TTX_{i*100}_axonKP_{j}_',axon_KP = j)

i=0.05
j=0.75
overexp(wt_fac = i,fnpre=f'Task_3/WT_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
mut_ttx(i,fnpre=f'Task_4/mut_TTX_{i*100}_axonKP_{j}_',axon_KP = j)

i=0.05
j=0.7
overexp(wt_fac = i,fnpre=f'Task_3/WT_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
mut_ttx(i,fnpre=f'Task_4/mut_TTX_{i*100}_axonKP_{j}_',axon_KP = j)

sim_config = {
                'section' : 'soma',
                'segment' : 0.5,
                'inward'  : ['ina','ica'],
                'outward' : ['ik']
            }
make_currentscape_plot(sim_config)
"""

#default_model()

#plot_mutant()
#i = 1.2
#for j in [0.7,0.9,1,1.1]:
for j in [1]:
#for j in [0.75]:
    #for i in [0.05,0.1,0.15,0.2]:
    for i in [0.05]:
        overexp(wt_fac = 1+i,fnpre=f'Task_1/WT_200plus_{i*100}_axonKP_{j}_',axon_KP = j)   
        overexp(wt_fac = 2,mut_fac = i,plot_wt = False,fnpre=f'Task_2/WT_200_mut_{i*100}_axonKP_{j}_',axon_KP = j)
        overexp(wt_fac = i,fnpre=f'Task_3/WT_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
        mut_ttx(i,fnpre=f'Task_4/mut_TTX_{i*100}_axonKP_{j}_',axon_KP = j)
    plot_het(fnpre = f'Task_5/100_wt_100_mut_axonKP_{j}_',axon_KP = j)
#print(np.linspace(0.45,0.55,3))
#python3 Na16HMM_Tau.py
