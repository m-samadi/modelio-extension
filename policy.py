# Export information of the policy
#==========================================================
import xml.etree.ElementTree as ET
import json

### Convert list to array
def conv_lst_arr(lst):
    s = str(lst)
    s = s.replace("[", "")
    s = s.replace("]", "")
    s = s.replace("'", "")

    arr = []
    if s.find(",") != -1:
        split = s.split(",")
        for i in range(len(split)):
            arr.append(split[i])
    else:
        arr.append(s)

    return(arr)

### Carry out the export process
def export():
    tree = ET.parse("modelio/cwd.xmi")
    root = tree.getroot()

    ## Fetch the information of the owner
    index = 0
    for elem in root:
        if str(elem.attrib).find("'name': 'Owner'") == -1:
            index += 1
        else:
            break

    policy_owner = []
    for i in range(6):
        value = str(root[index][i][0].attrib)
        split1 = value.split("'value': '")
        split2 = split1[1].split("'")

        policy_owner.append([split2[0]])

    ## Fetch the information of the observer
    index = 0
    for elem in root:
        if str(elem.attrib).find("'name': 'Observer'") == -1:
            index += 1
        else:
            break

    policy_observer = []
    for i in range(6):
        value = str(root[index][i][0].attrib)
        split1 = value.split("'value': '")
        split2 = split1[1].split("'")

        policy_observer.append([split2[0]])

    ### Write the obtained information in the JSON file
    json_str = {
        "policyId": "",
        "entries": {
            "owner": {
                "subjects": {
                    "nginx:ditto": {
                        "type": "nginx basic auth user"
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

    json_str["policyId"] = str(policy_owner[0]).replace("[", "").replace("]", "").replace("'", "")
    json_str["entries"]["owner"]["resources"]["thing:/"]["grant"] = conv_lst_arr(policy_owner[1])
    json_str["entries"]["owner"]["resources"]["policy:/"]["grant"] = conv_lst_arr(policy_owner[2])
    json_str["entries"]["owner"]["resources"]["dbconfig:/"]["grant"] = conv_lst_arr(policy_owner[3])
    json_str["entries"]["owner"]["resources"]["view:/"]["grant"] = conv_lst_arr(policy_owner[4])
    json_str["entries"]["owner"]["resources"]["connection:/"]["grant"] = conv_lst_arr(policy_owner[5])
    json_str["entries"]["observer"]["resources"]["thing:/"]["grant"] = conv_lst_arr(policy_observer[1])
    json_str["entries"]["observer"]["resources"]["policy:/"]["grant"] = conv_lst_arr(policy_observer[2])
    json_str["entries"]["observer"]["resources"]["dbconfig:/"]["grant"] = conv_lst_arr(policy_observer[3])
    json_str["entries"]["observer"]["resources"]["view:/"]["grant"] = conv_lst_arr(policy_observer[4])
    json_str["entries"]["observer"]["resources"]["connection:/"]["grant"] = conv_lst_arr(policy_observer[5])

    with open("output/policy/policy.json", "w") as f:
        json.dump(json_str, f, indent=4)

    return policy_owner[0]
