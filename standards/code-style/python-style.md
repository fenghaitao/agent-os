# Python Style Guide

## General Formatting
- Use 4 spaces for indentation (never tabs)
- Maximum line length of 88 characters (Black formatter default)
- Use trailing commas in multi-line structures
- Two blank lines between top-level functions and classes
- One blank line between methods in a class

## Import Organization
- Standard library imports first
- Third-party imports second
- Local application imports last
- Separate each group with a blank line

```python
import os
import sys
from pathlib import Path

import requests
from django.conf import settings

from myapp.models import User
from myapp.utils import helper_function
```

## Naming Conventions
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes: prefix with single underscore `_private_var`
- "Magic" methods: double underscores `__special__`

## Type Hints
- Use type hints for function parameters and return values
- Import types from `typing` module when needed
- Use `Optional[Type]` for nullable parameters

```python
from typing import Dict, List, Optional, Union

def process_users(
    users: List[Dict[str, Union[str, int]]],
    active_only: bool = True
) -> Optional[List[str]]:
    """Process a list of user dictionaries."""
    if not users:
        return None

    return [user['name'] for user in users if user.get('active', False)]
```

## Function and Method Structure
- Use descriptive function names
- Keep functions focused on a single responsibility
- Use docstrings for all public functions and methods
- Place default arguments at the end

```python
def calculate_monthly_payment(
    principal: float,
    annual_rate: float,
    years: int,
    down_payment: float = 0.0
) -> float:
    """Calculate monthly mortgage payment.

    Args:
        principal: Loan amount
        annual_rate: Annual interest rate as decimal (0.05 for 5%)
        years: Loan term in years
        down_payment: Down payment amount

    Returns:
        Monthly payment amount

    Raises:
        ValueError: If any input values are negative
    """
    if principal < 0 or annual_rate < 0 or years <= 0:
        raise ValueError("Invalid input values")

    adjusted_principal = principal - down_payment
    monthly_rate = annual_rate / 12
    num_payments = years * 12

    if monthly_rate == 0:
        return adjusted_principal / num_payments

    return (
        adjusted_principal
        * monthly_rate
        * (1 + monthly_rate) ** num_payments
        / ((1 + monthly_rate) ** num_payments - 1)
    )
```

## List and Dictionary Comprehensions
- Use comprehensions for simple transformations
- Break complex comprehensions into regular loops
- Prefer readability over brevity

```python
# Good: Simple and readable
active_users = [user for user in users if user.is_active]
user_emails = {user.id: user.email for user in users}

# Avoid: Too complex for comprehension
# Better as a regular loop
processed_data = []
for item in raw_data:
    if item.is_valid():
        processed = item.transform()
        if processed.meets_criteria():
            processed_data.append(processed.finalize())
```
