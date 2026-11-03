import datetime

from peewee import (
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
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return (
            f"{self.nome_jogador} - {self.pontos} pts "
            f"({self.tempo_partida:.1f}s)"
        )


def inicializar_banco():
    """Abre a conexão e cria as tabelas que ainda não existem."""
    db.connect(reuse_if_open=True)
    db.create_tables([Pontuacao])


def salvar_resultado(nome_jogador, pontos, tempo_partida):
    inicializar_banco()
    Pontuacao.create(
        nome_jogador=nome_jogador,
        pontos=pontos,
        tempo_partida=tempo_partida,
    )


def buscar_top10():
    """Retorna as 10 maiores pontuações; empates favorecem menor tempo."""
    consulta = (
        Pontuacao.select()
        .order_by(Pontuacao.pontos.desc(), Pontuacao.tempo_partida.asc())
        .limit(10)
    )
    return list(consulta)
