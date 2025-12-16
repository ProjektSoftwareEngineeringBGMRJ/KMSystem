from typing import TYPE_CHECKING
from models.benutzer import Benutzer
from models.datenbank import db
from models.modul import Modul
from models.meldung import Meldung

if TYPE_CHECKING:
    from models.kommentar import Kommentar
    from models.lehrende import Lehrende


class Admin(Benutzer):
    '''
    Repräsentiert einen Administrator.

    Attribute:
        id (int): Primärschlüssel, verknüpft mit der Basisklasse Benutzer.

    Hinweise:
        - Polymorphe Identität 'admin' für SQLAlchemy.
        - Administratoren haben volle Rechte zur Verwaltung von Modulen, Benutzern und Meldungen.
        - Sie können Module erstellen, löschen und Lehrende zuweisen oder entziehen.
        - Sie haben Zugriff auf alle Meldungen und Kommentare im System.
    '''
    __tablename__ = "admin"
    id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin"
    }

    def get_sichtbare_kommentare(self, meldung:"Meldung") -> list["Kommentar"]:
        '''
        Gibt alle Kommentare einer Meldung zurück.

        Besonderheit:
            - Administratoren haben uneingeschränkten Zugriff und sehen alle Kommentare,
              unabhängig von Sichtbarkeit oder Rolle.

        Args:
            meldung (Meldung): Die Meldung, deren Kommentare angezeigt werden sollen.

        Returns:
            List[Kommentar]: Liste aller Kommentare der Meldung.
        '''
        return meldung.kommentare

    def erstelle_modul(self, titel:str) -> "Modul":
        '''
        Erstellt ein neues Modul, sofern es noch nicht existiert.

        Args:
            titel (str): Titel des neuen Moduls.

        Returns:
            Modul: Das neu erstellte Modul.

        Raises:
            ValueError: Falls ein Modul mit dem angegebenen Titel bereits existiert.
        '''
        modul_vorhanden = Modul.query.filter_by(titel=titel).first()
        print(modul_vorhanden)
        if modul_vorhanden:
            raise ValueError(f"Modul \"{titel}\" bereits vorhanden.")

        neues_modul = Modul(titel=titel)
        db.session.add(neues_modul)
        db.session.commit()
        return neues_modul

    # def loesche_modul(self, modul: "Modul") -> bool:
    #     '''
    #     Löscht ein Modul, sofern es keine Meldungen enthält.

    #     Args:
    #         modul (Modul): Das zu löschende Modul.

    #     Returns:
    #         bool: True, wenn das Modul gelöscht wurde, False, wenn es noch Meldungen enthält.
    #     '''
    #     if modul.meldungen:
    #         return False
    #     db.session.delete(modul)
    #     db.session.commit()
    #     return True

    def modul_zuweisen(self, modul: "Modul", lehrende: "Lehrende") -> bool:
        '''
        Weist einem Modul einen Lehrenden zu.

        Args:
            modul (Modul): Das Modul, dem ein Lehrender zugewiesen wird.
            lehrende (Lehrende): Der Lehrende, der zugewiesen werden soll.

        Returns:
            bool: True, wenn die Zuweisung erfolgreich war, 
                  False, wenn der Lehrende bereits zugewiesen ist.
        '''
        if lehrende in modul.lehrende:
            return False

        modul.lehrende.append(lehrende)
        db.session.commit()
        return True

    def modul_entziehen(self, modul: "Modul", lehrende: "Lehrende") -> bool:
        '''
        Entzieht einem Modul einen Lehrenden.

        Args:
            modul (Modul): Das Modul, dem ein Lehrender entzogen wird.
            lehrende (Lehrende): Der Lehrende, der entfernt werden soll.

        Returns:
            bool: True, wenn der Lehrende erfolgreich entfernt wurde, 
                  False, wenn er nicht zugewiesen war.
        '''
        if lehrende not in modul.lehrende:
            return False

        modul.lehrende.remove(lehrende)
        db.session.commit()
        return True

    def get_alle_meldungen(self) -> list["Meldung"]:
        '''
        Gibt alle Meldungen im System zurück.

        Returns:
            List[Meldung]: Liste aller Meldungen.
        '''
        return db.session.query(Meldung).all()

    def get_alle_benutzer(self) -> list[Benutzer]:
        '''
        Gibt alle Benutzer im System zurück.

        Returns:
            List[Benutzer]: Liste aller Benutzer.
        '''
        return db.session.query(Benutzer).all()
