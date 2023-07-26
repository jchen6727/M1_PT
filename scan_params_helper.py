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
    for i in np.arange(0.1,0.5,5):

        

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
            sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],wt_fi = wt_fi,fnpre=f'{fnpre}mutX{mut_fac}_')
        else:
            sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],fnpre=f'{fnpre}mutX{mut_fac}_')
    else:
        sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],fnpre=f'{fnpre}_{mut_fac}_')
def mut_ttx(g_factor,fnpre = 'mut_TTX',axon_KP = 1):
    sim = Na1612Model(KP=axon_KP)
    sim.make_mut(['na16mut'],'na16_G1625R.txt')
    update_mod_param(sim.l5mdl,['na16'],0)
    update_mod_param(sim.l5mdl,['na16mut'],g_factor)
    sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],fnpre=f'{fnpre}{g_factor*100}_')
def plot_het(fnpre = 'het_wtX1_mutX1_',axon_KP = 1):
    sim = Na1612Model(KP=axon_KP)
    sim.make_mut(['na16mut'],'na16_G1625R.txt')
    sim.plot_model_FI_Vs_dvdt([0.3,0.5,1,1.5,2,2.5,3],fnpre=f'{fnpre}')
    #sim.plot_model_FI_Vs_dvdt([0.4,0.5],fnpre=f'{fnpre}',start = 0.45, end = 0.55,nruns= 3)

