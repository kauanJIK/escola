
from peewee import *
import datetime
db = SqliteDatabase("pontuacao.db")
class BaseModel(Model):
    class Meta:
        database = db
class Ranking(BaseModel):
    nome_jogador = CharField
    pontos = IntegerField
    tempo_partida = FloatField
    data_hora = DateTimeField(default=datetime.datetime.now)

    def mostrar_pontuacao(self,  self.pontuacao):
        return (f"{self.pontos : self_pontuacao} pts ")

    def mostar_ranking(self):
        return (f"{self.nome_jogador: self_nome_jogador} - "
                        f"{self.pontos : self_pontos} pts "
                        f"({self.tempo_partida: self_tempo_partida:.1f}s)")
        
        rank = Ranking.select()
        for i in rank:
            print(i)




db.connect()
db.create_tables([Ranking])