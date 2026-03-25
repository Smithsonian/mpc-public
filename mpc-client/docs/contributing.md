# Contributing

Thank you for your interest in contributing to `mpc_client`!

## Reporting Bugs

Please open an issue on [GitHub](https://github.com/Smithsonian/mpc-public/issues)
or use the [MPC Jira Helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portals).

## Development Setup

```bash
git clone https://github.com/Smithsonian/mpc-public.git
cd mpc-public/mpc-client
pip install -e '.[test]'
pytest -v
```

## Submitting Changes

1. Fork the repository and create a feature branch.
2. Make your changes and add or update tests as needed.
3. Run the test suite to confirm everything passes:
   ```bash
   pytest -v
   ```
4. Open a pull request against the `main` branch with a clear description of
   the change.

## Code Style

- Follow existing conventions in the codebase.
- All public methods should include NumPy-style docstrings.
- Use [Pydantic](https://docs.pydantic.dev/) models for request/response validation.
