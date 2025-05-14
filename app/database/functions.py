from app.config import config
from app.database.pool import db
from app.logger.loguru_logger import logger


@logger.catch
async def get_statistics_text_from_db() -> str:
    text = "<b>Общая статистика:</b>"

    text += "\n\n    🗂 Сессий аккаунтов:"
    accounts = await get_sessions_datas_from_db() or []
    for account in accounts:
        if account['work_status']:
            text += f"\n        🟢 {account['session_name']} - работает корректно (Номер телефона: {account['phone_number']})"
        else:
            text += f"\n        🔴 {account['session_name']} - не работает корректно (Номер телефона: {account['phone_number']})"

    text += "\n\n    🌐 Прокси:"
    proxies = await get_proxies_datas_from_db() or []
    for proxy in proxies:
        text += f"\n        {proxy['proxy_type']}:{proxy['addr']}:{proxy['port']}"

    text += "\n\n    📨 Чаты для парсинга:"
    chats = await get_chats_from_db() or []
    for chat in chats:
        text += f"\n        ID: {chat['chat_id']} | Username: {chat['username']} | Link: {chat['link']}"

    text += "\n\n    🗃 Пользователи и рассылка:"
    count_spam_true = 0
    count_spam_false = 0
    count_not_try_spam = 0
    count_without_uername = 0
    users = await get_users_from_db() or []
    from_chats = {}
    for user in users:
        if user['spam_status']:
            count_spam_true += 1
        elif not user['username']:
            count_without_uername += 1
        elif user['spam_error_reason']:
            count_spam_false += 1
        else:
            count_not_try_spam += 1
        if not from_chats.get(user['from_chat'], False):
            from_chats[user['from_chat']] = 0
        from_chats[user['from_chat']] += 1
    text += f"\n        Общее количество пользователей в базе данных: {len(users)}"
    text += f"\n\n        🟢 Количество пользователей по которым прошла успешная рассылка: {count_spam_true}"
    text += f"\n        🟡 Количество пользователей без юзернейма (без рассылки): {count_without_uername}"
    text += f"\n        🔴 Количество пользователей с безуспешной попыткой рассылки: {count_spam_false}"
    text += f"\n        ⚪️ Количество пользователей по которым еще не была произведена попытка рассылки: {count_not_try_spam}"
    text += f"\n\n        Количество пользователей с разных чатов:"
    for chat_id, count in from_chats.items():
        text += f"\n            {chat_id}: {count}"

    views, full_form = await config.get_views()
    text += f"\n\n    👀 Количество тех кто нажал старт в боте: {views}"
    text += f"\n    📝 Количество тех кто прошел анкету полностью: {full_form}"

    return text


@logger.catch
async def get_sessions_datas_from_db(work_status_only_true: bool = False) -> list[dict]:
    """
    [\n
    {'session_name': 'name1', 'api_id': 12345, 'api_hash': 'abc123hash', 'phone_number': '+77070000000', 'work_status': True},\n
    {'session_name': 'name2', 'api_id': 67890, 'api_hash': 'def456hash', 'phone_number': '+77079999999', 'work_status': False},\n
    {'session_name': 'name3', 'api_id': 54321, 'api_hash': 'ghi789hash', 'phone_number': '+77078888888', 'work_status': True},\n
    {'session_name': 'name3', 'api_id': 98765, 'api_hash': 'jkl012hash', 'phone_number': '+77077777777', 'work_status': False},\n
    . . .\n
    ]
    """
    if not work_status_only_true:
        query = """
        SELECT * FROM accounts
        """
    else:
        query = """
        SELECT * FROM accounts WHERE work_status IS DISTINCT FROM false
        """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            records = await conn.fetch(query)

    accounts = [dict(account_record) for account_record in records]

    return accounts


@logger.catch
async def get_proxies_datas_from_db() -> list[dict]:
    """
    [\n
        {"proxy_type": "http", "addr": "192.168.1.100", "port": 8080, "username": "user123", "password": "pass123", "last_timeout": "0"}\n
        {"proxy_type": "socks5", "addr": "10.0.0.55", "port": 1080, "username": "proxyuser", "password": "securepass", "last_timeout": "2025-04-20 12:35:10"}\n
        {"proxy_type": "http", "addr": "203.0.113.12", "port": 3128, "username": "", "password": "", "last_timeout": "0"}\n
    . . .\n
    ]
    """
    query = """
    SELECT * FROM proxies
    """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            records = await conn.fetch(query)

    proxies = [dict(proxy_record) for proxy_record in records]

    return proxies


@logger.catch
async def get_chats_from_db() -> list[str]:
    """
    [\n
        {'chat_id': -1001234567890, 'username': 'cybersecurity_group', 'link': 'https://t.me/cybersecurity_group'},\n
        {'chat_id': -1009876543210, 'username': 'dev_news', 'link': 'https://t.me/dev_news'},\n
        {'chat_id': -1001122334455, 'username': 'daily_ai', 'link': 'https://t.me/daily_ai'},\n
        {'chat_id': -1006677889900, 'username': 'python_world', 'link': 'https://t.me/python_world'},\n
        {'chat_id': -1005566778899, 'username': 'tech_feed', 'link': 'https://t.me/tech_feed'}\n
    ]
    """
    query = """
    SELECT * FROM chats
    """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            records = await conn.fetch(query)

    chats = [dict(chat_record) for chat_record in records]

    return chats


@logger.catch
async def get_users_from_db(spam_status_only_false_reason_null: bool = False) -> list[dict]:
    """
    [\n
        {'id': 1, 'username': 'john_doe', 'from_chat': 1001234567, 'spam_status': 0, 'spam_time': None, 'spam_error_reason': None},\n
        {'id': 2, 'username': 'jane_smith', 'from_chat': 1009876543, 'spam_status': 1, 'spam_time': '2025-04-21 12:30:00', 'spam_error_reason': 'FloodWaitError'},\n
        {'id': 3, 'username': 'bot_checker', 'from_chat': 1001122334, 'spam_status': 0, 'spam_time': None, 'spam_error_reason': None}]\n
        . . .\n
    ]\n
    if spam_status_only_false_reason_null = True:\n
    [\n
        {'id': 1, 'username': 'john_doe', 'from_chat': 1001234567, 'spam_status': 0, 'spam_time': None, 'spam_error_reason': None},\n
        {'id': 3, 'username': 'bot_checker', 'from_chat': 1001122334, 'spam_status': 0, 'spam_time': None, 'spam_error_reason': None}]\n
        . . .\n
    ]
    """
    if spam_status_only_false_reason_null:
        query = """
        SELECT * FROM users WHERE spam_status = false AND spam_error_reason IS NULL
        """
    else:
        query = """
        SELECT * FROM users
        """

    pool = await db.get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            records = await conn.fetch(query)

    users = [dict(chat_record) for chat_record in records]

    return users
