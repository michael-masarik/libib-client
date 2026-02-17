# Libib-Client
A synchronous, third-party client for the [Libib API](https://support.libib.com/rest-api/introduction.html)

## Install
TODO

## Usage

To initalize the client:

```python
import Libib

# For Pro accounts
client = Libib("your-api-key", "your-user-id")

# For Ultimate accounts, also pass your Ultimate ID
client = Libib("your-api-key", "your-user-id", "your-ultimate-id")
```

## Patrons

### Get Patrons
Retrieve a list of all existing patrons on your site. Returns 50 patrons at a time with pagination support.

> For lists of patrons greater than 50, this function auto-handles pagination (with a 2 second pause between calls)


```python
# Get all patrons
patrons = client.patrons.get_patrons()
```

**Returns (Success):**

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
        "address1": null,
        "phone": "555-123-4567",
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

**Returns (Error):**

```python
{"status": "error", "code": response.status_code,"body": response.json()}
```

### Get Patron By ID
Retrieve a single patron by passing the patron's barcode or email as an id.

**Using the patron's email:**
```python
patron = client.patrons.get_patron_id("frankenstein@example.com")
```

**Using the patron's email:**
```python
patron = client.patrons.get_patron_id("2020000000013")
```

**Returns (Success):**

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

**Returns (Error):**

```python
{"status": "error", "code": response.status_code,"body": response.json()}
```

### Create Patron
> You can pass any number of the following keywords as params:
> ```python
> ["barcode","first_name","last_name","email","notification_emails","tags","patron_id","phone","address1","address2","city","state","country","zip","freeze","password"]
>```
> Though Libib recomends NOT to use the barcode field

Creates a new patron in the account.

```python
new_patron = client.patrons.create(email = "frankenstein@example.com", first_name = "Mary", last_name = "Shelley", patron_id = "mshelley" )
```

**Returns (Success):**

```python
print(new_patron)
# True
```

**Returns (Error):**

```python
{"status": "error", "code": response.status_code,"body": response.json()}
```