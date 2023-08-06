import safetypy
x = safetypy.SafetyCulture('54819832824ddb01858e1eb9e766dab7b410ab46670c1a08de008bdc43138e78')

y = x.get_audit_actions('2017-09-08T00:20:44.926Z')

# print y
print str(len(y))

