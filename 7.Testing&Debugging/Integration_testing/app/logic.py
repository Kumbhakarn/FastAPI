def is_eligable_for_load(
        income: float, age: int, employment_status: str
) -> bool:
    """
    Loan eligibility logic.

    Rules:
    - Applicant must have income >= 50,000.
    - Applicant must be at least 21 years old.
    - Applicant must be either 'employed' or 'self-employed'.

    Returns:
        bool: True if eligible, False otherwise.
    """
    return (
        (income >= 50000)
        and (age >= 21)
        and (employment_status in ['employed', 'self-employed'])
    )