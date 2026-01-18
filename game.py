import random

class UnoGame:
    def __init__(self):
        self.cores = ["red", "green", "blue", "yellow"]
        self.deck = self.create_full_deck()
        self.players = [[] for _ in range(4)]
        self.table = []
        self.dificuldade = "Fácil"
        self.turn = 0
        self.direction = 1
        self.setup_game()

    def create_full_deck(self):
        deck = []
        for cor in self.cores:
            for val in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "+2"]:
                deck.append((val, cor))
        for _ in range(4):
            deck.append(("+4", "wild"))
        random.shuffle(deck)
        return deck

    def setup_game(self):
        for _ in range(7):
            for p in self.players:
                p.append(self.deck.pop())
        # Garante carta inicial válida
        first_card = self.deck.pop()
        while first_card[1] == "wild":
            self.deck.insert(0, first_card)
            first_card = self.deck.pop()
        self.table.append(first_card)

    def next_player(self):
        self.turn = (self.turn + self.direction) % 4

    def IA_decidir_jogada(self, mao, topo):
        jogaveis = [i for i, c in enumerate(mao) if self.pode_jogar(topo, c)]
        if not jogaveis: return None
        # IA Hard foca em cartas de ação
        if self.dificuldade == "Difícil":
            acoes = [i for i in jogaveis if mao[i][0] in ["+2", "+4", "skip"]]
            if acoes: return acoes[0]
        return random.choice(jogaveis)

    def pode_jogar(self, topo, carta):
        if carta[1] == "wild": return True
        return carta[0] == topo[0] or carta[1] == topo[1]

    def play_card(self, p_idx, c_idx):
        card = self.players[p_idx].pop(c_idx)
        if card[1] == "wild":
            # IA escolhe a cor que mais possui
            contas = {c: 0 for c in self.cores}
            for c in self.players[p_idx]:
                if c[1] in contas: contas[c[1]] += 1
            escolhida = max(contas, key=contas.get)
            self.table.append((card[0], escolhida))
        else:
            self.table.append(card)
        self.next_player()

    def mudar_dificuldade(self):
        niveis = ["Fácil", "Médio", "Difícil"]
        self.dificuldade = niveis[(niveis.index(self.dificuldade) + 1) % 3]

    def check_winner(self):
        for i, p in enumerate(self.players):
            if len(p) == 0: return i
        return None