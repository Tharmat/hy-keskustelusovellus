# hy-keskustelusovellus
Repository for University of Helsinki course Tietokannat ja Web-ohjelmointi

# Keskustelusovellus
Yksinkertainen keskustelusovellus Helsingin Yliopiston "Tietokannat ja Web-ohjelmointi" -kurssia varten. Toteutettu Pyhtonilla, Flaskilla ja PostgreSQL:lla.
Pääpiirteittäin toimii kuten moni muukin "bulletin board" -softa, eli tarjolla on läjä keskustelualueita joihin voi lisätä viestejä.

## Roolit
- Käyttäjä
- Ylläpitäjä (samat oikeudet ja toiminnot kuin käyttäjällä, mutta pystyy lisäämään/poistamaan keskustelualueita sekä poistamaan myös toisten käyttäjien viestejä)

## Pääominaisuudet (alustava määrittely)
1. Käyttäjä pystyy luomaan uuden tunnuksen ("rekisteröitymään") ja kirjautumaan tunnuksella palveluun, sekä kirjautumaan ulos palvelusta.
2. Käyttäjä näkee kirjauduttuaan listan keskustealueista, jokaisen alueen viestimäärän ja koska alueelle on edellisen kerran lisätty viesti
3. Käyttäjä voi lisätä uuden ketjun haluamalleen keskustelualueelle antamalla ketjulle otsikon ja aloitusviestin
4. Käyttäjä pystyy lisäämään viestin/kommentin toisten käyttäjien aloittamiin ketjuihin
5. (preliminary, eihän mikään oikea softa toimi näin) Käyttäjä voi muokata omia viestejään ja aloittamansa ketjun otsikkoa. Käyttäjä voi myös poistaa omia viestejään tai aloittamansa ketjun.
6. Käyttäjä voi myös etsiä olemassaolevista viesteistä ne joissa on annettu hakusana
7. Ylläpitäjä voi edellisten lisäksi poistaa/lisätä keskustelualueita ja poistaa/muokata myös toisten käyttäjien viestejä/ketjuja
8. Ylläpitäjä voi merkitä minkä tahansa keskustelualueen "salaiseksi" ja määrittää kenellä on sinne pääsy

## Käyttö
Oletuksena että asennettuna git, python3 jne.

1. Kloonaa repo
2. Repossa on jo valmiina venv jossa Flask ja muut tarvittavat riippuvuudet
3. Siirry virtual environmentiin ympäristösi (Linux/Windows) vaatimalla tavalla
4. Aja Flask komennolla `flask run`
