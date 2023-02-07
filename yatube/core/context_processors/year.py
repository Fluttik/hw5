from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    now = datetime.now()
    now_year = now.year
    return {'year': now_year}
