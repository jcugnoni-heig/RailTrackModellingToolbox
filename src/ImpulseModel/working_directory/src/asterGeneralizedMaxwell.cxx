/*!
* \file   src/asterGeneralizedMaxwell.cxx
* \brief  This file implements the aster interface for the GeneralizedMaxwell behaviour law
* \author BenoÃ®t Bary
* \date   8 / 10 / 2014
*/

#include<iostream>
#include<stdexcept>
#include"TFEL/Material/OutOfBoundsPolicy.hxx"
#include"TFEL/Material/GeneralizedMaxwell.hxx"
#include"MFront/Aster/AsterStressFreeExpansionHandler.hxx"

#include"MFront/Aster/AsterInterface.hxx"

#include"MFront/Aster/asterGeneralizedMaxwell.hxx"

static tfel::material::OutOfBoundsPolicy&
astergeneralizedmaxwell_getOutOfBoundsPolicy(){
using namespace tfel::material;
static OutOfBoundsPolicy policy = None;
return policy;
}

extern "C"{

MFRONT_SHAREDOBJ const char* 
astergeneralizedmaxwell_mfront_ept = "astergeneralizedmaxwell";

MFRONT_SHAREDOBJ const char* 
astergeneralizedmaxwell_tfel_version = "3.2.1";

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_mfront_mkt = 1u;

MFRONT_SHAREDOBJ const char *
astergeneralizedmaxwell_mfront_interface = "Aster";

MFRONT_SHAREDOBJ const char *
astergeneralizedmaxwell_src = "GeneralizedMaxwell.mfront";

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nModellingHypotheses = 4u;

MFRONT_SHAREDOBJ const char * 
astergeneralizedmaxwell_ModellingHypotheses[4u] = {"Axisymmetrical",
"PlaneStrain",
"GeneralisedPlaneStrain",
"Tridimensional"};

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nMainVariables = 1;
MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nGradients = 1;

MFRONT_SHAREDOBJ int astergeneralizedmaxwell_GradientsTypes[1] = {1};
MFRONT_SHAREDOBJ const char * astergeneralizedmaxwell_Gradients[1] = {"Strain"};
MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nThermodynamicForces = 1;

MFRONT_SHAREDOBJ int astergeneralizedmaxwell_ThermodynamicForcesTypes[1] = {1};
MFRONT_SHAREDOBJ const char * astergeneralizedmaxwell_ThermodynamicForces[1] = {"Stress"};
MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_BehaviourType = 1u;

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_BehaviourKinematic = 0u;

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_SymmetryType = 0u;

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_ElasticSymmetryType = 0u;

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_savesTangentOperator = 0;
MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_UsableInPurelyImplicitResolution = 1;

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nMaterialProperties = 11u;

MFRONT_SHAREDOBJ const char *astergeneralizedmaxwell_MaterialProperties[11u] = {"BulkModulus",
"ShearModulus",
"ViscoelasticBulkModulus[0]",
"ViscoelasticBulkModulus[1]",
"ViscoelasticBulkModulus[2]",
"ViscoelasticShearModulus[0]",
"ViscoelasticShearModulus[1]",
"ViscoelasticShearModulus[2]",
"TimeScale[0]",
"TimeScale[1]",
"TimeScale[2]"};

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nInternalStateVariables = 3;
MFRONT_SHAREDOBJ const char * astergeneralizedmaxwell_InternalStateVariables[3] = {"ViscoelasticStress[0]",
"ViscoelasticStress[1]","ViscoelasticStress[2]"};
MFRONT_SHAREDOBJ int astergeneralizedmaxwell_InternalStateVariablesTypes [] = {1,1,1};

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nExternalStateVariables = 0;
MFRONT_SHAREDOBJ const char * const * astergeneralizedmaxwell_ExternalStateVariables = nullptr;

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_nParameters = 2;
MFRONT_SHAREDOBJ const char * astergeneralizedmaxwell_Parameters[2] = {"minimal_time_step_scaling_factor",
"maximal_time_step_scaling_factor"};
MFRONT_SHAREDOBJ int astergeneralizedmaxwell_ParametersTypes [] = {0,0};

MFRONT_SHAREDOBJ double astergeneralizedmaxwell_minimal_time_step_scaling_factor_ParameterDefaultValue = 0.1;

MFRONT_SHAREDOBJ double astergeneralizedmaxwell_maximal_time_step_scaling_factor_ParameterDefaultValue = 1.79769e+308;

MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_requiresStiffnessTensor = 0;
MFRONT_SHAREDOBJ unsigned short astergeneralizedmaxwell_requiresThermalExpansionCoefficientTensor = 0;
MFRONT_SHAREDOBJ int
astergeneralizedmaxwell_setParameter(const char *const key,const double value){
using tfel::material::GeneralizedMaxwellParametersInitializer;
auto& i = GeneralizedMaxwellParametersInitializer::get();
try{
i.set(key,value);
} catch(std::runtime_error& e){
std::cerr << e.what() << std::endl;
return 0;
}
return 1;
}

MFRONT_SHAREDOBJ void
astergeneralizedmaxwell_setOutOfBoundsPolicy(const int p){
if(p==0){
astergeneralizedmaxwell_getOutOfBoundsPolicy() = tfel::material::None;
} else if(p==1){
astergeneralizedmaxwell_getOutOfBoundsPolicy() = tfel::material::Warning;
} else if(p==2){
astergeneralizedmaxwell_getOutOfBoundsPolicy() = tfel::material::Strict;
} else {
std::cerr << "astergeneralizedmaxwell_setOutOfBoundsPolicy: invalid argument\n";
}
}

char *astergeneralizedmaxwell_getIntegrationErrorMessage(){
#if (defined __GNUC__) && (!defined __clang__) && (!defined __INTEL_COMPILER) && (!defined __PGI)
#if __GNUC__ * 10000+__GNUC_MINOR__ * 100 <  40800
static __thread char msg[128];
#else
static thread_local char msg[128];
#endif
#else /* (defined __GNUC__) ...*/
static thread_local char msg[128];
#endif /* (defined __GNUC__) ...*/
return msg;
} // end of astergeneralizedmaxwell_getIntegrationErrorMessage

MFRONT_SHAREDOBJ void
GeneralizedMaxwell(aster::AsterReal *const STRESS,aster::AsterReal *const STATEV,aster::AsterReal *const DDSOE,const aster::AsterReal *const STRAN,const aster::AsterReal *const DSTRAN,const aster::AsterReal *const DTIME,const aster::AsterReal *const TEMP,const aster::AsterReal *const DTEMP,const aster::AsterReal *const PREDEF,const aster::AsterReal *const DPRED,const aster::AsterInt  *const NTENS,const aster::AsterInt  *const NSTATV,const aster::AsterReal *const PROPS,const aster::AsterInt  *const NPROPS,const aster::AsterReal *const DROT,aster::AsterReal *const PNEWDT,const aster::AsterInt *const NUMMOD)
{
char * msg = astergeneralizedmaxwell_getIntegrationErrorMessage();
if(aster::AsterInterface<tfel::material::GeneralizedMaxwell>::exe(msg,NTENS,DTIME,DROT,DDSOE,STRAN,DSTRAN,TEMP,DTEMP,PROPS,NPROPS,PREDEF,DPRED,STATEV,NSTATV,STRESS,NUMMOD,astergeneralizedmaxwell_getOutOfBoundsPolicy(),aster::AsterStandardSmallStrainStressFreeExpansionHandler)!=0){
*PNEWDT = -1.;
return;
}
}

MFRONT_SHAREDOBJ void
astergeneralizedmaxwell(aster::AsterReal *const STRESS,aster::AsterReal *const STATEV,aster::AsterReal *const DDSOE,const aster::AsterReal *const STRAN,const aster::AsterReal *const DSTRAN,const aster::AsterReal *const DTIME,const aster::AsterReal *const TEMP,const aster::AsterReal *const DTEMP,const aster::AsterReal *const PREDEF,const aster::AsterReal *const DPRED,const aster::AsterInt  *const NTENS,const aster::AsterInt  *const NSTATV,const aster::AsterReal *const PROPS,const aster::AsterInt  *const NPROPS,const aster::AsterReal *const DROT,aster::AsterReal *const PNEWDT,const aster::AsterInt *const NUMMOD)
{
GeneralizedMaxwell(STRESS,STATEV,DDSOE,STRAN,DSTRAN,DTIME,TEMP,DTEMP,
PREDEF,DPRED,NTENS,NSTATV,PROPS,NPROPS,DROT,PNEWDT,NUMMOD);
}

} // end of extern "C"
