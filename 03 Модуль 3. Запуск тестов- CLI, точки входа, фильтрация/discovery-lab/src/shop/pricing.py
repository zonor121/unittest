def final_price_cents(base_cents: int, discount_percent: int = 0, tax_percent: int = 20) -> int:
    """
    Контракт:
    - base_cents: int, >= 0
    - discount_percent: int, 0..100
    - tax_percent: int, 0..100
    Логика:
    - discount применяется к base
    - затем добавляется tax
    - результат округляется до целых центов (int)
    """
    if not isinstance(base_cents, int) or isinstance(base_cents, bool):
        raise TypeError("base_cents must be int")
    if not isinstance(discount_percent, int) or isinstance(discount_percent, bool):
        raise TypeError("discount_percent must be int")
    if not isinstance(tax_percent, int) or isinstance(tax_percent, bool):
        raise TypeError("tax_percent must be int")
    
    if base_cents < 0:
        raise ValueError("base_cents must be >= 0")
    if not (0 <= discount_percent <= 100):
        raise ValueError("discount_percent must be 0..100")
    if not (0 <= tax_percent <= 100):
        raise ValueError("tax_percent must be 0..100")
    
    discounted = base_cents * (100 - discount_percent) // 100
    final = discounted * (100 + tax_percent) // 100
    return final