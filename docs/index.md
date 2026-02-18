# libib-client
A synchronous, third-party client for the [Libib API](https://support.libib.com/rest-api/introduction.html)

## Install
```shell
pip install libib-client
```

## Usage

To initalize the client:

```python
import libib_client

# For Pro accounts
client = Libib("your-api-key", "your-user-id")

# For Ultimate accounts, also pass your Ultimate ID
client = Libib("your-api-key", "your-user-id", "your-ultimate-id")
```

### Patrons

Patron documentation can be [found here](Patrons.md)

### Managers

Manager documentation can be [found here](Managers.md)

### Accounts

Manager documentation can be [found here](Accounts.md)

## Note

I do not have an Ultimate account, so if the Ultimate features (or any features, for that matter) do not work, feel free to open an issue or a PR
