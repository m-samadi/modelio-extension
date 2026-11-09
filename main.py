#---- Modelio Extension ----#
# Export information of the model created in Modelio
#==========================================================
import policy
import device

policy_id = policy.export() # Export the policy information
device.export(policy_id) # Export the device information
