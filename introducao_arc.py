# pip install arcade no terminal
import arcade

ALTURA = 600
LARGURA = 800
TITULO = "Meu Joguinho"

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("luffy.png",scale=0.1)
        self.textura_direita = arcade.load_texture("luffy.png")
        self.textura_esquerda = arcade.load_texture("Luffy2.png")
        

    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y


        if self.change_x > 0:
           self.textura_direita = self.textura_direita
        elif self.change_x < 0:
            self.textura_esquerda = self.textura_esquerda
        
        if self.right  > LARGURA:
            self.change_x = 0
            self.right = LARGURA

        if self.left < 0:
            self.change_x = 0
            self.left =0

        if self.top > ALTURA:
            self.change_y = 0
            self.top = ALTURA
        
        if self.bottom < 0:
            self.change_y = 0
            self.bottom = 0 
    
           

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png",scale=0.1)
        self.textura_direita = arcade.load_texture("moeda.png")
        

    def update(self,delta_time):
     
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > LARGURA or self.left < 0:
            self.change_x *= -1
        

        if self.top > ALTURA or  self.bottom < 0:
            self.change_y *= -1

        elif self.bottom < 0:
            self.change_y *= -1



class MeuJogo(arcade.Window):
    def __init__(self):
        super().__init__(800,600,"Meu Joguinho")
        self.movimento = 3
        


        arcade.set_background_color((226, 237, 5))
        self.jogador = Player()
        self.jogador.center_x = 0
        self.jogador.center_y = 0

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.moeda_jogo = Moeda()
        self.moeda_jogo.center_x = 280
        self.moeda_jogo.center_y = 100
        self.moeda_jogo.change_x = self.movimento
        self.moeda_jogo.change_y= self.movimento

        self.sprite_moeda_jogo = arcade.SpriteList()
        self.sprite_moeda_jogo.append(self.moeda_jogo)

    def on_draw(self):
        self.clear()
        self.sprite_jogador.draw()
        self.sprite_moeda_jogo.draw()
    

    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)
        self.sprite_moeda_jogo.update(delta_time)
    
    def on_key_press(self,key, modifiers):
        if key == arcade.key.RIGHT:
            self.jogador.change_x += self.movimento

        elif key == arcade.key.LEFT:
            self.jogador.change_x -= self.movimento


        elif key == arcade.key.UP:
            self.jogador.change_y += self.movimento
        

        elif key == arcade.key.DOWN:
            self.jogador.change_y -= self.movimento

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.jogador.change_x = 0


        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.jogador.change_y = 0
       


def executar():
    tela = MeuJogo()
    arcade.run()
    

if __name__ == "__main__":
    executar()



        