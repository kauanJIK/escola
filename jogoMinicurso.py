import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class AplicativoBetEducativo:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Educativo: Arquitetura de Apostas")
        
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.sair_tela_cheia)
        self.root.bind("<space>", self.atalho_tecla_cashout)

        self.nome_equipe = "Equipe Padrão"
        self.saldo = 100.0
        self.aposta_atual = 10.0
        self.multiplicador = 1.0
        self.rodando = False
        self.limite_crash = 1.0
        
        self.rodada_atual = 0
        self.total_rodadas_meta = 10
        
        self.alternador_piscar = False
        
        self.total_apostado_equipe = 0.0
        self.total_retirado_equipe = 0.0
        self.lucro_acumulado_casa = 0.0
        self.divida_acumulada = 0.0  
        
        self.ranking_turma = []

        self.mostrar_menu()

    def sair_tela_cheia(self, event=None):
        self.root.attributes("-fullscreen", False)

    def atalho_tecla_cashout(self, event=None):
        if self.rodando:
            self.fazer_cashout()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        self.limpar_tela()
        self.root.config(bg="#1e1e2e")

        tk.Label(self.root, text="LABORATÓRIO DE ENGENHARIA DE APOSTAS", font=("Arial", 24, "bold"), fg="#f9e2af", bg="#1e1e2e").pack(pady=30)
        tk.Label(self.root, text=f"Última Equipe Ativa: {self.nome_equipe}", font=("Arial", 14), fg="#89b4fa", bg="#1e1e2e").pack(pady=5)

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🎮 CADASTRAR EQUIPE & JOGAR", font=("Arial", 13, "bold"), bg="#a6e3a1", fg="#11111b", width=35, pady=10, command=self.preparar_jogo).pack(pady=10)
        tk.Button(btn_frame, text="📊 DADOS REAIS & PLATAFORMAS (ALERTA)", font=("Arial", 13, "bold"), bg="#fab387", fg="#11111b", width=35, pady=10, command=self.mostrar_dados_reais).pack(pady=10)
        tk.Button(btn_frame, text="🏆 PLACAR DA TURMA", font=("Arial", 13, "bold"), bg="#f9e2af", fg="#11111b", width=35, pady=10, command=self.mostrar_placar).pack(pady=10)
        tk.Button(btn_frame, text="ℹ️ SOBRE O MINIGAME", font=("Arial", 13, "bold"), bg="#89b4fa", fg="#11111b", width=35, pady=10, command=self.mostrar_sobre).pack(pady=10)
        tk.Button(btn_frame, text="❌ SAIR (Aperte ESC para sair da Tela Cheia)", font=("Arial", 11), bg="#f38ba8", fg="#11111b", width=35, pady=8, command=self.root.quit).pack(pady=20)

    def mostrar_dados_reais(self):
        self.limpar_tela()
        self.root.config(bg="#1e1e2e")

        tk.Label(self.root, text="RADIOGRAFIA DO VÍCIO: DADOS REAIS NO BRASIL", font=("Arial", 18, "bold"), fg="#f38ba8", bg="#1e1e2e").pack(pady=15)

        frame_dados = tk.Frame(self.root, bg="#11111b", bd=3, relief="solid")
        frame_dados.pack(pady=5, fill="x", padx=80, ipady=10)

        info_texto = (
            "• PLATAFORMAS DE MAIOR CIRCULAÇÃO ENTRE JOVENS:\n"
            "  - Betano, Esportes da Sorte, Blaze (focada em crash/cassino), Stake, Bet365 e KTO.\n\n"
            "• ESTATÍSTICAS OFICIAIS DE ADOLESCENTES E JOVENS (PESQUISAS RECENTES):\n"
            "  - Cerca de 11% a 46% dos jovens e estudantes secundaristas já realizaram apostas online.\n"
            "  - Mais de 55% dos adolescentes expostos apresentam comportamento de risco ou jogam de forma problemática.\n"
            "  - Milhares de famílias no Brasil enfrentam endividamento extremo e perda de patrimônio devido ao vício."
        )

        tk.Label(frame_dados, text=info_texto, font=("Arial", 11), fg="#cdd6f4", bg="#11111b", justify="left").pack(padx=20, pady=5)

        frame_fontes = tk.Frame(self.root, bg="#181825", bd=2, relief="solid")
        frame_fontes.pack(pady=5, fill="x", padx=80, ipady=8)

        texto_fontes = (
            "📚 FONTES E REFERÊNCIAS OFICIAIS:\n"
            "1. Ministério da Fazenda / Secretaria de Prêmios e Apostas (SPA) - Dados regulatórios de tráfego financeiro.\n"
            "2. Associações de Proteção ao Crédito (Serasa / SPC Brasil) - Relatórios de endividamento por jogos digitais.\n"
            "3. Cobertura Jornalística e Investigativa (UOL, Agência Brasil, Folha de S.Paulo) - Casos de perda patrimonial familiar."
        )

        tk.Label(frame_fontes, text=texto_fontes, font=("Arial", 10, "italic"), fg="#89b4fa", bg="#181825", justify="left").pack(padx=20, pady=5)

        tk.Button(self.root, text="Voltar ao Menu", font=("Arial", 12, "bold"), bg="#bac2de", fg="#11111b", width=25, pady=6, command=self.mostrar_menu).pack(pady=15)

    def mostrar_sobre(self):
        self.limpar_tela()
        self.root.config(bg="#1e1e2e")

        tk.Label(self.root, text="SOBRE O SISTEMA", font=("Arial", 20, "bold"), fg="#89b4fa", bg="#1e1e2e").pack(pady=30)

        texto_sobre = (
            "Bem-vindo ao simulador de gerenciamento de risco e tomada de decisão.\n\n"
            "Sua equipe tem o desafio de completar no mínimo 10 rodadas de investimento\n"
            "sem zerar o saldo. Você pode apertar a barra de ESPAÇO do teclado a qualquer\n"
            "momento para realizar o 'Cash Out' (resgatar).\n\n"
            "Atenção aos Termos de Uso (que ninguém lê): taxas e retenções automáticas\n"
            "são aplicadas pela infraestrutura do sistema em todas as operações."
        )

        lbl_desc = tk.Label(self.root, text=texto_sobre, font=("Arial", 13), fg="#cdd6f4", bg="#1e1e2e", justify="left")
        lbl_desc.pack(padx=80, pady=20)

        tk.Button(self.root, text="Voltar ao Menu", font=("Arial", 12, "bold"), bg="#bac2de", fg="#11111b", width=20, command=self.mostrar_menu).pack(pady=30)

    def preparar_jogo(self):
        nome = simpledialog.askstring("Cadastro de Equipe", "Digite o nome da sua equipe de informática:")
        if not nome:
            return
        
        termo_gigante = (
            f"TERMOS DE USO E CONDIÇÕES GERAIS DE PRESTAÇÃO DE SERVIÇOS E LICENCIAMENTO DE SOFTWARE DA PLATAFORMA BET-EDUCATIVA S/A\n"
            f"Atualização: Versão 4.8.12 - Outubro de 2026.\n\n"
            f"Por favor, leia atentamente este instrumento jurídico antes de prosseguir com o acesso e utilização do ambiente virtual pela equipe '{nome}'. "
            f"O presente Contrato de Licença de Usuário Final ('CLUF') regula os direitos e obrigações entre a Plataforma e os Participantes.\n\n"
            f"CLÁUSULA 1ª - DA NATUREZA DOS SERVIÇOS: A Plataforma fornece exclusivamente a infraestrutura lógica, o motor de processamento assíncrono, "
            f"os serviços de rede, a interface gráfica de usuário (UI/UX), os protocolos de segurança criptográfica, o gerenciamento de sessões simultâneas "
            f"e a manutenção do banco de dados relacional que sustenta este simulador computacional de alta performance.\n\n"
            f"CLÁUSULA 2ª - DA PROPRIEDADE INTELECTUAL E MARCAS: Todos os algoritmos, fontes tipográficas, esquemas de cores em gradiente, assets gráficos "
            f"estáticos ou dinâmicos, scripts em linguagem Python, rotinas de tratamento de exceções, classes, objetos, instâncias e funções aqui contidas são "
            f"de propriedade exclusiva e intransferível dos desenvolvedores do sistema, sendo terminantemente proibida a engenharia reversa não autorizada.\n\n"
            f"CLÁUSULA 3ª - DA POLÍTICA DE PRIVACIDADE E DADOS: Os metadados gerados durante as interações da equipe, incluindo latência de resposta, histórico "
            f"de cliques na barra de espaço, contagem de rodadas efetuadas, saldo virtual flutuante e variações de capital, poderão ser coletados e processados "
            f"para fins estatísticos, pedagógicos e analíticos internos, sem direito a remuneração ou royalties aos titulares.\n\n"
            f"CLÁUSULA 4ª - DA LIMITAÇÃO DE RESPONSABILIDADE E RISCOS: O usuário reconhece expressamente que o ambiente operacional é volátil. A Plataforma "
            f"não se responsabiliza por quedas repentinas de conexão, instabilidades no motor de cálculo de probabilidades, falhas humanas de sincronismo no "
            f"acionamento de gatilhos de resgate, nem por flutuações de mercado simuladas que venham a causar o esgotamento total ou parcial do capital alocado.\n\n"
            f"CLÁUSULA 5ª - DAS DISPOSIÇÕES FINAIS E SUPORTES TÉCNICOS: Ao clicar em 'Sim' ou 'Aceitar' abaixo, o representante da equipe declara, sob as penas "
            f"da lei e das normas institucionais vigentes, que leu, compreendeu e concordou integralmente com cada uma das cláusulas, sub-cláusulas, parágrafos "
            f"e alíneas supramencionadas, assumindo total responsabilidade civil e técnica sobre o desempenho financeiro e estratégico de sua unidade.\n\n"
            f"IMPORTANTE (A FACADA FINAL): Fica estabelecido pelo presente termo irrevogável que, devido aos custos operacionais de manutenção dos servidores "
            f"e à taxa de licenciamento de infraestrutura, 35% (trinta e cinco por cento) de TODO E QUALQUER valor bruto resgatado com sucesso em qualquer "
            f"rodada será retido integralmente pela Plataforma (A Casa), sendo repassado à equipe apenas o saldo remanescente após o expurgo da referida comissão.\n\n"
            f"Você concorda com todos os termos descritos acima para iniciar a partida?"
        )

        resposta_termo = messagebox.askyesno("Contrato de Licença de Usuário Final (CLUF) - Termos e Condições", termo_gigante)

        if not resposta_termo:
            messagebox.showinfo("Aviso", "Você recusou os termos e não poderá acessar o ambiente de simulação.")
            return

        self.nome_equipe = nome
        self.saldo = 100.0
        self.aposta_atual = 10.0
        self.rodada_atual = 0
        self.total_apostado_equipe = 0.0
        self.total_retirado_equipe = 0.0
        self.lucro_acumulado_casa = 0.0
        self.divida_acumulada = 0.0
        
        self.iniciar_tela_jogo()

    def iniciar_tela_jogo(self):
        self.limpar_tela()
        self.root.config(bg="#1e1e2e")

        top_frame = tk.Frame(self.root, bg="#1e1e2e")
        top_frame.pack(fill="x", padx=60, pady=20)

        self.lbl_equipe_info = tk.Label(top_frame, text=f"Equipe: {self.nome_equipe}", font=("Arial", 16, "bold"), fg="#f9e2af", bg="#1e1e2e")
        self.lbl_equipe_info.pack(side="left")

        self.lbl_saldo = tk.Label(top_frame, text=f"Saldo: R$ {self.saldo:.2f}", font=("Arial", 16, "bold"), fg="#a6e3a1", bg="#1e1e2e")
        self.lbl_saldo.pack(side="right")

        self.lbl_rodadas = tk.Label(self.root, text=f"Rodada: {self.rodada_atual} / {self.total_rodadas_meta} obrigatórias", font=("Arial", 14, "bold"), fg="#fab387", bg="#1e1e2e")
        self.lbl_rodadas.pack(pady=5)

        self.frame_tela = tk.Frame(self.root, bg="#11111b", bd=5, relief="solid")
        self.frame_tela.pack(pady=20, fill="x", padx=100, ipady=50)

        self.lbl_multiplicador = tk.Label(self.frame_tela, text="1.00x", font=("Arial", 60, "bold"), fg="#cdd6f4", bg="#11111b")
        self.lbl_multiplicador.pack(expand=True)

        self.lbl_aposta_info = tk.Label(self.root, text=f"Aposta Atual: R$ {self.aposta_atual:.2f}", font=("Arial", 14), fg="#89b4fa", bg="#1e1e2e")
        self.lbl_aposta_info.pack(pady=5)

        self.lbl_status = tk.Label(self.root, text="Pressione 'Iniciar Rodada' ou aperte ESPAÇO para sacar durante o jogo!", font=("Arial", 13), fg="#bac2de", bg="#1e1e2e")
        self.lbl_status.pack(pady=5)

        botoes_frame = tk.Frame(self.root, bg="#1e1e2e")
        botoes_frame.pack(pady=15)

        self.btn_iniciar = tk.Button(botoes_frame, text="Iniciar Rodada", font=("Arial", 14, "bold"), bg="#a6e3a1", fg="#11111b", width=20, pady=8, command=self.iniciar_rodada)
        self.btn_iniciar.grid(row=0, column=0, padx=15)

        self.btn_cashout = tk.Button(botoes_frame, text="CASH OUT [BARRA DE ESPAÇO]", font=("Arial", 14, "bold"), bg="#fab387", fg="#11111b", width=28, pady=8, state="disabled", command=self.fazer_cashout)
        self.btn_cashout.grid(row=0, column=1, padx=15)

        controle_aposta_frame = tk.Frame(self.root, bg="#1e1e2e")
        controle_aposta_frame.pack(pady=5)

        self.btn_diminuir = tk.Button(controle_aposta_frame, text="-R$ 10 Aposta", font=("Arial", 12), bg="#fab387", fg="#11111b", width=18, pady=5, command=self.diminuir_aposta)
        self.btn_diminuir.pack(side="left", padx=10)

        self.btn_aumentar = tk.Button(controle_aposta_frame, text="+R$ 10 Aposta", font=("Arial", 12), bg="#f38ba8", fg="#11111b", width=18, pady=5, command=self.aumentar_aposta)
        self.btn_aumentar.pack(side="left", padx=10)

        dash_frame = tk.Frame(self.root, bg="#1e1e2e")
        dash_frame.pack(pady=10)

        tk.Button(dash_frame, text="📊 Ver Painel da Casa (Sabor Vencedor)", font=("Arial", 12, "bold"), bg="#cba6f7", fg="#11111b", padx=15, pady=6, command=self.mostrar_painel_casa).pack(side="left", padx=10)
        tk.Button(dash_frame, text="Menu Principal", font=("Arial", 12), bg="#bac2de", fg="#11111b", padx=15, pady=6, command=self.salvar_e_voltar_menu).pack(side="left", padx=10)

    def iniciar_rodada(self):
        if self.saldo <= 0:
            self.oferecer_emprestimo_ou_falencia()
            return

        self.rodada_atual += 1
        self.rodando = True
        self.multiplicador = 1.0
        self.total_apostado_equipe += self.aposta_atual
        self.lucro_acumulado_casa += self.aposta_atual  
        self.saldo -= self.aposta_atual

        self.btn_iniciar.config(state="disabled")
        self.btn_diminuir.config(state="disabled")
        self.btn_aumentar.config(state="disabled")
        self.btn_cashout.config(state="normal")

        sorte = random.random()
        if sorte < 0.15:
            self.limite_crash = 1.00
        elif sorte < 0.65:
            self.limite_crash = round(random.uniform(1.01, 1.25), 2)
        elif sorte < 0.90:
            self.limite_crash = round(random.uniform(1.26, 2.50), 2)
        else:
            self.limite_crash = round(random.uniform(2.51, 5.00), 2)

        self.lbl_status.config(text="Subindo! Aperte ESPAÇO no teclado para dar o Cash Out!", fg="#f9e2af")
        self.atualizar_loop_cronometro_lento()

    def atualizar_loop_cronometro_lento(self):
        if not self.rodando:
            return

        self.alternador_piscar = not self.alternador_piscar
        if self.alternador_piscar:
            self.root.config(bg="#2a1b3d")
            self.frame_tela.config(bg="#1a0f24")
        else:
            self.root.config(bg="#1e1e2e")
            self.frame_tela.config(bg="#11111b")

        self.multiplicador += 0.02
        self.lbl_multiplicador.config(text=f"{self.multiplicador:.2f}x")

        if self.multiplicador >= self.limite_crash:
            self.rodando = False
            self.root.config(bg="#3a1111")
            self.frame_tela.config(bg="#220a0a")

            self.lbl_multiplicador.config(text="CRASH! QUEBROU!", fg="#f38ba8")
            self.lbl_status.config(text=f"Queda brusca! Perda total da aposta para a banca.", fg="#f38ba8")
            self.atualizar_interface_jogo()
            
            if self.saldo <= 0:
                self.oferecer_emprestimo_ou_falencia()
            elif self.rodada_atual >= self.total_rodadas_meta:
                messagebox.showinfo("Meta Concluída", f"Parabéns! Vocês completaram as {self.total_rodadas_meta} rodadas mínimas obrigatórias.")
                self.mostrar_painel_casa()
            return

        self.root.after(150, self.atualizar_loop_cronometro_lento)

    def fazer_cashout(self):
        if not self.rodando:
            return

        self.rodando = False
        self.root.config(bg="#113311")
        self.frame_tela.config(bg="#081a08")

        ganho_bruto = self.aposta_atual * self.multiplicador
        lucro_bruto = ganho_bruto - self.aposta_atual
        
        comissao_casa = lucro_bruto * 0.35
        lucro_liquido_equipe = lucro_bruto - comissao_casa
        
        retorno_efetivo = self.aposta_atual + lucro_liquido_equipe
        
        self.saldo += retorno_efetivo
        self.total_retirado_equipe += retorno_efetivo
        
        self.lucro_acumulado_casa -= lucro_liquido_equipe

        self.lbl_multiplicador.config(text=f"RESGATADO! {self.multiplicador:.2f}x", fg="#a6e3a1")
        self.lbl_status.config(text=f"Sucesso! Taxa da Bet retida (35%): R$ {comissao_casa:.2f}", fg="#a6e3a1")
        self.atualizar_interface_jogo()

        if self.rodada_atual >= self.total_rodadas_meta:
            messagebox.showinfo("Meta Concluída", f"Parabéns! Vocês completaram as {self.total_rodadas_meta} rodadas mínimas obrigatórias.")
            self.mostrar_painel_casa()

    def oferecer_emprestimo_ou_falencia(self):
        aviso_endividamento = (
            "ATENÇÃO CRÍTICA: Seu saldo zerou e você acumulou dívidas!\n\n"
            "A plataforma oferece um 'Crédito Facilitado / Financiamento Instantâneo' de R$ 50,00 "
            "com juros compostos de 20% por rodada para você tentar recuperar o prejuízo e continuar jogando.\n\n"
            "Deseja aceitar o empréstimo para continuar jogando mesmo endividado?\n"
            "(Escolher 'Não' encerrará o ciclo e executará as garantias e bens)."
        )
        
        aceitou_emprestimo = messagebox.askyesno("CRÉDITO FACILITADO DA CASA (EMPRÉSTIMO)", aviso_endividamento)
        
        if aceitou_emprestimo:
            self.saldo += 50.0
            self.divida_acumulada += 60.0  
            messagebox.showinfo("Crédito Concedido", "Empréstimo aprovado instantaneamente! Sua dívida cresceu, mas você pode voltar a apostar.")
            self.atualizar_interface_jogo()
        else:
            self.divida_acumulada += 100.0
            aviso_falencia = (
                f"EXECUÇÃO DE DÍVIDA E GARANTIA\n\n"
                f"Sua equipe recusou o refinanciamento e acumulou um débito pendente de R$ {self.divida_acumulada:.2f} com a plataforma.\n\n"
                "Conforme nossos Termos de Uso, para evitar o protesto imediato do CPF dos responsáveis, "
                "a transferência judicial da escritura do imóvel residencial da família ou o bloqueio de "
                "bens em nome dos pais, os bens foram dados como garantia até a quitação total."
            )
            messagebox.showerror("FALÊNCIA E EXECUÇÃO DE BENS", aviso_falencia)
            self.mostrar_painel_casa()

    def aumentar_aposta(self):
        self.aposta_atual += 10.0
        if self.aposta_atual > self.saldo:
            self.aposta_atual = self.saldo if self.saldo > 0 else 0.0
        self.lbl_aposta_info.config(text=f"Aposta Atual: R$ {self.aposta_atual:.2f}")

    def diminuir_aposta(self):
        self.aposta_atual -= 10.0
        if self.aposta_atual < 10.0:
            self.aposta_atual = 10.0 if self.saldo >= 10.0 else self.saldo
        self.lbl_aposta_info.config(text=f"Aposta Atual: R$ {self.aposta_atual:.2f}")

    def atualizar_interface_jogo(self):
        self.lbl_saldo.config(text=f"Saldo: R$ {self.saldo:.2f}")
        self.lbl_rodadas.config(text=f"Rodada: {self.rodada_atual} / {self.total_rodadas_meta} obrigatórias")
        self.lbl_aposta_info.config(text=f"Aposta Atual: R$ {self.aposta_atual:.2f}")
        self.btn_iniciar.config(state="normal")
        self.btn_diminuir.config(state="normal")
        self.btn_aumentar.config(state="normal")
        self.btn_cashout.config(state="disabled")

    def mostrar_painel_casa(self):
        self.limpar_tela()
        self.root.config(bg="#1e1e2e")

        tk.Label(self.root, text="PAINEL ANALÍTICO: O SABOR VENCEDOR (CASA)", font=("Arial", 20, "bold"), fg="#cba6f7", bg="#1e1e2e").pack(pady=20)
        tk.Label(self.root, text=f"Relatório da Equipe: {self.nome_equipe} (Rodadas jogadas: {self.rodada_atual}/{self.total_rodadas_meta})", font=("Arial", 14), fg="#89b4fa", bg="#1e1e2e").pack(pady=5)

        frame_metricas = tk.Frame(self.root, bg="#11111b", bd=3, relief="solid")
        frame_metricas.pack(pady=10, fill="x", padx=100, ipady=10)

        patrimonio_atual = self.saldo
        balanco_equipe = patrimonio_atual - 100.0

        tk.Label(frame_metricas, text=f"Patrimônio Atual da Equipe: R$ {patrimonio_atual:.2f}", font=("Arial", 13), fg="#a6e3a1", bg="#11111b").pack(pady=5)
        tk.Label(frame_metricas, text=f"Total Movimentado (Apostado): R$ {self.total_apostado_equipe:.2f}", font=("Arial", 13), fg="#cdd6f4", bg="#11111b").pack(pady=5)
        tk.Label(frame_metricas, text=f"Balanço Líquido da Equipe: R$ {balanco_equipe:+.2f}", font=("Arial", 13, "bold"), fg="#f9e2af" if balanco_equipe >= 0 else "#f38ba8", bg="#11111b").pack(pady=5)
        
        tk.Label(frame_metricas, text=f"DÍVIDA OBTIDA / PENDENTE COM A PLATAFORMA: R$ {self.divida_acumulada:.2f}", font=("Arial", 13, "bold"), fg="#fab387", bg="#11111b").pack(pady=5)

        tk.Label(frame_metricas, text="-------------------------------------------------------------------", fg="#6c7086", bg="#11111b").pack(pady=5)
        
        lucro_exato_casa = max(0.0, self.lucro_acumulado_casa)
        tk.Label(frame_metricas, text=f"LUCRO LÍQUIDO DA BANCA (A Bet com 35% de comissão): R$ {lucro_exato_casa:.2f}", font=("Arial", 15, "bold"), fg="#f38ba8", bg="#11111b").pack(pady=8)

        tk.Button(self.root, text="Salvar no Placar e Voltar ao Menu", font=("Arial", 12, "bold"), bg="#89b4fa", fg="#11111b", width=30, pady=8, command=self.salvar_e_voltar_menu).pack(pady=15)

    def salvar_e_voltar_menu(self):
        # Salva o saldo, a dívida e o patrimônio líquido (saldo - dívida) para a ordenação correta
        patrimonio_liquido = self.saldo - self.divida_acumulada
        
        # Se a equipe já existir no placar, substitui o registro; se for nova, adiciona
        equipe_existente = False
        for item in self.ranking_turma:
            if item["equipe"] == self.nome_equipe:
                item["saldo"] = self.saldo
                item["divida"] = self.divida_acumulada
                item["patrimonio_liquido"] = patrimonio_liquido
                equipe_existente = True
                break
                
        if not equipe_existente:
            self.ranking_turma.append({
                "equipe": self.nome_equipe, 
                "saldo": self.saldo,
                "divida": self.divida_acumulada,
                "patrimonio_liquido": patrimonio_liquido
            })
            
        self.mostrar_menu()

    def mostrar_placar(self):
        self.limpar_tela()
        self.root.config(bg="#1e1e2e")

        tk.Label(self.root, text="RANKING DAS EQUIPES (ORDENADO POR PATRIMÔNIO LÍQUIDO)", font=("Arial", 20, "bold"), fg="#f9e2af", bg="#1e1e2e").pack(pady=20)

        frame_ranking = tk.Frame(self.root, bg="#11111b", bd=3, relief="solid")
        frame_ranking.pack(pady=15, fill="both", expand=True, padx=80)

        # ORDENAÇÃO: Maior Patrimônio Líquido (Saldo - Dívida) fica no topo
        ranking_ordenado = sorted(self.ranking_turma, key=lambda x: x["patrimonio_liquido"], reverse=True)

        if not ranking_ordenado:
            tk.Label(frame_ranking, text="Nenhuma equipe registrada ainda.", font=("Arial", 13), fg="#6c7086", bg="#11111b").pack(pady=30)
        else:
            for idx, item in enumerate(ranking_ordenado, start=1):
                pl = item["patrimonio_liquido"]
                saldo = item["saldo"]
                divida = item["divida"]
                
                texto = f"{idx}º Lugar — {item['equipe']}: Patrimônio Líquido: R$ {pl:+.2f}  (Saldo: R$ {saldo:.2f} | Dívida: R$ {divida:.2f})"
                
                if pl > 0:
                    cor = "#a6e3a1"
                elif pl == 0:
                    cor = "#cdd6f4"
                else:
                    cor = "#f38ba8"

                tk.Label(frame_ranking, text=texto, font=("Arial", 12, "bold"), fg=cor, bg="#11111b").pack(anchor="w", padx=30, pady=8)

        tk.Button(self.root, text="Voltar ao Menu", font=("Arial", 12, "bold"), bg="#bac2de", fg="#11111b", width=25, pady=10, command=self.mostrar_menu).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoBetEducativo(root)
    root.mainloop()