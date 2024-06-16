**Create Certificate Authority in Mininet**:
sudo openssl genrsa -aes256 -out cakey.pem 2048

**Generate Root CA signing Certificate**:
sudo openssl req -x509 -new -nodes -key cakey.pem -sha256 -days 1825 -out cacert.pem

**Network Configuration**: 
![dlv1](https://github.com/minhtriet359/Mininet_TLSChatServer/assets/148809094/8c7ab314-2c33-421f-9e59-e2075b850e86)


**Chat server running**: 
![image](https://github.com/minhtriet359/Mininet_TLSChatServer/assets/148809094/80adb41b-3f1b-421d-9f6e-fd0cbdd564b0)

**Server certificate generated:**
![image](https://github.com/minhtriet359/Mininet_TLSChatServer/assets/148809094/75767f92-e3ad-4bf7-8404-d6551ede5b7a)
