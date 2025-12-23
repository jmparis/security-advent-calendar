This year Santa Claus made the decision to secure the email communication between the toy factory and Santa' headquarter.
Thus the Grinch will not be able to read messages if he intercepts them.
After doing some research, Santa decided to use asymmetric encryption.

So, Santa has generated a RSA key pair and stored the private key in a safe place.
Then he distributed the following public key so that people can encrypt the messages to him.

```text
-----BEGIN PUBLIC KEY----- 
MDswDQYJKoZIhvcNAQEBBQADKgAwJwIgATDOKzp991nXIjXWEm0rCqjTmt6ZfDsh+Fj39HyGAdcCAwEAAQ== 
-----END PUBLIC KEY-----
```

It seems that Santa did the right thing but is it really the case?

The following string is the flag encrypted with the public key above.
Can you prove to Santa Claus that he chose a bad key pair?

		AO4dwRk2Gv0IAndrXO342riZMiO4qhnqBf9E/PmOwts= 

The format of the flag is **ADV{something}**
