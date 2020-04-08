from src.tavola import *
from src.globale import *

# PARAMETRI
FPS = 60  # Frames per second.
RISOLUZIONE = (1080, 720)
POS_TAVOLA = (RISOLUZIONE[0]/10, RISOLUZIONE[1]/10)
SIZE_TAVOLA = (RISOLUZIONE[0]*0.8, RISOLUZIONE[1]*0.8)  # ho scalato un po' la risoluzione dello schermo
DIM_TAVOLA = (10, 4)  # numero di caselle in goni direzione
NERO = (0, 0, 0)
PADDING = 4


class Game:  # gestisce code degli eventi, game loop e aggiornamento dello schermo e comunicazione server
    def __init__(self, inizia):
        succes, fail = pg.init()
        print("{0} successes and {1} failures".format(succes, fail))
        self.screen = pg.display.set_mode(RISOLUZIONE)  # mostro schermo
        self.clock = pg.time.Clock()  # inizializzo clock
        self.state = GameState(inizia)
        self.running = True
        Globale.new('game', self)  # verranno usate come varibili globali (sicome statiche posso accedere da ovunque)
        Globale.new('gameState', self.state)

    def run(self):  # fa il game loop
        while self.running:
            self.clock.tick(FPS)  # mi fa andare al giusto frame rate
            self.ceck_server()
            for event in pg.event.get():
                self.resolve_event(event)
            self.update_screen()

    def resolve_event(self, event):
        if event.type == pg.QUIT:
            quit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.state.mouse_click(event.pos)

    def update_screen(self):
        self.screen.fill(NERO)  # copro frame prec
        self.state.display(self.screen)  # disegno tutto quello che riguarda lo stato attuale
        pg.display.update()  # Or pg.display.flip()

    def send_move(self, x, y):
        self.state.possoGiocare = False  # devo aspettare per giocare
        pass  # dobbiamo inviare al server la richiesta di togliere una casella
        self.state.del_caselle(x, y)  # provvisorio, serve solo per prova (bypassa server)

    def ceck_server(self):  # controlla se sono arrivati messaggi dal server
        pass  # controllo se arriva risposta
        if False:  # bisogna mettere se è arrivato qualcosa
            x = 0  # ovviamente vanno messi a posto
            y = 0
            self.state.del_caselle(x, y)

    def fine_partita(self, win):
        print('fine, ha vinto il ' + win + ' giocatore')


class GameState:  # contiene tutte le var significative per descrivere il gioco e i metodi secondo cui modificarle
    def __init__(self, inizia):
        self.tavoletta = Tavola(POS_TAVOLA, RISOLUZIONE, DIM_TAVOLA, PADDING)
        self.tavoletta.crea_caselle()
        self.possoGiocare = inizia  # quando clicko una cella diventa false e quando l'altro gioca diventa true
        self.turnoMio = inizia

    def mouse_click(self, pos):
        if self.possoGiocare or True:  # solo per prova
            self.tavoletta.ceck_click(pos)

    def del_caselle(self, x, y):
        self.turnoMio = not self.turnoMio
        self.possoGiocare = self.turnoMio  # se prima non era il mio turno adesso posso giocare
        self.tavoletta.del_caselle(x, y)

    def display(self, screen):
        self.tavoletta.blit(screen)
