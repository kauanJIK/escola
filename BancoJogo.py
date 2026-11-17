import datetime

from peewee import (
    Case,
    CharField,
    DateTimeField,
    FloatField,
    IntegerField,
    Model,
    SqliteDatabase,
)


db = SqliteDatabase("ranking.db")


class BaseModel(Model):
    class Meta:
        database = db


class Pontuacao(BaseModel):
    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    modo_jogo = CharField(default="solo")
    dificuldade = CharField(default="medio")
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return (
            f"{self.nome_jogador} - {self.pontos} pts "
            f"({self.tempo_partida:.1f}s)"
        )


def inicializar_banco():
    """Abre o banco, cria a tabela e adiciona colunas ausentes."""
    db.connect(reuse_if_open=True)
    db.create_tables([Pontuacao])
    colunas = {
        coluna.name
        for coluna in db.get_columns(Pontuacao._meta.table_name)
    }
    if "modo_jogo" not in colunas:
        db.execute_sql(
            'ALTER TABLE "pontuacao" ADD COLUMN "modo_jogo" '
            "VARCHAR(255) NOT NULL DEFAULT 'solo'"
        )
    if "dificuldade" not in colunas:
        db.execute_sql(
            'ALTER TABLE "pontuacao" ADD COLUMN "dificuldade" '
            "VARCHAR(255) NOT NULL DEFAULT 'medio'"
        )


def salvar_resultado(
    nome_jogador,
    pontos,
    tempo_partida,
    modo_jogo="solo",
    dificuldade="medio",
):
    inicializar_banco()
    Pontuacao.create(
        nome_jogador=nome_jogador,
        pontos=pontos,
        tempo_partida=tempo_partida,
        modo_jogo=modo_jogo,
        dificuldade=dificuldade,
    )


def limpar_pontuacoes():
    inicializar_banco()
    return Pontuacao.delete().execute()


def buscar_top10(modo_jogo="solo"):
    """Retorna pontuações do modo; HARD vem antes de MÉDIO e FÁCIL."""
    prioridade_dificuldade = Case(
        None,
        (
            (Pontuacao.dificuldade == "hard", 0),
            (Pontuacao.dificuldade == "medio", 1),
            (Pontuacao.dificuldade == "facil", 2),
        ),
        3,
    )
    consulta = (
        Pontuacao.select()
        .where(Pontuacao.modo_jogo == modo_jogo)
        .order_by(
            prioridade_dificuldade,
            Pontuacao.pontos.desc(),
            Pontuacao.tempo_partida.asc(),
        )
        .limit(10)
    )
    return list(consulta)
