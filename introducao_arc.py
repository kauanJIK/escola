# pip install arcade no terminal
import random
import arcade

ALTURA = 600
LARGURA = 800
TITULO = "Meu Joguinho"

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("LuffyM.png",scale=0.8)
        self.textura_direita = arcade.load_texture("LuffyD.png")
        self.textura_esquerda = arcade.load_texture("LuffyE.png")
        self.textura_Normal = arcade.load_texture("LuffyM.png")
        

    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y


        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        
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


class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("Ini.png",scale = 0.8)
        self.textura_direita = arcade.load_texture("IniD.png")
        self.textura_esquerda = arcade.load_texture("IniE.png")
        self.textura_normal = arcade.load_texture("Ini.png")


    def update(self,delta_time):
        self.center_x += self.change_x
        # self.center_y += self.change_y


        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        
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

        if self.right > LARGURA or self.left < 0:
            self.change_x *= -1
        

        if self.top > ALTURA or  self.bottom < 0:
            self.change_y *= -1

        elif self.bottom < 0:
            self.change_y *= -1

           

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("Carne.png",scale=0.5)
        self.textura_direita = arcade.load_texture("Carne.png")
        

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
        self.movimento = 5
        


        arcade.set_background_color((226, 237, 5))
        self.jogador = Player()
        self.jogador.left = 0
        self.jogador.bottom = 0

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)



        self.sprite_moeda_jogo = arcade.SpriteList()
        
       
        for i in range(25):
            self.moeda_simples = Moeda()
            self.moeda_simples.center_x = random.randint(50, LARGURA -50)
            self.moeda_simples.center_y = random.randint(50, ALTURA -50)
            
            self.sprite_moeda_jogo.append(self.moeda_simples)


            self.sprite_inimigo = arcade.SpriteList()
        
       
       
            self.inimigo = Inimigo()
            self.inimigo.left = 100
            self.inimigo.bottom =0

            self.sprite_inimigo.append(self.inimigo)


     





        # self.moeda_jogo = Moeda()
        # self.moeda_jogo.center_x = 280
        # self.moeda_jogo.center_y = 100
        # self.moeda_jogo.change_x = self.movimento
        # self.moeda_jogo.change_y= self.movimento
        # self.sprite_moeda_jogo.append(self.moeda_jogo)

        # self.moeda2 = Moeda()
        # self.moeda2.left =0
        # self.moeda2.bottom = 60
        # self.sprite_moeda_jogo.append(self.moeda2)

        # self.moeda3 = Moeda()
        # self.moeda3.left =700
        # self.moeda3.bottom = 60
        # self.sprite_moeda_jogo.append(self.moeda3)
        

        # self.sprite_moeda_jogo = arcade.SpriteList()
        # self.sprite_moeda_jogo.append(self.moeda_jogo)
        # self.sprite_moeda_jogo.append(self.moeda2)
        # self.sprite_moeda_jogo.append(self.moeda3)


    def on_draw(self):
        self.clear()
        self.sprite_jogador.draw()
        self.sprite_moeda_jogo.draw()
        self.sprite_inimigo.draw()
    

    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)
        self.sprite_moeda_jogo.update(delta_time)
        self.sprite_inimigo.update(delta_time)
    
    def on_key_press(self,key, modifiers):
        if key == arcade.key.RIGHT:
            self.jogador.change_x += self.movimento
            self.inimigo.change_x += self.movimento
            


        elif key == arcade.key.LEFT:
            self.jogador.change_x -= self.movimento
            self.inimigo.change_x -= self.movimento


        # elif key == arcade.key.UP:
        #     self.jogador.change_y += self.movimento
        

        # elif key == arcade.key.DOWN:
        #     self.jogador.change_y -= self.movimento

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.jogador.change_x = 0
            self.jogador.texture = self.jogador.textura_Normal
            self.inimigo.texture = self.inimigo.textura_normal
            
            


        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.jogador.change_y = 0
            self.jogador.texture = self.jogador.textura_Normal
            self.inimigo.texture = self.inimigo.textura_normal
            
       


def executar():
    tela = MeuJogo()
    arcade.run()
    

if __name__ == "__main__":
    executar()
