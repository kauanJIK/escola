# pip install arcade no terminal
import arcade

ALTURA = 800
LARGURA = 600
TITULO = "Meu Joguinho"

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("Luffy.png",scale=0.1)
        self.textura_direita = arcade.load_texture("Luffy.png")
        self.textura_esquerda = arcade.load_texture("Luffy2.png")
        

    def update(self,delta_time):
       pass


class MeuJogo(arcade.Window):
    def __init__(self):
        super().__init__(800,600,"Meu Joguinho")


        arcade.set_background_color((226, 237, 5))
        self.personagem = Player()
        self.personagem.center_x = 400
        self.personagem.center_y = 200
        

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.personagem)

    def on_update(self, delta_time):
        pass




def executar():
    tela = MeuJogo()
    arcade.run()
    

if __name__ == "__main__":
    executar()



        