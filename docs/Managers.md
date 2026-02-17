# Managers

The `client.managers` sub-client contains methods for interacting with manager-related endpoints in the Libib API.

This page documents the available manager methods, expected parameters, and example responses.

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

## Get Managers

Retrieve a list of all existing managers on your site – including the owner.


### Example

```python
managers = client.managers.get_managers()
```

### Returns (Success)

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

---

## Get Manager By ID

Retrieve a single manager by passing the manager's email address as an identifier.


### Parameters

- `email` *(str)*: The manager's email.

### Example

```python
manager = client.managers.get_manager_by_id("samthewise@example.com")
```

### Returns (Success)

```python
{
    "first_name": "Samwise",
    "last_name": "Gamgee",
    "email": "samthewise@example.com",
    "role": "admin",
}
```

---

## Create a Manager

Create a new manager in the account.

This method requires that your Libib account has open manager seats available.

> Assigning Collections:
> If the new user has a `manager` or `lender` role, assigning collections must be completed by the account owner using the Libib website.

### Parameters

- `id` *(str)*: The manager's email.
- `first_name` *(str)*: The manager's first name.
- `last_name` *(str)*: The manager's last name.
- `email` *(str)*: The manager's email.
- `password` *(str)*: The manager's password.
- `role` *(str)*: The manager role (`admin`, `manager`, or `lender`).


### Example

```python
created = client.managers.create_manager(
    id="samthewise@example.com",
    email="samthewise@example.com",
    first_name="Samwise",
    last_name="Gamgee",
    password="secret-password",
    role="admin",
)
```

### Returns (Success)

```python
True
```

---

## Delete a Manager

Remove a single manager by their email address. You cannot remove the owner account via this method. Owners must delete their entire account manually.


### Parameters

- `email` *(str)*: The manager's email.

### Example

```python
deleted = client.managers.delete_manager("samthewise@example.com")
```

### Returns (Success)

```python
True
```
 