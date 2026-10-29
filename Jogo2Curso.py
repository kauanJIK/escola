import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class SimuladorBetEnterpriseEquilibrado:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Educativo Enterprise: Gestão Segmentada de Bets")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.sair_tela_cheia)

        # Orçamento inicial equilibrado
        self.verba_total = 8500.0
        self.verba_disponivel = 8500.0

        # Identificação
        self.nome_equipe = "Equipe Padrão"

        # Configurações Expandidas (Montagem da Bet)
        self.tipo_operacao = ""
        self.num_socios = 1
        self.custo_socios = 0.0
        self.tipo_equipe_contratada = ""
        self.custo_equipe = 0.0
        self.tipo_marketing = ""
        self.custo_marketing = 0.0
        self.modelo_fachada = ""
        self.custo_fachada = 0.0
        self.tipo_servidor = ""
        self.custo_servidor = 0.0
        self.gateway_pagamento = ""
        self.custo_gateway = 0.0
        self.provedor_odds = ""
        self.custo_provedor = 0.0
        self.nivel_kyc = ""
        self.custo_kyc = 0.0
        self.politica_bonus = ""
        self.custo_bonus = 0.0
        self.tipo_licenca = ""
        self.custo_licenca = 0.0
        self.reserva_tecnica = 0.0
        
        self.bonus_sorte_usado_no_ciclo = False
        self.projeto_montado = False

        # Variáveis de Simulação Mês a Mês (1 a 12 rigorosos)
        self.mes_atual = 1
        self.lucro_acumulado_banca = 0.0
        self.prejuizo_acumulado_jogadores = 0.0
        self.reputacao_empresa = 50
        self.status_operacional = "Não Iniciado"
        self.log_eventos = []
        self.perspectiva_donos = []
        self.perspectiva_jogadores = []

        # Nomes realistas para a narrativa detalhada
        self.nomes_donos = ["Kauan", "Enzo", "Brian", "João"]
        self.nomes_usuarios = ["Yasmin", "Davi", "Mariana", "Lucas", "Beatriz", "Gabriel"]

        self.projetos_turma = []

        self.glossario = {
            "Tipo de Operação": "Define o nicho principal da casa: Foco em Jogos de Cassino/Crash, Esportes ou Híbrido.",
            "Sócios Fundadores": "Número de pessoas dividindo o capital inicial e a responsabilidade jurídica.",
            "Equipe de Desenvolvimento": "Profissionais contratados para escalar o tráfego e manter o sistema ativo.",
            "Campanhas de Marketing": "Escolha entre atrair público com influenciadores agressivos ou investir em jogo responsável.",
            "Fachada Legal e Domínio": "Escolha do visual e da extensão de domínio (.com internacional ou .bet oficial).",
            "Política de Bônus Inicial": "Oferecer bônus de boas-vindas sem depósito para atrair massa ou exigir rollover.",
            "Cloud Elástica (AWS/GCP)": "Servidor em nuvem de alta performance (R$ 1.500,00). Suporta picos de acesso sem cair.",
            "Servidor Físico Local": "Computador básico mais barato (R$ 400,00), propenso a quedas em grandes jogos.",
            "Gateway Pix Regulado": "Instituição de pagamento oficial homologada pelo Banco Central (R$ 1.200,00).",
            "Processador Clandestino": "Canal de pagamento paralelo sem regulação (R$ 300,00), com risco de bloqueio.",
            "API de Odds (Sportradar)": "Dados globais de estatísticas em tempo real (R$ 1.500,00).",
            "Motor Próprio de Odds": "Sistema estatístico caseiro (R$ 0,00), sujeito a erros e explorações.",
            "KYC (Know Your Customer)": "Verificação rigorosa de identidade por biometria e documentos (R$ 1.000,00).",
            "Cadastro Instantâneo": "Sem checagem profunda de identidade (R$ 200,00).",
            "Licença Oficial (SPA/MF)": "Autorização do Ministério da Fazenda (R$ 2.000,00). Total segurança jurídica.",
            "Offshore / Pirata": "Empresa em paraíso fiscal sem licença no Brasil (R$ 0,00), alvo da Anatel.",
            "Reserva de Liquidez": "Caixa separado obrigatoriamente para pagar prêmios (R$ 1.500,00)."
        }

        self.banco_investigacao = {
            "Blaze": {
                "foco": "Crash Games e Cassino Online",
                "licenca": "Operação Offshore (Curaçao) e controvérsias regulatórias.",
                "divulgacao": "Uso ostensivo de influenciadores digitais.",
                "risco": "🔴 ALTO: Histórico de bloqueios e queixas de saques retidos."
            },
            "Betano": {
                "foco": "Apostas Esportivas e Cassino Live",
                "licenca": "Licenciada oficial da Secretaria de Prêmios e Apostas (SPA).",
                "divulgacao": "Patrocínio máster de campeonatos e times da Série A.",
                "risco": "🟡 MODERADO/REGULADO: Compliance ativo, foco em odds."
            }
        }

        self.mostrar_menu_principal()

    def sair_tela_cheia(self, event=None):
        self.root.attributes("-fullscreen", False)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_cabecalho_verba(self, titulo_passo):
        header_frame = tk.Frame(self.root, bg="#0f172a")
        header_frame.pack(fill="x", padx=30, pady=15)

        tk.Label(header_frame, text=f"Equipe: {self.nome_equipe} | {titulo_passo}", font=("Arial", 18, "bold"), fg="#38bdf8", bg="#0f172a", wraplength=950, justify="left").pack(side="left")

        cor_verba = "#4ade80" if self.verba_disponivel >= 0 else "#f87171"
        lbl_verba = tk.Label(header_frame, text=f"💰 Verba: R$ {self.verba_disponivel:.2f} | ⭐ Reputação: {self.reputacao_empresa}%", font=("Arial", 14, "bold"), fg=cor_verba, bg="#1e293b", padx=15, pady=8, relief="solid", bd=2)
        lbl_verba.pack(side="right")

    def mostrar_ajuda(self, termo):
        explicacao = self.glossario.get(termo, "Termo técnico corporativo.")
        messagebox.showinfo(f"Ajuda / Glossário: {termo}", explicacao)

    def checar_saldo_e_avancar(self, proxima_funcao):
        if self.verba_disponivel <= 0:
            messagebox.showwarning("Orçamento Esgotado!", "Sua verba chegou a zero! O simulador vai iniciar a operação da Bet imediatamente com a infraestrutura construída até aqui.")
            self.projeto_montado = True
            self.iniciar_simulacao_meses()
        else:
            proxima_funcao()

    def mostrar_menu_principal(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")

        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=15)

        tk.Label(container, text="LABORATÓRIO ENTERPRISE: GESTÃO SEGMENTADA DE BETS", font=("Arial", 24, "bold"), fg="#38bdf8", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        info_equipe = f"Equipe Ativa: {self.nome_equipe} | Caixa: R$ {self.verba_disponivel:.2f} | Status: {self.status_operacional}"
        tk.Label(container, text=info_equipe, font=("Arial", 16, "bold"), fg="#4ade80" if self.status_operacional != "Falido" else "#f87171", bg="#0f172a", wraplength=1200).pack(pady=8)

        btn_frame = tk.Frame(container, bg="#0f172a")
        btn_frame.pack(expand=True, fill="both", pady=5)

        tk.Button(btn_frame, text="👥 0. CADASTRAR NOME DA EQUIPE", font=("Arial", 14, "bold"), bg="#f43f5e", fg="#ffffff", pady=10, command=self.cadastrar_equipe).pack(fill="x", padx=100, pady=5)
        tk.Button(btn_frame, text="🛠️ 1. MONTAR ESTRUTURA DA BET (PASSOS DE CONFIGURAÇÃO)", font=("Arial", 14, "bold"), bg="#38bdf8", fg="#0f172a", pady=10, command=self.passo_0_nicho).pack(fill="x", padx=100, pady=5)
        tk.Button(btn_frame, text="📊 2. SALVAR PROJETO PARA A TURMA", font=("Arial", 14, "bold"), bg="#818cf8", fg="#0f172a", pady=10, command=self.salvar_projeto_turma).pack(fill="x", padx=100, pady=5)
        tk.Button(btn_frame, text="🔍 3. PAINEL DE AUDITORIA PEDAGÓGICA", font=("Arial", 14, "bold"), bg="#fbbf24", fg="#0f172a", pady=10, command=self.tela_auditoria_coletiva).pack(fill="x", padx=100, pady=5)
        tk.Button(btn_frame, text="🌐 4. RADAR DE INVESTIGAÇÃO DE BETS REAIS", font=("Arial", 14, "bold"), bg="#38def8", fg="#0f172a", pady=10, command=self.tela_investigar_bets).pack(fill="x", padx=100, pady=5)
        tk.Button(btn_frame, text="🔄 5. REINICIAR PROJETO", font=("Arial", 14), bg="#64748b", fg="#ffffff", pady=8, command=self.reiniciar_projeto).pack(fill="x", padx=100, pady=5)
        tk.Button(btn_frame, text="❌ SAIR (Aperte ESC)", font=("Arial", 13), bg="#f87171", fg="#0f172a", pady=8, command=self.root.quit).pack(fill="x", padx=100, pady=5)

    def cadastrar_equipe(self):
        nome = simpledialog.askstring("Identificação", "Digite o nome da sua equipe:")
        if nome:
            self.nome_equipe = nome
            messagebox.showinfo("Sucesso", f"Equipe '{self.nome_equipe}' registrada!")
            self.mostrar_menu_principal()

    def salvar_projeto_turma(self):
        if not self.projeto_montado:
            messagebox.showwarning("Atenção", "Você precisa concluir a montagem e a simulação até o mês 12 antes de salvar!")
            return

        custo_total_infra = self.custo_socios + self.custo_equipe + self.custo_marketing + self.custo_fachada + self.custo_servidor + self.custo_gateway + self.custo_provedor + self.custo_kyc + self.custo_bonus + self.custo_licenca
        
        projeto = {
            "equipe": self.nome_equipe,
            "nicho": self.tipo_operacao,
            "socios": self.num_socios,
            "equipe_trab": self.tipo_equipe_contratada,
            "marketing": self.tipo_marketing,
            "fachada": self.modelo_fachada,
            "servidor": self.tipo_servidor,
            "gateway": self.gateway_pagamento,
            "kyc": self.nivel_kyc,
            "bonus": self.politica_bonus,
            "licenca": self.tipo_licenca,
            "custo_total": custo_total_infra,
            "saldo_restante": self.verba_disponivel,
            "status": self.status_operacional,
            "reputacao": self.reputacao_empresa,
            "perspectiva_dono": self.perspectiva_donos,
            "perspectiva_usuario": self.perspectiva_jogadores
        }

        self.projetos_turma = [p for p in self.projetos_turma if p["equipe"] != self.nome_equipe]
        self.projetos_turma.append(projeto)
        messagebox.showinfo("Salvo", f"O projeto da equipe '{self.nome_equipe}' foi enviado para o Painel de Auditoria Pedagógica!")
        self.mostrar_menu_principal()

    def acionar_botao_bonus_sorte(self, proxima_funcao):
        if self.bonus_sorte_usado_no_ciclo:
            messagebox.showinfo("Bônus Já Utilizado", "Você já resgatou o bônus estratégico nesta sessão! Ele só pode ser usado uma única vez por ciclo.")
            proxima_funcao()
            return
        
        self.bonus_sorte_usado_no_ciclo = True
        evento_sorte = random.choice([
            ("🎲 Oportunidade de Mercado!", "Um investidor anjo apostou na sua ideia corporativa! Você ganhou +R$ 1.000,00 de verba bônus!", 1000.0, 10),
            ("⚠️ Alerta de Falha Técnica!", "Seus servidores sofreram instabilidade inesperada de tráfego. Você perdeu -R$ 600,00 e pontuação de reputação!", -600.0, -15),
            ("✨ Patrocínio Estratégico!", "Sua marca obteve destaque espontâneo em portais de notícias especializados. Você ganhou +R$ 800,00!", 800.0, 5)
        ])
        
        titulo, msg, valor_delta, rep_delta = evento_sorte
        self.verba_disponivel += valor_delta
        self.reputacao_empresa = max(0, min(100, self.reputacao_empresa + rep_delta))
        messagebox.showinfo(titulo, msg)
        proxima_funcao()

    def passo_0_nicho(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 0: ESCOLHA DO TIPO DE PLATAFORMA")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Escolha o nicho principal de entretenimento e apostas da sua casa:", font=("Arial", 20, "bold"), fg="#fbbf24", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1, 2, 3), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nicho):
            self.tipo_operacao = nicho
            self.checar_saldo_e_avancar(self.passo_1_socios)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Tipo de Operação")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🎰 Cassino & Crash\n(Slots, Tigrinho, Mines)\nAlta adicção rápida", font=("Arial", 13, "bold"), bg="#1e293b", fg="#f43f5e", wraplength=260, justify="left", command=lambda: escolher("Cassino Online")).pack(expand=True, fill="both", padx=8, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Tipo de Operação")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="⚽ Apostas Esportivas\n(Futebol, Basquete, E-Sports)\nFoco em paixão de torcedores", font=("Arial", 13, "bold"), bg="#1e293b", fg="#38bdf8", wraplength=260, justify="left", command=lambda: escolher("Apostas Esportivas")).pack(expand=True, fill="both", padx=8, pady=8)

        f3 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f3.grid(row=0, column=2, sticky="nsew", padx=8, pady=8)
        tk.Button(f3, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Tipo de Operação")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f3, text="🌐 Plataforma Híbrida\n(Cassino + Esportes juntos)\nUniverso completo de riscos", font=("Arial", 13, "bold"), bg="#1e293b", fg="#4ade80", wraplength=260, justify="left", command=lambda: escolher("Híbrida")).pack(expand=True, fill="both", padx=8, pady=8)

        f4 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f4.grid(row=0, column=3, sticky="nsew", padx=8, pady=8)
        tk.Button(f4, text="🎁", font=("Arial", 11, "bold"), bg="#a855f7", fg="#ffffff").pack(anchor="ne", padx=6, pady=6)
        
        texto_botao_bonus = "✨ BÔNUS ESTRATÉGICO\n(Já Resgatado)" if self.bonus_sorte_usado_no_ciclo else "✨ BÔNUS ESTRATÉGICO\n(Aporte Extraordinário)\nArrisque a Sorte Única"
        tk.Button(f4, text=texto_botao_bonus, font=("Arial", 13, "bold"), bg="#1e293b", fg="#c084fc", wraplength=260, justify="left", command=lambda: self.acionar_botao_bonus_sorte(self.passo_0_nicho)).pack(expand=True, fill="both", padx=8, pady=8)

        tk.Button(container, text="← Voltar ao Menu", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.mostrar_menu_principal).pack(fill="x", padx=100, pady=10)

    def passo_1_socios(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 1: NÚMERO DE SÓCIOS E SOCIEDADE")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Como o capital inicial será dividido entre os sócios?", font=("Arial", 20, "bold"), fg="#fbbf24", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1, 2), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(num, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Você não tem verba suficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente sem esta escolha!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.num_socios = num
            self.custo_socios = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_2_equipe)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Sócios Fundadores")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="👤 Apenas 1 Sócio (Autonomia Total)\nCusto: R$ 0,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=320, justify="left", command=lambda: escolher(1, 0.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Sócios Fundadores")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="👥 Grupo de 3 Sócios\nAporte Capital: R$ 500,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#fbbf24", wraplength=320, justify="left", command=lambda: escolher(3, 500.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f3 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f3.grid(row=0, column=2, sticky="nsew", padx=10, pady=8)
        tk.Button(f3, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Sócios Fundadores")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f3, text="🏢 5+ Sócios (Conselho Amplo)\nAporte Capital: R$ 1.000,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=320, justify="left", command=lambda: escolher(5, 1000.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_0_nicho).pack(fill="x", padx=100, pady=10)

    def passo_2_equipe(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 2: CONTRATAÇÃO DE SUPORTE E DESENVOLVIMENTO")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Quem vai codificar e manter o sistema ativo?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.tipo_equipe_contratada = nome
            self.custo_equipe = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_2_marketing)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Equipe de Desenvolvimento")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="💻 Autodidatas (Nós mesmos)\nCusto: R$ 0,00\n(Risco de bugs técnicos)", font=("Arial", 14, "bold"), bg="#1e293b", fg="#fbbf24", wraplength=400, justify="left", command=lambda: escolher("Autodidatas", 0.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Equipe de Desenvolvimento")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="📢 Agência Externa & Devs\nCusto: R$ 1.200,00\n(Estabilidade profissional)", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Agência Externa", 1200.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_1_socios).pack(fill="x", padx=100, pady=10)

    def passo_2_marketing(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 2.1: CAMPANHAS DE MARKETING E ÉTICA")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Qual será a estratégia de atração de novos apostadores?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.tipo_marketing = nome
            self.custo_marketing = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_2_fachada)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Campanhas de Marketing")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🔥 Influenciadores Agressivos\nPromessas milagrosas de ganho fácil\nCusto: R$ 800,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=400, justify="left", command=lambda: escolher("Influenciadores Agressivos", 800.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Campanhas de Marketing")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="🛡️ Jogo Responsável e Limites\nFoco em compliance e saúde financeira\nCusto: R$ 400,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Jogo Responsável", 400.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_2_equipe).pack(fill="x", padx=100, pady=10)

    def passo_2_fachada(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 2.2: FACHADA LEGAL E DOMÍNIO DA PLATAFORMA")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Qual será o design de fachada e terminação de domínio do site?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.modelo_fachada = nome
            self.custo_fachada = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_3_lucro)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Fachada Legal e Domínio")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🏴‍☠️ Domínio .com Pirata / Espelhado\nVisual chamativo com cores neon e caça-níqueis ocultos\nCusto: R$ 150,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=400, justify="left", command=lambda: escolher("Domínio Espelhado Neon", 150.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Fachada Legal e Domínio")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="🏛️ Domínio Oficial .bet.br\nVisual sobrio corporativo com selos de segurança do governo\nCusto: R$ 500,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Domínio Oficial .bet.br", 500.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_2_marketing).pack(fill="x", padx=100, pady=10)

    def passo_3_lucro(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 3: POLÍTICA DE DIVISÃO DE LUCROS")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Como o lucro gerado será tratado entre os fundadores?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def avancar():
            self.checar_saldo_e_avancar(self.passo_4_servidor)

        def retirar():
            custo = 300.0
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para taxa de dividendos (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.verba_disponivel -= custo
            avancar()

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Divisão de Lucros (Dividendos)")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🔄 Reinvestimento 100% na Casa\nFoco em expandir o negócio\nCusto: R$ 0,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=avancar).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Divisão de Lucros (Dividendos)")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="💰 Retirada de Dividendos\nRetirada mensal pelos sócios\nCusto: R$ 300,00 (Taxa)", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=400, justify="left", command=retirar).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_2_fachada).pack(fill="x", padx=100, pady=10)

    def passo_4_servidor(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 4: ARQUITETURA DE SERVIDORES")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Onde o sistema da Bet será hospedado?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para este servidor (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.tipo_servidor = nome
            self.custo_servidor = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_5_gateway)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Servidor Físico Local")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="💻 Servidor Local\nCusto: R$ 400,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#fbbf24", wraplength=400, justify="left", command=lambda: escolher("Servidor Local", 400.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Cloud Elástica (AWS/GCP)")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="☁️ Cloud Elástica\nCusto: R$ 1.500,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Cloud Elástica", 1500.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_3_lucro).pack(fill="x", padx=100, pady=10)

    def passo_5_gateway(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 5: GATEWAY DE PAGAMENTO (PIX)")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Como processar os pagamentos e saques instantâneos via Pix?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.gateway_pagamento = nome
            self.custo_gateway = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_6_provedor)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Processador Clandestino")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="💸 Processador Clandestino\nCusto: R$ 300,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=400, justify="left", command=lambda: escolher("Processador Clandestino", 300.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Gateway Pix Regulado")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="🏦 Gateway Regulado\nCusto: R$ 1.200,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Gateway Regulado", 1200.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_4_servidor).pack(fill="x", padx=100, pady=10)

    def passo_6_provedor(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 6: PROVEDOR DE ODDS E API")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="De onde virão as cotações estatísticas e motores de jogos?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.provedor_odds = nome
            self.custo_provedor = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_7_kyc)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Motor Próprio de Odds")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🛠️ Motor Próprio\nCusto: R$ 0,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#fbbf24", wraplength=400, justify="left", command=lambda: escolher("Motor Próprio", 0.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("API de Odds (Sportradar)")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="🌐 API Global (Sportradar)\nCusto: R$ 1.500,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("API Global", 1500.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_5_gateway).pack(fill="x", padx=100, pady=10)

    def passo_7_kyc(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 7: COMPLIANCE E KYC")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Qual será o nível de validação de identidade dos usuários?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.nivel_kyc = nome
            self.custo_kyc = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_7_bonus)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Cadastro Instantâneo")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="⚡ Cadastro Instantâneo\nCusto: R$ 200,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=400, justify="left", command=lambda: escolher("Instantâneo", 200.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("KYC (Know Your Customer)")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="🔍 KYC Rigoroso\nCusto: R$ 1.000,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Rigoroso", 1000.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_6_provedor).pack(fill="x", padx=100, pady=10)

    def passo_7_bonus(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 7.1: POLÍTICA DE BÔNUS DE CADASTRO")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Como serão distribuídos os bônus para novos apostadores?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.politica_bonus = nome
            self.custo_bonus = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_8_licenca)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Política de Bônus Inicial")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🎁 Bônus Grátis sem Depósito (R$ 50 no cadastro)\nAtrai massa jovem rapidamente, mas gera prejuízo inicial\nCusto: R$ 800,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=400, justify="left", command=lambda: escolher("Bônus Grátis Sem Depósito", 800.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Política de Bônus Inicial")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="💼 Apenas Cashback com Rollover Rigoroso\nO bônus só é liberado após apostar 10x o valor\nCusto: R$ 300,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Cashback com Rollover", 300.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_7_kyc).pack(fill="x", padx=100, pady=10)

    def passo_8_licenca(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 8: REGULAMENTAÇÃO JURÍDICA")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Qual será o modelo de licença de funcionamento da empresa?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(nome, custo):
            if self.verba_disponivel < custo:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para esta opção (Custo: R$ {custo:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.tipo_licenca = nome
            self.custo_licenca = custo
            self.verba_disponivel -= custo
            self.checar_saldo_e_avancar(self.passo_9_reserva)

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Offshore / Pirata")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🏴‍☠️ Offshore (Pirata)\nCusto: R$ 0,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f87171", wraplength=400, justify="left", command=lambda: escolher("Offshore", 0.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Licença Oficial (SPA/MF)")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="🏛️ Licença Oficial SPA\nCusto: R$ 2.000,00", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher("Licenciada SPA", 2000.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_7_bonus).pack(fill="x", padx=100, pady=10)

    def passo_9_reserva(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba("ETAPA 9: RESERVA DE LIQUIDEZ")
        
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="Qual será o capital de segurança separado para pagar prêmios?", font=("Arial", 20, "bold"), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=10)
        
        card_frame = tk.Frame(container, bg="#0f172a")
        card_frame.pack(expand=True, fill="both", pady=10)
        card_frame.columnconfigure((0, 1), weight=1)
        card_frame.rowconfigure(0, weight=1)

        def escolher(valor):
            if self.verba_disponivel < valor:
                messagebox.showerror("Saldo Insuficiente", f"Verba insuficiente para reserva de liquidez (Custo: R$ {valor:.2f}). A operação será iniciada imediatamente!")
                self.projeto_montado = True
                self.iniciar_simulacao_meses()
                return
            self.reserva_tecnica = valor
            self.verba_disponivel -= valor
            
            self.projeto_montado = True
            messagebox.showinfo("Sucesso", f"Estrutura concluída para o nicho [{self.tipo_operacao}]! Iniciando simulação.")
            self.iniciar_simulacao_meses()

        f1 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)
        tk.Button(f1, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Reserva de Liquidez")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f1, text="🛡️ Reserva Segura (R$ 1.500,00)", font=("Arial", 14, "bold"), bg="#1e293b", fg="#4ade80", wraplength=400, justify="left", command=lambda: escolher(1500.0)).pack(expand=True, fill="both", padx=10, pady=8)

        f2 = tk.Frame(card_frame, bg="#1e293b", bd=3, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        tk.Button(f2, text="?", font=("Arial", 11, "bold"), bg="#fbbf24", fg="#0f172a", command=lambda: self.mostrar_ajuda("Reserva de Liquidez")).pack(anchor="ne", padx=6, pady=6)
        tk.Button(f2, text="⚠️ Reserva Baixa (R$ 500,00)", font=("Arial", 14, "bold"), bg="#1e293b", fg="#fbbf24", wraplength=400, justify="left", command=lambda: escolher(500.0)).pack(expand=True, fill="both", padx=10, pady=8)

        tk.Button(container, text="← Voltar", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.passo_8_licenca).pack(fill="x", padx=100, pady=10)

    def iniciar_simulacao_meses(self):
        self.mes_atual = 1
        self.lucro_acumulado_banca = 0.0
        self.prejuizo_acumulado_jogadores = 0.0
        self.reputacao_empresa = 50
        self.status_operacional = "Ativo"
        self.log_eventos = []
        self.perspectiva_donos = []
        self.perspectiva_jogadores = []

        self.pool_cassino = [
            ("Bug Crítico no Sistema de Multiplicadores", "Estornar e cancelar todos os lucros gerados por falha técnica", "Honrar o pagamento do bug para blindar a credibilidade da marca", "Bloquear unilateralmente as contas dos usuários beneficiados"),
            ("Otimização de RTP e Margem da Casa", "Reduzir o RTP padrão para maximizar os dividendos corporativos", "Manter o RTP em conformidade com as diretrizes internacionais", "Elevar temporariamente o RTP para engajar campanhas de marketing"),
            ("Lançamento de Nova Categoria de Slots", "Implementar taxas extras ocultas para liberação de premiações", "Garantir liquidez imediata e simplificada para retenção de clientes", "Estabelecer limites operacionais de ganho diário por usuário"),
            ("Tráfego Automatizado por Bots de Apostas", "Banir em massa e reter fundos dos softwares automatizados", "Desenvolver ferramentas oficiais de controle interno", "Permitir a operação dos robôs ajustando o algoritmo da casa")
        ]

        self.pool_esportes = [
            ("Suspeita de Manipulação de Resultados", "Manter o mercado de apostas ativo e capitalizar sobre a volatilidade", "Suspender o evento imediatamente e estornar valores aos apostadores", "Notificar autoridades esportivas mantendo taxas operacionais"),
            ("Instabilidade na API de Cotações", "Anular todas as transações realizadas durante a janela de falha", "Assumir integralmente o prejuízo financeiro e honrar os bilhetes", "Negociar acordos parciais de liquidação com os clientes afetados"),
            ("Pico de Acesso em Final de Campeonato", "Elevar as margens de comissão corporativa sobre as apostas do dia", "Conceder bônus promocionais de depósito para expandir a base", "Estabelecer tetos máximos de apostas individuais por usuário"),
            ("Controvérsia em Decisão de Arbitragem", "Invalidar apostas vinculadas à equipe prejudicada", "Indenizar ambas as torcidas como estratégia de boa-fé institucional", "Reter os fundos sob custódia até parecer jurídico oficial")
        ]

        self.proximo_mes_simulacao()

    def proximo_mes_simulacao(self):
        if self.mes_atual > 12 or self.status_operacional != "Ativo":
            self.finalizar_simulacao()
            return

        if "Offshore" in self.tipo_licenca and self.mes_atual >= 4:
            if random.random() < 0.20:
                self.status_operacional = "Falido (Bloqueio Judicial/Anatel)"
                messagebox.showerror("Bloqueio da Anatel!", f"Mês {self.mes_atual}: O cerco regulatório fechou! A Bet opera sem licença oficial e órgãos competentes determinaram o bloqueio imediato do domínio.")
                self.finalizar_simulacao()
                return

        self.limpar_tela()
        self.root.config(bg="#0f172a")
        self.criar_cabecalho_verba(f"OPERAÇÃO MÊS {self.mes_atual} DE 12 [{self.tipo_operacao.upper()}]")

        lucro_mes = random.uniform(800.0, 1800.0)
        prejuizo_usuario_mes = lucro_mes * 2.5
        self.verba_disponivel += lucro_mes
        self.lucro_acumulado_banca += lucro_mes
        self.prejuizo_acumulado_jogadores += prejuizo_usuario_mes

        if self.mes_atual in [3, 6, 9]:
            self.mostrar_tela_reforma(lucro_mes)
        else:
            self.mostrar_dilema_dinamico(lucro_mes)

    def mostrar_dilema_dinamico(self, lucro_mes):
        dono_nome = self.nomes_donos[(self.mes_atual - 1) % len(self.nomes_donos)]
        user_nome = self.nomes_usuarios[(self.mes_atual - 1) % len(self.nomes_usuarios)]

        if self.tipo_operacao == "Cassino Online" and self.pool_cassino:
            tema, op1, op2, op3 = self.pool_cassino.pop(0)
        elif self.tipo_operacao == "Apostas Esportivas" and self.pool_esportes:
            tema, op1, op2, op3 = self.pool_esportes.pop(0)
        else:
            if self.pool_cassino and (self.mes_atual % 2 == 0):
                tema, op1, op2, op3 = self.pool_cassino.pop(0)
            elif self.pool_esportes:
                tema, op1, op2, op3 = self.pool_esportes.pop(0)
            else:
                tema, op1, op2, op3 = ("Oscilação de Mercado", "Aumentar taxas de saque", "Manter operações estáveis", "Oferecer rodadas grátis aos novatos")

        texto_evento = (
            f"AUDITORIA OPERACIONAL - MÊS {self.mes_atual} DE 12 [{tema.upper()}]:\n\n"
            f"Neste período, a infraestrutura da plataforma registrou ocorrências críticas relacionadas a {tema.lower()}. "
            f"A diretoria executiva precisa deliberar sobre diretrizes de conformidade, gerenciamento de risco de passivos financeiros e retenção de usuários ativos. "
            f"Decisões rigorosas protegem o caixa imediato, mas podem gerar repercussões na reputação pública da marca perante os órgãos reguladores e os apostadores."
        )

        opcoes = [
            (op1, 400, -15, f"Decisão rígida no evento {tema}.", 
             f"Mês {self.mes_atual} (Visão do Sócio {dono_nome}): 'Adotamos uma postura enérgica e implacável diante do incidente de {tema}. Nossa prioridade absoluta foi blindar o caixa da empresa contra perdas imprevistas, mesmo que isso gerasse reclamações públicas nos fóruns especializados.'",
             f"Mês {self.mes_atual} (Visão do Apostador {user_nome}): 'Fiquei extremamente frustrado com a atitude da plataforma durante o problema de {tema}. A impressão que fica é que a casa só pensa em lucrar e penaliza o usuário de forma injusta e unilateral.'"),
            
            (op2, -300, 15, f"Decisão amigável no evento {tema}.", 
             f"Mês {self.mes_atual} (Visão do Sócio {dono_nome}): 'Decidimos absorver o prejuízo financeiro e honrar os pagamentos no episódio de {tema}. Entendemos que a reputação e a lealdade da comunidade valem muito mais a longo prazo do que o lucro imediato.'",
             f"Mês {self.mes_atual} (Visão do Apostador {user_nome}): 'Surpreendeu positivamente a transparência da casa no ocorrido de {tema}. A diretoria resolveu tudo rapidamente, o que me deu muito mais confiança para continuar apostando e indicando a plataforma.'"),
            
            (op3, 150, -5, f"Decisão moderada no evento {tema}.", 
             f"Mês {self.mes_atual} (Visão do Sócio {dono_nome}): 'Optamos por um meio-termo equilibrado no caso de {tema}. Dividimos parte dos custos operacionais com a base de usuários para manter o fluxo de caixa saudável sem estagnar o crescimento.'",
             f"Mês {self.mes_atual} (Visão do Apostador {user_nome}): 'A solução adotada pela casa em {tema} foi aceitável, embora pudesse ser mais justa. Nem todos saíram ganhando, mas pelo menos o sistema continuou funcionando sem maiores interrupções.'")
        ]

        container_dilema = tk.Frame(self.root, bg="#0f172a")
        container_dilema.pack(expand=True, fill="both", padx=30, pady=10)

        frame_vida = tk.Frame(container_dilema, bg="#1e293b", bd=3, relief="solid")
        frame_vida.pack(expand=True, fill="both", padx=10, pady=8)

        tk.Label(frame_vida, text=f"📊 DECISÃO CORPORATIVA DO MÊS {self.mes_atual} DE 12 [{self.tipo_operacao.upper()}]", font=("Arial", 18, "bold"), fg="#fbbf24", bg="#1e293b", wraplength=1200).pack(anchor="w", padx=25, pady=10)
        tk.Label(frame_vida, text=texto_evento, font=("Arial", 13), fg="#f1f5f9", bg="#1e293b", justify="left", wraplength=1200).pack(anchor="w", padx=25, pady=8)

        btn_box = tk.Frame(frame_vida, bg="#1e293b")
        btn_box.pack(expand=True, fill="both", pady=10, padx=25)

        cores_botoes = ["#f87171", "#fbbf24", "#38bdf8"]
        for idx, (texto_acao, bonus, rep_delta, log_msg, persp_dono, persp_user) in enumerate(opcoes):
            acao_cmd = lambda b=bonus, r=rep_delta, l=log_msg, pd=persp_dono, pu=persp_user: [
                self.perspectiva_donos.append(pd), 
                self.perspectiva_jogadores.append(pu), 
                self.processar_escolha(b, r, l)
            ]
            tk.Button(btn_box, text=texto_acao, font=("Arial", 12, "bold"), bg=cores_botoes[idx], fg="#0f172a", pady=8, wraplength=1150, justify="left", command=acao_cmd).pack(fill="x", pady=6)

    def mostrar_tela_reforma(self, lucro_mes):
        container_ref = tk.Frame(self.root, bg="#0f172a")
        container_ref.pack(expand=True, fill="both", padx=30, pady=10)

        frame_ref = tk.Frame(container_ref, bg="#1e293b", bd=3, relief="solid")
        frame_ref.pack(expand=True, fill="both", padx=10, pady=8)

        dono_r = self.nomes_donos[(self.mes_atual - 1) % len(self.nomes_donos)]
        u_r = self.nomes_usuarios[(self.mes_atual - 1) % len(self.nomes_usuarios)]

        texto_trimestral = (
            f"AUDITORIA TRIMESTRAL DE INFRAESTRUTURA - MÊS {self.mes_atual} DE 12:\n\n"
            f"O balanço financeiro acumulado indica superávit operacional e a necessidade imperativa de novos aportes estruturais. "
            f"Para assegurar a conformidade regulatória contínua e a retenção qualificada da base de usuários, a diretoria deve escolher entre modernização visual, "
            f"reforço nos protocolos de cibersegurança ou retenção de capital em caixa. Cada escolha moldará o posicionamento institucional da empresa no mercado."
        )

        tk.Label(frame_ref, text=f"🔧 AUDITORIA TRIMESTRAL DE INFRAESTRUTURA (MÊS {self.mes_atual} DE 12)", font=("Arial", 18, "bold"), fg="#38bdf8", bg="#1e293b", wraplength=1200).pack(anchor="w", padx=25, pady=10)
        tk.Label(frame_ref, text=texto_trimestral, font=("Arial", 13), fg="#f1f5f9", bg="#1e293b", justify="left", wraplength=1200).pack(anchor="w", padx=25, pady=8)

        def acao_reforma(custo, rep_ganho, msg, pd, pu):
            self.verba_disponivel -= custo
            self.reputacao_empresa = min(100, self.reputacao_empresa + rep_ganho)
            self.log_eventos.append(f"Mês {self.mes_atual}: {msg}")
            self.perspectiva_donos.append(pd)
            self.perspectiva_jogadores.append(pu)
            self.mes_atual += 1
            container_ref.destroy()
            self.proximo_mes_simulacao()

        btn_box = tk.Frame(frame_ref, bg="#1e293b")
        btn_box.pack(expand=True, fill="both", pady=10, padx=25)

        btn_texto_1 = "🏗️ Reforma Visual Extrema [Custo: R$ 600,00]"
        btn_texto_2 = "🛡️ Auditoria de Segurança e Compliance [Custo: R$ 800,00]"
        btn_texto_3 = "🚫 Economizar e Não Fazer Nenhuma Reforma [Custo: R$ 0,00]"

        tk.Button(btn_box, text=btn_texto_1, font=("Arial", 12, "bold"), bg="#fbbf24", fg="#0f172a", pady=8, wraplength=1150, justify="left", command=lambda: acao_reforma(600, 10, "Fez reforma visual atraindo novos jogadores.", f"Mês {self.mes_atual} (Visão do Sócio {dono_r}): Investimos pesado em uma reestruturação estética da interface para prender a atenção dos novos cadastrados.", f"Mês {self.mes_atual} (Visão do Apostador {u_r}): A plataforma ficou visualmente incrível, muito moderna e com animações que tornam o jogo fluido.")).pack(fill="x", pady=6)
        tk.Button(btn_box, text=btn_texto_2, font=("Arial", 12, "bold"), bg="#4ade80", fg="#0f172a", pady=8, wraplength=1150, justify="left", command=lambda: acao_reforma(800, 20, "Investiu em segurança e melhorou a reputação.", f"Mês {self.mes_atual} (Visão do Sócio {dono_r}): Contratamos especialistas para blindar nosso sistema contra fraudes e auditorias externas.", f"Mês {self.mes_atual} (Visão do Apostador {u_r}): Senti uma segurança muito maior ao enviar meus documentos e realizar saques de valores altos.")).pack(fill="x", pady=6)
        tk.Button(btn_box, text=btn_texto_3, font=("Arial", 12, "bold"), bg="#f87171", fg="#0f172a", pady=8, wraplength=1150, justify="left", command=lambda: acao_reforma(0, -10, "Economizou, mas o sistema ficou defasado.", f"Mês {self.mes_atual} (Visão do Sócio {dono_r}): Guardamos cada centavo no cofre, mas percebemos que o sistema começou a apresentar lentidão.", f"Mês {self.mes_atual} (Visão do Apostador {u_r}): O site está difícil de navegar, vive instável e meu saque travou no meio do processo.")).pack(fill="x", pady=6)

    def processar_escolha(self, bonus_verba, variacao_rep, log_msg):
        self.verba_disponivel += bonus_verba
        self.reputacao_empresa = max(0, min(100, self.reputacao_empresa + variacao_rep))
        self.log_eventos.append(f"Mês {self.mes_atual}: {log_msg}")
        self.mes_atual += 1
        self.proximo_mes_simulacao()

    def finalizar_simulacao(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")
        
        header_frame = tk.Frame(self.root, bg="#0f172a")
        header_frame.pack(fill="x", padx=30, pady=8)
        tk.Label(header_frame, text=f"Equipe: {self.nome_equipe} | RELATÓRIO DOS 12 MESES DE OPERAÇÃO", font=("Arial", 15, "bold"), fg="#38bdf8", bg="#0f172a").pack(side="left")
        cor_verba = "#4ade80" if self.verba_disponivel >= 0 else "#f87171"
        tk.Label(header_frame, text=f"💰 Verba: R$ {self.verba_disponivel:.2f} | ⭐ Reputação: {self.reputacao_empresa}%", font=("Arial", 12, "bold"), fg=cor_verba, bg="#1e293b", padx=10, pady=5, relief="solid", bd=2).pack(side="right")

        container_res = tk.Frame(self.root, bg="#0f172a")
        container_res.pack(expand=True, fill="both", padx=30, pady=2)

        canvas = tk.Canvas(container_res, bg="#0f172a", highlightthickness=0)
        scrollbar = tk.Scrollbar(container_res, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f172a")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

        card_resumo = tk.Frame(scrollable_frame, bg="#1e293b", bd=3, relief="solid", padx=15, pady=12)
        card_resumo.pack(fill="x", padx=10, pady=8)

        resumo_texto = (
            f"🏆 FECHAMENTO ANUAL: {self.nome_equipe.upper()} [{self.tipo_operacao.upper()}]\n\n"
            f"• Status Operacional Final: {self.status_operacional}\n"
            f"• Lucro Bruto Acumulado da Banca: R$ {self.lucro_acumulado_banca:.2f}\n"
            f"• Prejuízo Financeiro Causado aos Apostadores: R$ {self.prejuizo_acumulado_jogadores:.2f}\n"
            f"• Índice Final de Reputação: {self.reputacao_empresa}%"
        )
        tk.Label(card_resumo, text=resumo_texto, font=("Arial", 12, "bold"), fg="#38bdf8", bg="#1e293b", justify="left").pack(anchor="w")

        tk.Label(scrollable_frame, text="👑 PERSPECTIVA DA EMPRESA (MÊS A MÊS)", font=("Arial", 15, "bold"), fg="#fbbf24", bg="#0f172a").pack(anchor="w", padx=10, pady=(12, 4))
        for item in (self.perspectiva_donos if self.perspectiva_donos else ["Sem registros."]):
            card_dono = tk.Frame(scrollable_frame, bg="#1e293b", bd=2, relief="solid", padx=12, pady=8)
            card_dono.pack(fill="x", padx=10, pady=4)
            tk.Label(card_dono, text=item, font=("Arial", 11), fg="#f1f5f9", bg="#1e293b", justify="left", wraplength=1100).pack(anchor="w")

        tk.Label(scrollable_frame, text="👥 PERSPECTIVA DOS USUÁRIOS (MÊS A MÊS)", font=("Arial", 15, "bold"), fg="#4ade80", bg="#0f172a").pack(anchor="w", padx=10, pady=(15, 4))
        for item in (self.perspectiva_jogadores if self.perspectiva_jogadores else ["Sem registros."]):
            card_user = tk.Frame(scrollable_frame, bg="#1e293b", bd=2, relief="solid", padx=12, pady=8)
            card_user.pack(fill="x", padx=10, pady=4)
            tk.Label(card_user, text=item, font=("Arial", 11), fg="#f1f5f9", bg="#1e293b", justify="left", wraplength=1100).pack(anchor="w")

        tk.Button(self.root, text="Salvar Projeto na Auditoria Pedagógica e Voltar ao Menu", font=("Arial", 13, "bold"), bg="#38bdf8", fg="#0f172a", pady=8, command=self.mostrar_menu_principal).pack(fill="x", padx=80, pady=8)

    def tela_auditoria_coletiva(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")

        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="PAINEL DE AUDITORIA PEDAGÓGICA DA TURMA", font=("Arial", 20, "bold"), fg="#fbbf24", bg="#0f172a", wraplength=1200).pack(pady=10)
        tk.Label(container, text="Selecione abaixo uma equipe salva para ver o histórico completo dos 12 meses e impacto:", font=("Arial", 14), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=6)

        frame_botoes = tk.Frame(container, bg="#0f172a")
        frame_botoes.pack(pady=8)

        self.frame_detalhes_turma = tk.Frame(container, bg="#1e293b", bd=3, relief="solid")
        self.frame_detalhes_turma.pack(expand=True, fill="both", padx=15, pady=10)

        self.lbl_detalhes_turma = tk.Label(self.frame_detalhes_turma, text="Nenhuma equipe selecionada para auditoria no momento.", font=("Arial", 14, "italic"), fg="#94a3b8", bg="#1e293b", justify="left", wraplength=1200)
        self.lbl_detalhes_turma.pack(padx=25, pady=15)

        if not self.projetos_turma:
            self.lbl_detalhes_turma.config(text="⚠️ Nenhum grupo concluiu e salvou o ciclo de 12 meses na auditoria ainda.")
        else:
            for proj in self.projetos_turma:
                eq = proj["equipe"]
                tk.Button(frame_botoes, text=eq, font=("Arial", 13, "bold"), bg="#1e293b", fg="#38bdf8", pady=8, command=lambda p=proj: self.exibir_auditoria_grupo(p)).pack(side="left", padx=8)

        tk.Button(container, text="← Voltar ao Menu Principal", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.mostrar_menu_principal).pack(fill="x", padx=100, pady=10)

    def exibir_auditoria_grupo(self, proj):
        nicho = proj['nicho']
        socios = proj['socios']
        devs = proj['equipe_trab']
        mkt = proj['marketing']
        fachada = proj.get('fachada', 'Padrão')
        bonus = proj.get('bonus', 'Padrão')
        licenca = proj['licenca']

        ponto_forte_mkt = "Uso de marketing agressivo" if "Influenciadores" in mkt else "Foco em jogo responsável"
        consequencia_mkt = "Atração rápida de público jovem impulsivo." if "Influenciadores" in mkt else "Construção de base leal e consciente."

        ponto_forte_juridico = "Offshore sem licença" if "Offshore" in licenca else "Licença Oficial SPA"
        consequencia_juridico = "Maior margem financeira imediata, mas risco de bloqueio da Anatel." if "Offshore" in licenca else "Total segurança jurídica perante o Estado."

        persp_dono_str = "\n".join(proj["perspectiva_dono"]) if proj["perspectiva_dono"] else "Sem registros."
        persp_user_str = "\n".join(proj["perspectiva_usuario"]) if proj["perspectiva_usuario"] else "Sem registros."
        
        texto_auditoria = (
            f"📋 FEEDBACK PEDAGÓGICO COMPLETO: {proj['equipe'].upper()} [{nicho.upper()}]\n\n"
            f"🔹 **PONTOS FORTES E ESCOLHAS:**\n"
            f"• Sócios ({socios}) | Devs ({devs}) | Fachada ({fachada}) | Bônus ({bonus})\n"
            f"• Marketing: {ponto_forte_mkt} | Jurídico: {ponto_forte_juridico}\n\n"
            f"⚠️ **CONSEQUÊNCIAS PRÁTICAS:**\n"
            f"• {consequencia_mkt} {consequencia_juridico}\n\n"
            f"👑 **VISÃO DOS DONOS (12 MESES):**\n{persp_dono_str}\n\n"
            f"👥 **VISÃO DOS USUÁRIOS (12 MESES):**\n{persp_user_str}"
        )
        self.lbl_detalhes_turma.config(text=texto_auditoria, font=("Arial", 11), fg="#f1f5f9", justify="left", wraplength=1200)

    def tela_investigar_bets(self):
        self.limpar_tela()
        self.root.config(bg="#0f172a")

        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(expand=True, fill="both", padx=30, pady=10)

        tk.Label(container, text="RADAR DE INVESTIGAÇÃO DE PLATAFORMAS REAIS", font=("Arial", 20, "bold"), fg="#fbbf24", bg="#0f172a", wraplength=1200).pack(pady=10)
        tk.Label(container, text="Selecione uma casa de apostas:", font=("Arial", 14), fg="#e2e8f0", bg="#0f172a", wraplength=1200).pack(pady=6)

        frame_botoes = tk.Frame(container, bg="#0f172a")
        frame_botoes.pack(pady=8)

        self.frame_detalhes = tk.Frame(container, bg="#1e293b", bd=3, relief="solid")
        self.frame_detalhes.pack(expand=True, fill="both", padx=15, pady=10)

        self.lbl_detalhes = tk.Label(self.frame_detalhes, text="Clique em uma empresa acima.", font=("Arial", 14, "italic"), fg="#94a3b8", bg="#1e293b", justify="left", wraplength=1200)
        self.lbl_detalhes.pack(padx=25, pady=15)

        for nome_bet in self.banco_investigacao.keys():
            tk.Button(frame_botoes, text=nome_bet, font=("Arial", 13, "bold"), bg="#1e293b", fg="#38bdf8", pady=8, command=lambda b=nome_bet: self.exibir_diagnostico_bet(b)).pack(side="left", padx=8)

        tk.Button(container, text="← Voltar ao Menu Principal", font=("Arial", 14, "bold"), bg="#64748b", fg="#ffffff", pady=10, command=self.mostrar_menu_principal).pack(fill="x", padx=100, pady=10)

    def exibir_diagnostico_bet(self, nome_bet):
        dados = self.banco_investigacao[nome_bet]
        texto = f"🔍 FICHA TÉCNICA: {nome_bet.upper()}\n\n• Nicho: {dados['foco']}\n• Licença: {dados['licenca']}\n• Divulgação: {dados['divulgacao']}\n\n⚠️ RISCO: {dados['risco']}"
        self.lbl_detalhes.config(text=texto, font=("Arial", 14), fg="#f1f5f9", justify="left", wraplength=1200)

    def reiniciar_projeto(self):
        self.verba_disponivel = self.verba_total
        self.tipo_operacao = ""
        self.num_socios = 1
        self.custo_socios = 0.0
        self.tipo_equipe_contratada = ""
        self.custo_equipe = 0.0
        self.tipo_marketing = ""
        self.custo_marketing = 0.0
        self.modelo_fachada = ""
        self.custo_fachada = 0.0
        self.tipo_servidor = ""
        self.custo_servidor = 0.0
        self.gateway_pagamento = ""
        self.custo_gateway = 0.0
        self.provedor_odds = ""
        self.custo_provedor = 0.0
        self.nivel_kyc = ""
        self.custo_kyc = 0.0
        self.politica_bonus = ""
        self.custo_bonus = 0.0
        self.tipo_licenca = ""
        self.custo_licenca = 0.0
        self.reserva_tecnica = 0.0
        self.bonus_sorte_usado_no_ciclo = False
        self.lucro_acumulado_banca = 0.0
        self.prejuizo_acumulado_jogadores = 0.0
        self.reputacao_empresa = 50
        self.status_operacional = "Não Iniciado"
        self.projeto_montado = False
        messagebox.showinfo("Reiniciado", "Projeto limpo e orçamento restaurado.")
        self.mostrar_menu_principal()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorBetEnterpriseEquilibrado(root)
    root.mainloop()