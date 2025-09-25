sudo systemctl daemon-reload
sudo systemctl start expo

# запуск при старте сервера
sudo systemctl enable expo  

sudo systemctl stop expo

# Проверить логи:
journalctl -u expo -f