Телеграм-бот для отримання курсу валют НБУ

# INSTALL

```
cd /opt
git clone https://github.com/alex-79/telegram-exchange-rates-bot.git
cd telegram-exchange-rates-bot
python3 -m venv venv
source venv/bin/activate
python3 -m pip install aiogram
python3 -m pip install requests
python3 -m pip install configparser
```

# CONFIGURE

```
cp bot.ini.sample bot.ini
```

Edit bot.ini:

```
[general]
token = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX <--- edit
```

# RUN

```
touch /lib/systemd/system/telegram-exchange-rates-bot.service
```

```
[Unit]
Description=telegram-exchange-rates-bot
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/opt/telegram-exchange-rates-bot/
ExecStart=/opt/telegram-exchange-rates-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```
systemctl daemon-reload 
systemctl enable telegram-exchange-rates-bot.service
systemctl start telegram-exchange-rates-bot.service
```

# DEMO

https://t.me/nbu_exchange_rates_bot