# Patrons

The `client.patrons` sub-client contains methods for interacting with patron-related endpoints in the Libib API.

This page documents the available patron methods, expected parameters, and example responses.

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

## Get Patrons

Retrieve a list of all existing patrons on your site.

- Returns **50 patrons per request**
- Supports pagination
- This client automatically handles pagination when retrieving more than 50 patrons

> For lists of patrons greater than 50, this method automatically handles pagination (with a 2 second pause between calls).

### Example

```python
patrons = client.patrons.get_patrons()
```

### Returns (Success)

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
        "address1": None,
        "phone": "555-123-4567",
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
    },
]
```

---

## Get Patron By ID

Retrieve a single patron by passing the patron's barcode or email.

### Parameters

- `id` *(str)*: The patron's barcode or email.

### Example (Using email)

```python
patron = client.patrons.get_patron_by_id("frankenstein@example.com")
```

### Example (Using barcode)

```python
patron = client.patrons.get_patron_by_id("2020000000013")
```

### Returns (Success)

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

---

## Create a Patron

Create a new patron in your Libib account.

### Supported Parameters

You may pass any number of the following keyword arguments:

```python
[
    "barcode",
    "first_name",
    "last_name",
    "email",
    "notification_emails",
    "tags",
    "patron_id",
    "phone",
    "address1",
    "address2",
    "city",
    "state",
    "country",
    "zip",
    "freeze",
    "password",
]
```

> Libib recommends **not** setting the `barcode` field manually.

### Example

```python
created = client.patrons.create_patron(
    email="frankenstein@example.com",
    first_name="Mary",
    last_name="Shelley",
    patron_id="mshelley",
)
```

### Returns (Success)

```python
True
```

---

## Update a Patron

Update one or more fields for an existing patron.

Pass the patron's barcode or email as the `id`.

### Parameters

- `id` *(str)*: The patron's barcode or email.

### Supported Update Fields

You may pass any number of the following keyword arguments:

```python
[
    "barcode",
    "first_name",
    "last_name",
    "email",
    "notification_emails",
    "tags",
    "patron_id",
    "phone",
    "address1",
    "address2",
    "city",
    "state",
    "country",
    "zip",
    "freeze",
    "password",
]
```

> Libib recommends **not** updating the `barcode` field.

### Example

```python
updated = client.patrons.update_patron(
    id="frankenstein@example.com",
    first_name="Mary",
    last_name="Shelley",
    patron_id="mshelley",
)
```

### Returns (Success)

```python
True
```

---

## Restore a Patron

Restore a previously deleted patron.

Patrons can be restored within 30 days of deletion.

### Parameters

- `id` *(str)*: The patron's barcode or email.

### Example (Using barcode)

```python
restored = client.patrons.restore_patron("2020000000013")
```

### Example (Using email)

```python
restored = client.patrons.restore_patron("frankenstein@example.com")
```

### Returns (Success)

```python
True
```

---

## Delete a Patron

Delete a patron by barcode or email.

Deleting a patron dissociates their lending and hold history.

### Parameters

- `id` *(str)*: The patron's barcode or email.

### Example (Using barcode)

```python
deleted = client.patrons.delete_patron("2020000000013")
```

### Example (Using email)

```python
deleted = client.patrons.delete_patron("frankenstein@example.com")
```

### Returns (Success)

```python
True
```