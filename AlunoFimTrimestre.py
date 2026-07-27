
import arcade
import random
#Definido Altura e Largura e Titulo da tela do jogo
ALTURA = 600
LARGURA = 800
TITULO = "A Garota, O Homen e O ET"
#anotações 
#right = direita
#left = esquerda
#bottom = fundo
# top = topo


#classe player
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("bia.png", scale = 1)
       
        self.texture_direita_a = arcade.load_texture("bia_direita2.png")
        self.texture_parado = arcade.load_texture("bia.png")

       
        self.texture_esquerda_e = arcade.load_texture("bia_esquerda2.png")
        
    def update(self,delta_time):
        self.change_y -= 0.5
        
        self.center_x += self.change_x
        self.center_y += self.change_y


        if self.change_x > 0:
            
            self.texture = self.texture_direita_a

        elif self.change_x < 0:
            
            self.texture = self.texture_esquerda_e


        if self.right  > LARGURA:
            self.right = LARGURA

        if self.left < 0:
            self.left =0

        if self.top > ALTURA:
            self.top = ALTURA
        
        if self.bottom < 0:
            self.bottom = 0 
            self.change_y =0 



class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png",scale = 0.3)

    def update(self,delta_time):
       
        if self.right > 800:
            self.right = 800
            self.change_x = 0
        if self.top > 600:
            self.top = 600
            self.change_y = 0
        if self.left < 0:
            self.left = 0
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
                

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda_especial.png", scale = 0.4)

  
    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
#right = direita
#left = esquerda
#bottom = fundo
# top = topo
        if self.right > LARGURA:
            self.right =LARGURA
            self.change_x *= -1 
        if self.left < 0:
            self.left = 0
            self.change_x *= -1 

        if self.top > ALTURA: 
            self.top = ALTURA
            self.change_y *= -1 
        
        if self.bottom < 0:
            self.bottom = 0
            self.change_y *= -1 
        


        
class Inimigo_Especial(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("alien.png", scale = 0.8)
        self.jogador = jogador
        
        self.texture_direita_a = arcade.load_texture("alien.png")       
        self.texture_esquerda_e = arcade.load_texture("alien2.png")
        self.velocidade = 3.5

    def update(self,delta_time):
        dx = self.jogador.center_x - self.center_x
        dy = self.jogador.center_y - self.center_y 

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
     
    
        if self.change_x > 0:                
            self.texture = self.texture_direita_a
        if self.change_x < 0:
            self.texture = self.texture_esquerda_e
    
        if self.right >800:
            self.right = 800
            self.change_x *=-1 
        if self.left < 0:
            self.left = 0
            self.change_x *= -1
        if self.top > 600:
            self.top = 600
            self.change_y *= -1
        if self.bottom < 0:
            self.bottom = 0
            self.change_y *= -1
    

        
#class inimigo
class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("prof.png", scale = 1)
        
        self.texture_direita_a = arcade.load_texture("prof_direita2.png")       
        self.texture_esquerda_e = arcade.load_texture("prof_esquerda2.png")

    

        
    

    def update(self,delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y -= 0.5

        if self.change_x > 0:
            self.texture = self.texture_direita_a
        if self.change_x < 0:
            self.texture = self.texture_esquerda_e

        if self.right >800:
            self.right = 800
            self.change_x *=-1 
        if self.left < 0:
            self.left = 0
            self.change_x *= -1
        if self.top > 600:
            self.top = 600
            self.change_y = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0

        
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
        arcade.draw_text("INSTRUÇÃO" ,295, 475, arcade.color.BLACK, 28)
        arcade.draw_text("|" ,360, 320, arcade.color.BLACK, 120)
        arcade.draw_text("|" ,360, 170, arcade.color.BLACK, 120)
        arcade.draw_text("OBJETIVOS" ,160, 370, arcade.color.BLACK, 30)
        arcade.draw_text("Colete 25 moedas comuns (1 ponto ",150, 345, arcade.color.BLACK, 10)
        arcade.draw_text("cada)  e 1 moeda especial (5 pontos)" ,150, 330, arcade.color.BLACK, 10)
        arcade.draw_text("Colete as 26 moedas para vencer" ,150, 315, arcade.color.BLACK, 10)
        arcade.draw_text("INIMIGOS" ,165, 250, arcade.color.BLACK, 30)
        arcade.draw_text("ET: Ninguém sabe de onde veio." ,160, 225, arcade.color.BLACK, 10)
        arcade.draw_text("Mas ele gosta de seguir a Bia " ,160, 210, arcade.color.BLACK, 10)
        arcade.draw_text("HOMEM: Dizem que está procurando" ,160, 195, arcade.color.BLACK, 10)
        arcade.draw_text("algo. Não entre no seu caminho!!" ,160, 180, arcade.color.BLACK, 10)
        arcade.draw_text("ele, só fica vagando pelo chão." ,160, 165, arcade.color.BLACK, 10)
        arcade.draw_text("CONTROLES" ,420, 370, arcade.color.BLACK, 30)
        arcade.draw_text("|W|",500,330,arcade.color.BLACK, 20)
        arcade.draw_text("|D|",545,290,arcade.color.BLACK, 20)
        arcade.draw_text("|A|", 463,290,arcade.color.BLACK, 20)
        arcade.draw_text("DESCRIÇÃO" ,425, 220, arcade.color.BLACK, 30)
        arcade.draw_text("W: Botão de Pular, OBS: x 2 pulo" ,425, 195, arcade.color.BLACK, 10)
        arcade.draw_text("A: Botão para andar para Esquerda " ,425, 180, arcade.color.BLACK, 10)
        arcade.draw_text("D: Botão para andar para direita" ,425, 165, arcade.color.BLACK, 10)
        arcade.draw_text("ESC| M: Botão para voltar pro menu" ,290, 70, arcade.color.BLACK, 10)
        

  
        






        
                
        




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

        arcade.draw_text("Kauan Campois",460, 180,arcade.color.BLACK,18)
        arcade.draw_text("ESC| M: Botão para voltar pro menu" ,173, 70, arcade.color.BLACK, 20)

        

    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_menu = TelaMenu()
            self.window.show_view(tela_menu)







class TelaMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.cenario_sprite = arcade.Sprite("menu.jpeg") 
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)
       
        

    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        
        arcade.draw_text(f"A Garota, O HomeM e O ET",75 ,500,
                arcade.color.BLACK, 40)
        
        arcade.draw_text(f"MENU",320 ,255,
        arcade.color.BLACK, 40)
        arcade.draw_text(f"CLIQUE J PARA JOGAR",320 ,220, arcade.color.BLACK, 12)
        arcade.draw_text(f"CLIQUE S PARA SOBRE O JOGO",305 ,170, arcade.color.BLACK, 10)
        arcade.draw_text(f"CLIQUE I PARA INSTRUÇÃO",305 ,120, arcade.color.BLACK, 11)


                
    def on_key_press(self,key,modyfiers):
        if key == arcade.key.I:
            tela_instrucao = TelaInstrucao()
            self.window.show_view(tela_instrucao)
        if key == arcade.key.S:
            tela_sobre = TelaSobre()
            self.window.show_view(tela_sobre)
        if key == arcade.key.J:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)

class TelaGanhou(arcade.View):
    def __init__(self, pontuacao, tempo):
        super().__init__()
        self.pontuacao = pontuacao
        self.tempo = tempo
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
        arcade.draw_text(f"PARABÉNS",220 ,470,arcade.color.BLACK, 50)
        if self.pontuacao == 30:
            arcade.draw_text(f"INACREDITÁVEL",155 ,380,arcade.color.BLACK, 50)

        arcade.draw_text(f"PONTUAÇÃO {self.pontuacao}",145 ,300, arcade.color.BLACK, 50)
        arcade.draw_text(f"TEMPO {self.tempo:.1f}s",320 ,200, arcade.color.BLACK, 20)

            
        
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_menu = TelaMenu()
            self.window.show_view(tela_menu)


    

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        
        self.pontuacao = 0
        self.registro =0
        self.velocidade = 3
        self.tempo = 0
        self.mensagem = ""
        self.tempo_mensagem = 0
        self.velocidade_ini = 2
        self.cenario_sprite = arcade.Sprite("tela_jogo.jpeg") 
        self.cenario_sprite.width = LARGURA
        self.cenario_sprite.height = ALTURA
        self.cenario_sprite.center_x = LARGURA / 2
        self.cenario_sprite.center_y = ALTURA / 2
        self.sprite_cenario = arcade.SpriteList()
        self.sprite_cenario.append(self.cenario_sprite)
        



        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 0
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.sprite_moedas = arcade.SpriteList()

        for i in range(25):
            self.moeda = Moeda()
            self.moeda.center_x = random.randint(50, LARGURA - 50)
            self.moeda.center_y = random.randint(50, ALTURA - 50)
            self.sprite_moedas.append(self.moeda)
        print(len(self.sprite_moedas))

        self.inimigo = Inimigo()
        self.inimigo.center_x = 0
        self.inimigo.center_y = 90
        self.inimigo.change_x = self.velocidade_ini
        self.inimigo.change_y = self.velocidade_ini
        self.sprite_inimigo = arcade.SpriteList()
        self.sprite_inimigo.append(self.inimigo)

        self.sprite_inimigo_especial = arcade.SpriteList()
        self.inimigo_especial = Inimigo_Especial(self.jogador)
        self.inimigo_especial.center_x = 800
        self.inimigo_especial.center_y = 600
        self.sprite_inimigo_especial.append(self.inimigo_especial)


        

        self.sprite_moeda_especial = arcade.SpriteList()
        self.moeda_especial = MoedaEspecial()
        self.moeda_especial.center_x = random.randint(100, LARGURA - 100)
        self.moeda_especial.center_y = random.randint(100, ALTURA - 100)
        self.moeda_especial.change_x = self.velocidade
        self.moeda_especial.change_y = self.velocidade
        

        self.sprite_moeda_especial.append(self.moeda_especial)
    def on_draw(self):
        self.clear()
        self.sprite_cenario.draw()
        
        
        self.sprite_inimigo.draw()
        self.sprite_moedas.draw()
        self.sprite_moeda_especial.draw()
        self.sprite_jogador.draw()
        self.sprite_inimigo_especial.draw()
        arcade.draw_text(f"Pontos Coletados: {self.pontuacao}", 10, 570,arcade.color.BLACK, 14)
        arcade.draw_text(f"Tempo: {self.tempo:.1f}s",10,545,arcade.color.BLACK,14)
        if self.tempo_mensagem > 0:
            arcade.draw_text(self.mensagem,220,515,arcade.color.RED,20)



        

    def on_update(self,delta_time):
        self.sprite_jogador.update(delta_time) 
        self.sprite_moedas.update()
        self.sprite_inimigo.update()
        self.sprite_inimigo_especial.update()
        self.sprite_moeda_especial.update()
        self.tempo += delta_time
        if self.tempo_mensagem > 0:
            self.tempo_mensagem -= delta_time

        moedas_colididas = arcade.check_for_collision_with_list(self.jogador,self.sprite_moedas)
        moeda_especial_colidida = arcade.check_for_collision_with_list(self.jogador,self.sprite_moeda_especial)
        npc_normal = arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigo)
        npc_especial = arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigo_especial)

        for inimigo in npc_normal:
            self.pontuacao -= 1
            print("Colidiu com o professor!")
            self.mensagem = "TOCOU NO HOMEN PERDEU 1 PONTO!"
            self.tempo_mensagem = 1.5
            while True:
                inimigo.center_x = random.randint(50, LARGURA - 50)
                inimigo.center_y = random.randint(50, 500)

                if arcade.get_distance_between_sprites(inimigo, self.jogador) >= 250:
                    break

        for inimigo_especial in npc_especial:
                    self.pontuacao -= 1
                    print("Colidiu com o alien!")
                    
                    self.mensagem = "TOCOU NO ET PERDEU 1 PONTO!"
                    self.tempo_mensagem = 1.5
                    while True:
                        inimigo_especial.center_x = random.randint(50, LARGURA - 50)
                        inimigo_especial.center_y = random.randint(50, ALTURA - 50)
        
                        if arcade.get_distance_between_sprites(inimigo_especial, self.jogador) >= 250:
                            break

        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
           
            self.pontuacao += 1
            self.registro +=1
            print(self.pontuacao)
            
        for moeda_especial in moeda_especial_colidida:
            moeda_especial.remove_from_sprite_lists()
            self.pontuacao +=5
            self.registro += 1
            print(self.pontuacao)

        
        if len(self.sprite_moeda_especial) == 0 and len(self.sprite_moedas) == 0:
                tela_final = TelaGanhou(self.pontuacao, self.tempo)
                self.window.show_view(tela_final)

        

        

                            
        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.D:
            self.jogador.change_x = self.velocidade
        if key == arcade.key.A:
            self.jogador.change_x = -self.velocidade
        if key == arcade.key.W and self.jogador.bottom <= 0:
            self.jogador.change_y = 23
        

        if key == arcade.key.ESCAPE:
            tela_menu = TelaMenu()
            self.window.show_view(tela_menu)


    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.jogador.change_x = 0
            self.jogador.texture = self.jogador.texture_parado
        
    



def executar():
    janela = arcade.Window(LARGURA,ALTURA,TITULO)
    menu_inicial = TelaMenu()
    janela.show_view(menu_inicial)
    arcade.run()
    
    

if __name__ == "__main__":
    executar() 