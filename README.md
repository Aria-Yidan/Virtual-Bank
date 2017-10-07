# Virtual-Bank
E-bank system based on Django implemented by Python, using RSA、AES、MD5、timestamp、challenge-respons

Realize the basic functions of E-bank system: account registration, user login, identity authentication, user transfer, access services. The identity authentication using a "challenge-response" mode, hybrid encryption mode is used in the data transmission process, asymmetric key encryption in hybrid encryption using RSA encryption algorithm, symmetric key encryption using CBC mode AES encryption algorithm; and then generate timestamp, MD5 hash function of the ciphertext and timestamp generation message the related information transfer transaction using hybrid encryption URL transactions in the interface, and use the time stamp to prevent replay attacks.


![image](https://github.com/githubforliyidan/Virtual-Bank/blob/master/screenshots/1.png)



![image](https://github.com/githubforliyidan/Virtual-Bank/blob/master/screenshots/2.png)