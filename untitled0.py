for jogo in partidas:
    utc_str = jogo["utcDate"]
    utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
    utc_dt = utc.localize(utc_dt)
    brasilia_dt = utc_dt.astimezone(brasilia)

    data_jogo = brasilia_dt.strftime('%Y-%m-%d')
    hora_jogo = brasilia_dt.strftime('%H:%M')

    time_a = jogo["homeTeam"]["name"]
    time_b = jogo["awayTeam"]["name"]
    status = jogo["status"]

    if status in ["SCHEDULED", "LIVE"] and data_jogo == hoje:
        lista_dia.append({
            "Data": data_jogo,
            "Hora": hora_jogo,
            "Time A": time_a,
            "Time B": time_b,
            "Status": status
        })

        odd_over25 = round(random.uniform(1.70, 2.30), 2)
        prob_estimada = 0.60
        ev = (prob_estimada * odd_over25) - 1
        valor_aposta = "✅ Valor" if ev > 0 else "❌ Sem valor"

        lista_valor.append({
            "Time A": time_a,
            "Time B": time_b,
            "Odd Over 2.5": f"{odd_over25:.2f}",
            "EV (60%)": f"{ev:.2f}",
            "Tem valor?": valor_aposta
        })

    elif status == "SCHEDULED" and data_jogo > hoje:
        lista_futuros.append({
            "Data": data_jogo,
            "Hora": hora_jogo,
            "Time A": time_a,
            "Time B": time_b,
            "Status": status
        })
