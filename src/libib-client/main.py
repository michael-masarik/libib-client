# Docs: https://support.libib.com/rest-api/introduction.html
import time

import requests

RATE = 2


class Libib:
    """
    Simple, Third-Party API Client for Libib
    """
    def __init__(self, apiKey: str, apiUserID: str, ultimateID: str | None = None) -> None:
        self.apiHeaders = {}
        self.apiHeaders["x-api-key"] = apiKey
        self.apiHeaders["x-api-user"] = apiUserID
        if ultimateID:
            self.apiHeaders["x-api-ultimate"] = ultimateID
        self.patrons = Patrons(self)
        self.managers = Managers(self)
        self.accounts = Accounts(self)

class Patrons:
    """
    Patron subclient
    """
    url = "https://api.libib.com/patrons"
    patron_sig = {"barcode","first_name","last_name","email","notification_emails","tags","patron_id","phone","address1","address2","city","state","country","zip","freeze","password"}

    def __init__(self, client: Libib) -> None:
        self.client = client
        self.headers = client.apiHeaders

    def get_patrons(self) -> dict | list:
        """
       Retrieve a list of all existing patrons on your site. Returns 50 patrons at a time with pagination support.
       For lists of patrons greater than 50, this function auto-handles pagination (with a 2 second pause between calls)

        :param self: `Self@Libib`

        :return success:
        ```python
            [
                {
                    "barcode": "2020000000013",
                    "first_name": "Mary",
                    "last_name": "Shelley",
                    "email": "frankenstein@example.com",
                    "notification_emails": None,
                    "tags": None,
                    "patron_id": "mshelley",
                    "phone": "555-123-4567",
                    "address1": None,
                    "address2": None,
                    "city": "Augusta",
                    "state": "KS",
                    "country": "US",
                    "zip": None,
                    "freeze": None,
                },
                {
                    "barcode": "2020000000037",
                    "first_name": "Marcus",
                    "last_name": "Aurelius",
                    "email": "meditations@example.com",
                    "notification_emails": None,
                    "tags": None,
                    "patron_id": None,
                    "phone": None,
                    "address1": None,
                    "address2": None,
                    "city": None,
                    "state": None,
                    "country": "US",
                    "zip": None,
                    "freeze": 1,
                }
            ]
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        params = {
            'page': 1
        }
        response = requests.get(self.url, headers=self.headers, params=params)
        data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": data}
        current_page = 1
        pages_to_go = data.get("pages", 1)
        patrons = []
        errors = None

        for patron in data.get("patrons", []):
            patrons.append(patron)

        while current_page < pages_to_go:
            time.sleep(RATE) # Pause to avoid rate limiting
            params["page"] += 1
            response = requests.get(self.url, headers=self.headers, params=params)
            data = response.json()
            if response.status_code != 200:
                errors = {"status": "error", "code": response.status_code, "body": data}
                break
            for patron in data.get("patrons", []):
                patrons.append(patron)
            current_page += 1
        if errors:
            return errors
        return patrons

    def get_patron_by_id(self, identifier: str) -> dict:
        """
        Retrieve a single patron by passing the patron's barcode or email as an identifier.

        :param self: `Self@Libib`
        :param identifier: patron email/barcode
        :type identifier: str
        :return success:
        ```python
        {
            "barcode": "2020000000013",
            "first_name": "Mary",
            "last_name": "Shelley",
            "email": "frankenstein@example.com",
            "notification_emails": None,
            "tags": None,
            "patron_id": "mshelley",
            "phone": "555-123-4567",
            "address1": None,
            "address2": None,
            "city": "Augusta",
            "state": "KS",
            "country": "US",
            "zip": None,
            "freeze": None,
        }
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{identifier}"
        response = requests.get(patronURL, headers=self.headers)
        data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": data}
        return data

    def create_patron(self, **data) -> dict | bool:
        """
        Create a new patron in the account.

        :param self: `Self@Libib`
        :param **data: Patron fields as keyword arguments. Accepts any of:
            barcode, first_name, last_name, email, notification_emails, tags, patron_id, phone, address1, address2, city, state, country, zip, freeze, password.
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        valid_data = {k: v for k, v in data.items() if k in self.patron_sig}
        invalid_data = {k: v for k, v in data.items() if k not in self.patron_sig}
        if len(valid_data) == 0:
            if len(invalid_data) > 0:
                print("Data is invalid:", invalid_data)
                return {"status": "error", "code": 400, "body": f"Data is invalid: {invalid_data}"}
            else:
                return {"status": "error", "code": 400, "body": "No Data Provided"}
        params = valid_data
        response = requests.post(self.url, headers=self.headers, params=params)
        resp_data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True
   
    def update_patron(self, identifier: str, **data) -> bool | dict:
        """
        Update specific fields for an existing patron. Pass the patron's barcode or email as the identifier.

        :param self: `Self@Libib`
        :param identifier: Patron email/barcode
        :type identifier: str
        :param **data: Patron fields as keyword arguments. Accepts any of:
            barcode, first_name, last_name, email, notification_emails, tags, patron_id, phone, address1, address2, city, state, country, zip, freeze, password.
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{identifier}"
        valid_data = {k: v for k, v in data.items() if k in self.patron_sig}
        invalid_data = {k: v for k, v in data.items() if k not in self.patron_sig}
        if len(valid_data) == 0:
            if len(invalid_data) > 0:
                print("Data is invalid:", invalid_data)
                return {"status": "error", "code": 400, "body": f"Data is invalid: {invalid_data}"}
            else:
                return {"status": "error", "code": 400, "body": "No Data Provided"}
        params = valid_data
        response = requests.post(patronURL, headers=self.headers, params=params)
        resp_data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True

    def restore_patron(self, identifier: str) -> bool | dict:
        """
        Restore a previously deleted patron. Patrons can be restored within 30 days of deletion. Pass the patron's barcode or email as the identifier.

        :param self: `Self@Libib`
        :param identifier: Patron email/barcode
        :type identifier: str
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{identifier}"
        response = requests.patch(patronURL, headers=self.headers)
        resp_data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True

    def delete_patron(self, identifier: str) -> bool | dict:
        """
        Remove a single patron by passing the patron's barcode or email as the identifier. Deleting a patron dissociates their entire lending/hold history.

        :param self: `Self@Libib`
        :param identifier: Patron email/barcode
        :type identifier: str
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{identifier}"
        response = requests.delete(patronURL, headers=self.headers)
        resp_data = response.json()
        if response.status_code != 204:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True


class Managers:
    """
    Manager subclient
    """
    url = "https://api.libib.com/managers"
    roles = {"admin", "manager", "lender"}

    def __init__(self, client: Libib) -> None:
        self.client = client
        self.headers = client.apiHeaders

    def get_managers(self) -> dict | list:
        """
        Retrieve a list of all existing managers on your site – including the owner.

        :param self: `Self@Libib`

        :return success:
        ```python
        [
            {
                "first_name": "Larry",
                "last_name": "McMurtry",
                "email": "lonesome@example.com",
                "role": "owner",
            },
            {
                "first_name": "Samwise",
                "last_name": "Gamgee",
                "email": "samthewise@example.com",
                "role": "lender",
            },
            {
                "first_name": "Anaïs",
                "last_name": "Nin",
                "email": "angela@example.com",
                "role": "admin",
            },
        ]
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        response = requests.get(self.url, headers=self.headers)
        data = dict(response.json())
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": data}
        return data.get("managers", [])

    def get_manager_by_id(self, email: str) -> dict:
        """
        Retrieve a single manager by passing the manager's email address as an identifier.

        :param self: `Self@Libib`
        :param email: Manager email
        :type email: str
        :return success:
        ```python
        {
            "first_name": "Samwise",
            "last_name": "Gamgee",
            "email": "samthewise@example.com",
            "role": "admin",
        }
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        managerURL = f"{self.url}/{email}"
        response = requests.get(managerURL, headers=self.headers)
        data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": data}
        return data

    def create_manager(self, first_name: str, last_name: str, email: str, password: str, role: str) -> dict | bool:
        """
        Create a new manager in the account. Must have open manager seats for this method to succeed.

        > Assigning Collections:
        > If user has a manager or lender role, assigning collections must be completed by the account owner using the website.

        :param self: `Self@Libib`
        :param first_name: Manager First Name
        :type first_name: str
        :param last_name: Manager Last Name
        :type last_name: str
        :param email: Manager Email
        :type email: str
        :param password: Manager Password
        :type password: str
        :param role: Manager Role
        :type role: str
        :rtype: dict[Any, Any]
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        if role not in self.roles:
            return {"status": "error", "code": 400, "body": f"Role is invalid: {role}"}

        params = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "role": role,
        }

        response = requests.post(url=self.url, headers=self.headers, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": data}

        return True

    def delete_manager(self, email: str) -> bool | dict:
        """
        Remove a single manager by their email address. You cannot remove the owner account via this method. Owners must delete their entire account manually.

        :param self: `Self@Libib`
        :param email: Manager email
        :type email: str
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        managerURL = f"{self.url}/{email}"
        response = requests.delete(managerURL, headers=self.headers)
        resp_data = response.json()
        if response.status_code != 204:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True

class Accounts:
    url = "https://api.libib.com/accounts"

    def __init__(self, client: Libib) -> None:
        self.client = client
        self.headers = client.apiHeaders

    def get_accounts(self) -> dict | list:
        """
        Retrieve a list of account information. For Pro users this will only return one account. For multi-account "Ultimate" users, this will return all accounts in their purview.

        The API returns an object with an 'accounts' list; this method returns that inner list.

        :param self: Self@Accounts

        :return success:
        ```python
        [
            {
                "organization": "My Organization Name",
                "api_id": "q44f0eb130194c31e9081bcc2412a7fe0a5b47ab",
                "email": "sriddell@example.com",
                "first_name": "Sepideh",
                "last_name": "Riddell",
                "manager_seats": 10,
                "url": "sr-library",
                "authorized": 1,
            }
        ]
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        response = requests.get(self.url, headers=self.headers)
        data = dict(response.json())
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": data}
        return data.get("accounts", [])