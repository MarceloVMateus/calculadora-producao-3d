# Escreva o seu código aqui :-)
import streamlit as st
import math
import pandas as pd


def formatar_hora(hora):
    horas = int(hora)
    minutos = round((hora - horas) * 60)

    return f"{horas:02d}:{minutos:02d}"


st.set_page_config(
    page_title="Calculadora de Produção 3D",
    page_icon="🖨️",
    layout="wide"
)

st.title("🖨️ Calculadora de Produção 3D")

st.write(
    "Calcule a capacidade, quantidade de rodadas "
    "e previsão de conclusão de um pedido."
)

coluna1, coluna2 = st.columns(2)

with coluna1:

    quantidade_pedido = st.number_input(
        "Quantidade do pedido",
        min_value=1,
        value=30
    )

    numero_impressoras = st.number_input(
        "Número de impressoras",
        min_value=1,
        value=6
    )

with coluna2:

    pecas_por_impressora = st.number_input(
        "Peças por impressora em cada rodada",
        min_value=1,
        value=1
    )

    tempo_por_rodada = st.number_input(
        "Tempo de cada rodada em horas",
        min_value=0.5,
        value=3.5,
        step=0.5
    )


if st.button("Calcular produção", type="primary"):

    pecas_por_rodada = numero_impressoras * pecas_por_impressora

    quantidade_rodadas = math.ceil(
        quantidade_pedido / pecas_por_rodada
    )

    dia = 1
    hora_atual = 8

    cronograma = []

    pecas_restantes = quantidade_pedido

    for rodada in range(1, quantidade_rodadas + 1):

        hora_inicio = hora_atual
        hora_fim = hora_inicio + tempo_por_rodada

        pecas_nesta_rodada = min(
            pecas_por_rodada,
            pecas_restantes
        )

        cronograma.append({
            "Rodada": rodada,
            "Dia": dia,
            "Início": formatar_hora(hora_inicio),
            "Fim": formatar_hora(hora_fim),
            "Peças": pecas_nesta_rodada
        })

        pecas_restantes -= pecas_nesta_rodada

        hora_atual = hora_fim

        if hora_atual > 18 and rodada < quantidade_rodadas:
            dia += 1
            hora_atual = 8

    st.divider()

    st.subheader("📊 Resumo da produção")

    resultado1, resultado2, resultado3, resultado4 = st.columns(4)

    resultado1.metric(
        "Pedido",
        f"{quantidade_pedido} peças"
    )

    resultado2.metric(
        "Capacidade por rodada",
        f"{pecas_por_rodada} peças"
    )

    resultado3.metric(
        "Rodadas necessárias",
        quantidade_rodadas
    )

    resultado4.metric(
        "Conclusão",
        f"Dia {dia} - {formatar_hora(hora_fim)}"
    )

    st.subheader("📅 Cronograma")

    tabela = pd.DataFrame(cronograma)

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )
