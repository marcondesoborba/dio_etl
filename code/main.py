import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ============================
# 1. EXTRACT
# ============================

# Criando dados fictícios de pedidos
dados = {
    "nome": ["Ana", "Carlos", "Mariana", "João", "Fernanda", "Pedro"],
    "endereco": [
        "Rua A, 123", "Av. Central, 456", "Rua das Flores, 789",
        "Rua B, 321", "Av. Brasil, 654", "Rua C, 987"
    ],
    "numero_pedido": [101, 102, 103, 104, 105, 106],
    "status_entrega": ["entregue", "atrasado", "entregue", "atrasado", "entregue", "atrasado"],
    "data_entrega": [
        "2025-11-20", "2025-11-25", "2025-11-28",
        "2025-11-15", "2025-11-27", "2025-11-10"
    ]
}

# Criando DataFrame
df = pd.DataFrame(dados)

# Salvando em CSV (simulação do Extract)
df.to_csv("pedidos.csv", index=False)

# ============================
# 2. TRANSFORM
# ============================

# Carregando o CSV
df = pd.read_csv("pedidos.csv")

# Convertendo datas
df["data_entrega"] = pd.to_datetime(df["data_entrega"])

# Data atual
data_atual = datetime(2025, 11, 29)

# Calculando dias de atraso
df["dias_de_atraso"] = (data_atual - df["data_entrega"]).dt.days
df["dias_de_atraso"] = df["dias_de_atraso"].apply(lambda x: x if x > 0 else 0)

# Multa: R$1 por dia de atraso
multa = 1
df["multa_por_atraso"] = df["dias_de_atraso"] * multa

# ============================
# 3. LOAD
# ============================

# Agrupando por semana
df["semana"] = df["data_entrega"].dt.isocalendar().week

# Contagem de pedidos entregues e atrasados
resumo = df.groupby("semana").agg({
    "status_entrega": lambda x: (x == "entregue").sum(),
    "dias_de_atraso": lambda x: (x > 0).sum(),
    "multa_por_atraso": "sum"
}).reset_index()

resumo.rename(columns={
    "status_entrega": "entregues",
    "dias_de_atraso": "atrasados",
    "multa_por_atraso": "custo_multa"
}, inplace=True)

print(resumo)

# ============================
# Gráfico
# ============================

plt.figure(figsize=(10,6))

plt.plot(resumo["semana"], resumo["entregues"], marker="o", label="Pedidos Entregues")
plt.plot(resumo["semana"], resumo["atrasados"], marker="o", label="Pedidos Atrasados")
plt.bar(resumo["semana"], resumo["custo_multa"], alpha=0.3, label="Custo Multa (R$)")

plt.title("Resumo de Entregas por Semana")
plt.xlabel("Semana")
plt.ylabel("Quantidade / Multa (R$)")
plt.legend()
plt.grid(True)
plt.show()
