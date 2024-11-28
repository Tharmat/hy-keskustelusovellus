# hy-keskustelusovellus
Repository for University of Helsinki course Tietokannat ja Web-ohjelmointi

# Keskustelusovellus
Yksinkertainen keskustelusovellus Helsingin Yliopiston "Tietokannat ja Web-ohjelmointi" -kurssia varten. Toteutettu Pyhtonilla, Flaskilla ja PostgreSQL:lla.
Pääpiirteittäin toimii kuten moni muukin "bulletin board" -softa, eli tarjolla on läjä keskustelualueita joihin voi lisätä viestejä.

## Roolit
- Käyttäjä
- Ylläpitäjä (samat oikeudet ja toiminnot kuin käyttäjällä, mutta pystyy lisäämään/poistamaan keskustelualueita sekä poistamaan myös toisten käyttäjien viestejä)

## Pääominaisuudet (alustava määrittely)
(ruksatut kohdat toteutettu as of 17.11.2024)
- [x] Käyttäjä pystyy luomaan uuden tunnuksen ("rekisteröitymään") ja kirjautumaan tunnuksella palveluun, sekä kirjautumaan ulos palvelusta.
- [x] Käyttäjä näkee kirjauduttuaan listan keskustealueista, jokaisen alueen viestimäärän ja koska alueelle on edellisen kerran lisätty viesti
- [x] Käyttäjä voi lisätä uuden ketjun haluamalleen keskustelualueelle antamalla ketjulle otsikon ja aloitusviestin
- [x] Käyttäjä pystyy lisäämään viestin/kommentin toisten käyttäjien aloittamiin ketjuihin
- [ ] (preliminary, eihän mikään oikea softa toimi näin) Käyttäjä voi muokata omia viestejään ja aloittamansa ketjun otsikkoa. Käyttäjä voi myös poistaa omia viestejään tai aloittamansa ketjun.
- [ ] Käyttäjä voi myös etsiä olemassaolevista viesteistä ne joissa on annettu hakusana
- [ ] Ylläpitäjä voi edellisten lisäksi poistaa/lisätä keskustelualueita ja poistaa/muokata myös toisten käyttäjien viestejä/ketjuja
- [ ] Ylläpitäjä voi merkitä minkä tahansa keskustelualueen "salaiseksi" ja määrittää kenellä on sinne pääsy

## Käyttö
Oletuksena että asennettuna git, python3, PostgreSQL jne.

1. Kloonaa repo
2. Repossa tiedostossa `requirements.txt` listattu vaadittavat riippuvuudet jotka täytyy asentaa esim. komennolla `pip install -r requirements.txt`
3. Repon juuresta täytyy löytyä tiedosto `.secret_env` joka sisältää rivin `SECRET_KEY=xxx` jossa `xxx` on jokin satunnaisesti valittu avain
4. Sovellus käyttää oletuksena _testitietokantaa_ `postgresql://postgres:admin@localhost`. Käytetyn kannan voi määrittää tiedostossa `.env`
5. Repossa on tiedosto `schemas.sql` joka tulee ajaa käytettyyn kantaan käsin / haluamallaan työkalulla
6. Aja lisäksi `seed.sql` tietokantaan. Tämä tiedosto luo minimaalisen testisetupin. 
7. Aja Flask komennolla `flask run`
8. Luo uusi käyttäjä rekisteröintisivulla tai kirjaudu sisään admin-tunnuksilla (admin/admin)
