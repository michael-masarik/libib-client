# Managers

The `client.accounts` sub-client contains methods for interacting with account-related endpoints in the Libib API.

This page documents the available account methods, expected parameters, and example responses.

---

## Error Format

All methods return a Python `dict` on failure in the following format:

```python
{
    "status": "error",
    "code": response.status_code,
    "body": response.json(),
}
```

---

## Get Accounts

Retrieve a list of account information. For Pro users this will only return one account. For multi-account "Ultimate" users, this will return all accounts in their purview.

### Example:
```python
accounts = client.accounts.get_accounts()
```

### Returns (Success):
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
        "authorized": 1
    }
]
```
