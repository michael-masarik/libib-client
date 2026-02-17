# Docs: https://support.libib.com/rest-api/introduction.html
import time

import requests

RATE = 2

class Libib:
    """
    Simple, Third-Party API Client for Libib
    """
    def __init__(self, apiKey: str, apiUserID: str, ultimateID = None) -> None:
        self.apiHeaders = {}
        self.apiHeaders["x-api-key"] = apiKey
        self.apiHeaders["x-api-user"] = apiUserID
        if ultimateID:
            self.apiHeaders["x-api-ultimate"] = ultimateID
        self.patrons = Patrons(self)
        self.managers = Managers(self)
        
    
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
                "notification_emails": null,
                "tags": null,
                "patron_id": "mshelley",
                "phone": "555-123-4567",
                "address1": null,
                "address2": null,
                "city": "Augusta",
                "state": "KS",
                "country": "US",
                "zip": null,
                "freeze": null
                },
                {
                "barcode": "2020000000037",
                "first_name": "Marcus",
                "last_name": "Aurelius",
                "email": "meditations@example.com",
                "notification_emails": null,
                "tags": null,
                "patron_id": null,
                "phone": null,
                "address1": null,
                "address2": null,
                "city": null,
                "state": null,
                "country": "US",
                "zip": null,
                "freeze": 1
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

    def get_patron_by_id(self, id: str) -> dict:
        
        """
        Retrieve a single patron by passing the patron's barcode or email as an id.
       
        :param self: `Self@Libib`
        :param id: patron email/barcode
        :type id: str
        :return success:
        ```python
        {
            "barcode": "2020000000013",
            "first_name": "Mary",
            "last_name": "Shelley",
            "email": "frankenstein@example.com",
            "notification_emails": null,
            "tags": null,
            "patron_id": "mshelley",
            "phone": "555-123-4567",
            "address1": null,
            "address2": null,
            "city": "Augusta",
            "state": "KS",
            "country": "US",
            "zip": null,
            "freeze": null
        }
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{id}"
        response = requests.get(patronURL, headers=self.headers)
        data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": data}
        return data

    def create_patron(self, **data) -> dict | bool:
        """
        Create a new patron in the account.
       
        :param self: `Self@Libib`
        :param id: Patron Email
        :type id: str
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
                print("Data is invaild:", invalid_data)
                return {"status": "error", "code": 400, "body": f"Data is invaild: {invalid_data}"}
            else:
                return {"status": "error", "code": 400, "body": "No Data Provided"}
        params = valid_data
        response = requests.post(self.url, headers=self.headers, params=params)
        resp_data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True
   
    def update_patron(self, id: str, **data) -> bool | dict:
        """
        Update specific fields for an existing patron. Pass the patron's barcode or email as the id.

        :param self: `Self@Libib`
        :param id: Patron email/barcode
        :type id: str
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{id}"
        valid_data = {k: v for k, v in data.items() if k in self.patron_sig}
        invalid_data = {k: v for k, v in data.items() if k not in self.patron_sig}
        if len(valid_data) == 0:
            if len(invalid_data) > 0:
                print("Data is invaild:", invalid_data)
                return {"status": "error", "code": 400, "body": f"Data is invaild: {invalid_data}"}
            else:
                return {"status": "error", "code": 400, "body": "No Data Provided"}
        params = valid_data
        response = requests.post(patronURL, headers=self.headers, params=params)
        resp_data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True
        
    def restore_patron(self, id: str) -> bool | dict:
        """
        Restore a previously deleted patron. Patrons can be restored within 30 days of deletion. Pass the patron's barcode or email as the id.

        :param self: `Self@Libib`
        :param id: Patron email/barcode
        :type id: str
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{id}"
        response = requests.patch(patronURL, headers=self.headers)
        resp_data = response.json()
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True
  
    def delete_patron(self, id: str)->bool | dict:
        """
        Remove a single patron by passing the patron's barcode or email as the id. Deleting a patron dissociates their entire lending/hold history.

        :param self: `Self@Libib`
        :param id: Manager email
        :type id: str
        :return success:
        ```python
        True
        ```
        :return error:
        ```python
        {"status": "error", "code": response.status_code, "body": response.json()}
        ```
        """
        patronURL = f"{self.url}/{id}"
        response = requests.delete(patronURL, headers=self.headers)
        resp_data = response.json()
        if response.status_code != 204:
            return {"status": "error", "code": response.status_code, "body": resp_data}
        return True


class Managers:
    """
    Manager subclient
    """
    def __init__(self, client: Libib) -> None:
        self.client = client
        self.headers = client.apiHeaders
    # TODO
    def get_accounts(self) :
        """
        Retrieve a list of account information. For Pro users this will only return one account. For multi-account "Ultimate" users, this will return all accounts in their purview.
        Throws on network errors or non-2xx status codes

        :param self: `Self@Libib`
        :return success: 
        ```json
        {
            "accounts": [
                {
                "organization": "My Organization Name",
                "api_id": "q44f0eb130194c31e9081bcc2412a7fe0a5b47ab",
                "email": "sriddell@example.com",
                "first_name": "Sepideh",
                "last_name": "Riddell",
                "manager_seats": 10,
                "url": "sr-library",
                "authorized": 1
                }
            ]
        }
        ```
        """
        return 
    # TODO
    def get_managers(self):
        """
        Retrieve a list of all existing managers on your site – including the owner.
        Throws on network errors or non-2xx status codes

        :param self: `Self@Libib`

        :return success:
        ```json
            {
                "total": 3,
                "managers": [
                    {
                    "first_name": "Larry",
                    "last_name": "McMurtry",
                    "email": "lonesome@example.com",
                    "role": "owner"
                    },
                    {
                    "first_name": "Samwise",
                    "last_name": "Gamgee",
                    "email": "samthewise@example.com",
                    "role": "lender"
                    },
                    {
                    "first_name": "Anaïs",
                    "last_name": "Nin",
                    "email": "angela@example.com",
                    "role": "admin"
                    }
                ]
            }
        ```

        """
        pass
    # TODO
    def get_manager_id(self, id: str):
        """
        Retrieve a single manager by passing the manager's email address as an identifier.
        Throws on network errors or non-2xx status codes

        :param self: `Self@Libib`
        :param id: Manager email
        :type id: str
        :return success:
        ```json
        {
            "first_name": "Samwise",
            "last_name": "Gamgee",
            "email": "samthewise@example.com",
            "role": "admin"
        }
        ```
        """
        pass

    # TODO
    def create_manager(self, id: str):
        """
        Create a new manager in the account. Must have open manager seats for this method to succeed.
        Throws on network errors or non-2xx status codes

        Assigning Collections:
        If user has a manager or lender role, assigning collections must be completed by the account owner using the website.

        :param self: `Self@Libib`
        :param id: Manager email
        :type id: str
        :return success:
        ```json
        {
            "first_name": "Samwise",
            "last_name": "Gamgee",
            "email": "samthewise@example.com",
            "role": "admin"
        }
        ```
        """
        pass

    # TODO
    def delete_manager(self, id: str)->bool:
        """
        Remove a single manager by their email address. You cannot remove the owner account via this method. Owners must delete their entire account manually.
        Throws on network errors or non-2xx status codes


        :param self: `Self@Libib`
        :param id: Manager email
        :type id: str
        :return success:
        ```python
        True
        ```
        """
        return True        