def customDiagnosisVariablesWriter(rules):
    #potencijalno dodati variable kao import
    file = None
    if(len(rules)<1):
        return
    if(rules[0].extendsRuleset=="disv"):
        file = open("./diagnostics/custom_variables_d.py",'w')
        file.write("from business_rules.variables import numeric_rule_variable\n\n")
        file.write("from .resoner import DiseaseVariables\n\n")
        file.write("class CustomDiseaseVariables(DiseaseVariables):\n")
    elif(rules[0].extendsRuleset=="patv"):
        file = open("./diagnostics/custom_variables_p.py",'w')
        file.write("from business_rules.variables import numeric_rule_variable,select_multiple_rule_variable\n\n")
        file.write("from .models import Disease\n")
        file.write("from .resoner import PatientVariables,getNamesList\n\n")
        file.write("class CustomPatientVariables(PatientVariables):\n")
    
    for rule in rules:
        parametars = rule.params.split(",")
        if(rule.extendsRuleset=="disv"):
            if(rule.extendedRule=="dv_hdc"):
                file.write("\t@numeric_rule_variable(label='Patient had "+parametars[0]+" diagnosed multiple times in last "+ parametars[1] +" days')\n")
                file.write("\tdef customRuleHDC"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.hadDisease('"+parametars[0]+"',"+parametars[1]+")\n")
            elif(rule.extendedRule=="dv_hsc"):
                file.write("\t@numeric_rule_variable(label='Patient had "+ parametars[0] +" syndrome multiple times in last "+ parametars[1] +" days')\n")
                file.write("\tdef customRuleHSC"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.hadSyndrome('"+parametars[0]+"',"+parametars[1]+")\n")
            elif(rule.extendedRule=="dv_htc"):
                file.write("\t@numeric_rule_variable(label='Patient had high temperature multiple times in last "+ parametars[0] +" days')\n")
                file.write("\tdef customRuleHTC"+parametars[0].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.hadTemperature("+parametars[0]+")\n")
            elif(rule.extendedRule=="dv_tac"):
                file.write("\t@numeric_rule_variable(label='Patient had temperature above "+ parametars[0] +" multiple times in last "+ parametars[1] +" days')\n")
                file.write("\tdef customRuleTAC"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.hadTemperatureAbove("+parametars[0]+","+parametars[1]+")\n")
            elif(rule.extendedRule=="dv_hmc"):
                file.write("\t@numeric_rule_variable(label='Patient had medicine that is "+ parametars[0] +" prescribed multiple times in last "+ parametars[1] +" days')\n")
                file.write("\tdef customRuleHMC"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.hadMedicineType('"+parametars[0]+"',"+parametars[1]+")\n")
        elif(rule.extendsRuleset=="patv"):
            if(rule.extendedRule=="pv_rdn"):
                file.write("\t@select_multiple_rule_variable(label='Names of diseases that had repeated "+ parametars[0] +" times in last "+ parametars[1] +" days',options=getNamesList(Disease.objects.all()))\n")
                file.write("\tdef customRuleRDN"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.getRepetedDisNames("+parametars[0]+","+parametars[1]+")\n")
            elif(rule.extendedRule=="pv_cmt"):
                file.write("\t@numeric_rule_variable(label='Number of medicines of "+ parametars[0] +" type prescribed in last "+ parametars[1] +" days')\n")
                file.write("\tdef customRuleCMT"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.getNumberofMedicinesByType('"+parametars[0]+"',"+parametars[1]+")\n")
            elif(rule.extendedRule=="pv_dpc"):
                file.write("\t@numeric_rule_variable(label='Number of different doctors prescribing medicine of "+ parametars[0] +" type in last "+ parametars[1] +" days')\n")
                file.write("\tdef customRuleDPC"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.getDoctorPrescribingMedByTypeCount('"+parametars[0]+"',"+parametars[1]+")\n")
            elif(rule.extendedRule=="pv_dmc"):
                file.write("\t@numeric_rule_variable(label='Number of diseases that had medicine of "+ parametars[0] +" type prescribed in last "+ parametars[1] +" days')\n")
                file.write("\tdef customRuleDMC"+parametars[0].replace(" ", "")+parametars[1].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.getDiseaseNumByMedType('"+parametars[0]+"',"+parametars[1]+")\n")
    file.close()