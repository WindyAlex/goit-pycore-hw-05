import re
from decimal import Decimal
from typing import Callable, Iterable, Generator


def generator_numbers(text: str) -> Generator[Decimal, None, None]:
    # handle case of numbers at start or end
    text_with_borders = f" {text} "
    pattern = r'(?<=\s)\d+(?:\.\d+)?(?=\s)'
    for match in re.finditer(pattern, text_with_borders):
        yield Decimal(match.group())


def sum_profit(text: str, func: Callable[[str], Iterable[Decimal]]) -> Decimal:
    return sum(func(text), Decimal(0))


def main():
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )

    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


main()
