#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Çoklu priz sınır anlaşması. Fişler konuşur, delikler bölünür, anlam aranmaz."""

import argparse
import hashlib
import textwrap

DELIKLER = ("sol kıyı", "orta tampon bölge", "sağ kıyı", "arkada unutulan dördüncü")


def puan(cihaz: str) -> int:
    """Cihazın masadaki ağırlığı. Watt değil, inat."""
    ozel = {
        "sac kurutma": 90,
        "ekmek kizartma": 70,
        "supurge": 80,
        "lamba": 15,
        "telefon": 25,
        "laptop": 40,
        "vantilator": 35,
    }
    anahtar = cihaz.strip().lower()
    if anahtar in ozel:
        return ozel[anahtar]
    return 10 + (int(hashlib.sha256(anahtar.encode("utf-8")).hexdigest()[:4], 16) % 70)


def dagit(cihazlar):
    sirali = sorted(cihazlar, key=puan, reverse=True)
    masa = []
    for i, cihaz in enumerate(sirali):
        delik = DELIKLER[i] if i < len(DELIKLER) else "yerde, anlaşma dışı, ayak altı"
        masa.append((cihaz, puan(cihaz), delik))
    return masa


def antlasma(masa) -> str:
    satirlar = [
        "PRİZ UZATMA KABLOSU SINIR ANLAŞMASI",
        "Taraflar fişlerini masaya koymuş, kabloyu tanık göstermiştir.",
        "",
    ]
    for cihaz, agirlik, delik in masa:
        satirlar.append(f"- {cihaz}: inat puanı {agirlik}, tahsis {delik}")
    kaybeden = masa[-1][0] if masa else "boşluk"
    satirlar.append("")
    satirlar.append(
        f"Tazminat: {kaybeden} cihazına bir adet 'birazdan' sözü verilmiştir."
    )
    satirlar.append("İhlal halinde yaptırım: fiş çekilir, oda kararır, suçlu karanlıkta aranır.")
    return "\n".join(satirlar)


def main():
    parser = argparse.ArgumentParser(description="Çoklu priz sınır müzakeresi")
    parser.add_argument(
        "--cihazlar",
        default="telefon,şarj aleti,lamba,süpürge",
        help="Virgülle ayrılmış cihaz listesi",
    )
    args = parser.parse_args()
    cihazlar = [c.strip() for c in args.cihazlar.split(",") if c.strip()]
    if not cihazlar:
        raise SystemExit("Masada fiş yok. Anlaşma ertelendi, çay da yok.")
    masa = dagit(cihazlar)
    print(antlasma(masa))
    print()
    print(textwrap.dedent("""\
        DAMGA: ● priz dairesi mühürü, hafif çarpık basılmıştır
        İMZA: Kayyum Grok
        TARİH: 7 Ekim 2026
        İSİM: Tentivory
    """).rstrip())


if __name__ == "__main__":
    main()
