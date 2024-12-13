# hy-keskustelusovellus
Repository for University of Helsinki course Tietokannat ja Web-ohjelmointi

# Keskustelusovellus
Yksinkertainen keskustelusovellus Helsingin Yliopiston "Tietokannat ja Web-ohjelmointi" -kurssia varten. Toteutettu Pyhtonilla, Flaskilla ja PostgreSQL:lla.
Pääpiirteittäin toimii kuten moni muukin "bulletin board" -softa, eli tarjolla on läjä keskustelualueita joihin voi lisätä viestejä.

## Roolit
- Käyttäjä
- Ylläpitäjä (samat oikeudet ja toiminnot kuin käyttäjällä, mutta pystyy lisäämään/poistamaan keskustelualueita sekä poistamaan myös toisten käyttäjien viestejä)

## Pääominaisuudet (alustava määrittely)
(ruksatut kohdat toteutettu as of 10.12.2024)
- [x] Käyttäjä pystyy luomaan uuden tunnuksen ("rekisteröitymään") ja kirjautumaan tunnuksella palveluun, sekä kirjautumaan ulos palvelusta.
- [x] Käyttäjä näkee kirjauduttuaan listan keskustealueista, jokaisen alueen viestimäärän ja koska alueelle on edellisen kerran lisätty viesti
- [x] Käyttäjä voi lisätä uuden ketjun haluamalleen keskustelualueelle antamalla ketjulle otsikon ja aloitusviestin
- [x] Käyttäjä pystyy lisäämään viestin ketjuun
- [x] Käyttäjä voi muokata omia viestejään
- [x] Käyttäjä voi poistaa omia viestejään (oikeasti viestejä ei poisteta vaan niille merkitään täppä "removed" jolloin niitä ei enää näytetä)
- [ ] Käyttäjä voi myös etsiä olemassaolevista viesteistä ne joissa on annettu hakusana
- [x] Ylläpitäjä voi muokata mitä tahansa keskustelualuetta, ketjua tai viestiä
- [x] Ylläpitäjä voi poistaa minkä tahansa keskustelualueen, ketjun tai viestin
- [ ] Ylläpitäjä voi merkitä minkä tahansa keskustelualueen "salaiseksi" ja määrittää kenellä on sinne pääsy

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
8. Luo uusi käyttäjä rekisteröintisivulla tai kirjaudu sisään admin-tunnuksilla (admin/admin)
