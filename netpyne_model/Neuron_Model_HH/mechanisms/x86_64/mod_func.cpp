#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _branching_reg(void);
extern void _CaDynamics_E2_reg(void);
extern void _Ca_HVA_reg(void);
extern void _Ca_LVAst_reg(void);
extern void _Ih_reg(void);
extern void _Im_reg(void);
extern void _K_Pst_reg(void);
extern void _K_Tst_reg(void);
extern void _na12_reg(void);
extern void _na12_mut_reg(void);
extern void _na16_reg(void);
extern void _na16_mut_reg(void);
extern void _ProbAMPANMDA_EMS_reg(void);
extern void _ProbGABAAB_EMS_reg(void);
extern void _SK_E2_reg(void);
extern void _SKv3_1_reg(void);
extern void _vclmp_pl_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"branching.mod\"");
    fprintf(stderr, " \"CaDynamics_E2.mod\"");
    fprintf(stderr, " \"Ca_HVA.mod\"");
    fprintf(stderr, " \"Ca_LVAst.mod\"");
    fprintf(stderr, " \"Ih.mod\"");
    fprintf(stderr, " \"Im.mod\"");
    fprintf(stderr, " \"K_Pst.mod\"");
    fprintf(stderr, " \"K_Tst.mod\"");
    fprintf(stderr, " \"na12.mod\"");
    fprintf(stderr, " \"na12_mut.mod\"");
    fprintf(stderr, " \"na16.mod\"");
    fprintf(stderr, " \"na16_mut.mod\"");
    fprintf(stderr, " \"ProbAMPANMDA_EMS.mod\"");
    fprintf(stderr, " \"ProbGABAAB_EMS.mod\"");
    fprintf(stderr, " \"SK_E2.mod\"");
    fprintf(stderr, " \"SKv3_1.mod\"");
    fprintf(stderr, " \"vclmp_pl.mod\"");
    fprintf(stderr, "\n");
  }
  _branching_reg();
  _CaDynamics_E2_reg();
  _Ca_HVA_reg();
  _Ca_LVAst_reg();
  _Ih_reg();
  _Im_reg();
  _K_Pst_reg();
  _K_Tst_reg();
  _na12_reg();
  _na12_mut_reg();
  _na16_reg();
  _na16_mut_reg();
  _ProbAMPANMDA_EMS_reg();
  _ProbGABAAB_EMS_reg();
  _SK_E2_reg();
  _SKv3_1_reg();
  _vclmp_pl_reg();
}

#if defined(__cplusplus)
}
#endif
