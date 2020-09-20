##mapping

def attack_category_mapping(preds):
    attack_cat = ['Analysis', 'Backdoor', 'DoS', 'Exploits', 'Fuzzers', 'Generic', 'Normal', 'Reconnaissance', 'Shellcode', 'Worms']
    prediction = []
    for i in preds:
      prediction.append(attack_cat[i])

    return prediction
