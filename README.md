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

### Patrons

Patron documentation can be [found here](/docs/patrons.md)
