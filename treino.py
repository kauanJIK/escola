from peewee import *

print("Conectando ao banco de dados...")
banco = SqliteDatabase("treino.db")
print("menu")
print("1 - Cadastrar contato")
print("2 - Ver todos os contatos")
print("3 - Buscar contato pelo nome")
print("4 - Editar contato pelo ID")
print("5 - Excluir contato pelo ID")
print("6 - Sair")

pritn