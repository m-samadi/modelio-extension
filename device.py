# Export information of the devices
#==========================================================
import xml.etree.ElementTree as ET
import json
import copy

### Carry out the export process
def export(policy_id):
    tree = ET.parse("modelio/cwd.xmi")
    root = tree.getroot()

    ### All devices
    ## Define a JSON structure
    json_def = {
        "policyId": "",
        "attributes": {
        },
        "features": {
        }
    }

    ## Define the device, tag, and measurement unit information
    device_fullname = ["Bateria Solis - Bateria", "OMIE PT", "Victron", "Grid meter", "PV meter"]
    device_name = ["bateria_solis", "omie", "victron", "grid_meter", "pv_meter"]

    tag = []
    feature = []
    measurement_unit = []

    # Bateria Solis
    tag.append(["Battery Current", "Battery SoC", "Battery Status", "Battery Charge Current Max", "Battery Discharge Current Max", "Battery SoH", "Battery Charging Energy"])
    feature.append(["BatteryCurrent", "BatterySoC", "BatteryStatus", "BatteryChargeCurrentMax", "BatteryDischargeCurrentMax", "BatterySoH", "BatteryChargingEnergy"])
    measurement_unit.append(["Battery Current Unit", "Battery SoC Unit", "Battery Status Unit", "Battery Charge Current Max Unit", "Battery Discharge Current Max Unit", "Battery SoH Unit", "Battery Charging Energy Unit"])

    # OMIE
    tag.append(["OMIE Surplus Price"])
    feature.append(["OMIESurplusPrice"])
    measurement_unit.append(["OMIE Surplus Price Unit"])

    # Victron
    tag.append(["Battery Voltage AC", "Grid Frequency", "Battery Current AC", "Battery Power", "Battery Voltage"])
    feature.append(["BatteryVoltageAC", "GridFrequency", "BatteryCurrentAC", "BatteryPower", "BatteryVoltage"])
    measurement_unit.append(["Battery Voltage AC Unit", "Grid Frequency Unit", "Battery Current AC Unit", "Battery Power Unit", "Battery Voltage Unit"])

    # Grid meter
    tag.append(["GM Active Power"])
    feature.append(["GMActivePower"])
    measurement_unit.append(["GM Active Power Unit"])

    # PV meter
    tag.append(["PV Energy", "PV Power"])
    feature.append(["PVEnergy", "PVPower"])
    measurement_unit.append(["PV Energy Unit", "PV Power Unit"])

    ## Write the network information for the devices in the YAML file
    with open("output/device/house.yaml", "w") as f:
        f.write("path: house1.sensors")
        f.write("\ndevices:")

        for i in range(len(device_name)):
            f.write('\n    "' + device_name[i] + '": ' + device_name[i] + '.json')

        f.close()

    ### Each device
    for i in range(len(device_fullname)):
        device_json = copy.deepcopy(json_def)

        ## Set the policy
        device_json["policyId"] = str(policy_id).replace("[", "").replace("]", "").replace("'", "")

        ## Set the attributes
        index = 0
        for elem in root:
            if str(elem.attrib).find(f"'name': '{device_fullname[i]}'") == -1:
                index += 1
            else:
                break

        attribute = []
        for j in range(14):
            value = str(root[index][j][0].attrib)

            split1 = value.split("'value': '")
            split2 = split1[1].split("'")

            attribute.append(split2[0])

        device_json["attributes"].update({"Id":f"{attribute[0]}"})
        device_json["attributes"].update({"Serial":f"{attribute[1]}"})
        device_json["attributes"].update({"Name":f"{attribute[2]}"})
        device_json["attributes"].update({"DeviceTypeId":f"{attribute[3]}"})
        device_json["attributes"].update({"UnitId":f"{attribute[4]}"})
        device_json["attributes"].update({"Address":f"{attribute[5]}"})
        device_json["attributes"].update({"State":f"{attribute[6]}"})
        device_json["attributes"].update({"PhysicalAddress":f"{attribute[7]}"})
        device_json["attributes"].update({"PhysicalAddressType":f"{attribute[8]}"})
        device_json["attributes"].update({"TariffId":f"{attribute[9]}"})
        device_json["attributes"].update({"ContractedOptionId":f"{attribute[10]}"})
        device_json["attributes"].update({"LocalId":f"{attribute[11]}"})
        device_json["attributes"].update({"DeviceTypeTypeCode":f"{attribute[12]}"})
        device_json["attributes"].update({"Domain":f"{attribute[13]}"})

        ## Set the features
        for j in range(len(tag[i])):
            device_json["features"].update({feature[i][j]:{}})
            device_json["features"][feature[i][j]].update({"properties":{}})

            index = 0
            for elem in root:
                if str(elem.attrib).find(f"'name': '{tag[i][j]}'") == -1:
                    index += 1
                else:
                    break

            value = str(root[index][0][0].attrib)
            split1 = value.split("'symbol': '")
            split2 = split1[1].split("'")
            try:
                device_json["features"][feature[i][j]]["properties"].update({"value":int(split2[0])})
            except ValueError:
                device_json["features"][feature[i][j]]["properties"].update({"value":float(split2[0])})

            index = 0
            for elem in root:
                if str(elem.attrib).find(f"'name': '{measurement_unit[i][j]}'") == -1:
                    index += 1
                else:
                    break

            value = str(root[index][0][0].attrib)
            split1 = value.split("'value': '")
            split2 = split1[1].split("'")
            device_json["features"][feature[i][j]]["properties"].update({"unit":split2[0]})

        with open("output/device/" + device_name[i] + ".json", "w") as f:
            json.dump(device_json, f, indent=4)
