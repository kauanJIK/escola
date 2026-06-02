# pip install arcade no terminal
import arcade

ALTURA = 800
LARGURA = 600
TITULO = "Meu Joguinho"

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("luffy.png",scale=0.3)
        self.textura_direita = arcade.load_texture("luffy.png")
        self.textura_esquerda = arcade.load_texture("Luffy2.png")
        

    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y


        if self.center_x > 0:
           self.textura_direita = self.textura_direita
        elif self.center_x < 0:
            self.textura_esquerda = self.textura_esquerda
    
           

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png",scale=0.1)
        self.textura_direita = arcade.load_texture("moeda.png")
        

    def update(self,delta_time):
       self.center_x += self.change_x
       self.center_y += self.change_y


class MeuJogo(arcade.Window):
    def __init__(self):
        super().__init__(800,600,"Meu Joguinho")


        arcade.set_background_color((226, 237, 5))
        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 320

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.moeda_jogo = Moeda()
        self.moeda_jogo.center_x = 280
        self.moeda_jogo.center_y = 100

        self.sprite_moeda_jogo = arcade.SpriteList()
        self.sprite_moeda_jogo.append(self.moeda_jogo)

    def on_draw(self):
        self.clear()
        self.sprite_jogador.draw()
        self.sprite_moeda_jogo.draw()
        

        




def executar():
    tela = MeuJogo()
    arcade.run()
    

if __name__ == "__main__":
    executar()



        