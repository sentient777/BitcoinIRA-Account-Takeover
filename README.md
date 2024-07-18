# BitcoinIRA(dot)com Exploit - Account Takeover
t.me/schizodev - t.me/palantir7

A simple but yet powerful exploit, we are taking advantage of an incompetent software engineer at BitcoinIRA.
When sending a reset password request, we take abuse of the 'redirectLink' parameter. We can hijack this to use our own server and steal the tokens required to reset the password of *any* account.

This exploit only works, if the target clicks on the reset password link that BitcoinIRA is sending to the target.

# Explanation of the Exploit
1. Password request is sent with a malicious redirect link
2. Target clicks on the password request sent by BitcoinIRA
3. Target is getting redirected to the malicious link, leaking the password reset tokens
4. Password is instantly reset by the threat actor, with the just obtained password reset tokens
5. The malicious link is redirecting the target to the homepage of BitcoinIRA

# What is this?
A POC (Proof Of Concept) on how this exploit works. A simple Flask (Python) server that you can use to obtain the password reset tokens, and send malicious password reset requests. 
On arrival of the password reset tokens, the password is instantly resetted to a password to your choice.

# How to use this?
1. Download the source code
2. Setup the config.json with the required changes. 
3. Download the requirements with: `pip install -r requirements.txt`
4. Start the server with `python app.py`
5. Upon starting the Flask server a malicious password reset link is being sent to the target (step 2) from BitcoinIRA
6. When the target clicks, the password is being reset to what you have configured in step 2.

# Requirements
1. Basic programming and web hosting knowledge
2. Python 3.8+
3. Capsolver.com key with balance
4. A server
5. Optional: Domain name

*Note: This a  quickly made POC, and not a fully ready to use production app. Minor changes are required to use this in the wild*