#!/usr/bin/env python3
"""Генерирует widget/countdown.svg — виджет обратного отсчёта для README.

Запуск: python3 widget/generate.py
Без внешних зависимостей. Дни считаются по московскому времени.
"""
import base64
import datetime as dt
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
TARGET = dt.date(2027, 3, 9)          # день встречи
TITLE = "ДО ВСТРЕЧИ С АЛИНОЙ:"
STEP = 2                              # секунд на одну подпись

CAPTIONS = [
    "литералли мои 4 звезды ⭐⭐⭐⭐",
    "кд чд?", "окак", "емае", "ку кд чд", "мявк",
    "мяу или не мяу? неизвестно",
    "перелом задней шерстинки",
    "слаб мрежни сигнал",
    "ваувау, плюс вайб",
    "мы в сатурне", "+- нормик", "понпон", "угуг", "воть",
    "мороженое кусни?",
    "оказывается 4 + 1 это не 6",
    "тебе 18 и ты сеньор?",
    "ВЗЯТЬ ЛАБУБУ ДЛЯ АЛИНЫ",
    "я прочитала большую картошку",
    "Вас исключили из семьи",
    "клон Фенвика",
    "интерполируем?",
    "А че нас депортируют?",
    "выбери своего бойца",
    "я все клодом решаю",
    "навыки гуглижа",
    "епаресете",
    "смешнявка", "лапочковое", "крутышк!!",
    "Ахахахкхпхаха0",
]


def plural(n, forms):
    a, b = n % 10, n % 100
    if a == 1 and b != 11:
        return forms[0]
    if 2 <= a <= 4 and not 12 <= b <= 14:
        return forms[1]
    return forms[2]


def main():
    today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=3)).date()
    diff = (TARGET - today).days
    days = diff - 1                  # полных суток до 00:00 9 марта, как на сайте
    if diff == 1:
        big, small = "ЗАВТРА", "уже совсем скоро"
    elif days > 0:
        big, small = str(days), plural(days, ("день", "дня", "дней"))
    elif diff == 0:
        big, small = "СЕГОДНЯ", "ваувау, встреча! 🍉"
    else:
        big, small = "❤", "встретились"
    big_size = 64 if len(big) <= 3 else 40

    photo = base64.b64encode((HERE / "photo.jpg").read_bytes()).decode()
    n = len(CAPTIONS)
    total = n * STEP
    on = 100 / n
    caps = "\n".join(
        f'    <text class="cap" x="236" y="222" style="animation-delay:-{(n - i) % n * STEP}s">{escape(c)}</text>'
        for i, c in enumerate(CAPTIONS)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="250" viewBox="0 0 600 250" role="img" aria-label="{escape(TITLE)} {escape(big)} {escape(small)}">
  <title>{escape(TITLE)} {escape(big)} {escape(small)}</title>
  <style>
    .wall{{fill:url(#g)}}
    .card{{fill:#ffffff}}
    .bub{{fill:#e3fec6}}
    .ink{{fill:#141414}}
    .meta{{fill:#5e8a4e}}
    .num{{fill:#2f7d1f}}
    text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
    .title{{font-size:21px;font-weight:800}}
    .big{{font-size:{big_size}px;font-weight:800}}
    .small{{font-size:20px;font-weight:700}}
    .name{{font-size:15px;font-weight:700;fill:#3a9be0}}
    .cap{{font-size:17px;font-weight:600;fill:#141414;opacity:0;animation:c {total}s linear infinite}}
    @keyframes c{{0%{{opacity:1}}{on:.3f}%{{opacity:1}}{on + 0.01:.3f}%{{opacity:0}}100%{{opacity:0}}}}
    @media (prefers-color-scheme: dark){{
      .card{{fill:#17212b}} .bub{{fill:#2b5278}} .ink,.cap{{fill:#f2f5f8}}
      .meta{{fill:#8eb4d4}} .num{{fill:#9fd0ff}}
      #g stop:first-child{{stop-color:#0f1a12}} #g stop:last-child{{stop-color:#1d2b1e}}
    }}
    @media (prefers-reduced-motion: reduce){{.cap{{animation:none}} .cap:first-of-type{{opacity:1}}}}
  </style>
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#d7e7b4"/><stop offset="1" stop-color="#9fc79a"/>
    </linearGradient>
    <clipPath id="p"><rect x="16" y="16" width="200" height="218" rx="16"/></clipPath>
  </defs>
  <rect class="wall" width="600" height="250" rx="22"/>
  <rect class="card" x="10" y="10" width="212" height="230" rx="20"/>
  <image href="data:image/jpeg;base64,{photo}" x="16" y="16" width="200" height="218" preserveAspectRatio="xMidYMid slice" clip-path="url(#p)"/>
  <rect class="card" x="232" y="14" width="356" height="160" rx="18"/>
  <text class="name" x="250" y="40">Алина Жена</text>
  <text class="title ink" x="250" y="72">{escape(TITLE)}</text>
  <text class="big num" x="250" y="146">{escape(big)}<tspan class="small meta" dx="10">{escape(small)}</tspan></text>
  <text class="meta" x="572" y="162" text-anchor="end" font-size="12">9 марта 🍉</text>
  <rect class="bub" x="226" y="190" width="362" height="48" rx="16"/>
{caps}
</svg>
'''
    (HERE / "countdown.svg").write_text(svg, encoding="utf-8")
    print(f"countdown.svg: {big} {small}")


if __name__ == "__main__":
    main()
