#---- Modelio Extension ----#
# Export the model information provided in Modelio to JSON
# and YAML files
#==========================================================
import xml.etree.ElementTree as ET
import json
import copy

# Function
#==========================================================
### Convert string to array
def conv_str_arr(str):
    arr = []
    if str.find(";") != -1:
        split = str.split(";")
        for i in range(len(split)):
            arr.append(split[i])
    else:
        arr.append(str)

    return(arr)

# Policy
#==========================================================
### Fetch the policy information from the XML file
tree = ET.parse('cwd.xmi')
root = tree.getroot()

index = 0
for elem in root:
    if str(elem.attrib).find("'name': 'Policy'") == -1:
        index += 1
    else:
        break

policy = []
for i in range(11):
    name = str(root[index][i].attrib)
    split1 = name.split("'name': '")
    split2 = split1[1].split("', 'visibility'")

    value = str(root[index][i][1].attrib)
    split3 = value.split("'value': '")
    split4 = split3[1].split("'")

    policy.append([split2[0], split4[0]])

### Write the obtained information in the JSON file
json_str = {
    "policyId": "",
    "entries": {
        "owner": {
            "subjects": {
                "ditto:owner": {
                    "type": "basic user"
                }
            },
            "resources": {
                "thing:/": {
                    "grant": [],
                    "revoke": []
                },
                "policy:/": {
                    "grant": [],
                    "revoke": []
                },
                "dbconfig:/": {
                    "grant": [],
                    "revoke": []
                },
                "view:/": {
                    "grant": [],
                    "revoke": []
                },
                "connection:/": {
                    "grant": [],
                    "revoke": []
                }
            }
        },
        "observer": {
            "subjects": {
                "ditto:observer": {
                    "type": "observer user"
                }
            },
            "resources": {
                "thing:/": {
                    "grant": [],
                    "revoke": []
                },
                "policy:/": {
                    "grant": [],
                    "revoke": []
                },
                "dbconfig:/": {
                    "grant": [],
                    "revoke": []
                },
                "view:/": {
                    "grant": [],
                    "revoke": []
                },
                "connection:/": {
                    "grant": [],
                    "revoke": []
                }
            }
        }
    }
}

json_str["policyId"] = policy[0][1]
json_str["entries"]["owner"]["resources"]["thing:/"]["grant"] = conv_str_arr(policy[1][1])
json_str["entries"]["owner"]["resources"]["policy:/"]["grant"] = conv_str_arr(policy[2][1])
json_str["entries"]["owner"]["resources"]["dbconfig:/"]["grant"] = conv_str_arr(policy[3][1])
json_str["entries"]["owner"]["resources"]["view:/"]["grant"] = conv_str_arr(policy[4][1])
json_str["entries"]["owner"]["resources"]["connection:/"]["grant"] = conv_str_arr(policy[5][1])
json_str["entries"]["observer"]["resources"]["thing:/"]["grant"] = conv_str_arr(policy[6][1])
json_str["entries"]["observer"]["resources"]["policy:/"]["grant"] = conv_str_arr(policy[7][1])
json_str["entries"]["observer"]["resources"]["dbconfig:/"]["grant"] = conv_str_arr(policy[8][1])
json_str["entries"]["observer"]["resources"]["view:/"]["grant"] = conv_str_arr(policy[9][1])
json_str["entries"]["observer"]["resources"]["connection:/"]["grant"] = conv_str_arr(policy[10][1])

with open("output/policy.json", "w") as f:
    json.dump(json_str, f, indent=4)

# Device
#==========================================================
### All devices
# Define a JSON structure
json_def = {
    "policyId": "",
    "attributes": {
    },
    "features": {
    }
}

# Fetch common device information (i.e., attributes) from the XML file
index = 0
for elem in root:
    if str(elem.attrib).find("'name': 'Device'") == -1:
        index += 1
    else:
        break

device = []
for i in range(26):
    name = str(root[index][i].attrib)

    split1 = name.split("'name': '")
    split2 = split1[1].split("', 'visibility'")

    device.append(split2[0])
device = list(dict.fromkeys(device))

# Insert the obtained information into the JSON structure
json_def["policyId"] = policy[0][1]
for i in range(len(device)):
    json_def["attributes"].update({device[i]:""})

# Write the network information for the devices in the YAML file
device_name = ["omie", "grid meter", "victron", "bateria solis", "pv meter"]
device_filename = ["omie", "grid_meter", "victron", "bateria_solis", "pv_meter"]

with open("output/house.yaml", "w") as f:
    f.write("path: house.sensors")
    f.write("\ndevices:")

    for i in range(len(device_name)):
        f.write('\n    "' + device_name[i] + '": ' + device_filename[i] + '.json')

    f.close()

### Each device
# Fetch device information (i.e., attributes) from the XML file
index = 0
for elem in root:
    if str(elem.attrib).find("'name': 'DeviceDetail'") == -1:
        index += 1
    else:
        break

device = []
for i in range(15):
    name = str(root[index][i].attrib)

    split1 = name.split("'name': '")
    split2 = split1[1].split("', 'visibility'")

    value = str(root[index][i][1].attrib)
    split3 = value.split("'value': '")
    split4 = split3[1].split("'")

    device.append([split2[0], split4[0]])

# Write the information obtained for each device in the JSON file
for i in range(len(device_filename)):
    device_json = copy.deepcopy(json_def)

    # Set the Id
    device_json["features"].update({"Id":{}})
    device_json["features"]["Id"].update({"properties":{}})
    device_json["features"]["Id"]["properties"].update({"value":int(device[i*3][1])})
    device_json["features"]["Id"]["properties"].update({"unit":"Int"})

    # Set the feature and the unit
    feature = device[i*3+1][1]
    if feature.find(";") == -1:
        feature_list = [feature]
    else:
        feature_list = feature.split(";")

    unit = device[i*3+2][1]
    if unit.find(";") == -1:
        unit_list = [unit]
    else:
        unit_list = unit.split(";")

    for j in range(len(feature_list)):
        device_json["features"].update({feature_list[j]:{}})
        device_json["features"][feature_list[j]].update({"properties":{}})
        device_json["features"][feature_list[j]]["properties"].update({"value":""})
        device_json["features"][feature_list[j]]["properties"].update({"unit":unit_list[j]})

    with open("output/" + device_filename[i] + ".json", "w") as f:
        json.dump(device_json, f, indent=4)
