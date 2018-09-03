def customMonitoringVariablesWriter(rules):
    file = open("custom_variables_m.py",'w')
    file.write("from resoner import MonitoringVariables\n\n")
    file.write("class CustomMonitoringVariables(MonitoringVariables):\n")
    for rule in rules:
        parametars = rule.params.split(",")
        if(rule.extendsRuleset=="monv"):
            if(rule.extendedRule=="mv_tll"):
                file.write("\t@numeric_rule_variable(label='Amount of urin relieved in last "+ parametars[0] +" hours')\n")
                file.write("\tdef customRuleTLL"+parametars[0].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.getTimedLiquidLevel("+parametars[0]+")\n")
            elif(rule.extendedRule=="mv_htr"):
                file.write("\t@numeric_rule_variable(label='Number of hearthbeats in last "+ parametars[0] +" secounds')\n")
                file.write("\tdef customRuleHTR"+parametars[0].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.getHearthRate("+parametars[0]+")\n")
            elif(rule.extendedRule=="mv_dih"):
                file.write("\t@boolean_rule_variable(label='"+ parametars[0] +" is in patients disease records history')\n")
                file.write("\tdef customRuleDIH"+parametars[0].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.checkDiseaseInHistory('"+parametars[0]+"')\n")
            elif(rule.extendedRule=="mv_owu"):
                file.write("\t@boolean_rule_variable(label='Oxygen level went up in last "+ parametars[0] +" minutes')\n")
                file.write("\tdef customRuleOWU"+parametars[0].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.oxygenWentUp("+parametars[0]+")\n")
            elif(rule.extendedRule=="mv_owd"):
                file.write("\t@boolean_rule_variable(label='Oxygen level went down in last "+ parametars[0] +" minutes')\n")
                file.write("\tdef customRuleOWD"+parametars[0].replace(" ", "")+"(self):\n")
                file.write("\t\treturn self.oxygenWentDown("+parametars[0]+")\n")
    file.close()
