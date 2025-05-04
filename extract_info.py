def extract_high_level_signals(ind: dict) -> dict:
    sent = 'Positivo' if ind['macd'] > 0 else 'Negativo'
    trend = 'Alta' if ind['macd'] > 0 else 'Baixa'
    strength = max(1, min(5, int(abs(ind['macd']) / (ind['bb_width'] or 1))))
    return {'sentimento': sent, 'tendencia': trend, 'forca_tendencia': strength, **ind}
