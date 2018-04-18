18/04/2018:
Refactored AccessGetter into DataEncryptor
Added function in DataEncryptor/__main__ :
      If .json files are present, encrypt them to .encrypted.json then delete the file
      If no .json files present, decrypt all .encrypted.json and create .json file