# MobilaTa

*Mobila ta, de la noi.* Magazin online de mobilă, proiect de practică.

Flask + PostgreSQL (Supabase), pe Vercel: catalog pe categorii, pagini de produs cu recenzii, coș, comandă
și plată simulată, conturi de client (inclusiv login cu Google) cu zonă GDPR,
plus panou de administrare pentru produse, comenzi, clienți și utilizatori.

Varianta reală, cu admin, conturi și comenzi salvate în Supabase. Tabelele se creează din `supabase/`.

## Pornire locală

```bash
pip install -r requirements.txt
# setează DATABASE_URL (adresa Transaction pooler din Supabase), apoi:
python server.py
```

Site-ul pornește pe http://localhost:8835. Pe Vercel, `DATABASE_URL` și `MOBILATA_SECRET` se pun în setările proiectului.
