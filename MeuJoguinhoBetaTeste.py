import arcade 
class Player(arcade.sprite):
    def __init__(self):
        super().__init__("LuffyM.png",scale=0.1)
        self.textura_direita = arcade.load_texture("LuffyD.png")
        self.textura_esquerda = arcade.load_texture("LuffyE.png")
    
    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y



class Inimigo:
    def __init__(self):
        pass




class Mundo(arcade.Window):
    def __init__(self):
        super().__init__(800,600,"Meu Joguinho")
        self.movimento = 3
        


        arcade.set_background_color((226, 237, 5))
        self.jogador = Player()
        self.jogador.left = 0
        self.jogador.bottom = 0

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

    def on_draw(self):
        self.clear()
        self.sprite_jogador.draw()

    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)




class Recompensa:
    def __init__(self):
        pass



def executar():
    tela = Mundo()
    arcade.run()
    

if __name__ == "__main__":
    executar()
