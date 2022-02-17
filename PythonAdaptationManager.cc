/*******************************************************************************
 * Simulator of Web Infrastructure and Management
 * Copyright (c) 2016 Carnegie Mellon University.
 * All Rights Reserved.
 *  
 * THIS SOFTWARE IS PROVIDED "AS IS," WITH NO WARRANTIES WHATSOEVER. CARNEGIE
 * MELLON UNIVERSITY EXPRESSLY DISCLAIMS TO THE FULLEST EXTENT PERMITTED BY LAW
 * ALL EXPRESS, IMPLIED, AND STATUTORY WARRANTIES, INCLUDING, WITHOUT
 * LIMITATION, THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE, AND NON-INFRINGEMENT OF PROPRIETARY RIGHTS.
 *  
 * Released under a BSD license, please see license.txt for full terms.
 * DM-0003883
 *******************************************************************************/

#include "PythonAdaptationManager.h"
#include "managers/adaptation/UtilityScorer.h"
#include "managers/execution/AllTactics.h"
#include <Python.h>
#include <fstream>
#include <iostream>
#include <string>
using namespace std;
using namespace omnetpp;


#define BANDIT_ALG omnetpp::getSimulation()->getSystemModule()->par("banditAlgorithmName").stringValue()
#define BANDIT_FORM omnetpp::getSimulation()->getSystemModule()->par("banditFormulaType").stringValue()
#define SLIDING_W omnetpp::getSimulation()->getSystemModule()->par("slidingWindowSize").stringValue()


Define_Module(PythonAdaptationManager);


double PythonAdaptationManager::SEAMS2022Utility(double arrival_rate, double dimmer, double avg_response_time, double max_servers, double servers)
{
    double OPT_REVENUE = 1.5;
    double BASIC_REVENUE = 1;
    double SERVER_COST = 10;
    double RT_THRESH = 0.75;

    double ur = arrival_rate * ((1 - dimmer) * BASIC_REVENUE + dimmer * OPT_REVENUE);
    double uc = SERVER_COST * (max_servers - servers);

    double UPPER_RT_THRESHOLD = RT_THRESH * 4;

    double delta_threshold = UPPER_RT_THRESHOLD-RT_THRESH;

    double UrtPosFct = (delta_threshold/RT_THRESH);

    double urt = 0;
    if(avg_response_time <= UPPER_RT_THRESHOLD){
        urt = ((RT_THRESH - avg_response_time)/RT_THRESH);
    }
    else{
        urt = ((RT_THRESH - UPPER_RT_THRESHOLD)/RT_THRESH);
    }

    double urt_final = 0;
    if(avg_response_time <= RT_THRESH) {
        urt_final = urt*UrtPosFct;}
    else{
        urt_final = urt;}

    double revenue_weight = 0.7;
    double server_weight = 0.3;
    double utility = urt_final*((revenue_weight*ur)+(server_weight*uc));

    return utility;
}


/**
 * Embedded Python adaptation
 *
 */
Tactic* PythonAdaptationManager::evaluate() {
    MacroTactic* pMacroTactic = new MacroTactic;
    Model* pModel = getModel();
    const double dimmerStep = 1.0 / (pModel->getNumberOfDimmerLevels() - 1);
    double dimmer = pModel->getDimmerFactor();
    double spareUtilization =  pModel->getConfiguration().getActiveServers() - pModel->getObservations().utilization;
    bool isServerBooting = pModel->getServers() > pModel->getActiveServers();
    bool isServerRemoving = pModel->getServers() < pModel->getActiveServers();
    double responseTime = pModel->getObservations().avgResponseTime;
    double totalUtilization = pModel->getObservations().utilization; //I think this is correct
    double activeServers = pModel->getConfiguration().getActiveServers();
    double servers = pModel->getServers();
    double maxServers = pModel->getMaxServers();
    double arrivalRate = (pModel->getEnvironment().getArrivalMean() > 0) ? (1 / pModel->getEnvironment().getArrivalMean()) : 0.0;
    PyObject *pModule, *pModule2, *pFunc, *pFunc2;
    PyObject *pArgs, *pArgs2, *pValue, *pElement, *pInstance;


    //double utility = PythonAdaptationManager::SEAMS2022Utility(arrivalRate, dimmer, responseTime, maxServers, servers);


    if(!isServerBooting && !isServerRemoving){
        Py_Initialize();

        std::string alg(BANDIT_ALG);
        std::string runner_name = "some_bandits.SWIMInternalInterface"; //+ alg;
        std::string module_name = "some_bandits." + alg;
        std::string class_name = alg + "C";

        pModule = PyImport_ImportModule(module_name.c_str());// ucb");
        if(pModule != NULL){

            pFunc = PyObject_GetAttrString(pModule, class_name.c_str());

            if(pFunc && PyCallable_Check(pFunc)) {


                //pInstance = PyObject_CallObject(pFunc, nullptr);

                pModule2 = PyImport_ImportModule(runner_name.c_str());// ucb")

                pFunc2 = PyObject_GetAttrString(pModule2, "start");

                if(pFunc2 && PyCallable_Check(pFunc2)) {

                    pArgs = PyTuple_New(9);

                    double foo [] = {dimmer, responseTime, activeServers, servers, maxServers, totalUtilization, arrivalRate};
                    PyTuple_SetItem(pArgs, 0, PyUnicode_FromString(BANDIT_ALG));

                    for(int i = 1; i < 8; i++){
                        pValue = PyFloat_FromDouble(foo[i-1]);
                        PyTuple_SetItem(pArgs, i, pValue);
                    }

                    PyTuple_SetItem(pArgs, 8, PyUnicode_FromString(BANDIT_FORM));

                    pValue = PyObject_CallObject(pFunc2, pArgs);



                    if(pValue != NULL) {
                        int py_list_size = PyList_Size(pValue);

                        for(Py_ssize_t i = 0; i < py_list_size; i++)
                        {
                        pElement = PyList_GetItem(pValue, i);
                        std::string tactic_element = PyUnicode_AsUTF8(pElement);
                        //std::cout << "The tactic " << tactic_element << " was added\n";

                        switch (tactic_element[0]) {
                           case 'r': pMacroTactic->addTactic(new RemoveServerTactic); break;
                           case 'a':  pMacroTactic->addTactic(new AddServerTactic); break;
                           case 's':
                           char * cstr = new char [tactic_element.length()+1];
                           strcpy (cstr, tactic_element.c_str());
                           char * parts = strtok(cstr, " ");
                           double dimmer_value = atof(strtok(NULL, " "));
                           pMacroTactic->addTactic(new SetDimmerTactic(dimmer_value));
                           }
                        }

                    }
                    else {
                           Py_DECREF(pFunc);
                           Py_DECREF(pModule);
                           PyErr_Print();
                           fprintf(stderr, "Method call failed\n");}
                                    }

                    return pMacroTactic;

                }

        }
        else{
            PyErr_Print();
            fprintf(stderr, "something failed2\n");
        }
    //Py_Finalize();

        //pMacroTactic->addTactic(new SetDimmerTactic(0.75));
    }
    return pMacroTactic;

}
