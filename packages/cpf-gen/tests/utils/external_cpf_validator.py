import json
import os
import urllib.parse
import urllib.request

from .env_variables import load_test_env


class ExternalCpfValidator:
    def __init__(self):
        load_test_env()

    def is_valid(self, cpf_string: str) -> bool:
        api_url = os.getenv("API_URL")

        if not api_url:
            raise Exception("API URL not defined.")

        api_token = os.getenv("API_TOKEN")

        if not api_token:
            raise Exception("API secret not defined.")

        cpf_escaped = urllib.parse.quote(cpf_string, safe="")
        request_url = f"{api_url}/cpf/val/{cpf_escaped}"
        req = urllib.request.Request(request_url)
        req.add_header("Authorization", f"Bearer {api_token}")

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())

                return data.get("result", False)
        except urllib.error.HTTPError as e:
            raise Exception(f'HTTP error ({e.code}) with CPF "{cpf_string}"') from e
        except urllib.error.URLError as e:
            raise Exception(f'Network error with CPF "{cpf_string}"') from e
        except json.JSONDecodeError as e:
            raise Exception(f'Invalid JSON response for CPF "{cpf_string}"') from e
