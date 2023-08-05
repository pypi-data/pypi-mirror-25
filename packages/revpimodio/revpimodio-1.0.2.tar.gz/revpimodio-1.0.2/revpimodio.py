#
# python3-RevPiModIO
# Version: 1.0.2
#
# Webpage: https://revpimodio.org/
# (c) Sven Sager, License: LGPLv3
#
# -*- coding: utf-8 -*-
"""Stellt alle Klassen fuer den RevolutionPi zur Verfuegung.

Stellt Klassen fuer die einfache Verwendung des Revolution Pis der
Kunbus GmbH (https://revolution.kunbus.de/) zur Verfuegung. Alle I/Os werden
aus der piCtory Konfiguration eingelesen und mit deren Namen direkt zugreifbar
gemacht. Fuer Gateways sind eigene IOs ueber mehrere Bytes konfigurierbar
Mit den definierten Namen greift man direkt auf die gewuenschten Daten zu.
Auf alle IOs kann der Benutzer Funktionen als Events registrieren. Diese
fuehrt das Modul bei Datenaenderung aus.

"""
import struct
import warnings
from json import load as jload
from os import access, F_OK, R_OK
from signal import signal, SIG_DFL, SIGINT, SIGTERM
from threading import Thread, Event, Lock
from timeit import default_timer

# Globale Werte
OFF = 0
GREEN = 1
RED = 2
RISING = 31
FALLING = 32
BOTH = 33

warnings.simplefilter(action="always")


class RevPiCallback(Thread):

    """Thread fuer das interne Aufrufen von Event-Funktionen.

    Der Eventfunktion, welche dieser Thread aufruft, wird der Thread selber
    als Parameter uebergeben. Darauf muss bei der definition der Funktion
    geachtet werden z.B. "def event(th):". Bei umfangreichen Funktionen kann
    dieser ausgewertet werden um z.B. doppeltes Starten zu verhindern.
    Ueber RevPiCallback.ioname kann der Name des IO-Objekts abgerufen werden,
    welches das Event ausgeloest hast. RevPiCallback.iovalue gibt den Wert des
    IO-Objekts zum Ausloesezeitpunkt zurueck.
    Der Thread stellt das RevPiCallback.exit Event als Abbruchbedingung fuer
    die aufgerufene Funktion zur Verfuegung.
    Durch Aufruf der Funktion RevPiCallback.stop() wird das exit-Event gesetzt
    und kann bei Schleifen zum Abbrechen verwendet werden.
    Mit dem .exit() Event auch eine Wartefunktion realisiert
    werden: "th.exit.wait(0.5)" - Wartet 500ms oder bricht sofort ab, wenn
    fuer den Thread .stop() aufgerufen wird.

    while not th.exit.is_set():
        # IO-Arbeiten
        th.exit.wait(0.5)

    """

    def __init__(self, func, name, value):
        """Init RevPiCallback class.

        @param func Funktion die beim Start aufgerufen werden soll
        @param name IO-Name
        @param value IO-Value zum Zeitpunkt des Events

        """
        super().__init__()
        self.daemon = True
        self.exit = Event()
        self.func = func
        self.ioname = name
        self.iovalue = value

    def run(self):
        """Ruft die registrierte Funktion auf."""
        self.func(self)

    def stop(self):
        """Setzt das exit-Event mit dem die Funktion beendet werden kann."""
        self.exit.set()


class RevPiCycletools():

    """Werkzeugkasten fuer Cycleloop-Funktion.

    Diese Klasse enthaelt Werkzeuge fuer Zyklusfunktionen, wie Taktmerker
    und Flankenmerker.
    Zu beachten ist, dass die Flankenmerker beim ersten Zyklus alle den Wert
    True haben! Ueber den Merker RevPiCycletools.first kann ermittelt werden,
    ob es sich um den ersten Zyklus handelt.

    Taktmerker flag1c, flag5c, flag10c, usw. haben den als Zahl angegebenen
    Wert an Zyklen jeweils False und True.
    Beispiel: flag5c hat 5 Zyklen den Wert False und in den naechsten 5 Zyklen
    den Wert True.

    Flankenmerker flank5c, flank10c, usw. haben immer im, als Zahl angebenen
    Zyklus fuer einen Zyklusdurchlauf den Wert True, sonst False.
    Beispiel: flank5c hat immer alle 5 Zyklen den Wert True.

    Diese Merker koennen z.B. verwendet werden um, an Outputs angeschlossene,
    Lampen synchron blinken zu lassen.

    """

    def __init__(self):
        """Init RevPiCycletools class."""
        self.__cycle = 0
        self.__ucycle = 0
        self.__dict_ton = {}
        self.__dict_tof = {}
        self.__dict_tp = {}

        # Taktmerker
        self.first = True
        self.flag1c = False
        self.flag5c = False
        self.flag10c = False
        self.flag15c = False
        self.flag20c = False

        # Flankenmerker
        self.flank5c = True
        self.flank10c = True
        self.flank15c = True
        self.flank20c = True

    def _docycle(self):
        """Zyklusarbeiten."""
        # Einschaltverzoegerung
        for tof in self.__dict_tof:
            if self.__dict_tof[tof] > 0:
                self.__dict_tof[tof] -= 1

        # Ausschaltverzoegerung
        for ton in self.__dict_ton:
            if self.__dict_ton[ton][1]:
                if self.__dict_ton[ton][0] > 0:
                    self.__dict_ton[ton][0] -= 1
                self.__dict_ton[ton][1] = False
            else:
                self.__dict_ton[ton][0] = -1

        # Impuls
        for tp in self.__dict_tp:
            if self.__dict_tp[tp][1]:
                if self.__dict_tp[tp][0] > 0:
                    self.__dict_tp[tp][0] -= 1
                else:
                    self.__dict_tp[tp][1] = False
            else:
                self.__dict_tp[tp][0] = -1

        # Flankenmerker
        self.flank5c = False
        self.flank10c = False
        self.flank15c = False
        self.flank20c = False

        # Logische Flags
        self.first = False
        self.flag1c = not self.flag1c

        # Berechnete Flags
        self.__cycle += 1
        if self.__cycle == 5:
            self.__ucycle += 1
            if self.__ucycle == 3:
                self.flank15c = True
                self.flag15c = not self.flag15c
                self.__ucycle = 0
            if self.flag5c:
                if self.flag10c:
                    self.flank20c = True
                    self.flag20c = not self.flag20c
                self.flank10c = True
                self.flag10c = not self.flag10c
            self.flank5c = True
            self.flag5c = not self.flag5c
            self.__cycle = 0

    def get_tofc(self, name):
        """Wert der Ausschaltverzoegerung.
        @param name Eindeutiger Name des Timers
        @return Wert der Ausschaltverzoegerung"""
        return self.__dict_tof.get(name, 0) > 0

    def set_tofc(self, name, cycles):
        """Startet bei Aufruf einen ausschaltverzoegerten Timer.

        @param name Eindeutiger Name fuer Zugriff auf Timer
        @param cycles Zyklusanzahl, der Verzoegerung wenn nicht neu gestartet

        """
        self.__dict_tof[name] = cycles

    def get_tonc(self, name):
        """Einschaltverzoegerung.
        @param name Eindeutiger Name des Timers
        @return Wert der Einschaltverzoegerung"""
        return self.__dict_ton.get(name, [-1])[0] == 0

    def set_tonc(self, name, cycles):
        """Startet einen einschaltverzoegerten Timer.

        @param name Eindeutiger Name fuer Zugriff auf Timer
        @param cycles Zyklusanzahl, der Verzoegerung wenn neu gestartet

        """
        if self.__dict_ton.get(name, [-1])[0] == -1:
            self.__dict_ton[name] = [cycles, True]
        else:
            self.__dict_ton[name][1] = True

    def get_tpc(self, name):
        """Impulstimer.
        @param name Eindeutiger Name des Timers
        @return Wert der des Impulses"""
        return self.__dict_tp.get(name, [-1])[0] > 0

    def set_tpc(self, name, cycles):
        """Startet einen Impuls Timer.

        @param name Eindeutiger Name fuer Zugriff auf Timer
        @param cycles Zyklusanzahl, die der Impuls anstehen soll

        """
        if self.__dict_tp.get(name, [-1])[0] == -1:
            self.__dict_tp[name] = [cycles, True]
        else:
            self.__dict_tp[name][1] = True


class RevPiProcimgWriter(Thread):

    """Klasse fuer Synchroniseriungs-Thread.

    Diese Klasse wird als Thread gestartet, wenn das Prozessabbild zyklisch
    synchronisiert werden soll. Diese Funktion wird hauptsaechlich fuer das
    Event-Handling verwendet.

    """

    def __init__(self, procimg, length, refreshlist, monitoring):
        """Init RevPiProcimgWriter class.

        @param procimg Dateiname des piControl Devices
        @param length Laenge des benutzen Speicherbereichs
        @param refreshlist list() mit devices fuer Aktualisierung
        @param monitoring In- und Outputs werden gelesen, niemals geschrieben

        """
        super().__init__()
        self._adjwait = 0
        self._buffedwrite = False
        self._ioerror = 0
        self._length = length
        self._lst_refresh = refreshlist
        self._monitoring = monitoring
        self._procimg = procimg
        self._refresh = 0.05
        self._work = Event()

        self.daemon = True
        self.lck_refresh = Lock()
        self.maxioerrors = 0
        self.newdata = Event()

    def _create_myfh(self, path):
        """Erstellt FileObject.
        param path Pfad zur Datei
        return FileObject"""
        self._buffedwrite = False
        return open(path, "r+b", 0)

    def _gotioerror(self):
        """IOError Verwaltung fuer auto_refresh."""
        self._ioerror += 1
        if self.maxioerrors != 0 and self._ioerror >= self.maxioerrors:
            raise RuntimeError(
                "reach max io error count {} on process image".format(
                    self.maxioerrors
                )
            )
        warnings.warn(
            "count {} io errors on process image".format(self._ioerror),
            RuntimeWarning
        )

    def get_refresh(self):
        """Gibt Zykluszeit zurueck.
        @return int() Zykluszeit in Millisekunden"""
        return int(self._refresh * 1000)

    def run(self):
        """Startet die automatische Prozessabbildsynchronisierung."""
        fh = self._create_myfh(self._procimg)
        self._adjwait = self._refresh
        while not self._work.is_set():
            ot = default_timer()

            # Lockobjekt holen und Fehler werfen, wenn nicht schnell genug
            if not self.lck_refresh.acquire(timeout=self._adjwait):
                warnings.warn(
                    "cycle time of {} ms exceeded on lock".format(
                        int(self._refresh * 1000)
                    ),
                    RuntimeWarning
                )
                continue

            try:
                fh.seek(0)
                bytesbuff = bytearray(fh.read(self._length))
            except IOError:
                self._gotioerror()
                self.lck_refresh.release()
                self._work.wait(self._adjwait)
                continue

            if self._monitoring:
                # Inputs und Outputs in Puffer
                for dev in self._lst_refresh:
                    dev.filelock.acquire()
                    dev._ba_devdata[:] = bytesbuff[dev.slc_devoff]
                    dev.filelock.release()
            else:
                # Inputs in Puffer, Outputs in Prozessabbild
                ioerr = False
                for dev in self._lst_refresh:
                    dev.filelock.acquire()
                    dev._ba_devdata[dev.slc_inp] = bytesbuff[dev.slc_inpoff]
                    try:
                        fh.seek(dev.slc_outoff.start)
                        fh.write(dev._ba_devdata[dev.slc_out])
                    except IOError:
                        ioerr = True
                    finally:
                        dev.filelock.release()

                if self._buffedwrite:
                    try:
                        fh.flush()
                    except IOError:
                        ioerr = True

                if ioerr:
                    self._gotioerror()
                    self.lck_refresh.release()
                    self._work.wait(self._adjwait)
                    continue

            self.lck_refresh.release()

            # Alle aufwecken
            self.newdata.set()
            self._work.wait(self._adjwait)

            # Wartezeit anpassen um echte self._refresh zu erreichen
            if default_timer() - ot >= self._refresh:
                self._adjwait -= 0.001
                if self._adjwait < 0:
                    warnings.warn(
                        "cycle time of {} ms exceeded".format(
                            int(self._refresh * 1000)
                        ),
                        RuntimeWarning
                    )
                    self._adjwait = 0
            else:
                self._adjwait += 0.001

        # Alle am Ende erneut aufwecken
        self.newdata.set()
        fh.close()

    def stop(self):
        """Beendet die automatische Prozessabbildsynchronisierung."""
        self._work.set()

    def set_refresh(self, value):
        """Setzt die Zykluszeit in Millisekunden.
        @param value int() Millisekunden"""
        if value >= 10 and value < 2000:
            self._refresh = value / 1000
            self._adjwait = self._refresh
        else:
            raise ValueError(
                "refresh time must be 10 to 2000 milliseconds"
            )

    refresh = property(get_refresh, set_refresh)


class RevPiModIO():

    """Klasse fuer die Verwaltung aller piCtory Informationen.

    Diese Klasse uebernimmt die gesamte Konfiguration aus piCtory und bilded
    die Devices und IOs ab. Sie uebernimmt die exklusive Verwaltung des
    Prozessabbilds und stellt sicher, dass die Daten synchron sind.
    Sollten nur einzelne Devices gesteuert werden, verwendet man
    RevPiModIOSelected() und uebergibt bei Instantiierung eine Liste mit
    Device Positionen oder Device Namen.

    """

    def __init__(self, **kwargs):
        """Instantiiert die Grundfunktionen.

        @param kwargs Weitere Parameter:
            - auto_refresh: Wenn True, alle Devices zu auto_refresh hinzufuegen
            - configrsc: Pfad zur piCtory Konfigurationsdatei
            - procimg: Pfad zum Prozessabbild
            - monitoring: In- und Outputs werden gelesen, niemals geschrieben
            - simulator: Laed das Modul als Simulator und vertauscht IOs
            - syncoutputs: Aktuell gesetzte Outputs vom Prozessabbild einlesen

        """
        self.auto_refresh = kwargs.get("auto_refresh", False)
        self.configrsc = kwargs.get("configrsc", None)
        self.procimg = kwargs.get("procimg", "/dev/piControl0")
        self.monitoring = kwargs.get("monitoring", False)
        self.simulator = kwargs.get("simulator", False)
        self.syncoutputs = kwargs.get("syncoutputs", True)

        self._cleanupfunc = None
        self._lst_devselect = []

        # piCtory Klassen
        self.app = None
        self.devices = None
        self.summary = None

        # Nur Konfigurieren, wenn nicht vererbt
        if type(self) == RevPiModIO:
            self.configure()

    def __del__(self):
        """Zerstoert alle Klassen um auzuraeumen."""
        if self.devices is not None:
            self.devices.exit(full=True)

    def _evt_exit(self, signum, sigframe):
        """Eventhandler fuer Programmende.
        @param signum Signalnummer
        @param sigframe Signalframe"""
        if self.devices is not None:
            self.devices.exit(full=True)
            if self._cleanupfunc is not None:
                self.devices.readprocimg()
                self._cleanupfunc()
                self.devices.writeprocimg()
        signal(SIGINT, SIG_DFL)
        signal(SIGTERM, SIG_DFL)

    def cleanup(self):
        """Beendet auto_refresh und alle Threads."""
        if self.devices is not None:
            self.devices.exit(full=True)
            self.app = None
            self.devices = None
            self.summary = None

    def configure(self):
        """Verarbeitet die piCtory Konfigurationsdatei."""
        jconfigrsc = self.get_jconfigrsc()

        # App Klasse instantiieren
        self.app = RevPiApp(jconfigrsc["App"])

        # Device Klasse instantiieren
        if len(self._lst_devselect) > 0:
            lst_found = []

            if type(self) == RevPiModIODriver:
                _searchtype = "VIRTUAL"
            else:
                _searchtype = None

            # Angegebene Devices suchen
            for dev in jconfigrsc["Devices"]:
                if _searchtype is None or dev["type"] == _searchtype:
                    if dev["name"] in self._lst_devselect:
                        lst_found.append(dev)
                    elif dev["position"].isnumeric() \
                            and int(dev["position"]) in self._lst_devselect:
                        lst_found.append(dev)

        self.devices = RevPiDevicelist(
            self.procimg,
            (
                jconfigrsc["Devices"] if len(self._lst_devselect) == 0
                else lst_found
            ),
            auto_refresh=self.auto_refresh,
            monitoring=self.monitoring,
            simulator=self.simulator,
            syncoutputs=self.syncoutputs
        )

        # Summary Klasse instantiieren
        self.summary = RevPiSummary(jconfigrsc["Summary"])

    def get_jconfigrsc(self):
        """Laed die piCotry Konfiguration und erstellt ein dict().
        @return dict() der piCtory Konfiguration"""
        # piCtory Konfiguration prüfen
        if self.configrsc is not None:
            if not access(self.configrsc, F_OK | R_OK):
                raise RuntimeError(
                    "can not access pictory configuration at {}".format(
                        self.configrsc))
        else:
            # piCtory Konfiguration an bekannten Stellen prüfen
            lst_rsc = ["/etc/revpi/config.rsc", "/opt/KUNBUS/config.rsc"]
            for rscfile in lst_rsc:
                if access(rscfile, F_OK | R_OK):
                    self.configrsc = rscfile
                    break
            if self.configrsc is None:
                raise RuntimeError(
                    "can not access known pictory configurations at {} - "
                    "use 'configrsc' parameter so specify location"
                    "".format(", ".join(lst_rsc))
                )

        with open(self.configrsc, "r") as fhconfigrsc:
            return jload(fhconfigrsc)

    def handlesignalend(self, cleanupfunc=None):
        """Signalhandler fuer Programmende verwalten.

        Wird diese Funktion aufgerufen, uebernimmt RevPiModIO die SignalHandler
        fuer SIGINT und SIGTERM. Diese werden Empfangen, wenn das
        Betriebssystem oder der Benutzer das Steuerungsprogramm sauber beenden
        will.

        Die optionale Funktion "cleanupfunc" wird als letztes nach dem letzten
        Einlesen der Inputs ausgefuehrt. Dort gesetzte Outputs werden nach
        Ablauf der Funktion ein letztes Mal geschrieben.
        Gedacht ist dies fuer Aufraeumarbeiten, wie z.B. das abschalten der
        LEDs am RevPi-Core.

        Nach einmaligem Empfangen eines der Signale und dem Beenden der
        RevPiModIO Thrads / Funktionen werden die SignalHandler wieder
        freigegeben.

        @param cleanupfunc Funktion wird nach dem letzten Lesen der Inputs
        ausgefuehrt, gefolgt vom letzten Schreiben der Outputs

        """
        # Prüfen ob Funktion callable ist
        if not (cleanupfunc is None or callable(cleanupfunc)):
            raise RuntimeError(
                "registered function '{}' is not callable".format(cleanupfunc)
            )
        self._cleanupfunc = cleanupfunc
        signal(SIGINT, self._evt_exit)
        signal(SIGTERM, self._evt_exit)

    def exit(self, full=True):
        """Beendet mainloop() und optional auto_refresh.
        @see #RevPiDevicelist.exit RevPiDevicelist.exit(...)"""
        if self.devices is not None:
            self.devices.exit(full=full)

    def mainloop(self, freeze=False, blocking=True):
        """Startet den Mainloop mit Eventueberwachung.
        @see #RevPiDevicelist.mainloop RevPiDevicelist.mainloop(...)"""
        if self.devices is not None:
            self.devices.mainloop(freeze=freeze, blocking=blocking)


class RevPiModIOSelected(RevPiModIO):

    """Klasse fuer die Verwaltung einzelner Devices aus piCtory.

    Diese Klasse uebernimmt nur angegebene Devices der piCtory Konfiguration
    und bilded sie inkl. IOs ab. Sie uebernimmt die exklusive Verwaltung des
    Adressbereichs im Prozessabbild an dem sich die angegebenen Devices
    befinden und stellt sicher, dass die Daten synchron sind.

    """

    def __init__(self, deviceselection, **kwargs):
        """Instantiiert nur fuer angegebene Devices die Grundfunktionen.

        Der Parameter deviceselection kann eine einzelne
        Device Position / einzelner Device Name sein oder eine Liste mit
        mehreren Positionen / Namen

        @param deviceselection Positionsnummer oder Devicename
        @param kwargs Weitere Parameter
        @see #RevPiModIO.__init__ RevPiModIO.__init__(...)

        """
        super().__init__(**kwargs)

        # Device liste erstellen
        if type(deviceselection) == list:
            for dev in deviceselection:
                self._lst_devselect.append(dev)
        else:
            self._lst_devselect.append(deviceselection)

        for vdev in self._lst_devselect:
            if type(vdev) != int and type(vdev) != str:
                raise ValueError(
                    "need device position as int() or device name as str()"
                )

        self.configure()

        if len(self.devices._device) == 0:
            if type(self) == RevPiModIODriver:
                raise RuntimeError(
                    "could not find any given VIRTUAL devices in config"
                )
            else:
                raise RuntimeError(
                    "could not find any given devices in config"
                )
        elif len(self.devices._device) != len(self._lst_devselect):
            if type(self) == RevPiModIODriver:
                raise RuntimeError(
                    "could not find all given VIRTUAL devices in config"
                )
            else:
                raise RuntimeError(
                    "could not find all given devices in config"
                )


class RevPiModIODriver(RevPiModIOSelected):

    """Klasse um eigene Treiber fuer die virtuellen Devices zu erstellen.

    Mit dieser Klasse werden nur angegebene Virtuelle Devices mit RevPiModIO
    verwaltet. Bei Instantiierung werden automatisch die Inputs und Outputs
    verdreht, um das Schreiben der Inputs zu ermoeglichen. Die Daten koennen
    dann ueber logiCAD an den Devices abgerufen werden.

    """

    def __init__(self, vdev, **kwargs):
        """Instantiiert die Grundfunktionen.

        @param vdev Virtuelles Device fuer die Verwendung / oder list()
        @param kwargs Weitere Parameter (nicht monitoring und simulator)
        @see #RevPiModIO.__init__ RevPiModIO.__init__(...)

        """
        kwargs["monitoring"] = False
        kwargs["simulator"] = True
        super().__init__(vdev, **kwargs)


class RevPiApp(object):

    """Bildet die App Sektion der config.rsc ab."""

    def __init__(self, app):
        """Instantiiert die RevPiApp-Klasse.
        @param app piCtory Appinformationen"""
        self.name = app["name"]
        self.version = app["version"]
        self.language = app["language"]
        self.layout = app["layout"]


class RevPiSummary(object):

    """Bildet die Summary Sektion der config.rsc ab."""

    def __init__(self, summary):
        """Instantiiert die RevPiSummary-Klasse.
        @param summary piCtory Summaryinformationen"""
        self.inptotal = summary["inpTotal"]
        self.outtotal = summary["outTotal"]


class RevPiDevicelist():

    """Enthaelt alle Devices des RevolutionPi Buses."""

    def __init__(self, procimg, list_devices, **kwargs):
        """Instantiiert die einzelnen Bus-Devices.

        @param procimg Dateiname des piControl Devices
        @param list_devices piCtory Devicesinformationen
        @param kwargs Weitere Parameter:
            - auto_refresh: Wenn True, alle Devices zu auto_refresh hinzufuegen
            - monitoring: In- und Outputs werden gelesen, niemals geschrieben
            - simulator: Laed das Modul als Simulator und vertauscht IOs
            - syncoutputs: Aktuell gesetzte Outputs vom Prozessabbild einlesen

        """
        self._buffedwrite = False
        self._exit = Event()
        self._waitexit = Event()
        self._procimg = procimg
        self.myfh = self._create_myfh(procimg)
        self.core = None
        self._device = []
        self._dict_devname = {}
        self._dict_devposition = {}
        self.imgwriter = None
        self.length = 0
        self._lst_refresh = []
        self._th_mainloop = None
        self._looprunning = False

        self.monitoring = kwargs.get("monitoring", False)
        simulator = kwargs.get("simulator", False)

        err_names = False

        for device in sorted(list_devices, key=lambda x: x["position"]):

            # Bei VDev in alter piCtory Version, Position eindeutig machen
            if device["position"] == "adap.":
                device["position"] = -1
                while device["position"] in self._dict_devposition:
                    device["position"] -= 1

            if device["type"] == "BASE":
                # Core
                dev_new = RevPiCore(device, simulator=simulator)
                self.core = dev_new

                if not (self.monitoring or simulator):
                    # Für RS485 errors defaults laden sollte procimg NULL sein
                    if dev_new._ioerrorlimit1 is not None:
                        dev_new._lst_io[dev_new._ioerrorlimit1].set_value(
                            dev_new._lst_io[
                                dev_new._ioerrorlimit1].defaultvalue
                        )
                    if dev_new._ioerrorlimit2 is not None:
                        dev_new._lst_io[dev_new._ioerrorlimit2].set_value(
                            dev_new._lst_io[
                                dev_new._ioerrorlimit2].defaultvalue
                        )

                    # RS485 errors schreiben
                    self.writeprocimg(True, dev_new)

            elif device["type"] == "LEFT_RIGHT":
                # IOs
                dev_new = RevPiDevice(device, simulator=simulator)
            elif device["type"] == "VIRTUAL":
                # Virtuals
                dev_new = RevPiVirtual(device, simulator=simulator)
            elif device["type"] == "EDGE":
                # Gateways
                dev_new = RevPiGateway(device, simulator=simulator)
            else:
                # Device-Type nicht gefunden
                warnings.warn("device type {} unknown", Warning)
                dev_new = None

            if dev_new is not None:
                self._device.append(dev_new)

                # Offset prüfen, muss mit Länge übereinstimmen
                if self.length < dev_new.offset:
                    self.length = dev_new.offset

                self.length += dev_new.length

                # Auf doppelte Namen prüfen, da piCtory dies zulässt
                if dev_new.name in self._dict_devname:
                    err_names = True

                # Dict()s für schnelle Zugriffe aufbauen
                self._dict_devname[dev_new.name] = dev_new
                self._dict_devposition[dev_new.position] = dev_new

        # dict_devname zerstören, wenn doppelte Namen vorhanden sind
        if err_names:
            self._dict_devname.clear()
            warnings.warn(
                "equal device names in pictory configuration. can not "
                "build name dictionary. you can access all devices by "
                "position number only!",
                Warning
            )

        if kwargs.get("syncoutputs", True):
            # Aktuellen Outputstatus von procimg einlesen
            self.syncoutputs(force=True)

        # Optional ins auto_refresh aufnehmen
        if kwargs.get("auto_refresh", False):
            for dev in self._device:
                self.auto_refresh(dev)

    def __contains__(self, key):
        """Prueft ob Device existiert.
        @param key DeviceName str() / Positionsnummer int()
        @return True, wenn device vorhanden"""
        if type(key) == str:
            return key in self._dict_devname
        if type(key) == int:
            return key in self._dict_devposition
        else:
            return key in self._device

    def __del__(self):
        """FileHandler und RevPiProcimgWriter beenden."""
        if self.imgwriter is not None:
            self.imgwriter.stop()
        if not self.myfh.closed:
            self.myfh.close()

    def __getitem__(self, key):
        """Gibt angegebenes Device zurueck.
        @param key DeviceName str() / Positionsnummer int()
        @return Gefundenes RevPiDevice()-Objekt"""
        if type(key) == str:
            return self._dict_devname[key]
        if type(key) == int:
            return self._dict_devposition[key]
        else:
            raise KeyError(
                "need device name as str() or device position as int()"
            )

    def __iter__(self):
        """Gibt alle Devices zurueck.
        @return Iterator alle Devices"""
        return iter(self._device)

    def __len__(self):
        """Gibt Anzahl der Devices zurueck.
        @return int() Anzalh der Devices"""
        return len(self._device)

    def _create_myfh(self, path):
        """Erstellt FileObject.
        param path Pfad zur Datei
        return FileObject"""
        self._buffedwrite = False
        return open(path, "r+b", 0)

    def auto_refresh(self, device, remove=False):
        """Registriert ein Device fuer die automatische Synchronisierung.
        @param device Device fuer Synchronisierung
        @param remove bool() True entfernt Device aus Synchronisierung"""

        dev = device if issubclass(type(device), RevPiDevice) \
            else self.__getitem__(device)

        if not remove and dev not in self._lst_refresh:

            # Daten bei Aufnahme direkt einlesen!
            self.readprocimg(True, dev)

            # Datenkopie anlegen
            dev.filelock.acquire()
            dev._ba_datacp = dev._ba_devdata[:]
            dev.filelock.release()

            dev._selfupdate = True
            self._lst_refresh.append(dev)

            # Thread starten, wenn er noch nicht läuft
            if self.imgwriter is None or not self.imgwriter.is_alive():
                self.imgwriter = RevPiProcimgWriter(
                    self._procimg,
                    self.length,
                    self._lst_refresh,
                    self.monitoring
                )
                self.imgwriter.start()

        elif remove and dev in self._lst_refresh:
            # Sicher aus Liste entfernen
            with self.imgwriter.lck_refresh:
                self._lst_refresh.remove(dev)
            dev._selfupdate = False

            # Beenden, wenn keien Devices mehr in Liste sind
            if len(self.imgwriter._lst_refresh) == 0:
                self.imgwriter.stop()

            # Daten beim Entfernen noch einmal schreiben
            if not self.monitoring:
                self.writeprocimg(True, dev)

    def auto_refresh_maxioerrors(self, value=None):
        """Maximale IO Fehler fuer auto_refresh.
        @param value Setzt maximale Anzahl bis exception ausgeloest wird
        @return Maximale Anzahl bis exception ausgeloest wird"""
        if value is None:
            return self.imgwriter.maxioerrors
        elif type(value) == int and value >= 0:
            self.imgwriter.maxioerrors = value

    def auto_refresh_resetioerrors(self):
        """Setzt aktuellen IOError-Zaehler auf 0 zurueck."""
        if self.imgwriter is not None:
            self.imgwriter.maxioerrors = 0

    def cycleloop(self, func, cycletime=None):
        """Startet den Cycleloop.

        Der aktuelle Programmthread wird hier bis Aufruf von
        RevPiDevicelist.exit() "gefangen". Er fuehrt nach jeder Aktualisierung
        des Prozessabbilds die uebergebene Funktion "func" aus und arbeitet sie
        ab. Waehrend der Ausfuehrung der Funktion wird das Prozessabbild nicht
        weiter aktualisiert. Die Inputs behalten bis zum Ende den aktuellen
        Wert. Gesetzte Outputs werden nach Ende des Funktionsdurchlaufs in das
        Prozessabbild geschrieben.

        Verlassen wird der Cycleloop, wenn die aufgerufene Funktion einen
        Rueckgabewert nicht gleich None liefert, oder durch Aufruf von
        revpimodio.exit().

        HINWEIS: Die Aktualisierungszeit und die Laufzeit der Funktion duerfen
        die eingestellte auto_refresh Zeit, bzw. uebergebene cycletime nicht
        ueberschreiten!

        Ueber den Parameter cycletime kann die Aktualisierungsrate fuer das
        Prozessabbild gesetzt werden (selbe Funktion wie
        set_refreshtime(milliseconds)).

        @param func Funktion, die ausgefuehrt werden soll
        @param cycletime Zykluszeit in Millisekunden, bei Nichtangabe wird
               aktuelle auto_refresh Zeit verwendet - Standardwert 50 ms
        @return None

        """
        # Prüfen ob ein Loop bereits läuft
        if self._looprunning:
            raise RuntimeError(
                "can not start multiple loops mainloop/cycleloop"
            )

        # Prüfen ob Devices in auto_refresh sind
        if len(self._lst_refresh) == 0:
            raise RuntimeError("no device with auto_refresh activated")

        # Prüfen ob Funktion callable ist
        if not callable(func):
            raise RuntimeError(
                "registered function '{}' ist not callable".format(func)
            )

        # Zykluszeit übernehmen
        if not (cycletime is None or cycletime == self.imgwriter.refresh):
            self.imgwriter.refresh = cycletime

        # Cycleloop starten
        self._looprunning = True
        cycleinfo = RevPiCycletools()
        ec = None
        while ec is None and not self._exit.is_set():
            # Auf neue Daten warten und nur ausführen wenn set()
            if not self.imgwriter.newdata.wait(2.5):
                if not self._exit.is_set() and not self.imgwriter.is_alive():
                    raise RuntimeError("auto_refresh thread not running")
                continue
            self.imgwriter.newdata.clear()

            # Vor Aufruf der Funktion auto_refresh sperren
            self.imgwriter.lck_refresh.acquire()

            # Funktion aufrufen und auswerten
            ec = func(cycleinfo)
            cycleinfo._docycle()

            # auto_refresh freigeben
            self.imgwriter.lck_refresh.release()

        # Cycleloop beenden
        self._looprunning = False

        return ec

    def exit(self, full=True):
        """Beendet mainloop() und optional auto_refresh.

        Wenn sich das Programm im mainloop() befindet, wird durch Aufruf
        von exit() die Kontrolle wieder an das Hauptprogramm zurueckgegeben.

        Der Parameter full ist mit True vorbelegt und entfernt alle Devices aus
        dem auto_refresh. Der Thread fuer die Prozessabbildsynchronisierung
        wird dann gestoppt und das Programm kann sauber beendet werden.

        @param full Entfernt auch alle Devices aus auto_refresh"""
        self._exit.set()
        self._waitexit.set()
        if full and self.imgwriter is not None:
            self.imgwriter.stop()
            self.imgwriter.join(self.imgwriter._refresh)
            while len(self._lst_refresh) > 0:
                dev = self._lst_refresh.pop()
                dev._selfupdate = False
                if not self.monitoring:
                    self.writeprocimg(True, dev)

    def get_devbyname(self, name):
        """Gibt durch Namen angegebenes Device zurueck.
        @param name Devicename aus piCtory
        @return Gefundenes RevPiDevice()"""
        return self._dict_devname[name]

    def get_devbyposition(self, position):
        """Gibt durch Position angegebenes Device zurueck.
        @param position Deviceposition aus piCtory
        @return Gefundenes RevPiDevice()"""
        return self._dict_devposition[position]

    def get_refreshtime(self):
        """Gibt Aktualisierungsrate in ms der Prozessabbildsynchronisierung aus.
        @return Millisekunden"""
        return self.imgwriter.refresh

    def readprocimg(self, force=False, device=None):
        """Einlesen aller Inputs aller Devices vom Prozessabbild.

        @param force auch Devices mit autoupdate=False
        @param device nur auf einzelnes Device anwenden
        @return True, wenn Arbeiten an allen Devices erfolgreich waren

        """
        if device is None:
            mylist = self._device
        else:
            dev = device if issubclass(type(device), RevPiDevice) \
                else self.__getitem__(device)

            if dev._selfupdate:
                raise RuntimeError(
                    "can not read process image, while device '{}|{}'"
                    "is in auto_refresh mode".format(dev.position, dev.name)
                )
            mylist = [dev]

        # Daten komplett einlesen
        try:
            self.myfh.seek(0)
            bytesbuff = self.myfh.read(self.length)
        except IOError:
            warnings.warn(
                "read error on process image '{}'".format(self.myfh.name),
                RuntimeWarning
            )
            return False

        for dev in mylist:
            if (force or dev.autoupdate) and not dev._selfupdate:

                # FileHandler sperren
                dev.filelock.acquire()

                if self.monitoring:
                    # Alles vom Bus einlesen
                    dev._ba_devdata[:] = bytesbuff[dev.slc_devoff]
                else:
                    # Inputs vom Bus einlesen
                    dev._ba_devdata[dev.slc_inp] = bytesbuff[dev.slc_inpoff]

                    # Mems vom Bus lesen
                    dev._ba_devdata[dev.slc_mem] = bytesbuff[dev.slc_memoff]

                dev.filelock.release()

        return True

    def mainloop(self, freeze=False, blocking=True):
        """Startet den Mainloop mit Eventueberwachung.

        Der aktuelle Programmthread wird hier bis Aufruf von
        RevPiDevicelist.exit() "gefangen" (es sei denn blocking=False). Er
        durchlaeuft die Eventueberwachung und prueft Aenderungen der, mit
        einem Event registrierten, IOs. Wird eine Veraenderung erkannt,
        fuert das Programm die dazugehoerigen Funktionen der Reihe nach aus.

        Wenn der Parameter "freeze" mit True angegeben ist, wird die
        Prozessabbildsynchronisierung angehalten bis alle Eventfunktionen
        ausgefuehrt wurden. Inputs behalten fuer die gesamte Dauer ihren
        aktuellen Wert und Outputs werden erst nach Durchlauf aller Funktionen
        in das Prozessabbild geschrieben.

        Wenn der Parameter "blocking" mit False angegeben wird, aktiviert
        dies die Eventueberwachung und blockiert das Programm NICHT an der
        Stelle des Aufrufs. Eignet sich gut fuer die GUI Programmierung, wenn
        Events vom RevPi benoetigt werden, aber das Programm weiter ausgefuehrt
        werden soll.

        @param freeze Wenn True, Prozessabbildsynchronisierung anhalten
        @param blocking Wenn False, blockiert das Programm NICHT
        @return None

        """
        # Prüfen ob ein Loop bereits läuft
        if self._looprunning:
            raise RuntimeError(
                "can not start multiple loops mainloop/cycleloop"
            )

        # Prüfen ob Devices in auto_refresh sind
        if len(self._lst_refresh) == 0:
            raise RuntimeError("no device with auto_refresh activated")

        # Thread erstellen, wenn nicht blockieren soll
        if not blocking:
            self._th_mainloop = Thread(
                target=self.mainloop,
                kwargs={"freeze": freeze, "blocking": True}
            )
            self._th_mainloop.start()
            return

        # Event säubern vor Eintritt in Mainloop
        self._exit.clear()
        self._looprunning = True

        # Beim Eintritt in mainloop Bytecopy erstellen
        for dev in self._lst_refresh:
            dev.filelock.acquire()
            dev._ba_datacp = dev._ba_devdata[:]
            dev.filelock.release()

        lst_fire = []
        while not self._exit.is_set():

            # Auf neue Daten warten und nur ausführen wenn set()
            if not self.imgwriter.newdata.wait(2.5):
                if not self._exit.is_set() and not self.imgwriter.is_alive():
                    raise RuntimeError("auto_refresh thread not running")
                continue

            self.imgwriter.newdata.clear()

            # Während Auswertung refresh sperren
            self.imgwriter.lck_refresh.acquire()

            for dev in self._lst_refresh:

                if len(dev._dict_events) == 0 \
                        or dev._ba_datacp == dev._ba_devdata:
                    continue

                for io_event in dev._dict_events:

                    if dev._ba_datacp[io_event.slc_address] == \
                            dev._ba_devdata[io_event.slc_address]:
                        continue

                    if io_event._bitaddress >= 0:
                        boolcp = bool(int.from_bytes(
                            dev._ba_datacp[io_event.slc_address],
                            byteorder=io_event._byteorder
                        ) & 1 << io_event._bitaddress)
                        boolor = bool(int.from_bytes(
                            dev._ba_devdata[io_event.slc_address],
                            byteorder=io_event._byteorder
                        ) & 1 << io_event._bitaddress)

                        if boolor == boolcp:
                            continue

                        for regfunc in dev._dict_events[io_event]:
                            if regfunc[1] == BOTH \
                                    or regfunc[1] == RISING and boolor \
                                    or regfunc[1] == FALLING and not boolor:
                                lst_fire.append(
                                    (regfunc, io_event.name, io_event.value)
                                )

                    else:
                        for regfunc in dev._dict_events[io_event]:
                            lst_fire.append(
                                (regfunc, io_event.name, io_event.value)
                            )

                # Nach Verarbeitung aller IOs die Bytes kopieren
                dev.filelock.acquire()
                dev._ba_datacp = dev._ba_devdata[:]
                dev.filelock.release()

            # Refreshsperre aufheben wenn nicht freeze
            if not freeze:
                self.imgwriter.lck_refresh.release()

            # Erst nach Datenübernahme alle Events feuern
            while len(lst_fire) > 0:
                tup_fire = lst_fire.pop()
                event_func = tup_fire[0][0]
                passname = tup_fire[1]
                passvalue = tup_fire[2]
                if tup_fire[0][2]:
                    th = RevPiCallback(
                        event_func, passname, passvalue
                    )
                    th.start()
                else:
                    # Direct callen da Prüfung in RevPiDevice.reg_event ist
                    event_func(passname, passvalue)

            # Refreshsperre aufheben wenn freeze
            if freeze:
                self.imgwriter.lck_refresh.release()

        # Mainloop verlassen
        self._looprunning = False

    def set_refreshtime(self, milliseconds):
        """Setzt Aktualisierungsrate der Prozessabbild-Synchronisierung.
        @param milliseconds int() in Millisekunden"""
        self.imgwriter.refresh = milliseconds

    def setdefaultvalues(self, force=False, device=None):
        """Alle Outputbuffer werden auf die piCtory default Werte gesetzt.
        @param force auch Devices mit autoupdate=False
        @param device nur auf einzelnes Device anwenden"""
        if self.monitoring:
            raise RuntimeError(
                "can not set default values, while system is in monitoring "
                "mode"
            )

        if device is None:
            mylist = self._device
        else:
            dev = device if issubclass(type(device), RevPiDevice) \
                else self.__getitem__(device)
            mylist = [dev]

        for dev in mylist:
            if (force or dev.autoupdate):
                for io in dev._lst_io:
                    if not io._readonly:
                        io.set_value(io.defaultvalue)

    def syncoutputs(self, force=False, device=None):
        """Lesen aller aktuell gesetzten Outputs im Prozessabbild.

        @param force auch Devices mit autoupdate=False
        @param device nur auf einzelnes Device anwenden
        @return True, wenn Arbeiten an allen Devices erfolgreich waren

        """
        if device is None:
            mylist = self._device
        else:
            dev = device if issubclass(type(device), RevPiDevice) \
                else self.__getitem__(device)

            if dev._selfupdate:
                raise RuntimeError(
                    "can not sync process image, while device '{}|{}'"
                    "is in auto_refresh mode".format(dev.position, dev.name)
                )
            mylist = [dev]

        try:
            self.myfh.seek(0)
            bytesbuff = self.myfh.read(self.length)
        except IOError:
            warnings.warn(
                "read error on process image '{}'".format(self.myfh.name),
                RuntimeWarning
            )
            return False

        for dev in mylist:
            if (force or dev.autoupdate) and not dev._selfupdate:
                dev.filelock.acquire()
                # Outputs vom Bus einlesen
                dev._ba_devdata[dev.slc_out] = bytesbuff[dev.slc_outoff]
                dev.filelock.release()
        return True

    def updateprocimg(self, force=False, device=None):
        """Schreiben/Lesen aller Outputs/Inputs aller Devices im Prozessab.

        @param force auch Devices mit autoupdate=False
        @param device nur auf einzelnes Device anwenden
        @return True, wenn Arbeiten an allen Devices erfolgreich waren

        """
        return self.readprocimg(force=force, device=device) and \
            self.writeprocimg(force=force, device=device)

    def wait(self, device, io, **kwargs):
        """Wartet auf Wertaenderung eines IOs.

        Die Wertaenderung wird immer uerberprueft, wenn fuer Devices
        in RevPiDevicelist.auto_refresh() neue Daten gelesen wurden.

        Bei Wertaenderung, wird das Warten mit 0 als Rueckgabewert beendet.

        HINWEIS: Wenn RevPiProcimgWriter() keine neuen Daten liefert, wird
        bis in die Ewigkeit gewartet (nicht bei Angabe von "timeout").

        Wenn edge mit RISING oder FALLING angegeben wird muss diese Flanke
        ausgeloest werden. Sollte der Wert 1 sein beim Eintritt mit Flanke
        RISING, wird das Warten erst bei Aenderung von 0 auf 1 beendet.

        Als exitevent kann ein threading.Event()-Objekt uebergeben werden,
        welches das Warten bei is_set() sofort mit 1 als Rueckgabewert
        beendet.

        Wenn der Wert okvalue an dem IO fuer das Warten anliegt, wird
        das Warten sofort mit -1 als Rueckgabewert beendet.

        Der Timeoutwert bricht beim Erreichen das Warten sofort mit
        Wert 2 Rueckgabewert ab. (Das Timeout wird ueber die Zykluszeit
        der auto_refresh Funktion berechnet, entspricht also nicht exact den
        angegeben Millisekunden! Es wird immer nach oben gerundet!)

        @param device Device auf dem sich der IO befindet
        @param io Name des IOs auf dessen Aenderung gewartet wird
        @param kwargs Weitere Parameter:
            - edge: Flanke RISING, FALLING, BOTH bei der mit True beendet wird
            - exitevent: thrading.Event() fuer vorzeitiges Beenden mit False
            - okvalue: IO-Wert, bei dem das Warten sofort mit True beendet wird
            - timeout: Zeit in ms nach der mit False abgebrochen wird
        @return int() erfolgreich Werte <= 0
            - Erfolgreich gewartet
                Wert 0: IO hat den Wert gewechselt
                Wert -1: okvalue stimmte mit IO ueberein
            - Fehlerhaft gewartet
                Wert 1: exitevent wurde gesetzt
                Wert 2: timeout abgelaufen
                Wert 100: RevPiDevicelist.exit() wurde aufgerufen

        """
        dev = device if issubclass(type(device), RevPiDevice) \
            else self.__getitem__(device)

        # Prüfen ob Device in auto_refresh ist
        if not dev._selfupdate:
            raise RuntimeError(
                "auto_refresh is not activated for device '{}|{}' - there "
                "will never be new data".format(dev.position, dev.name)
            )

        io_watch = dev[io]
        if type(io_watch) == list:
            if len(io_watch) == 1:
                io_watch = io_watch[0]
            else:
                raise KeyError(
                    "byte '{}' contains more than one bit-input".format(io)
                )
        val_start = io_watch.value

        # kwargs auswerten
        edge = kwargs.get("edge", None)
        evt_exit = kwargs.get("exitevent", Event())
        val_ok = kwargs.get("okvalue", None)
        flt_timeout = kwargs.get("timeout", 0) / 1000
        bool_timecount = flt_timeout > 0

        if edge is not None and io_watch._bitaddress < 0:
            raise AttributeError(
                "parameter 'edge' can be used with bit Inputs only"
            )

        # Edge auflösen, wenn nicht angegeben
        if edge is None:
            edge = BOTH

        # Abbruchwert prüfen
        if val_ok == io_watch.value:
            return -1

        # WaitExit Event säubern
        self._waitexit.clear()

        flt_timecount = 0 if bool_timecount else -1
        while not self._waitexit.is_set() and not evt_exit.is_set() \
                and flt_timecount < flt_timeout:
            if self.imgwriter.newdata.wait(2.5):
                self.imgwriter.newdata.clear()

                if val_start != io_watch.value:
                    if edge == BOTH \
                            or edge == RISING and not val_start \
                            or edge == FALLING and val_start:
                        return 0
                    else:
                        val_start = not val_start
                if bool_timecount:
                    flt_timecount += self.imgwriter._refresh
            elif bool_timecount:
                flt_timecount += 1

        # Abbruchevent wurde gesetzt
        if evt_exit.is_set():
            return 1

        # RevPiModIO mainloop wurde verlassen
        if self._waitexit.is_set():
            return 100

        # Timeout abgelaufen
        return 2

    def writedefaultinputs(self, virtual_device):
        """Schreibt fuer ein virtuelles Device piCtory Defaultinputwerte.

        Sollten in piCtory Defaultwerte fuer Inputs eines virtuellen Devices
        angegeben sein, werden diese nur beim Systemstart oder einem piControl
        Reset gesetzt. Sollte danach das Prozessabbild mit NULL ueberschrieben,
        gehen diese Werte verloren.
        Diese Funktion kann nur auf virtuelle Devices angewendet werden!

        @param virtual_device Virtuelles Device fuer Wiederherstellung
        @return True, wenn Arbeiten am virtuellen Device erfolgreich waren

        """
        if self.monitoring:
            raise RuntimeError(
                "can not write process image, while system is in monitoring "
                "mode"
            )

        # Device suchen
        dev = virtual_device if issubclass(type(virtual_device), RevPiDevice) \
            else self.__getitem__(virtual_device)

        # Prüfen ob es ein virtuelles Device ist
        if not issubclass(type(dev), RevPiVirtual):
            raise RuntimeError(
                "this function can be used for virtual devices only"
            )

        workokay = True
        dev.filelock.acquire()

        for io in dev._lst_io:
            if io._readonly:
                dev._ba_devdata[io.slc_address] = io.defaultvalue

        # Outpus auf Bus schreiben
        try:
            self.myfh.seek(dev.slc_inpoff.start)
            self.myfh.write(dev._ba_devdata[dev.slc_inp])
            if self._buffedwrite:
                self.myfh.flush()
        except IOError:
            warnings.warn(
                "write error on process image '{}'"
                "".format(self.myfh.name),
                RuntimeWarning
            )
            workokay = False

        dev.filelock.release()
        return workokay

    def writeprocimg(self, force=False, device=None):
        """Schreiben aller Outputs aller Devices ins Prozessabbild.

        @param force auch Devices mit autoupdate=False
        @param device nur auf einzelnes Device anwenden
        @return True, wenn Arbeiten an allen Devices erfolgreich waren

        """
        if self.monitoring:
            raise RuntimeError(
                "can not write process image, while system is in monitoring "
                "mode"
            )

        if device is None:
            mylist = self._device
        else:
            dev = device if issubclass(type(device), RevPiDevice) \
                else self.__getitem__(device)

            if dev._selfupdate:
                raise RuntimeError(
                    "can not write process image, while device '{}|{}'"
                    "is in auto_refresh mode".format(dev.position, dev.name)
                )
            mylist = [dev]

        workokay = True
        for dev in mylist:
            if (force or dev.autoupdate) and not dev._selfupdate:
                dev.filelock.acquire()

                # Outpus auf Bus schreiben
                try:
                    self.myfh.seek(dev.slc_outoff.start)
                    self.myfh.write(dev._ba_devdata[dev.slc_out])
                except IOError:
                    workokay = False

                dev.filelock.release()

        if self._buffedwrite:
            try:
                self.myfh.flush()
            except IOError:
                workokay = False

        if not workokay:
            warnings.warn(
                "write error on process image '{}'"
                "".format(self.myfh.name),
                RuntimeWarning
            )

        return workokay


class RevPiDevice(object):

    """Basisklasse fuer alle Device-Objekte der RevPiDevicelist()-Klasse.

    Die Basisfunktionalitaet generiert bei Instantiierung alle IOs und
    erweitert den Prozessabbildpuffer um die benoetigten Bytes. Ueber diese
    Klasse oder von dieser abgeleiteten Klassen, werden alle IOs angesprochen.
    Sie verwaltet ihren Prozessabbildpuffer und sorgt fuer die Aktualisierung
    der IO-Werte.

    """

    def __init__(self, dict_device, **kwargs):
        """Instantiierung der RevPiDevice()-Klasse.

        @param dict_device dict() fuer dieses Device aus piCotry Konfiguration
        @param kwargs Weitere Parameter:
            - autoupdate: Wenn True fuehrt dieses Device Arbeiten am
              Prozessabbild bei Aufruf der RevPiDevicelist-Funktionen aus
            - simulator: Laed das Modul als Simulator und vertauscht IOs

        """
        self._selfupdate = False
        self.autoupdate = kwargs.get("autoupdate", True)
        self._dict_ioname = {}
        self._dict_events = {}
        self.filelock = Lock()
        self._lst_io = []
        self.length = 0

        # Wertzuweisung aus dict_device
        self.name = dict_device.pop("name")
        self.offset = int(dict_device.pop("offset"))
        self.position = int(dict_device.pop("position"))
        self.producttype = int(dict_device.pop("productType"))

        # Neues bytearray und Kopie für mainloop anlegen
        self._ba_devdata = bytearray()
        self._ba_datacp = bytearray()

        # Erst inp/out/mem poppen, dann in Klasse einfügen
        if kwargs.get("simulator", False):
            self.slc_inp = self._buildio(dict_device.pop("out"), True)
            self.slc_out = self._buildio(dict_device.pop("inp"), False)
        else:
            self.slc_inp = self._buildio(dict_device.pop("inp"), True)
            self.slc_out = self._buildio(dict_device.pop("out"), False)
        self.slc_mem = self._buildio(dict_device.pop("mem"), True)

        # Alle IOs nach Adresse sortieren
        self._lst_io.sort(key=lambda x: x.slc_address.start)

        # SLCs mit offset berechnen
        self.slc_devoff = slice(self.offset, self.offset + self.length)
        self.slc_inpoff = slice(
            self.slc_inp.start + self.offset, self.slc_inp.stop + self.offset
        )
        self.slc_outoff = slice(
            self.slc_out.start + self.offset, self.slc_out.stop + self.offset
        )
        self.slc_memoff = slice(
            self.slc_mem.start + self.offset, self.slc_mem.stop + self.offset
        )

        # Byteadressen im Dict führen
        self._dict_iobyte = {k: [] for k in range(self.length)}
        for io in self._lst_io:
            if io._bitaddress < 0:
                self._dict_iobyte[io.slc_address.start].append(io)
            else:
                if len(self._dict_iobyte[io.slc_address.start]) != 8:
                    # "schnell" 8 Einträge erstellen da es BIT IOs sind
                    self._dict_iobyte[io.slc_address.start] += [
                        None, None, None, None, None, None, None, None
                    ]

                self._dict_iobyte[io.slc_address.start][io._bitaddress] = io

        # Alle restlichen attribute an Klasse anhängen
        self.__dict__.update(dict_device)

        # Spezielle Konfiguration von abgeleiteten Klassen durchführen
        self._devconfigure()

    def __bytes__(self):
        """Gibt alle Daten des Devices als bytes() zurueck.
        @return Devicedaten als bytes()"""
        return bytes(self._ba_devdata)

    def __contains__(self, key):
        """Prueft ob IO existiert.
        @param key IO-Name str() / Positionsnummer int()
        @return True, wenn device vorhanden"""
        if type(key) == str:
            return key in self._dict_ioname
        if type(key) == int:
            return key in self._dict_iobyte \
                and len(self._dict_iobyte[key]) > 0
        else:
            return key in self._lst_io

    def __getitem__(self, key):
        """Gibt angegebenes IO-Objekt zurueck.
        @param key Name order Byteadresse des IOs
        @return IO-Objekt wenn Name, sonst list() mit IO-Objekt"""
        if type(key) == int:
            if key in self._dict_iobyte:
                return self._dict_iobyte[key]
            else:
                raise KeyError("byte '{}' does not exist".format(key))
        else:
            if key in self._dict_ioname:
                return self._dict_ioname[key]
            else:
                raise KeyError("'{}' does not exist".format(key))

    def __int__(self):
        """Gibt die Positon im RevPi Bus zurueck.
        @return Positionsnummer"""
        return self.position

    def __iter__(self):
        """Gibt Iterator aller IOs zurueck.
        @return iter() alle IOs"""
        return iter(self._lst_io)

    def __str__(self):
        """Gibt den Namen des Devices zurueck.
        @return Devicename"""
        return self.name

    def __setitem__(self, key, value):
        """Setzt den Wert des angegebenen Inputs.
        @param key Name oder Byte des Inputs
        @param value Wert der gesetzt werden soll"""
        if type(key) == int:
            if key in self._dict_iobyte:
                if len(self._dict_iobyte[key]) == 1:
                    self._dict_iobyte[key][0].value = value
                elif len(self._dict_iobyte[key]) == 0:
                    raise KeyError("byte '{}' contains no input".format(key))
                else:
                    raise KeyError(
                        "byte '{}' contains more than one bit-input"
                        "".format(key)
                    )
            else:
                raise KeyError("byte '{}' does not exist".format(key))
        else:
            self._dict_ioname[key].value = value

    def _buildio(self, dict_io, readonly):
        """Erstellt aus der piCtory-Liste die IOs fuer dieses Device.

        @param dict_io dict()-Objekt aus piCtory Konfiguration
        @param readonly True bei inp und mem, False bei out
        @return slice()-Objekt mit Start und Stop Position dieser IOs

        """
        if len(dict_io) > 0:
            int_min, int_max = 4096, 0
            for key in sorted(dict_io, key=lambda x: int(x)):

                # Neuen IO anlegen
                if bool(dict_io[key][7]) or self.producttype == 95:
                    # Bei Bitwerten oder Core RevPiIOBase verwenden
                    io_new = RevPiIOBase(
                        self.offset,
                        dict_io[key],
                        readonly,
                        self._ba_devdata,
                        byteorder="little"
                    )
                else:
                    io_new = RevPiIO(
                        self.offset,
                        dict_io[key],
                        readonly,
                        self._ba_devdata,
                        byteorder="little",
                        signed=self.producttype == 103
                    )

                # IO registrieren
                if io_new.name in self._dict_ioname:
                    raise NameError(
                        "name '{}' already exists on device '{}'".format(
                            io_new._name, self.name
                        )
                    )
                else:
                    # Namesregister aufbauen
                    self._dict_ioname[io_new._name] = io_new

                    # Speicherbereich zuweisen
                    self._ba_devdata.extend(bytes(io_new.length))

                    # IO eintragen
                    self._lst_io.append(io_new)
                    self.length += io_new.length

                # Kleinste und größte Speicheradresse ermitteln
                if io_new.slc_address.start < int_min:
                    int_min = io_new.slc_address.start
                if io_new.slc_address.stop > int_max:
                    int_max = io_new.slc_address.stop

            return slice(int_min, int_max)

        else:
            return slice(0, 0)

    def _devconfigure(self):
        """Funktion zum ueberschreiben von abgeleiteten Klassen."""
        pass

    def get_inps(self):
        """Gibt eine Liste aller Inputs zurueck.
        @return list() Inputs"""
        return [
            io for io in self._lst_io if
            self.slc_inp.start <= io.slc_address.start < self.slc_inp.stop
        ]

    def get_outs(self):
        """Gibt eine Liste aller Outputs zurueck.
        @return list() Outputs"""
        return [
            io for io in self._lst_io if
            self.slc_out.start <= io.slc_address.start < self.slc_out.stop
        ]

    def get_mems(self):
        """Gibt eine Liste aller mems zurueck.
        @return list() Mems"""
        return [
            io for io in self._lst_io if
            self.slc_mem.start <= io.slc_address.start < self.slc_mem.stop
        ]

    def get_iobyabsaddress(self, address):
        """Gibt das IO-Objekt an angegebenen Byte im Prozessabbild zurueck.
        @param address Byteadresse im Prozessabbild
        @return list() mit IO-Objekt/en"""
        return self._dict_iobyte[address - self.offset]

    def get_iobyaddress(self, address):
        """Gibt das IO-Objekt an angegebenen Byte zurueck.
        @param address Byteadresse im Deviceabbild
        @return list() mit IO-Objekt/en"""
        return self._dict_iobyte[address]

    def get_iobyname(self, name):
        """Gibt das IO-Objekt mit angegebenen Namen zurueck.
        @param name Name des IO-Objekts
        @return IO-Objekt"""
        return self._dict_ioname[name]

    def reg_event(self, io_name, func, **kwargs):
        """Registriert ein Event bei der Eventueberwachung.

        @param io_name Name des Inputs oder Outputs der ueberwacht wird
        @param func Funktion die bei Aenderung aufgerufen werden soll
        @param kwargs Weitere Parameter:
            - as_thread: Bei True, Funktion als RevPiCallback-Thread ausfuehren
            - edge: Ausfuehren bei RISING, FALLING or BOTH Wertaenderung

        """
        as_thread = kwargs.get("as_thread", False)
        edge = kwargs.get("edge", None)

        io_event = self.__getitem__(io_name)
        if type(io_event) == list:
            if len(io_event) == 1:
                io_event = io_event[0]
            elif len(io_event) == 0:
                raise KeyError(
                    "byte '{}' contains no io object".format(io_name))
            else:
                raise KeyError(
                    "byte '{}' contains more than one bit io object".format(
                        io_name
                    )
                )

        # Prüfen ob Funktion callable ist
        if not callable(func):
            raise RuntimeError(
                "registered function '{}' ist not callable".format(func)
            )

        if edge is not None and io_event._bitaddress < 0:
            raise AttributeError(
                "parameter 'edge' can be used with bit io objects only"
            )

        # Edge auflösen, wenn nicht angegeben
        if edge is None:
            edge = BOTH

        if io_event not in self._dict_events:
            self._dict_events[io_event] = [(func, edge, as_thread)]
        else:
            # Prüfen ob Funktion schon registriert ist
            for regfunc in self._dict_events[io_event]:
                if regfunc[0] != func:
                    # Nächsten Eintrag testen
                    continue

                if edge == BOTH or regfunc[1] == BOTH:
                    if io_event._bitaddress < 0:
                        raise AttributeError(
                            "io '{}' with function '{}' already in list."
                            "".format(io_name, func)
                        )
                    else:
                        raise AttributeError(
                            "io '{}' with function '{}' already in list with "
                            "edge 'BOTH' or RISING/FALLING - you can use BOTH "
                            "or RISING and FALLING only".format(
                                io_name, func
                            )
                        )
                elif regfunc[1] == edge:
                    raise AttributeError(
                        "io '{}' with function '{}' for given edge "
                        "already in list".format(io_name, func)
                    )

            # Eventfunktion einfügen
            self._dict_events[io_event].append((func, edge, as_thread))

    def unreg_event(self, io_name, func=None, edge=None):
        """Entfernt ein Event aus der Eventueberwachung.

        @param io_name Name des Inputs, dessen Events entfert werden sollen
        @param func Nur Events mit angegebener Funktion
        @param edge Nur Events mit angegebener Funktion und angegebener Edge

        """
        io_event = self.__getitem__(io_name)
        if type(io_event) == list:
            if len(io_event) == 1:
                io_event = io_event[0]
            elif len(io_event) == 0:
                raise KeyError(
                    "byte '{}' contains no io object".format(io_name))
            else:
                raise KeyError(
                    "byte '{}' contains more than one bit io object".format(
                        io_name
                    )
                )

        if io_event in self._dict_events:
            if func is None:
                del self._dict_events[io_event]
            else:
                newlist = []
                for regfunc in self._dict_events[io_event]:
                    if regfunc[0] != func or edge is not None \
                            and regfunc[1] != edge:

                        newlist.append(regfunc)

                # Wenn Funktionen übrig bleiben, diese übernehmen
                if len(newlist) > 0:
                    self._dict_events[io_event] = newlist
                else:
                    del self._dict_events[io_event]


class RevPiCore(RevPiDevice):

    """Klasse fuer den RevPi Core.

    Stellt Funktionen fuer die LEDs und den Status zur Verfuegung.

    """

    def _devconfigure(self):
        """Core-Klasse vorbereiten."""
        self._iocycle = None
        self._iotemperature = None
        self._iofrequency = None
        self._ioerrorcnt = None
        self._ioled = 1
        self._ioerrorlimit1 = None
        self._ioerrorlimit2 = None

        int_lenio = len(self._lst_io)
        if int_lenio == 6:
            # Core 1.1
            self._iocycle = 1
            self._ioerrorcnt = 2
            self._ioled = 3
            self._ioerrorlimit1 = 4
            self._ioerrorlimit2 = 5
        elif int_lenio == 8:
            # core 1.2
            self._iocycle = 1
            self._ioerrorcnt = 2
            self._iotemperature = 3
            self._iofrequency = 4
            self._ioled = 5
            self._ioerrorlimit1 = 6
            self._ioerrorlimit2 = 7

    def _errorlimit(self, io_id, errorlimit):
        """Verwaltet das Lesen und Schreiben der ErrorLimits.
        @param io_id Index des IOs fuer ErrorLimit
        @return Aktuellen ErrorLimit oder None wenn nicht verfuegbar"""
        if errorlimit is None:
            return None if io_id is None else int.from_bytes(
                self._lst_io[io_id].get_value(),
                byteorder=self._lst_io[io_id]._byteorder
            )
        else:
            if 0 <= errorlimit <= 65535:
                self._lst_io[io_id].set_value(errorlimit.to_bytes(
                    2, byteorder=self._lst_io[io_id]._byteorder
                ))
            else:
                raise ValueError(
                    "errorlimit value int() must be between 0 and 65535"
                )

    def get_status(self):
        """Gibt den RevPi Core Status zurueck.
        @return Status als int()"""
        return int.from_bytes(
            self._lst_io[0].get_value(), byteorder=self._lst_io[0]._byteorder
        )

    def get_leda1(self):
        """Gibt den Zustand der LED A1 vom core zurueck.
        @return 0=aus, 1=gruen, 2=rot"""
        int_led = int.from_bytes(
            self._lst_io[self._ioled].get_value(),
            byteorder=self._lst_io[self._ioled]._byteorder
        )
        led = int_led & 1
        led += int_led & 2
        return led

    def get_leda2(self):
        """Gibt den Zustand der LED A2 vom core zurueck.
        @return 0=aus, 1=gruen, 2=rot"""
        int_led = int.from_bytes(
            self._lst_io[self._ioled].get_value(),
            byteorder=self._lst_io[self._ioled]._byteorder
        )
        led = 1 if bool(int_led & 4) else 0
        led = led + 2 if bool(int_led & 8) else led
        return led

    def set_leda1(self, value):
        """Setzt den Zustand der LED A1 vom core.
        @param value 0=aus, 1=gruen, 2=rot"""
        if 0 <= value <= 3:
            int_led = (self.get_leda2() << 2) + value
            self._lst_io[self._ioled].set_value(int_led.to_bytes(
                length=1, byteorder=self._lst_io[self._ioled]._byteorder
            ))
        else:
            raise ValueError("led status int() must be between 0 and 3")

    def set_leda2(self, value):
        """Setzt den Zustand der LED A2 vom core.
        @param value 0=aus, 1=gruen, 2=rot"""
        if 0 <= value <= 3:
            int_led = (value << 2) + self.get_leda1()
            self._lst_io[self._ioled].set_value(int_led.to_bytes(
                length=1, byteorder=self._lst_io[self._ioled]._byteorder
            ))
        else:
            raise ValueError("led status int() must be between 0 and 3")

    A1 = property(get_leda1, set_leda1)
    A2 = property(get_leda2, set_leda2)
    status = property(get_status)

    @property
    def picontrolrunning(self):
        """Statusbit fuer piControl-Treiber laeuft.
        @return True, wenn Treiber laeuft"""
        return bool(int.from_bytes(
            self._lst_io[0].get_value(),
            byteorder=self._lst_io[0]._byteorder
        ) & 1)

    @property
    def unconfdevice(self):
        """Statusbit fuer ein IO-Modul nicht mit PiCtory konfiguriert.
        @return True, wenn IO Modul nicht konfiguriert"""
        return bool(int.from_bytes(
            self._lst_io[0].get_value(),
            byteorder=self._lst_io[0]._byteorder
        ) & 2)

    @property
    def missingdeviceorgate(self):
        """Statusbit fuer ein IO-Modul fehlt oder piGate konfiguriert.
        @return True, wenn IO-Modul fehlt oder piGate konfiguriert"""
        return bool(int.from_bytes(
            self._lst_io[0].get_value(),
            byteorder=self._lst_io[0]._byteorder
        ) & 4)

    @property
    def overunderflow(self):
        """Statusbit Modul belegt mehr oder weniger Speicher als konfiguriert.
        @return True, wenn falscher Speicher belegt ist"""
        return bool(int.from_bytes(
            self._lst_io[0].get_value(),
            byteorder=self._lst_io[0]._byteorder
        ) & 8)

    @property
    def leftgate(self):
        """Statusbit links vom RevPi ist ein piGate Modul angeschlossen.
        @return True, wenn piGate links existiert"""
        return bool(int.from_bytes(
            self._lst_io[0].get_value(),
            byteorder=self._lst_io[0]._byteorder
        ) & 16)

    @property
    def rightgate(self):
        """Statusbit rechts vom RevPi ist ein piGate Modul angeschlossen.
        @return True, wenn piGate rechts existiert"""
        return bool(int.from_bytes(
            self._lst_io[0].get_value(),
            byteorder=self._lst_io[0]._byteorder
        ) & 32)

    @property
    def iocycle(self):
        """Gibt Zykluszeit der Prozessabbildsynchronisierung zurueck.
        @return Zykluszeit in ms"""
        return None if self._iocycle is None else int.from_bytes(
            self._lst_io[self._iocycle].get_value(),
            byteorder=self._lst_io[self._iocycle]._byteorder
        )

    @property
    def temperature(self):
        """Gibt CPU-Temperatur zurueck.
        @return CPU-Temperatur in Celsius"""
        return None if self._iotemperature is None else int.from_bytes(
            self._lst_io[self._iotemperature].get_value(),
            byteorder=self._lst_io[self._iotemperature]._byteorder
        )

    @property
    def frequency(self):
        """Gibt CPU Taktfrequenz zurueck.
        @return CPU Taktfrequenz in MHz"""
        return None if self._iofrequency is None else int.from_bytes(
            self._lst_io[self._iofrequency].get_value(),
            byteorder=self._lst_io[self._iofrequency]._byteorder
        ) * 10

    @property
    def ioerrorcount(self):
        """Gibt Fehleranzahl auf RS485 piBridge Bus zurueck.
        @return Fehleranzahl der piBridge"""
        return None if self._ioerrorcnt is None else int.from_bytes(
            self._lst_io[self._ioerrorcnt].get_value(),
            byteorder=self._lst_io[self._ioerrorcnt]._byteorder
        )

    @property
    def errorlimit1(self):
        """Gibt RS485 ErrorLimit1 Wert zurueck.
        @return Aktueller Wert fuer ErrorLimit1"""
        return self._errorlimit(self._ioerrorlimit1, None)

    @errorlimit1.setter
    def errorlimit1(self, value):
        """Setzt RS485 ErrorLimit1 auf neuen Wert.
        @param value Neuer ErrorLimit1 Wert"""
        self._errorlimit(self._ioerrorlimit1, value)

    @property
    def errorlimit2(self):
        """Gibt RS485 ErrorLimit2 Wert zurueck.
        @return Aktueller Wert fuer ErrorLimit2"""
        return self._errorlimit(self._ioerrorlimit2, None)

    @errorlimit2.setter
    def errorlimit2(self, value):
        """Setzt RS485 ErrorLimit2 auf neuen Wert.
        @param value Neuer ErrorLimit2 Wert"""
        self._errorlimit(self._ioerrorlimit2, value)


class RevPiGateway(RevPiDevice):

    """Klasse fuer die RevPi Gateway-Devices.

    Stellt neben den Funktionen von RevPiDevice weitere Funktionen fuer die
    Gateways bereit. Es koennen ueber die reg_*-Funktionen eigene IOs definiert
    werden, die ein RevPiStructIO-Objekt abbilden.
    Dieser IO-Typ kann Werte ueber mehrere Bytes verarbeiten und zurueckgeben.

    """

    def __init__(self, dict_device, **kwargs):
        """Erweitert RevPiDevice um reg_*-Funktionen.
        @see #RevPiDevice.__init__ RevPiDevice.__init__(...)"""
        super().__init__(dict_device, **kwargs)

        self._dict_iorefbyte = {}
        self._dict_iorefname = {}
        self._dict_slc = {
            "inp": self.slc_inp, "out": self.slc_out, "mem": self.slc_mem
        }

    def _create_io(self, name, startio, frm, io_type, **kwargs):
        """Erstellt einen neuen IO und ersetzt den/die Bestehenden.

        @param name Name des neuen IO
        @param startio IO ab dem eingefuegt wird
        @param frm struct() formatierung (1 Zeichen)
        @param io_type IO-Type "inp", "out", "mem"
        @param kwargs Weitere Parameter:
            - bmk: Bezeichnung fuer IO
            - bit: Registriert IO als bool() am angegebenen Bit im Byte
            - byteorder: Byteorder fuer diesen IO, Standardwert=little
            - defaultvalue: Standardwert fuer IO, Standard ist 0

        """
        if len(frm) == 1:

            # Byteorder prüfen und übernehmen
            byteorder = kwargs.get("byteorder", "little")
            if not (byteorder == "little" or byteorder == "big"):
                raise ValueError("byteorder must be 'little' or 'big'")
            bofrm = "<" if byteorder == "little" else ">"

            bitaddress = "" if frm != "?" else str(kwargs.get("bit", 0))
            if bitaddress == "" or \
                    (int(bitaddress) >= 0 and int(bitaddress) < 8):

                bitlength = "1" if bitaddress.isnumeric() else \
                    struct.calcsize(bofrm + frm) * 8

                if startio in self._dict_iorefname:
                    startaddress = self._dict_iorefname[startio]
                else:
                    startaddress = self.__getitem__(startio).slc_address.start

                # [name,default,anzbits,adressbyte,export,adressid,bmk,bitaddress]
                list_value = [
                    name,
                    kwargs.get("defaultvalue", 0),
                    bitlength,
                    startaddress,
                    False,
                    str(startaddress).rjust(4, "0"),
                    kwargs.get("bmk", ""),
                    bitaddress
                ]

                # Neuen IO instantiieren
                io_new = RevPiStructIO(
                    self.offset,
                    list_value,
                    io_type != "out",
                    self._ba_devdata,
                    byteorder,
                    bofrm + frm
                )
                io_new._byteorder = byteorder

                # Platz für neuen IO prüfen
                if (io_new.slc_address.start >=
                        self._dict_slc[io_type].start and
                        io_new.slc_address.stop <=
                        self._dict_slc[io_type].stop):

                    self._replace_io(io_new)

                else:
                    raise BufferError(
                        "registered value does not fit process image {} "
                        "scope".format(io_type)
                    )
            else:
                raise AttributeError(
                    "bitaddress must be a value between 0 and 7"
                )
        else:
            raise AttributeError("parameter frm has to be a single sign")

    def _getbytename(self, iobyte):
        """Ermittelt den Namen eines IOs auf der Byteadresse.
        @param iobyte Bytenummer
        @return IO-Namen"""

        # Wenn IO schon ausgetauscht wurde
        if iobyte in self._dict_iorefbyte:
            return self._dict_iorefbyte[iobyte]

        # Wenn IO jetzt ausgetauscht wird
        if iobyte in self._dict_iobyte:
            intlen = len(self._dict_iobyte[iobyte])
            if intlen == 1:
                return self._dict_iobyte[iobyte][0].name
            elif len == 0:
                raise KeyError("byte '{}' contains no input".format(iobyte))
            else:
                raise KeyError(
                    "byte '{}' contains more than one bit-input".format(iobyte)
                )
        else:
            raise KeyError("byte '{}' does not exist".format(iobyte))

    def _replace_io(self, io):
        """Ersetzt bestehende IOs durch den neu Registrierten.
        @param io IO ab dem der Neue eingefuegt werden soll"""
        if io.name in self._dict_ioname:
            raise NameError(
                "name '{}' already exists on device '{}'".format(
                    io._name, self.name
                )
            )
        else:
            dict_oldio = {}
            for oldio in self._lst_io:
                # Alle IOs Prüfen ob sie im neuen Speicherbereich sind
                errstart = oldio.slc_address.start >= io.slc_address.start \
                    and oldio.slc_address.start < io.slc_address.stop
                errstop = oldio.slc_address.stop > io.slc_address.start \
                    and oldio.slc_address.stop <= io.slc_address.stop
                if errstart or errstop:

                    if type(oldio) == RevPiStructIO:
                        # Hier gibt es schon einen neuen IO
                        if oldio._bitaddress >= 0:
                            if io._bitaddress == oldio._bitaddress:
                                raise MemoryError(
                                    "bit {} already assigned to '{}'".format(
                                        io._bitaddress, oldio._name
                                    )
                                )

                        else:
                            # Bereits überschriebene bytes() sind ungültig
                            raise MemoryError(
                                "new io '{}' overlaps memory of '{}'".format(
                                    io._name, oldio._name
                                )
                            )

                    else:
                        # IOs im Speicherbereich des neuen IO merken
                        dict_oldio[oldio.name] = oldio

            for oldio in dict_oldio.values():
                if io._bitaddress >= 0:
                    # ios für ref bei bitaddress speichern
                    self._dict_iorefbyte[oldio.slc_address.start] = oldio.name
                    self._dict_iorefname[oldio.name] = oldio.slc_address.start

                # ios aus listen entfernen
                self._dict_iobyte[oldio.slc_address.start].remove(oldio)
                del self._dict_ioname[oldio.name]
                self._lst_io.remove(oldio)

            # Byteregister erweitern
            if io._bitaddress >= 0:
                if len(self._dict_iobyte[io.slc_address.start]) != 8:
                    # Wenn kein 8 Bits vorhandne sind, "schnell" anlegen
                    self._dict_iobyte[io.slc_address.start] = [
                        None, None, None, None, None, None, None, None
                    ]

                self._dict_iobyte[io.slc_address.start][io._bitaddress] = io
            else:
                self._dict_iobyte[io.slc_address.start].append(io)

            # Namensregister erweitern
            self._dict_ioname[io.name] = io

            # io einfügen (auch wenn nicht richtige stelle wegen BitOffset)
            self._lst_io.insert(io.slc_address.start, io)

            # Liste neu sortieren
            self._lst_io.sort(key=lambda x: x.slc_address.start)

    def get_rawbytes(self):
        """Gibt die Bytes aus, die dieses Device verwendet.
        @return bytes() des Devices"""
        return bytes(self._ba_devdata)

    def reg_inp(self, name, startinp, frm, **kwargs):
        """Registriert einen neuen Input.

        @param name Name des neuen Inputs
        @param startinp Inputname ab dem eingefuegt wird
        @param frm struct() formatierung (1 Zeichen)
        @param kwargs Weitere Parameter:
            - bmk: Bezeichnung fuer Input
            - bit: Registriert Input als bool() am angegebenen Bit im Byte
            - byteorder: Byteorder fuer den Input, Standardwert=little
            - defaultvalue: Standardwert fuer Input, Standard ist 0
            - event: Funktion fuer Eventhandling registrieren
            - as_thread: Fuehrt die event-Funktion als RevPiCallback-Thread aus
            - edge: event-Ausfuehren bei RISING, FALLING or BOTH Wertaenderung
        @see <a target="_blank"
        href="https://docs.python.org/3/library/struct.html#format-characters"
        >Python3 struct()</a>

        """
        if type(startinp) == int:
            # Byte int() umwandeln in Namen
            startinp = self._getbytename(startinp)

        if type(startinp) == str:
            self._create_io(name, startinp, frm, "inp", **kwargs)
        else:
            raise TypeError(
                "start input must be str() or int() not {}".format(
                    type(startinp)
                )
            )

        # Optional Event eintragen
        reg_event = kwargs.get("event", None)
        if reg_event is not None:
            as_thread = kwargs.get("as_thread", False)
            edge = kwargs.get("edge", None)
            self.reg_event(name, reg_event, as_thread=as_thread, edge=edge)

    def reg_out(self, name, startout, frm, **kwargs):
        """Registriert einen neuen Output.

        @param name Name des neuen Outputs
        @param startout Outputname ab dem eingefuegt wird
        @param frm struct() formatierung (1 Zeichen)
        @param kwargs Weitere Parameter:
            - bmk: Bezeichnung fuer Output
            - bit: Registriert Outputs als bool() am angegebenen Bit im Byte
            - byteorder: Byteorder fuer den Output, Standardwert=little
            - defaultvalue: Standardwert fuer Output, Standard ist 0
            - event: Funktion fuer Eventhandling registrieren
            - as_thread: Fuehrt die event-Funktion als RevPiCallback-Thread aus
            - edge: event-Ausfuehren bei RISING, FALLING or BOTH Wertaenderung
        @see <a target="_blank"
        href="https://docs.python.org/3/library/struct.html#format-characters"
        >Python3 struct()</a>

        """
        if type(startout) == int:
            # Byte int() umwandeln in Namen
            startout = self._getbytename(startout)

        if type(startout) == str:
            self._create_io(name, startout, frm, "out", **kwargs)
        else:
            raise TypeError(
                "start output must be str() or int() not {}".format(
                    type(startout)
                )
            )

        # Optional Event eintragen
        reg_event = kwargs.get("event", None)
        if reg_event is not None:
            as_thread = kwargs.get("as_thread", False)
            edge = kwargs.get("edge", None)
            self.reg_event(name, reg_event, as_thread=as_thread, edge=edge)

    def reg_mem(self, name, startmem, frm, **kwargs):
        """Registriert einen neuen Memory.

        @param name Name des neuen Memory
        @param startinp Memname ab dem eingefuegt wird
        @param frm struct() formatierung (1 Zeichen)
        @param kwargs Weitere Parameter:
            - bmk: Bezeichnung fuer Memory
            - bit: Registriert Memory als bool() am angegebenen Bit im Byte
            - byteorder: Byteorder fuer den Memory, Standardwert=little
            - defaultvalue: Standardwert fuer Memory, Standard ist 0
        @see <a target="_blank"
        href="https://docs.python.org/3/library/struct.html#format-characters"
        >Python3 struct()</a>

        """
        if type(startmem) == int:
            # Byte int() umwandeln in Namen
            startmem = self._getbytename(startmem)

        if type(startmem) == str:
            self._create_io(name, startmem, frm, "mem", **kwargs)
        else:
            raise TypeError(
                "start mem must be str() or int() not {}".format(
                    type(startmem)
                )
            )


class RevPiVirtual(RevPiGateway):

    """Klasse fuer die RevPi Virtual-Devices.

    Stellt die selben Funktionen wie RevPiGateway zur Verfuegung. Es koennen
    ueber die reg_*-Funktionen eigene IOs definiert werden, die ein
    RevPiStructIO-Objekt abbilden.
    Dieser IO-Typ kann Werte ueber mehrere Bytes verarbeiten und zurueckgeben.
    @see #RevPiGateway RevPiGateway

    """

    pass


class RevPiIOBase(object):

    """Basisklasse fuer alle IO-Objekte der RevPiDevice()-Klasse.

    Die Basisfunktionalitaet ermoeglicht das Lesen und Schreiben der Werte
    als bytes() oder bool(). Dies entscheidet sich bei der Instantiierung.
    Wenn eine Bittadresse angegeben wird, werden bool()-Werte erwartet
    und zurueckgegeben, ansonsten bytes().

    Diese Klasse dient als Basis fuer andere IO-Klassen mit denen die Werte
    auch als int() verwendet werden koennen.

    """

    def __init__(
            self, offset, valuelist, readonly, byteproc,
            byteorder, signed=False):
        """Instantiierung der RevPiIOBase()-Klasse.

        @param offset Deviceoffset
        @param valuelist Datenliste fuer Instantiierung
        @param readonly True bei Inp und mem, False bei out
        @param byteproc bytearray() Daten des Devices
        @param byteorder Byteorder 'little' / 'big' fuer int() Berechnung
        @param signed Vorzeichen bei int() Berechnung beruecksichtigen

        """
        # Bitadressen auf Bytes aufbrechen und umrechnen
        self._bitaddress = -1 if valuelist[7] == "" else int(valuelist[7]) % 8

        # Längenberechnung
        self._bitlength = int(valuelist[2])
        self.length = 1 if self._bitaddress == 0 else int(self._bitlength / 8)

        self._byteproc = byteproc
        self._byteorder = byteorder
        self._devoffset = offset
        self._name = valuelist[0]
        self._readonly = readonly
        self._signed = signed
        self.bmk = valuelist[6]

        int_startaddress = int(valuelist[3])
        if self._bitaddress == -1:
            self.slc_address = slice(
                int_startaddress, int_startaddress + self.length
            )
            # Defaultvalue aus Zahl in Bytes umrechnen
            if str(valuelist[1]).isnumeric():
                self.defaultvalue = int(valuelist[1]).to_bytes(
                    self.length, byteorder=self._byteorder
                )
            else:
                # Defaultvalue direkt von bytes übernehmen
                if type(valuelist[1]) == bytes:
                    if len(valuelist[1]) != self.length:
                        raise ValueError(
                            "given bytes for default value must have a length "
                            "of {}".format(self.length)
                        )
                    else:
                        self.defaultvalue = valuelist[1]
                else:
                    self.defaultvalue = bytes(self.length)

        else:
            # Höhere Bits als 7 auf nächste Bytes umbrechen
            int_startaddress += int((int(valuelist[7]) % 16) / 8)
            self.slc_address = slice(
                int_startaddress, int_startaddress + 1
            )
            self.defaultvalue = bool(int(valuelist[1]))

    def __bool__(self):
        """bool()-wert der Klasse.
        @return IO-Wert als bool(). Nur False wenn False oder 0 sonst True"""
        return bool(self.get_value())

    def __bytes__(self):
        """bytes()-wert der Klasse.
        @return IO-Wert als bytes()"""
        if self._bitaddress >= 0:
            int_byte = int.from_bytes(
                self._byteproc[self.slc_address], byteorder=self._byteorder
            )
            if bool(int_byte & 1 << self._bitaddress):
                return b'\x01'
            else:
                return b'\x00'
        else:
            return bytes(self._byteproc[self.slc_address])

    def __str__(self):
        """str()-wert der Klasse.
        @return Namen des IOs"""
        return self._name

    def _get_byteorder(self):
        """Gibt konfigurierte Byteorder zurueck.
        @return str() Byteorder"""
        return self._byteorder

    def get_name(self):
        """Gibt den Namen des IOs zurueck.
        @return IO Name"""
        return self._name

    def get_absaddress(self):
        """Gibt die absolute Byteadresse im Prozessabbild zurueck.
        @return Absolute Byteadresse"""
        return self._devoffset + self.slc_address.start

    def get_address(self):
        """Gibt die Byteadresse auf dem Device zurueck.
        @return Byteadresse auf dem Device"""
        return self.slc_address.start

    def get_value(self):
        """Gibt den Wert des IOs als bytes() oder bool() zurueck.
        @return IO-Wert"""
        if self._bitaddress >= 0:
            int_byte = int.from_bytes(
                self._byteproc[self.slc_address], byteorder=self._byteorder
            )
            return bool(int_byte & 1 << self._bitaddress)

        else:
            return bytes(self._byteproc[self.slc_address])

    def set_value(self, value):
        """Setzt den Wert des IOs mit bytes() oder bool().
        @param value IO-Wert als bytes() oder bool()"""
        if self._readonly:
            raise AttributeError("can not write to input")

        else:
            if self._bitaddress >= 0:
                # Versuchen egal welchen Typ in Bool zu konvertieren
                value = bool(value)

                # ganzes Byte laden
                byte_buff = self._byteproc[self.slc_address]

                # Bytes in integer umwandeln
                int_len = len(byte_buff)
                int_byte = int.from_bytes(byte_buff, byteorder=self._byteorder)
                int_bit = 1 << self._bitaddress

                # Aktuellen Wert vergleichen und ggf. setzen
                if not bool(int_byte & int_bit) == value:
                    if value:
                        int_byte += int_bit
                    else:
                        int_byte -= int_bit

                    # Zurückschreiben wenn verändert
                    self._byteproc[self.slc_address] = int_byte.to_bytes(
                        int_len, byteorder=self._byteorder
                    )

            else:
                if type(value) == bytes:
                    if self.length == len(value):
                        self._byteproc[self.slc_address] = value
                    else:
                        raise ValueError(
                            "requires a bytes() object of length {}, but"
                            " {} was given".format(self.length, len(value))
                        )
                else:
                    raise ValueError(
                        "requires a bytes() object, not {}".format(type(value))
                    )

    name = property(get_name)
    value = property(get_value, set_value)


class RevPiIO(RevPiIOBase):

    """Klasse fuer den Zugriff auf die Daten mit Konvertierung in int().

    Diese Klasse erweitert die Funktion von RevPiIOBase() um Funktionen,
    ueber die mit int() Werten gearbeitet werden kann. Fuer die Umwandlung
    koennen 'Byteorder' (Default 'little') und 'signed' (Default False) als
    Parameter gesetzt werden.
    @see #RevPiIOBase RevPiIOBase

    """

    def __int__(self):
        """Gibt IO als int() Wert zurueck mit Beachtung byteorder/signed.
        @return int() Wert"""
        return self.get_int()

    def _get_signed(self):
        """Ruft ab, ob der Wert Vorzeichenbehaftet behandelt werden soll.
        @return True, wenn Vorzeichenbehaftet"""
        return self._signed

    def _set_byteorder(self, value):
        """Setzt Byteorder fuer int() Umwandlung.
        @param value str() 'little' or 'big'"""
        if not (value == "little" or value == "big"):
            raise ValueError("byteorder must be 'little' or 'big'")
        if self._byteorder != value:
            self._byteorder = value
            self.defaultvalue = self.defaultvalue[::-1]

    def _set_signed(self, value):
        """Left fest, ob der Wert Vorzeichenbehaftet behandelt werden soll.
        @param value True, wenn mit Vorzeichen behandel"""
        if type(value) != bool:
            raise ValueError("signed must be bool() True or False")
        self._signed = value

    def get_int(self):
        """Gibt IO als int() Wert zurueck mit Beachtung byteorder/signed.
        @return int() Wert"""
        return int.from_bytes(
            self._byteproc[self.slc_address],
            byteorder=self._byteorder,
            signed=self._signed
        )

    def set_int(self, value):
        """Setzt IO mit Beachtung byteorder/signed.
        @param value int()"""
        if type(value) == int:
            self.set_value(value.to_bytes(
                self.length,
                byteorder=self._byteorder,
                signed=self._signed
            ))
        else:
            raise ValueError(
                "need an int() value, but {} was given".format(type(value))
            )

    byteorder = property(RevPiIOBase._get_byteorder, _set_byteorder)
    signed = property(_get_signed, _set_signed)
    value = property(get_int, set_int)


class RevPiStructIO(RevPiIOBase):

    """Klasse fuer den Zugriff auf Daten ueber ein definierten struct().

    Diese Klasse ueberschreibt get_value() und set_value() der RevPiIOBase()
    Klasse. Sie stellt ueber struct die Werte in der gewuenschten Formatierung
    bereit. Der struct-Formatwert wird bei der Instantiierung festgelegt.
    @see #RevPiIOBase RevPiIOBase

    """

    def __init__(self, offset, valuelist, readonly, byteproc, byteorder, frm):
        """Erweitert RevPiIOBase um struct-Formatierung.
        @see #RevPiIOBase.__init__ RevPiIOBase.__init__(...)"""
        super().__init__(offset, valuelist, readonly, byteproc, byteorder)
        self.frm = frm

    def get_structvalue(self):
        """Gibt den Wert mit struct Formatierung zurueck.
        @return Wert vom Typ der struct-Formatierung"""
        if self._bitaddress >= 0:
            return self.get_value()
        else:
            return struct.unpack(self.frm, self.get_value())[0]

    def set_structvalue(self, value):
        """Setzt den Wert mit struct Formatierung.
        @param value Wert vom Typ der struct-Formatierung"""
        if self._bitaddress >= 0:
            self.set_value(value)
        else:
            self.set_value(struct.pack(self.frm, value))

    byteorder = property(RevPiIOBase._get_byteorder)
    value = property(get_structvalue, set_structvalue)
