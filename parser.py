def seconds_to_hms(seconds):
    minutes = (seconds % 3600) // 60  # Получаем количество полных минут
    seconds_remaining = seconds % 60  # Получаем оставшиеся секунды

    return (f"{minutes} минут {seconds_remaining} секунд")
