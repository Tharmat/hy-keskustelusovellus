# hy-keskustelusovellus
Repository for University of Helsinki course Tietokannat ja Web-ohjelmointi

# Keskustelusovellus
Yksinkertainen keskustelusovellus Helsingin Yliopiston "Tietokannat ja Web-ohjelmointi" -kurssia varten. Toteutettu Pyhtonilla, Flaskilla ja PostgreSQL:lla.
Pääpiirteittäin toimii kuten moni muukin "bulletin board" -softa, eli tarjolla on läjä keskustelualueita joihin voi lisätä viestejä.

## Roolit
- Käyttäjä
- Ylläpitäjä (samat oikeudet ja toiminnot kuin käyttäjällä, mutta pystyy lisäämään/poistamaan keskustelualueita sekä poistamaan myös toisten käyttäjien viestejä)

## Pääominaisuudet (alustava määrittely)
(ruksatut kohdat toteutettu as of 15.12.2024)
- [x] Käyttäjä pystyy luomaan uuden tunnuksen ("rekisteröitymään") ja kirjautumaan tunnuksella palveluun, sekä kirjautumaan ulos palvelusta.
- [x] Käyttäjä näkee kirjauduttuaan listan keskustealueista, jokaisen alueen viestimäärän ja koska alueelle on edellisen kerran lisätty viesti
- [x] Käyttäjä voi lisätä uuden ketjun haluamalleen keskustelualueelle antamalla ketjulle otsikon ja aloitusviestin
- [x] Käyttäjä pystyy lisäämään viestin ketjuun
- [x] Käyttäjä voi muokata omia viestejään
- [x] Käyttäjä voi poistaa omia viestejään (oikeasti viestejä ei poisteta vaan niille merkitään täppä "removed" jolloin niitä ei enää näytetä)
- [x] Käyttäjä voi myös etsiä olemassaolevista viesteistä ne joissa on annettu hakusana
- [x] Ylläpitäjä voi muokata mitä tahansa keskustelualuetta, ketjua tai viestiä
- [x] Ylläpitäjä voi poistaa minkä tahansa keskustelualueen, ketjun tai viestin
- [x] Ylläpitäjä voi merkitä minkä tahansa keskustelualueen "salaiseksi" ja määrittää kenellä on sinne pääsy.

## Käyttö
Oletuksena että asennettuna git, python3, PostgreSQL jne.

1. Kloonaa repo
2. Käynnistä luo virutaaliympäristö ja käynnistä se, sekä asenna riippuvuudet, esim. seuraavilla komennoilla
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
3. Repon juuresta täytyy löytyä `.env` tiedosto jossa on sovelluksen käyttämä tiedot `SECRET_KEY` ja `DATABASE_URL`
```
DATABASE_URL=postgresql://<username:password@hostname>
SECRET_KEY=<randomly generate secret key>
```
5. Repossa on tiedosto `schemas.sql` joka tulee ajaa käytettyyn kantaan käsin / haluamallaan työkalulla
6. Aja lisäksi `seed.sql` tietokantaan. Tämä tiedosto luo minimaalisen testisetupin. 
7. Aja Flask komennolla `flask run`
8. Seed.sql:n mukana tulee valmiina seuraavat käyttäjätunnukset admin/admin, alice/alice ja bob/bob

## Testaus / huomioita
- Admin-tunnuksilla on mahdollisuus tehdä kaikkea, eli lisätä/poistaa/muokata keskustelualueita, ketjuja ja viestejä sekä määrittää onko joku keskustelualue salattu. Admin myös näkee minkälaisia oikeuksia käyttäjille on annettu keskustelualueisiin. Lähtökohtaisesti kaikki alueet näkyvät kaikille, mutta admin voi piilottaa alueita. Jos käyttäjällä on admin-oikeudet (users.is_admin = true) niin hän näkee myös piilotetut keskustelualueet. 
- Softassa on myös toiminnallisuus jolla voi antaa yksittäisille käyttäjille oikeuden piilotettuun keskustelualueseseen. Seed.sql:n mukana tulee "Alice <3 admin" -keskustelualue jonka admin näkee admin-oikeuksien perusteella, alice user_right-taulussa annettujen oikeuksien perusteella, mutta bob ei näe tätä aluetta. Admin voi halutessaan poistaa piilotuksen. Tämän suhteen softassa on pieni puute, kts. "Puutteet".
- Admin voi myös poistaa viestejä / ketjuja / keskustelualueita. Näitä ei kuitenkaan poisteta oikeasti tietokannasta vaan asetetaan täppä "removed" jolloin ko. rivi ei näy enää hauissa.

## Puutteet
Softassa on muutamia puutteita ajanpuutteen vuoksi.
1. Validointeja on softassa varsin vähän. Esim. kenttien pituuksien validointi ja client-side validoinnit puuttuvat kokonaan.
2. Ulkoasu on karu. Stylesheetit ovat käytössä mutta näitä ei ole käytetty juurikaan muuhin kuin ihan perusasioihin.
3. Keskustelualuiden käyttäjäkohtainen näkyvyys toimii ja nämä tiedot myös näkyvät adminille, mutta näitä ei pääse muokkaamaan käyttöliittymän kautta vaan vaatii kantapuukotusta. 
