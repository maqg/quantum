# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode

RC4_Key = "octopuslink!"


def gen_random_bytes(k):
	i = 0
	j = 0
	while True:
		i = (i + 1) % 256
		j = (j + k[i]) % 256
		k[i], k[j] = k[j], k[i]
		yield k[(k[i] + k[j]) % 256]


def rc4_crypt(data, key):
	S = list(range(256))
	j = 0
	out = []
	
	# Algoritmo pseudo aleatorio
	for i in range(256):
		j = (j + S[i] + ord(key[i % len(key)])) % 256
		S[i], S[j] = S[j], S[i]
	
	# Algoritmo de 1 clave
	i = j = 0
	for char in data:
		i = (i + 1) % 256
		j = (j + S[i]) % 256
		S[i], S[j] = S[j], S[i]
		out.append(char ^ S[(S[i] + S[j]) % 256])
	
	return bytes(out)


def replace(data):
	return data.replace("/", "*").replace("+", "_")


def unreplace(data):
	return data.replace("*", "/").replace("_", "+")


def encrypt(data, key, encode=False):
	data = rc4_crypt(data.encode(encoding="ascii"), key)
	if encode:
		data = b64encode(data)
	return replace(data.decode(encoding="utf-8"))


def decrypt(data, key, decode=False):
	if decode:
		data = b64decode(unreplace(data).encode(encoding="utf-8"))
	return rc4_crypt(data, key)


def getCipherPassword(password, source="client"):
	return encrypt(source + "#" + password, RC4_Key, encode=True)


def getPlainPassword(password):
	outText = decrypt(password, RC4_Key, decode=True).decode(encoding="utf-8")
	return outText.split("#")[-1]


if __name__ == "__main__":
	# y = getPlainPassword("INIeuWGImdrckyTRP1JMlOPwqQGP77Fka09rpQ==")
	y = getCipherPassword("hellohjkjkjkjkjkjkjkafdfasfjkadk/fadsfdkfasdenry")
	print(y)
	x = getPlainPassword(y)
	print(x)
