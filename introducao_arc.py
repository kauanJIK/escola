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
        self.gravity = -0.5
        

    def update(self,delta_time):
        self.change_y += self.gravity
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
        self.center_y += self.change_y


        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_y < 0:
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

        
class TelaVitoria(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.PINK_LACE)


    def on_draw(self):
        self.clear()
        arcade.draw_text("Parabéns, você venceu!", LARGURA // 2, ALTURA // 2, arcade.color.BLACK, 20, anchor_x = "center")
        arcade.draw_text("Pressione ESC para sair", LARGURA // 2, 230, arcade.color.PURPLE, 16, anchor_x="center")

    def on_key_press(self,key, modifiers):
        if key == arcade.key.K:
            tela_jogo = Tela_Jogo()
            self.window.show_view(tela_jogo)

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    # Criação da tela Inicial
class Tela_Inicial(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        # self.fundo = arcade.load_texture("")

    # Desenhar tela
    def on_draw(self):
        self.clear()
        arcade.draw_text("Jogo - O luffy e a Caçada ao Rango", LARGURA // 2, ALTURA // 2, arcade.color.BLACK, 20, anchor_x = "center")
        arcade.draw_text("Pressione K para jogar ", LARGURA // 2,248, arcade.color.RED_BROWN, 16, anchor_x ="center" )
        arcade.draw_text("Pressione ESC para sair", LARGURA // 2, 230, arcade.color.PURPLE, 16, anchor_x="center")

    def on_key_press(self,key, modifiers):
        if key == arcade.key.K:
            tela_jogo = Tela_Jogo()
            self.window.show_view(tela_jogo)

        elif key == arcade.key.ESCAPE:
            arcade.close_window()


        







class Tela_Jogo(arcade.View):
    def __init__(self):
        super().__init__()
        self.movimento = 5
        self.salto = 15
        

        arcade.set_background_color((255, 200, 137))
        self.jogador = Player()
        self.jogador.left = 0
        self.jogador.bottom = 0

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)



        self.sprite_moeda_jogo = arcade.SpriteList()
        self.sprite_inimigo = arcade.SpriteList()
        self.score = 0
       
        for i in range(25):
            self.moeda_simples = Moeda()
            self.moeda_simples.center_x = random.randint(50, LARGURA - 50)
            self.moeda_simples.center_y = random.randint(50, ALTURA - 50)
            self.moeda_simples.change_x = random.choice([-2, 2])
            self.moeda_simples.change_y = random.choice([-2, 2])
            self.sprite_moeda_jogo.append(self.moeda_simples)

        self.inimigo = Inimigo()
        self.inimigo.left = 100
        self.inimigo.bottom = 0
        self.inimigo.change_x = 0
        self.inimigo.change_y = 0
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
        arcade.draw_text(f"Carnes: {self.score}", 10, ALTURA - 30, arcade.color.BLACK, 16)
    
    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)
        self.sprite_moeda_jogo.update(delta_time)
        self.sprite_inimigo.update(delta_time)

        moedas_coletadas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moeda_jogo)
        for moeda in moedas_coletadas:
            moeda.remove_from_sprite_lists()
            self.score += 1

        if len(self.sprite_moeda_jogo) == 0:
            self.window.show_view(TelaVitoria())
    
    def on_key_press(self,key, modifiers):
        if key == arcade.key.RIGHT:
            self.jogador.change_x += self.movimento
            self.inimigo.change_x -= self.movimento

        elif key == arcade.key.LEFT:
            self.jogador.change_x -= self.movimento
            self.inimigo.change_x += self.movimento

        elif key == arcade.key.UP:
            if self.jogador.bottom <= 0:
                self.jogador.change_y = self.salto

        elif key == arcade.key.ESCAPE:
            tela_inicial = Tela_Inicial()
            self.window.show_view(tela_inicial)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.jogador.change_x = 0
            self.inimigo.change_x = 0
            self.jogador.texture = self.jogador.textura_Normal
            self.inimigo.texture = self.inimigo.textura_normal
            
            
       


def executar():
    janela = arcade.Window(LARGURA,ALTURA,TITULO)
    menu_inicial = Tela_Inicial()
    janela.show_view(menu_inicial)

    arcade.run()
    
    

if __name__ == "__main__":
    executar()
