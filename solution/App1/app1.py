import asyncio
import time
from nats.aio.client import Client as NATS
from config import your_ip as IP
from config import port

async def handler(msg):
    # Получаем тик времени и
    # Округляем время до мс
    t_real = time.time()
    t_real_rounded = float('{:.4f}'.format(t_real))

    # Получаем t_sign из сообщения
    t_sign = float(msg.data.decode())

    # Вычисляем dt и округляем его
    dt = t_real_rounded - t_sign
    t_dt_rounded = float('{:.4f}'.format(dt))

    # Выводим dt в консоль
    print(f"dt = {t_dt_rounded}")

async def pub_sub_loop():
    # Подключаемся к локальному серверу NATS на порт 4222
    nc = NATS()
    await nc.connect(servers=[f"nats://{IP}:{port}"])

    # Подписываюсь на топик от второго приложения и
    # указываю обработчик  полученного сообщения
    await nc.subscribe("app2_tick", cb=handler)

    while True:
        # Получаем тик времени и
        # Округляем время до мс
        t_real = time.time()
        t_rounded = float('{:.4f}'.format(t_real))

        # Публикуем сообщение с округленным временем в шину данных
        await nc.publish("app1_tick", str(t_rounded).encode())
        # Ставлю задержку между публикациями в 10 мс
        await asyncio.sleep(0.01)

asyncio.run(pub_sub_loop())
