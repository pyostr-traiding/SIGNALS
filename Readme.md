Сервис создает сигналы для символа
Выходные сигналы: 
- RSI 
- Stoch RSI 
- MACD (В разработке)
- ADX (В разработке)

Сигналы отправляются в Redis Pub/Sub

Подключение - "signals:BTCUSDT"

---

Форматы

RSI

```json
{
      "kline_ms": 1234567890,
      "symbol": "BTCUSDT",
      "type": "PREDICT.RSI",
      "ex": "bybit",
      "values": [
        {
            "kline_ms": 1234567890,
            "interval": 1,
            "value": 30,
            "side": "buy",
            "percent": 0.1,
            "target_rate": 100000.22
        }
  ]
}
```

Stoch RSI

```json
{
      "kline_ms": 1234567890,
      "symbol": "BTCUSDT",
      "type": "PREDICT.RSI",
      "ex": "bybit",
      "values": [
        {
            "kline_ms": 1234567890,
            "interval": 1,
            "value_k": 11.1,
            "value_d": 9.02,
            "side": "buy",
            "percent": 0.1,
            "target_rate": 100000.22
        }
  ]
}
```