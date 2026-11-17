import arcade
import random
import time
from BancoJogo import buscar_top10, inicializar_banco, limpar_pontuacoes, salvar_resultado

#Definido Altura e Largura e Titulo da tela do jogo
ALTURA = 600
LARGURA = 800
TITULO = "A Garota, O Homem e O ET"
GRAVIDADE = 0.5
DURACAO_ESCUDO = 6.0
VIDAS_INICIAIS = 10
INTERVALO_TELEPORTE_MOEDAS = 8.0
MOEDAS_POR_TELEPORTE = 3
MOEDAS_PARA_PERSEGUICAO = 15
MULTIPLICADOR_VELOCIDADE_PERSEGUIDOR = 0.65
INTERVALO_PULO_PERSEGUIDOR = 1.2
TEMPO_REAPARECER_MOEDA_FINAL = 10.0
TEMPO_PODER_SORTE = 8.0
TEMPO_ITEM_SORTE = 12.0
INTERVALO_MIN_SORTE = 12.0
INTERVALO_MAX_SORTE = 22.0
PRIMEIRA_SORTE_MIN = 4.0
PRIMEIRA_SORTE_MAX = 7.0
MULTIPLICADORES_DIFICULDADE = {
    "facil": 0.65,
    "medio": 1.0,
    "hard": 1.6,
}
NOMES_DIFICULDADE = {
    "facil": "FÁCIL",
    "medio": "MÉDIO",
    "hard": "HARD",
}


def normalizar_vidas(vidas, quantidade_jogadores):
    if isinstance(vidas, int):
        return [vidas] * quantidade_jogadores
    valores = list(vidas)
    return (valores + [VIDAS_INICIAIS] * quantidade_jogadores)[:quantidade_jogadores]


FASES = {
    1: {
        "cenario": "tela_jogo.jpeg",
        "tom": (255, 255, 255),
        "moedas": 25,
        "ets": 1,
        "perseguidores": 1,
        "velocidade_et": 0.9,
        "velocidade_chao": 1.35,
        "plataformas": [(300, 250), (500, 250), (100, 400), (700, 400)],
    },
    2: {
        "cenario": "FundoJogo.jpeg",
        "tom": (255, 255, 255),
        "moedas": 16,
        "ets": 2,
        "perseguidores": 1,
        "velocidade_et": 0.95,
        "velocidade_chao": 1.4,
        "plataformas": [(170, 190), (400, 270), (630, 190), (100, 390), (700, 390)],
    },
    3: {
        "cenario": "tela_jogo.jpeg",
        "tom": (150, 175, 230),
        "moedas": 18,
        "ets": 2,
        "perseguidores": 2,
        "velocidade_et": 1.0,
        "velocidade_chao": 1.45,
        "plataformas": [(140, 210), (360, 340), (580, 210), (100, 440), (700, 440)],
    },
    4: {
        "cenario": "FundoJogo.jpeg",
        "tom": (175, 185, 225),
        "moedas": 12,
        "ets": 3,
        "perseguidores": 2,
        "velocidade_et": 1.05,
        "velocidade_chao": 1.5,
        "plataformas": [(170, 180), (400, 280), (630, 180), (120, 400), (680, 400)],
    },
}
#anotações 
#right = direita
#left = esquerda
#bottom = fundo
# top = topo

def confBordas(objeto, rebater=False):
    # --- Parede Direita ---
    if objeto.right >= LARGURA:
        objeto.right = LARGURA
        if rebater:
            objeto.change_x *= -1

    # --- Parede Esquerda ---
    if objeto.left <= 0:
        objeto.left = 0
        if rebater:
            objeto.change_x *= -1

    # --- Teto ---
    if objeto.top >= ALTURA:
        objeto.top = ALTURA
        if rebater:
            objeto.change_y *= -1
        else:
            objeto.change_y = 0

    # --- Chão ---
    if objeto.bottom <= 0:
        objeto.bottom = 0
        if rebater:
            objeto.change_y *= -1
        else:
            objeto.change_y = 0

#classe player
class Player(arcade.Sprite):
   # 3. Inicializa o Sprite com a primeira textura da lista (quadro 0)
    def __init__(self, personagem="mulher"):
        # 1. Carregar a folha de sprites
        if personagem == "homem":
            arquivo_personagem = "golt.png.png"
            tamanho_quadro = (100, 250)
        else:
            arquivo_personagem = "Ana.png"
            tamanho_quadro = (200, 500)
        sheet_direita = arcade.load_spritesheet(arquivo_personagem)

        # 2. Extrair a grelha de texturas (10 quadros no total: 2 linhas, 5 colunas)
        quadros = sheet_direita.get_texture_grid(
            size=tamanho_quadro,
            columns=5,
            count=10
        )

        # 3. Criar a lista de texturas invertidas para a esquerda
        quadros_esquerda = []
        for frame in quadros:
            quadros_esquerda.append(frame.flip_left_right())
        
        # 4. Inicializar o sprite com a primeira textura (parado)
        escala = 0.4 if personagem == "homem" else 0.2
        super().__init__(quadros[0], scale=escala)
        self.personagem = personagem

        # 5. Mapeamento das poses para a direita e esquerda
        self.texture_parado_d = quadros[0]


        self.texture_parado_e = quadros_esquerda[0]
        self.passos_dano_d = [quadros[7], quadros[8], quadros[9]]
        self.passos_dano_e = [quadros_esquerda[7], quadros_esquerda[8], quadros_esquerda[9]]
        
        self.tomando_dano: bool = False
        self.tempo_dano: float = 0.0
        self.vivo = True
        # Passos (utiliza os quadros 1, 2 e 3 da primeira linha)
        self.passos_direita = [quadros[1], quadros[2], quadros[3]]
        self.passos_esquerda = [quadros_esquerda[1], quadros_esquerda[2], quadros_esquerda[3]]

        # Pulo (utiliza o primeiro quadro da segunda linha, índice 5)
        self.texture_pulo_d = quadros[5]
        self.texture_pulo_e = quadros_esquerda[5]

        # 6. Controladores de estado e animação
        self.quadro_atual: int = 0
        self.tempo_animacao: float = 0.0
        self.virado_para: str = "Direita"
        self.texture = self.texture_parado_d
    def sofrer_dano(self):
        self.tomando_dano = True
        self.tempo_dano = 0.5  # Tempo em segundos que fica exibindo o dano
        self.quadro_atual = 0
    def update(self, delta_time):
        if self.change_x > 0:
            self.virado_para = "Direita"
        elif self.change_x < 0:
            self.virado_para = "Esquerda"

        confBordas(self, rebater=False)

        # Se estiver a saltar (movimento vertical)
        if self.change_y != 0:
            if self.virado_para == "Direita":
                self.texture = self.texture_pulo_d
            else:
                self.texture = self.texture_pulo_e
            return

        # Se estiver a andar horizontalmente
        if self.change_x != 0:
            self.tempo_animacao += delta_time
            if self.tempo_animacao >= 0.1:
                self.tempo_animacao = 0.0
                self.quadro_atual = (self.quadro_atual + 1) % len(self.passos_direita)

            if self.virado_para == "Direita":
                self.texture = self.passos_direita[self.quadro_atual]
            else:
                self.texture = self.passos_esquerda[self.quadro_atual]
        else:
            # Parado
            self.quadro_atual = 0
            self.tempo_animacao = 0.0
            if self.virado_para == "Direita":
                self.texture = self.texture_parado_d
            else:
                self.texture = self.texture_parado_e
        if self.tomando_dano:
            self.tempo_dano -= delta_time
            if self.tempo_dano <= 0:
                self.tomando_dano = False
            
            # Anima os quadros de dano rapidamente
            self.tempo_animacao += delta_time
            if self.tempo_animacao >= 0.1:
                self.tempo_animacao = 0.0
                self.quadro_atual = (self.quadro_atual + 1) % len(self.passos_dano_d)

            if self.virado_para == "Direita":
                self.texture = self.passos_dano_d[self.quadro_atual]
            else:
                self.texture = self.passos_dano_e[self.quadro_atual]
            return        
                


class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png",scale = 0.21)

    def update(self,delta_time):
       
        confBordas(self, rebater = False)

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda_especial.png", scale = 0.35)

  
    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        confBordas(self, rebater = True)


        
class Inimigo_Especial(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("alien.png", scale = 0.46)
        self.jogadores = jogador if isinstance(jogador, (list, tuple)) else [jogador]
        
        self.texture_direita_a = arcade.load_texture("alien.png")       
        self.texture_esquerda_e = arcade.load_texture("alien2.png")
        self.velocidade = 0.9

    def update(self,delta_time):
        jogadores_ativos = [jogador for jogador in self.jogadores if jogador.vivo]
        if not jogadores_ativos:
            return
        jogador_alvo = min(
            jogadores_ativos,
            key=lambda jogador: arcade.get_distance_between_sprites(self, jogador),
        )
        dx = jogador_alvo.center_x - self.center_x
        dy = jogador_alvo.center_y - self.center_y

        distancia =(dx **2 + dy**2) **0.5
        if distancia > 0:

            dx /= distancia
            dy /= distancia
        self.change_x = dx * self.velocidade
        self.change_y = dy * self.velocidade

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.texture_direita_a
        elif self.change_x < 0:
            self.texture = self.texture_esquerda_e
    
        confBordas(self, rebater = False)
    

        
#class inimigo
class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("prof.png", scale = 0.7)
        
        self.texture_direita_a = arcade.load_texture("prof_direita2.png")       
        self.texture_esquerda_e = arcade.load_texture("prof_esquerda2.png")

    

        
    

    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.texture_direita_a
        elif self.change_x < 0:
            self.texture = self.texture_esquerda_e

        confBordas(self, rebater=True)

class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("bloco.png", scale=1)
        self.center_x = x
        self.center_y = y

class BlocoV(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("blocoV.png", scale=1)
        self.center_x = x
        self.center_y = y

class TelaMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.nome_jogador = ""
        self.digitando_nome = False
        self.ignorar_n_inicial = False
        self.sequencia_g = 0
        self.g_pressionado = False
        self.ultima_tecla_g = 0.0
        self.mensagem_ranking = ""
        self.expira_mensagem_ranking = 0.0
        arcade.set_background_color(arcade.color.WHITE)
        self.cenario_sprite = arcade.Sprite("menu.jpg") 
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)
       
        

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        arcade.draw_text(f"A Garota, O Homem e O ET",75 ,500,
                arcade.color.BLACK, 40)
        arcade.draw_text(f"MENU",320 ,305,
        arcade.color.BLACK, 40)
        if self.digitando_nome:
            arcade.draw_text("DIGITE SEU NOME E PRESSIONE ENTER",285,420,arcade.color.BLACK,12)
            arcade.draw_text(self.nome_jogador + "_",340,390,arcade.color.BLACK,16)
            arcade.draw_text("_________________________________________",260,390,arcade.color.BLACK,12)
        else:
            arcade.draw_text("CLIQUE N PARA NOME",314,265,arcade.color.BLACK,12)
        arcade.draw_text("J: JOGAR",310,220,arcade.color.BLACK,12)
        arcade.draw_text(f"CLIQUE S PARA SOBRE O JOGO",305 ,170, arcade.color.BLACK, 10)
        arcade.draw_text(f"CLIQUE I PARA INSTRUÇÃO",305 ,120, arcade.color.BLACK, 11)
        arcade.draw_text(f"CLIQUE R PARA PONTUAÇÃO",305 ,70, arcade.color.BLACK, 11)
        arcade.draw_text(f"X ESC",710 ,570, arcade.color.RED, 20)
        if time.monotonic() < self.expira_mensagem_ranking:
            arcade.draw_text(
                self.mensagem_ranking,
                LARGURA / 2,
                35,
                arcade.color.BLACK,
                12,
                anchor_x="center",
            )



                
    def on_key_press(self,key,modyfiers):
        if self.digitando_nome:
            if key == arcade.key.BACKSPACE:
                self.nome_jogador = self.nome_jogador[:-1]
            elif key == arcade.key.ENTER:
                self.digitando_nome = False
            elif key == arcade.key.ESCAPE:
                self.digitando_nome = False
                self.nome_jogador = ""
                self.ignorar_n_inicial = False
            return

        if key == arcade.key.G:
            if not self.g_pressionado:
                agora = time.monotonic()
                if agora - self.ultima_tecla_g > 1.5:
                    self.sequencia_g = 0
                self.sequencia_g += 1
                self.ultima_tecla_g = agora
                self.g_pressionado = True

                if self.sequencia_g == 3:
                    removidas = limpar_pontuacoes()
                    self.mensagem_ranking = f"RANKING LIMPO: {removidas} REGISTROS REMOVIDOS"
                    self.expira_mensagem_ranking = agora + 3.0
                    self.sequencia_g = 0
            return

        self.sequencia_g = 0

        if key == arcade.key.R:
            tela_ranking = TelaRanking()
            self.window.show_view(tela_ranking)
        if key == arcade.key.I:
            tela_instrucao = TelaInstrucao()
            self.window.show_view(tela_instrucao)
        if key == arcade.key.S:
            tela_sobre = TelaSobre()
            self.window.show_view(tela_sobre)
        if key == arcade.key.J:
            self.window.show_view(TelaModoJogo(self.nome_jogador.strip() or "Jogador"))


        if key == arcade.key.N:
            self.digitando_nome = True
            self.ignorar_n_inicial = True
        if key == arcade.key.ESCAPE:
            self.window.close()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.G:
            self.g_pressionado = False

    def on_text(self, texto):
        if self.digitando_nome:
            if self.ignorar_n_inicial:
                self.ignorar_n_inicial = False
                if texto.lower() == "n":
                    return
            caracteres_validos = "".join(
                caractere for caractere in texto
                if caractere.isalnum() or caractere == " "
            )
            self.nome_jogador = (self.nome_jogador + caracteres_validos)[:20]


class TelaModoJogo(arcade.View):
    def __init__(self, nome_jogador, quantidade_jogadores=1):
        super().__init__()
        self.nome_jogador = nome_jogador
        self.quantidade_jogadores = quantidade_jogadores
        self.cenario = arcade.Sprite("menu.jpg")
        self.cenario.width = LARGURA
        self.cenario.height = ALTURA
        self.cenario.center_x = LARGURA / 2
        self.cenario.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario)

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        arcade.draw_lrbt_rectangle_filled(140, 660, 190, 430, (0, 0, 0, 180))
        arcade.draw_text(
            "ESCOLHA O MODO",
            LARGURA / 2,
            380,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        opcoes = ("1 JOGADOR", "2 JOGADORES")
        for indice, opcao in enumerate(opcoes, start=1):
            cor = arcade.color.YELLOW if indice == self.quantidade_jogadores else arcade.color.WHITE
            arcade.draw_text(
                opcao,
                LARGURA / 2,
                315 - (indice - 1) * 55,
                cor,
                22,
                anchor_x="center",
            )
        arcade.draw_text(
            "SETAS: ESCOLHER   |   ENTER: CONTINUAR",
            LARGURA / 2,
            220,
            arcade.color.WHITE,
            14,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaMenu())
        elif key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.quantidade_jogadores = 3 - self.quantidade_jogadores
        elif key == arcade.key.ENTER:
            self.window.show_view(
                TelaDificuldadeJogo(self.nome_jogador, self.quantidade_jogadores)
            )


class TelaDificuldadeJogo(arcade.View):
    def __init__(self, nome_jogador, quantidade_jogadores):
        super().__init__()
        self.nome_jogador = nome_jogador
        self.quantidade_jogadores = quantidade_jogadores
        self.opcoes = ("facil", "medio", "hard")
        self.indice_dificuldade = 1
        self.cenario = arcade.Sprite("menu.jpg")
        self.cenario.width = LARGURA
        self.cenario.height = ALTURA
        self.cenario.center_x = LARGURA / 2
        self.cenario.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario)

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        arcade.draw_lrbt_rectangle_filled(140, 660, 125, 450, (0, 0, 0, 180))
        arcade.draw_text(
            "ESCOLHA A DIFICULDADE",
            LARGURA / 2,
            395,
            arcade.color.WHITE,
            28,
            anchor_x="center",
        )
        descricoes = {
            "facil": "Inimigos mais lentos",
            "medio": "Velocidade normal",
            "hard": "Inimigos muito rápidos",
        }
        for indice, dificuldade in enumerate(self.opcoes):
            cor = (
                arcade.color.YELLOW
                if indice == self.indice_dificuldade
                else arcade.color.WHITE
            )
            y = 335 - indice * 55
            arcade.draw_text(
                NOMES_DIFICULDADE[dificuldade],
                LARGURA / 2,
                y,
                cor,
                22,
                anchor_x="center",
            )
            arcade.draw_text(
                descricoes[dificuldade],
                LARGURA / 2,
                y - 22,
                arcade.color.WHITE,
                12,
                anchor_x="center",
            )
        arcade.draw_text(
            "SETAS: ESCOLHER   |   ENTER: CONTINUAR   |   ESC: VOLTAR",
            LARGURA / 2,
            145,
            arcade.color.WHITE,
            12,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(
                TelaModoJogo(self.nome_jogador, self.quantidade_jogadores)
            )
        elif key in (arcade.key.UP, arcade.key.LEFT):
            self.indice_dificuldade = (
                self.indice_dificuldade - 1
            ) % len(self.opcoes)
        elif key in (arcade.key.DOWN, arcade.key.RIGHT):
            self.indice_dificuldade = (
                self.indice_dificuldade + 1
            ) % len(self.opcoes)
        elif key == arcade.key.ENTER:
            self.window.show_view(
                TelaSelecaoPersonagens(
                    self.nome_jogador,
                    self.quantidade_jogadores,
                    self.opcoes[self.indice_dificuldade],
                )
            )


class TelaSelecaoPersonagens(arcade.View):
    def __init__(self, nome_jogador, quantidade_jogadores, dificuldade="medio"):
        super().__init__()
        self.nome_jogador = nome_jogador
        self.quantidade_jogadores = quantidade_jogadores
        self.dificuldade = dificuldade
        self.selecoes = ["mulher", "homem"]
        self.cenario = arcade.Sprite("menu.jpg")
        self.cenario.width = LARGURA
        self.cenario.height = ALTURA
        self.cenario.center_x = LARGURA / 2
        self.cenario.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario)
        self._atualizar_previews()

    def _atualizar_previews(self):
        self.sprite_previews = arcade.SpriteList()
        self.preview_jogador_1 = Player(self.selecoes[0])
        self.preview_jogador_1.center_x = 280
        self.preview_jogador_1.center_y = 320
        self.sprite_previews.append(self.preview_jogador_1)

        if self.quantidade_jogadores == 2:
            self.preview_jogador_2 = Player(self.selecoes[1])
            self.preview_jogador_2.center_x = 520
            self.preview_jogador_2.center_y = 320
            self.sprite_previews.append(self.preview_jogador_2)

    def _alternar_personagem(self, indice):
        self.selecoes[indice] = "homem" if self.selecoes[indice] == "mulher" else "mulher"
        self._atualizar_previews()

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        arcade.draw_lrbt_rectangle_filled(90, 710, 150, 470, (0, 0, 0, 180))
        arcade.draw_text(
            "ESCOLHA OS PERSONAGENS",
            LARGURA / 2,
            420,
            arcade.color.WHITE,
            28,
            anchor_x="center",
        )
        self.sprite_previews.draw()
        arcade.draw_text(
            f"JOGADOR 1: {self.selecoes[0].upper()}",
            280,
            235,
            arcade.color.WHITE,
            16,
            anchor_x="center",
        )
        arcade.draw_text(
            "A/D: TROCAR",
            280,
            205,
            arcade.color.WHITE,
            13,
            anchor_x="center",
        )
        if self.quantidade_jogadores == 2:
            arcade.draw_text(
                f"JOGADOR 2: {self.selecoes[1].upper()}",
                520,
                235,
                arcade.color.WHITE,
                16,
                anchor_x="center",
            )
            arcade.draw_text(
                "SETAS: TROCAR",
                520,
                205,
                arcade.color.WHITE,
                13,
                anchor_x="center",
            )
        arcade.draw_text(
            "ENTER: CONTINUAR   |   ESC: MENU",
            LARGURA / 2,
            170,
            arcade.color.WHITE,
            14,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaMenu())
        elif key in (arcade.key.A, arcade.key.D):
            self._alternar_personagem(0)
        elif self.quantidade_jogadores == 2 and key in (arcade.key.LEFT, arcade.key.RIGHT):
            self._alternar_personagem(1)
        elif key == arcade.key.ENTER:
            self.window.show_view(
                TelaFase(
                    self.nome_jogador,
                    1,
                    personagens=tuple(self.selecoes[:self.quantidade_jogadores]),
                    dificuldade=self.dificuldade,
                )
            )


class TelaRanking(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.cenario_sprite = arcade.Sprite("kauan.jpg") 
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)
        self.melhores_solo = buscar_top10("solo")
        self.melhores_cooperativo = buscar_top10("cooperativo")
        

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        arcade.draw_text("TOP 10", 330, 550, arcade.color.BLACK, 24)
        arcade.draw_text(
            "1 JOGADOR",
            200,
            505,
            arcade.color.BLACK,
            16,
            anchor_x="center",
        )
        arcade.draw_text(
            "2 JOGADORES",
            600,
            505,
            arcade.color.BLACK,
            16,
            anchor_x="center",
        )
        arcade.draw_line(390, 160, 390, 485, arcade.color.LIGHT_GRAY, 1)
        arcade.draw_text("[ESC] PARA MENU", 100, 120, arcade.color.BLACK, 12)
        arcade.draw_text("[J] PARA JOGAR", 100, 100, arcade.color.BLACK, 12)

        for centro_x, x, melhores in (
            (200, 120, self.melhores_solo),
            (600, 470, self.melhores_cooperativo),
        ):
            if not melhores:
                arcade.draw_text(
                    "Sem partidas",
                    centro_x,
                    426,
                    arcade.color.BLACK,
                    14,
                    anchor_x="center",
                )
                continue
            for posicao, resultado in enumerate(melhores, start=1):
                texto = (
                    f"{posicao}. {resultado.nome_jogador[:12]} | "
                    f"{resultado.pontos} pts | "
                    f"{NOMES_DIFICULDADE[resultado.dificuldade]} | "
                    f"{resultado.tempo_partida:.1f}s"
                )
                arcade.draw_text(
                    texto,
                    x,
                    465 - (posicao - 1) * 30,
                    arcade.color.BLACK,
                    11,
                )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_menu = TelaMenu()
            self.window.show_view(tela_menu)
        if key == arcade.key.J:
            self.window.show_view(TelaModoJogo("Jogador"))
        
class TelaInstrucao(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.RED)
        self.cenario_sprite = arcade.Sprite("I_S.jpeg") 
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)
        

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        arcade.draw_text("INSTRUÇÃO", 400, 475, arcade.color.BLACK, 28, anchor_x="center")
        arcade.draw_text("|", 360, 320, arcade.color.BLACK, 120)
        arcade.draw_text("|", 360, 170, arcade.color.BLACK, 120)

        arcade.draw_text("OBJETIVOS", 265, 370, arcade.color.BLACK, 27, anchor_x="center")
        objetivos = (
            "Comum 1pt; especial 5pt.",
            "Junte moedas para avançar.",
            "Pontos x2 não mudam a meta.",
            "LUCK: poder por 8s ou vida.",
            "Coop: 10 vidas individuais.",
            "Com 15 restantes, professor caça.",
        )
        for indice, texto in enumerate(objetivos):
            arcade.draw_text(
                texto,
                150,
                345 - indice * 14,
                arcade.color.BLACK,
                9,
                width=200,
                align="left",
                anchor_x="left",
            )

        arcade.draw_text("INIMIGOS", 245, 235, arcade.color.BLACK, 27, anchor_x="center")
        inimigos = (
            "ET: persegue o jogador mais proximo.",
            "Professor: patrulha e depois persegue.",
            "Final: 3 ETs e 2 perseguidores.",
        )
        for indice, texto in enumerate(inimigos):
            arcade.draw_text(
                texto,
                245,
                203 - indice * 15,
                arcade.color.BLACK,
                10,
                anchor_x="center",
            )

        arcade.draw_text("CONTROLES", 555, 370, arcade.color.BLACK, 27, anchor_x="center")
        arcade.draw_text("↑", 555, 340, arcade.color.BLACK, 18, anchor_x="center")
        arcade.draw_text("W", 555, 315, arcade.color.BLACK, 20, anchor_x="center")
        arcade.draw_text("←", 495, 285, arcade.color.BLACK, 18, anchor_x="center")
        arcade.draw_text("A", 525, 285, arcade.color.BLACK, 20, anchor_x="center")
        arcade.draw_text("D", 585, 285, arcade.color.BLACK, 20, anchor_x="center")
        arcade.draw_text("→", 615, 285, arcade.color.BLACK, 18, anchor_x="center")
        arcade.draw_text("DESCRIÇÃO", 555, 215, arcade.color.BLACK, 27, anchor_x="center")
        comandos = (
            "Solo: A/D move | W pula.",
            "Coop: P1 W/A/D | P2 setas.",
            "Menu: JOGAR > modo.",
            "P: pausa | ESC: menu.",
        )
        for indice, texto in enumerate(comandos):
            arcade.draw_text(
                texto,
                555,
                183 - indice * 17,
                arcade.color.BLACK,
                10,
                anchor_x="center",
            )
        arcade.draw_text("M: VOLTAR AO MENU", 400, 70, arcade.color.BLACK, 10, anchor_x="center")
        

  
        






        
                
        




    def on_key_press(self, key,modyfiers):
        if key == arcade.key.ESCAPE or key == arcade.key.M:
            tela_inicial = TelaMenu()
            self.window.show_view(tela_inicial)
            
            

class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.WHITE)

        # Fundo
        self.cenario_sprite = arcade.Sprite("I_S.jpeg")
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2

        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)

        # Avatares
        self.sprite_integrantes = arcade.SpriteList()

        # Julia
        julia = arcade.Sprite("bia.png", scale=2)
        julia.center_x = 250
        julia.center_y = 300
        self.sprite_integrantes.append(julia)

        # Kauan
        kauan = arcade.Sprite("prof.png", scale=2)
        kauan.center_x = 550
        kauan.center_y = 300
        self.sprite_integrantes.append(kauan)

    def on_draw(self):
        self.clear()

        self.sprite_cenario.draw()
        self.sprite_integrantes.draw()

        arcade.draw_text("SOBRE O JOGO" ,295, 475, arcade.color.BLACK, 23)
        arcade.draw_text("Desenvolvedores",290, 420,arcade.color.BLACK,20)

        arcade.draw_text("Julia Matias",185, 180, arcade.color.BLACK,18)
        arcade.draw_text("|" ,360, 285, arcade.color.BLACK, 120)
        arcade.draw_text("|" ,360, 193, arcade.color.BLACK, 120)

        arcade.draw_text("Kauan Campois",480, 180,arcade.color.BLACK,18)
        arcade.draw_text("ESC| M: Botão para voltar pro menu" ,173, 70, arcade.color.BLACK, 20)

        

    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_menu = TelaMenu()
            self.window.show_view(tela_menu)









class TelaGanhou(arcade.View):
    def __init__(
        self,
        pontuacao,
        tempo,
        nome_jogador="",
        venceu=True,
        modo_jogo="solo",
        dificuldade="medio",
    ):
        super().__init__()
        self.pontuacao = pontuacao
        self.tempo = tempo
        self.nome_jogador = nome_jogador[:20]
        self.venceu = venceu
        self.modo_jogo = modo_jogo
        self.dificuldade = dificuldade
        self.resultado_salvo = False
        arcade.set_background_color(arcade.color.PURPLE)
        self.cenario_sprite = arcade.Sprite("Parabens.jpeg") 
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)
        

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        titulo = "PARABÉNS" if self.venceu else "FIM DE JOGO"
        arcade.draw_text(titulo,220 ,470,arcade.color.BLACK, 50)
        if not self.venceu:
            arcade.draw_text("SUAS VIDAS ACABARAM", 240, 400, arcade.color.BLACK, 22)
        elif self.pontuacao >= 30:
            arcade.draw_text(f"INACREDITÁVEL",155 ,380,arcade.color.BLACK, 50)

        arcade.draw_text(f"PONTUAÇÃO {self.pontuacao}",145 ,300, arcade.color.BLACK, 50)
        arcade.draw_text(f"TEMPO {self.tempo:.1f}s",320 ,200, arcade.color.BLACK, 20)
        modo_texto = "2 JOGADORES" if self.modo_jogo == "cooperativo" else "1 JOGADOR"
        arcade.draw_text(
            f"{modo_texto} | {NOMES_DIFICULDADE[self.dificuldade]}",
            400,
            170,
            arcade.color.BLACK,
            14,
            anchor_x="center",
        )
        arcade.draw_text("CONFIRME OU EDITE SEU NOME", 255, 135, arcade.color.BLACK, 16)
        arcade.draw_text(self.nome_jogador + "_", 340, 105, arcade.color.BLACK, 18)
        if self.resultado_salvo:
            arcade.draw_text("PONTUACAO SALVA", 325, 65, arcade.color.BLACK, 14)
        else:
            arcade.draw_text("ENTER: SALVAR", 325, 65, arcade.color.BLACK, 14)
        arcade.draw_text("R: RANKING | ESC: MENU", 620, 570, arcade.color.BLACK, 12)

    def on_key_press(self, key, modifiers):
        if not self.resultado_salvo:
            if key == arcade.key.BACKSPACE:
                self.nome_jogador = self.nome_jogador[:-1]
                return
            if key == arcade.key.ENTER:
                self._salvar_resultado()
                return

        if key == arcade.key.R:
            self._salvar_resultado()
            self.window.show_view(TelaRanking())
            return
        if key == arcade.key.ESCAPE:
            self._salvar_resultado()
            tela_menu = TelaMenu()
            self.window.show_view(tela_menu)

    def on_text(self, texto):
        if not self.resultado_salvo:
            caracteres_validos = "".join(
                caractere for caractere in texto
                if caractere.isalnum() or caractere == " "
            )
            self.nome_jogador = (self.nome_jogador + caracteres_validos)[:20]

    def _salvar_resultado(self):
        if self.resultado_salvo:
            return
        self.nome_jogador = self.nome_jogador.strip() or "Jogador"
        salvar_resultado(
            self.nome_jogador,
            self.pontuacao,
            self.tempo,
            self.modo_jogo,
            self.dificuldade,
        )
        self.resultado_salvo = True


class TelaFase(arcade.View):
    def __init__(
        self,
        nome_jogador,
        fase,
        pontuacao=0,
        tempo=0,
        vidas=VIDAS_INICIAIS,
        personagens=("mulher",),
        dificuldade="medio",
    ):
        super().__init__()
        self.nome_jogador = nome_jogador
        self.dificuldade = dificuldade
        self.fase = fase
        self.pontuacao = pontuacao
        self.tempo = tempo
        self.personagens = tuple(personagens)
        self.vidas_jogadores = normalizar_vidas(vidas, len(self.personagens))
        self.cenario = arcade.Sprite(FASES[fase]["cenario"])
        self.cenario.width = LARGURA
        self.cenario.height = ALTURA
        self.cenario.center_x = LARGURA / 2
        self.cenario.center_y = ALTURA / 2
        self.cenario.color = FASES[fase]["tom"]
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario)

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        arcade.draw_lrbt_rectangle_filled(120, 680, 190, 440, (0, 0, 0, 170))
        titulo = "FASE FINAL" if self.fase == 4 else f"FASE {self.fase}"
        arcade.draw_text(
            titulo,
            LARGURA / 2,
            365,
            arcade.color.WHITE,
            42,
            anchor_x="center",
        )
        descricoes = {
            1: "Explore a arena e colete as moedas.",
            2: "A escola foi tomada. Fique de olho nos dois ETs.",
            3: "Mais plataformas e perseguidores na arena.",
            4: "3 ETs e 2 perseguidores: um voando e outro no chao.",
        }
        arcade.draw_text(
            descricoes[self.fase],
            LARGURA / 2,
            300,
            arcade.color.WHITE,
            16,
            anchor_x="center",
        )
        vidas_texto = "   ".join(
            f"J{indice + 1}: {vidas} vidas"
            for indice, vidas in enumerate(self.vidas_jogadores)
        )
        arcade.draw_text(
            f"{vidas_texto}   Pontos: {self.pontuacao}",
            LARGURA / 2,
            255,
            arcade.color.WHITE,
            16,
            anchor_x="center",
        )
        arcade.draw_text(
            "ENTER: COMECAR   |   ESC: MENU",
            LARGURA / 2,
            215,
            arcade.color.WHITE,
            14,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.window.show_view(
                TelaJogo(
                    self.nome_jogador,
                    fase=self.fase,
                    pontuacao=self.pontuacao,
                    tempo=self.tempo,
                    vidas=self.vidas_jogadores,
                    personagens=self.personagens,
                    dificuldade=self.dificuldade,
                )
            )
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaMenu())


class TelaJogo(arcade.View):
    def _iniciar_efeito_colisao(self):
        self.tempo_tremor = 0.32
        self.tempo_flash = 0.2

    def _receber_dano(self, mensagem, jogador=None):
        jogador = jogador or self.jogador
        indice_jogador = self.jogadores.index(jogador)
        if not jogador.vivo:
            return False
        if self.tempo_escudo > 0:
            self.mensagem = "ESCUDO BLOQUEOU O ATAQUE!"
        elif self.tempo_invulnerabilidade[indice_jogador] > 0:
            return False
        else:
            self.vidas_jogadores[indice_jogador] = max(
                0,
                self.vidas_jogadores[indice_jogador] - 1,
            )
            self.pontuacao -= 1
            self.tempo_invulnerabilidade[indice_jogador] = 1.0
            self._iniciar_efeito_colisao()
            jogador.sofrer_dano()
            self.mensagem = mensagem

            if self.vidas_jogadores[indice_jogador] == 0:
                jogador.vivo = False
                jogador.change_x = 0
                jogador.change_y = 0
                jogador.color = (100, 100, 100)
                self.mensagem = f"JOGADOR {indice_jogador + 1} ELIMINADO"
                if not any(self.vidas_jogadores):
                    self.window.show_view(
                        TelaGanhou(
                            self.pontuacao,
                            self.tempo,
                            self.nome_jogador,
                            venceu=False,
                            modo_jogo=self.modo_jogo,
                            dificuldade=self.dificuldade,
                        )
                    )
                    return True

        self.tempo_mensagem = 1.5
        return False

    def _reposicionar_moeda_segura(self, moeda):
        for _ in range(100):
            moeda.center_x = random.randint(50, LARGURA - 50)
            moeda.center_y = random.randint(70, ALTURA - 50)

            if arcade.check_for_collision_with_list(moeda, self.sprite_blocos):
                continue
            if any(
                arcade.get_distance_between_sprites(moeda, jogador) < 100
                for jogador in self.jogadores
            ):
                continue
            if any(
                arcade.get_distance_between_sprites(moeda, outra) < 45
                for outra in self.sprite_moedas
                if outra is not moeda
            ):
                continue
            if arcade.check_for_collision_with_list(moeda, self.sprite_moeda_especial):
                continue
            if arcade.check_for_collision(moeda, self.escudo):
                continue
            return True

        return False

    def _processar_reaparecimento_moedas(self, delta_time):
        pendentes = []
        for tipo, tempo_restante in self.moedas_pendentes_reaparecer:
            tempo_restante -= delta_time
            if tempo_restante > 0:
                pendentes.append((tipo, tempo_restante))
                continue

            if tipo == "comum":
                moeda = Moeda()
                if self._reposicionar_moeda_segura(moeda):
                    self.sprite_moedas.append(moeda)
                else:
                    pendentes.append((tipo, 0.5))
            else:
                moeda = MoedaEspecial()
                moeda.change_x = self.velocidade
                moeda.change_y = self.velocidade
                if self._reposicionar_moeda_segura(moeda):
                    self.moeda_especial = moeda
                    self.sprite_moeda_especial.append(moeda)
                else:
                    pendentes.append((tipo, 0.5))

        self.moedas_pendentes_reaparecer = pendentes

    def _processar_aparicao_sorte(self, delta_time):
        if self.item_sorte is not None:
            self.tempo_item_sorte -= delta_time
            if self.tempo_item_sorte <= 0:
                self.item_sorte.remove_from_sprite_lists()
                self.item_sorte = None
                self.tempo_proxima_sorte = random.uniform(
                    INTERVALO_MIN_SORTE,
                    INTERVALO_MAX_SORTE,
                )
            return

        self.tempo_proxima_sorte -= delta_time
        if self.tempo_proxima_sorte > 0:
            return

        item = arcade.Sprite("luck.png", scale=0.18)
        if self._reposicionar_moeda_segura(item):
            self.item_sorte = item
            self.sprite_sorte.append(item)
            self.tempo_item_sorte = TEMPO_ITEM_SORTE
            self.mensagem = "BLOCO DA SORTE APARECEU!"
            self.tempo_mensagem = 2.0
        else:
            self.tempo_proxima_sorte = 2.0

    def _aplicar_poder_sorte(self, jogador):
        indice = self.jogadores.index(jogador)
        poderes = (
            "inimigos_lentos",
            "inimigos_pequenos",
            "jogador_pequeno",
            "pontos_dobrados",
            "vida_extra",
        )
        poder = random.choice(poderes)

        if poder == "inimigos_lentos":
            self.tempo_inimigos_lentos = TEMPO_PODER_SORTE
            self.mensagem = "SORTE: INIMIGOS LENTOS!"
        elif poder == "inimigos_pequenos":
            self.tempo_inimigos_pequenos = TEMPO_PODER_SORTE
            self.mensagem = "SORTE: INIMIGOS MENORES!"
        elif poder == "jogador_pequeno":
            self.tempo_jogadores_pequenos[indice] = TEMPO_PODER_SORTE
            self.mensagem = "SORTE: VOCE FICOU PEQUENO!"
        elif poder == "pontos_dobrados":
            self.tempo_pontos_dobrados = TEMPO_PODER_SORTE
            self.mensagem = "SORTE: PONTOS DAS MOEDAS EM DOBRO!"
        else:
            self.vidas_jogadores[indice] = min(
                VIDAS_INICIAIS,
                self.vidas_jogadores[indice] + 1,
            )
            self.mensagem = "SORTE: GANHOU UMA VIDA!"

        self.tempo_mensagem = 2.0

    def _atualizar_poderes_sorte(self, delta_time):
        self.tempo_inimigos_lentos = max(
            0.0,
            self.tempo_inimigos_lentos - delta_time,
        )
        self.tempo_inimigos_pequenos = max(
            0.0,
            self.tempo_inimigos_pequenos - delta_time,
        )
        self.tempo_pontos_dobrados = max(
            0.0,
            self.tempo_pontos_dobrados - delta_time,
        )

        for indice, jogador in enumerate(self.jogadores):
            self.tempo_jogadores_pequenos[indice] = max(
                0.0,
                self.tempo_jogadores_pequenos[indice] - delta_time,
            )
            escala = self.escalas_originais_jogadores[indice]
            fator = 0.55 if self.tempo_jogadores_pequenos[indice] > 0 else 1.0
            jogador.scale = (escala[0] * fator, escala[1] * fator)

        fator_inimigos = 0.55 if self.tempo_inimigos_pequenos > 0 else 1.0
        for inimigo, escala in zip(self.todos_inimigos, self.escalas_originais_inimigos):
            inimigo.scale = (escala[0] * fator_inimigos, escala[1] * fator_inimigos)

    def _alternar_pause(self):
        self.pausado = not self.pausado
        for jogador in self.jogadores:
            jogador.change_x = 0

    def _reposicionar_sprite_seguro(self, sprite, distancia_minima=250, margem=40):
        for _ in range(200):
            x = random.randint(margem, LARGURA - margem)
            y = random.randint(50, ALTURA - 150)
            sprite.center_x = x
            sprite.center_y = y

            outros_inimigos = [
                *getattr(self, "sprite_inimigo", ()),
                *getattr(self, "sprite_inimigo_especial", ()),
            ]
            inimigos_muito_proximos = any(
                outro is not sprite
                and arcade.get_distance_between_sprites(sprite, outro) < 120
                for outro in outros_inimigos
            )

            if (
                all(
                    arcade.get_distance_between_sprites(sprite, jogador) >= distancia_minima
                    for jogador in self.jogadores
                )
                and not inimigos_muito_proximos
                and not arcade.check_for_collision_with_list(sprite, self.sprite_blocos)
            ):
                return True

        sprite.center_x = 100
        sprite.center_y = 150
        return False

    def __init__(
        self,
        nome_jogador="Jogador",
        fase=1,
        pontuacao=0,
        tempo=0,
        vidas=VIDAS_INICIAIS,
        personagens=("mulher",),
        dificuldade="medio",
    ):
        super().__init__()
        self.nome_jogador = nome_jogador
        self.personagens = tuple(personagens)[:2] or ("mulher",)
        self.modo_jogo = "cooperativo" if len(self.personagens) == 2 else "solo"
        self.dificuldade = dificuldade
        self.multiplicador_dificuldade = MULTIPLICADORES_DIFICULDADE[dificuldade]
        self.fase = fase
        self.config_fase = FASES[fase]
        arcade.set_background_color(arcade.color.WHITE)
        
        self.pontuacao = pontuacao
        self.camera = arcade.Camera2D(position=(LARGURA / 2, ALTURA / 2))
        self.tempo_tremor = 0.0
        self.tempo_flash = 0.0
        self.deslocamento_camera_x = 0.0
        self.deslocamento_camera_y = 0.0
        self.velocidade = 3
        self.tempo = tempo
        self.tempo_escudo = 0.0
        self.tempo_invulnerabilidade = [0.0] * len(self.personagens)
        self.vidas_jogadores = normalizar_vidas(vidas, len(self.personagens))
        self.pausado = False
        self.tempo_teleporte_moedas = 0.0
        self.tempo_proxima_sorte = random.uniform(
            PRIMEIRA_SORTE_MIN,
            PRIMEIRA_SORTE_MAX,
        )
        self.tempo_item_sorte = 0.0
        self.tempo_inimigos_lentos = 0.0
        self.tempo_inimigos_pequenos = 0.0
        self.tempo_pontos_dobrados = 0.0
        self.tempo_jogadores_pequenos = [0.0] * len(self.personagens)
        self.item_sorte = None
        self.moedas_pendentes_reaparecer = []
        self.perseguidor_ativado = False
        self.mensagem = ""
        self.tempo_mensagem = 0
        self.velocidade_ini = (
            self.config_fase["velocidade_chao"] * self.multiplicador_dificuldade
        )
        self.cenario_sprite = arcade.Sprite(self.config_fase["cenario"])
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2
        self.cenario_sprite.color = self.config_fase["tom"]
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)
        
        # Criar blocos PRIMEIRO
        self.sprite_blocos = arcade.SpriteList()

        for x in range(32, LARGURA + 32, 64):
            chao = Bloco(x, y=30)
            self.sprite_blocos.append(chao)
        posicoes_plataforma = self.config_fase["plataformas"]
        for x, y in posicoes_plataforma:
            plataforma = BlocoV(x, y)
            self.sprite_blocos.append(plataforma)

        # Agora criar jogador
        self.jogadores = []
        self.sprite_jogador = arcade.SpriteList()
        for indice, personagem in enumerate(self.personagens):
            jogador = Player(personagem)
            jogador.center_x = 350 if indice == 0 else 450
            jogador.center_y = 150
            if self.vidas_jogadores[indice] == 0:
                jogador.vivo = False
                jogador.color = (100, 100, 100)
            self.jogadores.append(jogador)
            self.sprite_jogador.append(jogador)
        self.jogador = self.jogadores[0]

        self.escudo = arcade.Sprite("moeda_especial.png", scale=0.28)
        self.sprite_escudo = arcade.SpriteList()
        self.sprite_sorte = arcade.SpriteList()
        self._reposicionar_sprite_seguro(self.escudo, distancia_minima=100)
        self.sprite_escudo.append(self.escudo)
        
        # Criar moedas garantindo que não nasçam sobre blocos
        self.sprite_moedas = arcade.SpriteList()
        
        for i in range(self.config_fase["moedas"]):
            moeda_valida = False
            while not moeda_valida:
                self.moeda = Moeda()
                self.moeda.center_x = random.randint(50, LARGURA - 50)
                self.moeda.center_y = random.randint(50, ALTURA - 50)
                
                # Verifica se colidiu com algum bloco
                if not arcade.check_for_collision_with_list(self.moeda, self.sprite_blocos):
                    moeda_valida = True
                    self.sprite_moedas.append(self.moeda)
        self.sprite_inimigo = arcade.SpriteList()
        self.inimigos_chao = []
        for indice in range(self.config_fase["perseguidores"]):
            inimigo = Inimigo()
            divisor = max(1, self.config_fase["perseguidores"] - 1)
            inimigo.center_x = 90 + indice * (LARGURA - 180) / divisor
            inimigo.center_y = 154
            inimigo.change_x = self.velocidade_ini if indice % 2 == 0 else -self.velocidade_ini
            inimigo.change_y = 0
            self.inimigos_chao.append(inimigo)
            self.sprite_inimigo.append(inimigo)
        self.inimigo = self.inimigos_chao[0]
        self.intervalos_pulo_inimigos = [0.0] * len(self.inimigos_chao)

        self.sprite_inimigo_especial = arcade.SpriteList()
        posicoes_ets = (
            (LARGURA - 70, ALTURA - 70),
            (70, ALTURA - 70),
            (LARGURA / 2, ALTURA - 70),
        )
        for indice in range(self.config_fase["ets"]):
            inimigo_especial = Inimigo_Especial(self.jogadores)
            inimigo_especial.velocidade = (
                self.config_fase["velocidade_et"] * self.multiplicador_dificuldade
            )
            inimigo_especial.center_x, inimigo_especial.center_y = posicoes_ets[indice]
            self.sprite_inimigo_especial.append(inimigo_especial)
        self.inimigo_especial = self.sprite_inimigo_especial[0]
        self.todos_inimigos = [
            *self.inimigos_chao,
            *self.sprite_inimigo_especial,
        ]
        self.escalas_originais_inimigos = [inimigo.scale for inimigo in self.todos_inimigos]
        self.escalas_originais_jogadores = [jogador.scale for jogador in self.jogadores]

        


        

        self.sprite_moeda_especial = arcade.SpriteList()
        
        # Criar moeda especial garantindo que não nasça sobre blocos
        moeda_especial_valida = False
        while not moeda_especial_valida:
            self.moeda_especial = MoedaEspecial()
            self.moeda_especial.center_x = random.randint(100, LARGURA - 100)
            self.moeda_especial.center_y = random.randint(100, ALTURA - 100)
            
            # Verifica se colidiu com algum bloco
            if not arcade.check_for_collision_with_list(self.moeda_especial, self.sprite_blocos):
                moeda_especial_valida = True
        
        self.moeda_especial.change_x = self.velocidade
        self.moeda_especial.change_y = self.velocidade
        
        self.sprite_moeda_especial.append(self.moeda_especial)


        self.engines_fisica_jogadores = [
            arcade.PhysicsEnginePlatformer(
                player_sprite=jogador,
                walls=self.sprite_blocos,
                gravity_constant=GRAVIDADE,
            )
            for jogador in self.jogadores
        ]
        self.engine_fisica = self.engines_fisica_jogadores[0]

        self.engines_fisica_inimigos = [
            arcade.PhysicsEnginePlatformer(
                player_sprite=inimigo,
                walls=self.sprite_blocos,
                gravity_constant=GRAVIDADE,
            )
            for inimigo in self.inimigos_chao
        ]
        self.engine_fisica_inimigo = self.engines_fisica_inimigos[0]
       
       
    def on_draw(self):
        self.clear()
        self.camera.position = (
            LARGURA / 2 - self.deslocamento_camera_x,
            ALTURA / 2 - self.deslocamento_camera_y,
        )
        self.camera.use()
        self.sprite_cenario.draw()
        self.sprite_blocos.draw()

        self.sprite_inimigo.draw()
        self.sprite_moedas.draw()
        self.sprite_moeda_especial.draw()
        self.sprite_jogador.draw()
        self.sprite_inimigo_especial.draw()
        if len(self.sprite_escudo) > 0:
            self.sprite_escudo.draw()
            arcade.draw_circle_outline(
                self.escudo.center_x,
                self.escudo.center_y,
                max(self.escudo.width, self.escudo.height) * 0.65,
                arcade.color.CYAN,
                3,
            )
        if self.item_sorte is not None:
            self.sprite_sorte.draw()
            arcade.draw_circle_outline(
                self.item_sorte.center_x,
                self.item_sorte.center_y,
                max(self.item_sorte.width, self.item_sorte.height) * 0.65,
                arcade.color.YELLOW,
                3,
            )
        if self.tempo_escudo > 0:
            for jogador in self.jogadores:
                if not jogador.vivo:
                    continue
                arcade.draw_circle_outline(
                    jogador.center_x,
                    jogador.center_y,
                    max(jogador.width, jogador.height) * 0.7,
                    arcade.color.CYAN,
                    3,
                )
        if self.tempo_flash > 0:
            alpha = int(125 * self.tempo_flash / 0.2)
            arcade.draw_lrbt_rectangle_filled(
                -16,
                LARGURA + 16,
                -16,
                ALTURA + 16,
                (255, 0, 0, alpha),
            )
        modo_jogo = "COOPERATIVO" if len(self.jogadores) == 2 else self.nome_jogador
        arcade.draw_text(f"{modo_jogo} | Pontos: {self.pontuacao}", 10, 570, arcade.color.BLACK, 14)
        arcade.draw_text(f"FASE {self.fase}/4", 350, 570, arcade.color.BLACK, 14)
        arcade.draw_text(f"Tempo: {self.tempo:.1f}s",10,545,arcade.color.BLACK,14)
        status_escudo = f"Escudo: {self.tempo_escudo:.1f}s" if self.tempo_escudo > 0 else "Escudo: vazio"
        arcade.draw_text(status_escudo,10,520,arcade.color.BLACK,14)
        efeitos_sorte = []
        if self.tempo_inimigos_lentos > 0:
            efeitos_sorte.append(f"Inimigos lentos: {self.tempo_inimigos_lentos:.0f}s")
        if self.tempo_inimigos_pequenos > 0:
            efeitos_sorte.append(f"Inimigos pequenos: {self.tempo_inimigos_pequenos:.0f}s")
        if self.tempo_pontos_dobrados > 0:
            efeitos_sorte.append(f"Pontos x2: {self.tempo_pontos_dobrados:.0f}s")
        for indice, tempo_pequeno in enumerate(self.tempo_jogadores_pequenos):
            if tempo_pequeno > 0:
                efeitos_sorte.append(f"J{indice + 1} pequeno: {tempo_pequeno:.0f}s")
        texto_efeitos_sorte = " | ".join(efeitos_sorte)
        if texto_efeitos_sorte:
            arcade.draw_text(
                f"♣ Bônus: {texto_efeitos_sorte}",
                10,
                475,
                arcade.color.BLACK,
                12,
            )
        vidas_texto = " | ".join(
            f"J{indice + 1}: {vidas}"
            for indice, vidas in enumerate(self.vidas_jogadores)
        )
        arcade.draw_text(
            f"{vidas_texto} | Moedas: {len(self.sprite_moedas)}"
            f" | Dificuldade: {NOMES_DIFICULDADE[self.dificuldade]}",
            10,
            495,
            arcade.color.BLACK,
            14,
        )
        arcade.draw_text("ESC: MENU",700,510,arcade.color.BLACK,12)

        if self.tempo_mensagem > 0:
            arcade.draw_text(self.mensagem,220,440,arcade.color.RED,20)

        if self.pausado:
            arcade.draw_lrbt_rectangle_filled(0, LARGURA, 0, ALTURA, (0, 0, 0, 170))
            arcade.draw_text("PAUSADO", 300, 330, arcade.color.WHITE, 42)
            arcade.draw_text("P ou clique em CONTINUAR", 275, 285, arcade.color.WHITE, 18)

        texto_pause = "CONTINUAR" if self.pausado else "|| PAUSAR"
        arcade.draw_text(
            texto_pause,
            735,
            552,
            arcade.color.BLACK,
            12,
            anchor_x="center",
        )
        



    def on_update(self,delta_time):
        if self.pausado:
            return

        perseguicao_ativa = self.fase == 4 or len(self.sprite_moedas) <= MOEDAS_PARA_PERSEGUICAO
        fator_lento = 0.55 if self.tempo_inimigos_lentos > 0 else 1.0
        if self.tempo_inimigos_lentos > 0 and not perseguicao_ativa:
            for inimigo in self.inimigos_chao:
                direcao = -1 if inimigo.change_x < 0 else 1
                inimigo.change_x = direcao * self.velocidade_ini * fator_lento

        if perseguicao_ativa:
            if not self.perseguidor_ativado:
                self.perseguidor_ativado = True
                self.mensagem = "OS PERSEGUIDORES COMECARAM A TE CACAR!"
                self.tempo_mensagem = 2.5

            for indice, (inimigo, engine) in enumerate(zip(
                self.inimigos_chao,
                self.engines_fisica_inimigos,
            )):
                jogadores_ativos = [jogador for jogador in self.jogadores if jogador.vivo]
                if not jogadores_ativos:
                    return
                jogador_alvo = min(
                    jogadores_ativos,
                    key=lambda jogador: arcade.get_distance_between_sprites(inimigo, jogador),
                )
                direcao = jogador_alvo.center_x - inimigo.center_x
                velocidade = (
                    self.config_fase["velocidade_chao"]
                    * MULTIPLICADOR_VELOCIDADE_PERSEGUIDOR
                    * self.multiplicador_dificuldade
                    * fator_lento
                )
                inimigo.change_x = velocidade if direcao > 0 else -velocidade if direcao < 0 else 0
                self.intervalos_pulo_inimigos[indice] = max(
                    0.0,
                    self.intervalos_pulo_inimigos[indice] - delta_time,
                )
                if (
                    jogador_alvo.center_y > inimigo.center_y + 45
                    and engine.can_jump()
                    and self.intervalos_pulo_inimigos[indice] == 0
                ):
                    inimigo.change_y = 10
                    self.intervalos_pulo_inimigos[indice] = INTERVALO_PULO_PERSEGUIDOR

        for indice, engine in enumerate(self.engines_fisica_jogadores):
            if self.jogadores[indice].vivo:
                engine.update()
        for engine in self.engines_fisica_inimigos:
            engine.update()
        
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_inimigo.update(delta_time)
        fator_lento_ets = 0.55 if self.tempo_inimigos_lentos > 0 else 1.0
        for et in self.sprite_inimigo_especial:
            et.velocidade = (
                self.config_fase["velocidade_et"]
                * self.multiplicador_dificuldade
                * fator_lento_ets
            )
        self.sprite_inimigo_especial.update(delta_time)
        self.sprite_moeda_especial.update(delta_time)
       
        self.tempo += delta_time
        self._processar_aparicao_sorte(delta_time)
        self._atualizar_poderes_sorte(delta_time)
        if self.fase == 4:
            self._processar_reaparecimento_moedas(delta_time)
        self.tempo_escudo = max(0.0, self.tempo_escudo - delta_time)
        self.tempo_invulnerabilidade = [
            max(0.0, tempo - delta_time)
            for tempo in self.tempo_invulnerabilidade
        ]
        self.tempo_teleporte_moedas += delta_time
        if self.tempo_teleporte_moedas >= INTERVALO_TELEPORTE_MOEDAS:
            self.tempo_teleporte_moedas = 0.0
            moedas_selecionadas = random.sample(
                list(self.sprite_moedas),
                min(MOEDAS_POR_TELEPORTE, len(self.sprite_moedas)),
            )
            moedas_movidas = sum(
                self._reposicionar_moeda_segura(moeda)
                for moeda in moedas_selecionadas
            )
            if moedas_movidas:
                self.mensagem = f"{moedas_movidas} moedas mudaram de lugar!"
                self.tempo_mensagem = 1.5
        if self.tempo_mensagem > 0:
            self.tempo_mensagem -= delta_time
        self.tempo_tremor = max(0, self.tempo_tremor - delta_time)
        self.tempo_flash = max(0, self.tempo_flash - delta_time)
        if self.tempo_tremor > 0:
            intensidade = 8 * self.tempo_tremor / 0.32
            self.deslocamento_camera_x = random.uniform(-intensidade, intensidade)
            self.deslocamento_camera_y = random.uniform(-intensidade, intensidade)
        else:
            self.deslocamento_camera_x = 0.0
            self.deslocamento_camera_y = 0.0

        moedas_colididas = []
        moeda_especial_colidida = []
        escudo_colidido = []
        sorte_colidida = None
        for jogador in self.jogadores:
            if not jogador.vivo:
                continue
            for moeda in arcade.check_for_collision_with_list(jogador, self.sprite_moedas):
                if moeda not in moedas_colididas:
                    moedas_colididas.append(moeda)
            for moeda in arcade.check_for_collision_with_list(jogador, self.sprite_moeda_especial):
                if moeda not in moeda_especial_colidida:
                    moeda_especial_colidida.append(moeda)
            for escudo in arcade.check_for_collision_with_list(jogador, self.sprite_escudo):
                if escudo not in escudo_colidido:
                    escudo_colidido.append(escudo)
            sorte_encontrada = arcade.check_for_collision_with_list(jogador, self.sprite_sorte)
            if sorte_encontrada:
                sorte_colidida = (jogador, sorte_encontrada[0])
                break
        moedas_direc = arcade.check_for_collision_with_list(self.moeda_especial,self.sprite_blocos)

        for escudo in escudo_colidido:
            escudo.remove_from_sprite_lists()
            self.tempo_escudo = DURACAO_ESCUDO
            self.mensagem = "ESCUDO ATIVADO POR 6 SEGUNDOS!"
            self.tempo_mensagem = 1.5

        if sorte_colidida is not None:
            jogador, item = sorte_colidida
            item.remove_from_sprite_lists()
            self.item_sorte = None
            self.tempo_proxima_sorte = random.uniform(
                INTERVALO_MIN_SORTE,
                INTERVALO_MAX_SORTE,
            )
            self._aplicar_poder_sorte(jogador)


        for jogador in self.jogadores:
            if not jogador.vivo:
                continue
            for inimigo in arcade.check_for_collision_with_list(jogador, self.sprite_inimigo):
                if self._receber_dano("TOCOU NO HOMEN PERDEU 1 PONTO!", jogador):
                    return
                self._reposicionar_sprite_seguro(inimigo)

            for inimigo_especial in arcade.check_for_collision_with_list(
                jogador,
                self.sprite_inimigo_especial,
            ):
                if self._receber_dano("TOCOU NO ET PERDEU 1 PONTO!", jogador):
                    return
                self._reposicionar_sprite_seguro(inimigo_especial, distancia_minima=220)
        for bloco in moedas_direc:
            print("moeda colidiu")
            # Calcula penetração em cada lado do bloco
            penetracao_esquerda = self.moeda_especial.right - bloco.left
            penetracao_direita = bloco.right - self.moeda_especial.left
            penetracao_topo = bloco.top - self.moeda_especial.bottom
            penetracao_fundo = self.moeda_especial.top - bloco.bottom
            
            # Encontra o lado com menor penetração (lado de colisão)
            min_penetracao = min(penetracao_esquerda, penetracao_direita, penetracao_topo, penetracao_fundo)
            
            # Rebate baseado em qual lado colidiu E reposiciona
            if min_penetracao == penetracao_esquerda:
                # Colisão na esquerda do bloco
                self.moeda_especial.right = bloco.left - 2
                self.moeda_especial.change_x *= -1
            elif min_penetracao == penetracao_direita:
                # Colisão na direita do bloco
                self.moeda_especial.left = bloco.right + 2
                self.moeda_especial.change_x *= -1
            elif min_penetracao == penetracao_topo:
                # Colisão no topo do bloco
                self.moeda_especial.bottom = bloco.top + 2
                self.moeda_especial.change_y *= -1
            else:
                # Colisão no fundo do bloco
                self.moeda_especial.top = bloco.bottom - 2
                self.moeda_especial.change_y *= -1
                                
                
                               

        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            multiplicador = 2 if self.tempo_pontos_dobrados > 0 else 1
            self.pontuacao += multiplicador
            if self.fase == 4:
                self.moedas_pendentes_reaparecer.append(
                    ("comum", TEMPO_REAPARECER_MOEDA_FINAL)
                )
           
            print(self.pontuacao)
            
        for moeda_especial in moeda_especial_colidida:
            moeda_especial.remove_from_sprite_lists()
            multiplicador = 2 if self.tempo_pontos_dobrados > 0 else 1
            self.pontuacao += 5 * multiplicador
            if self.fase == 4:
                self.moedas_pendentes_reaparecer.append(
                    ("especial", TEMPO_REAPARECER_MOEDA_FINAL)
                )
            
            print(self.pontuacao)

        
        if (
            self.fase < 4
            and len(self.sprite_moeda_especial) == 0
            and len(self.sprite_moedas) == 0
        ):
            self.window.show_view(
                TelaFase(
                    self.nome_jogador,
                    self.fase + 1,
                    self.pontuacao,
                    self.tempo,
                    self.vidas_jogadores,
                    self.personagens,
                    self.dificuldade,
                )
            )
            return

       
        

        

                            
        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self._alternar_pause()
            return
        if self.pausado and key != arcade.key.ESCAPE:
            return
        if self.jogadores[0].vivo and (
            key == arcade.key.D or (len(self.jogadores) == 1 and key == arcade.key.RIGHT)
        ):
            self.jogadores[0].change_x = self.velocidade
        if self.jogadores[0].vivo and (
            key == arcade.key.A or (len(self.jogadores) == 1 and key == arcade.key.LEFT)
        ):
            self.jogadores[0].change_x = -self.velocidade
        if self.jogadores[0].vivo and (
            key == arcade.key.W or (len(self.jogadores) == 1 and key == arcade.key.UP)
        ):
            if self.engines_fisica_jogadores[0].can_jump():
                self.jogadores[0].change_y = 16
        if len(self.jogadores) == 2 and self.jogadores[1].vivo:
            if key == arcade.key.RIGHT:
                self.jogadores[1].change_x = self.velocidade
            if key == arcade.key.LEFT:
                self.jogadores[1].change_x = -self.velocidade
            if key == arcade.key.UP and self.engines_fisica_jogadores[1].can_jump():
                self.jogadores[1].change_y = 16

        if key == arcade.key.ESCAPE:
            tela_menu = TelaMenu()
            self.window.show_view(tela_menu)

    def on_mouse_press(self, x, y, button, modifiers):
        if (
            button == arcade.MOUSE_BUTTON_LEFT
            and 680 <= x <= 790
            and 540 <= y <= 585
        ):
            self._alternar_pause()


    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D) or (
            len(self.jogadores) == 1 and key in (arcade.key.LEFT, arcade.key.RIGHT)
        ):
            self.jogadores[0].change_x = 0
            self.jogadores[0].texture = (
                self.jogadores[0].texture_parado_e
                if self.jogadores[0].virado_para == "Esquerda"
                else self.jogadores[0].texture_parado_d
            )
        if len(self.jogadores) == 2 and key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.jogadores[1].change_x = 0
            self.jogadores[1].texture = (
                self.jogadores[1].texture_parado_e
                if self.jogadores[1].virado_para == "Esquerda"
                else self.jogadores[1].texture_parado_d
            )



def executar():
    inicializar_banco()
    janela = arcade.Window(LARGURA, ALTURA, TITULO, fullscreen=False, resizable=False)
    menu_inicial = TelaMenu()
    janela.show_view(menu_inicial)
    arcade.run()


    
    
    

if __name__ == "__main__":
    executar()