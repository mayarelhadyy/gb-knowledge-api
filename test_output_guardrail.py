from services.output_guardrail_service import validate_answer


context = """
Remote or hybrid work, where permitted, remains subject
to manager approval, information-security requirements,
availability expectations, and business needs.
"""


supported_answer = """
Remote work is subject to manager approval and
information-security requirements.
"""


unsupported_answer = """
Employees may work remotely three days per week
and receive a monthly home-office allowance.
"""


print(
    "Supported test:",
    validate_answer(
        supported_answer,
        context
    )
)

print(
    "Unsupported test:",
    validate_answer(
        unsupported_answer,
        context
    )
)