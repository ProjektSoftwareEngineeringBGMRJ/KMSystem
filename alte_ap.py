#Flask-Startpunkt
#from flask import Flask
from models.benutzer import Benutzer
from models.studierende import Studierende
from models.lehrende import Lehrende
from models.admin import Admin
from models.modul import Modul
from models.enums import Kategorie, Sichtbarkeit

# Java -> camelCase, 
# Python -> snake_case

# Admin erstellen
admin = Admin(1, "Administrator", "admin@example.com")

# Lehrende hinzufügen
prof_1 = Lehrende(1,"Mustermann", "mustermann@example.com") 
tutor_1 = Lehrende(2,"super Tutor", "super@example.com")

# Modul hinzufügen
modul_1 = Modul(1, "Software Engineering")
modul_2 = Modul(2, "Literatur")


# Lehrenden Modul zuweisen
admin.modul_zuweisen(modul_1, prof_1)
admin.modul_zuweisen(modul_2, tutor_1)

try:
    modul_2._weise_lehrende_zu(prof_1,prof_1)
except PermissionError as e:
    print("Das ist nicht erlaubt:", e)
    
print(prof_1.name, "betreut: ", [m.titel for m in prof_1.module])
print(modul_1.titel, "wird betreut von: ", [l.name for l in modul_1.lehrende])


# Studierende hinzufügen
student_1 = Studierende(1,"Max", "max@example.com")
student_2 = Studierende(2,"Emma","emma@example.com")
#print(student_1.name)

# Meldung erstellen
meldung_1 = student_1.erstelle_meldung(1,"Fehler in Aufgabe 3", Kategorie.ONLINESKRIPT, modul_1) 
meldung_2 = student_1.erstelle_meldung(2,"Das ist Meldung 2", Kategorie.PDFSKRIPT, modul_2)
meldung_3 = student_2.erstelle_meldung(3,"Das ist Meldung 1 von Student 2", Kategorie.VIDEO, modul_1)


print(meldung_1.beschreibung) # String
print(meldung_1.kategorie.value) ######
print(meldung_1.ersteller.name)
print(meldung_1.modul.titel)
print(meldung_1.status.value)
print(meldung_1.zeitstempel)

# Kommentar hinzufügen
prof_1.add_kommentar(meldung_1, "Hallo", Sichtbarkeit.ÖFFENTLICH)
prof_1.add_kommentar(meldung_1, "Halloooo", Sichtbarkeit.PRIVAT)
prof_1.add_kommentar(meldung_3, "Kommentar für Meldung 3 (von Student 1 erstellt)", Sichtbarkeit.PRIVAT)

try:
    prof_1.add_kommentar(meldung_1, "Ok, das ist privat.")
except PermissionError as e:
    print("Kommentieren nicht möglich:", e)
    
try:
    tutor_1.add_kommentar(meldung_1, "Tutor versucht Meldung von Modul zu kommentieren, was ihm nicht gehört")
except PermissionError as e:
    print("Kommentieren nicht möglich:", e)

# ersten Kommentar anzeigen
print(meldung_1.kommentare[0].text)

print(" ")

# Alle Kommentare einer Meldung anzeigen
for kommentar in meldung_1.kommentare: 
    print(f"{kommentar.lehrende.name}: {kommentar.text} ({kommentar.zeitstempel}, {kommentar.sichtbarkeit})")

for kommentar in student_1.get_sichtbare_kommentare(meldung_1):
    print("Sichtbare Kommentare Student 1: ", kommentar.text)

for kommentar in student_2.get_sichtbare_kommentare(meldung_1):
    print("Sichtbare Kommentare Student 2: ", kommentar.text)


# student_2 zu Admin machen (Rolle zuweisen)
#student_2 = admin.rolle_zuweisen(student_2,Admin)
#for kommentar in student_2.get_sichtbare_kommentare(meldung_1):
#    print("Sichtbare Kommentare student_2 als Admin: ", kommentar.text," von:", kommentar.meldung.ersteller.name) 
  
try:    
    student_2.add_kommentar(meldung_1,"fff",Sichtbarkeit.PRIVAT)
except AttributeError as e:
    print("Kommentieren nicht möglich:", e)
   
