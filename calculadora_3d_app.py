import streamlit as st
import math
import pandas as pd

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Calculadora de Produção 3D",
    page_icon="🖨️",
    layout="wide"
)


# =========================================================
# FUNÇÕES
# =========================================================

def formatar_hora(hora):
    horas = int(hora)
    minutos = round((hora - horas) * 60)

    return f"{horas:02d}:{minutos:02d}"


def formatar_tempo(horas):
    horas_inteiras = int(horas)
    minutos = round((horas - horas_inteiras) * 60)

    if minutos == 0:
        return f"{horas_inteiras}h"

    return f"{horas_inteiras}h{minutos:02d}"


def moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# =========================================================
# GERAR PDF
# =========================================================

def gerar_pdf_producao(resultado):

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=22,
        leftMargin=22,
        topMargin=18,
        bottomMargin=18
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "Titulo",
        parent=estilos["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=1
    )

    estilo_subtitulo_central = ParagraphStyle(
        "SubtituloCentral",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=5
    )

    estilo_secao = ParagraphStyle(
        "Secao",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=10,
        spaceBefore=4,
        spaceAfter=4
    )

    estilo_normal = ParagraphStyle(
        "NormalPDF",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9
    )

    estilo_negrito = ParagraphStyle(
        "NegritoPDF",
        parent=estilo_normal,
        fontName="Helvetica-Bold"
    )

    elementos = []


    # =====================================================
    # CABEÇALHO
    # =====================================================

    elementos.append(
        Paragraph(
            "ATENTO 3D",
            estilo_titulo
        )
    )

    elementos.append(
        Paragraph(
            "FICHA DE PRODUÇÃO",
            estilo_subtitulo_central
        )
    )


    # =====================================================
    # DADOS DO PEDIDO
    # =====================================================

    elementos.append(
        Paragraph(
            "DADOS DO PEDIDO",
            estilo_secao
        )
    )

    dados_pedido = [
        [
            Paragraph("<b>Cliente</b>", estilo_normal),
            Paragraph(
                resultado["cliente"]
                if resultado["cliente"]
                else "-",
                estilo_normal
            ),
            Paragraph("<b>Pedido / OS</b>", estilo_normal),
            Paragraph(
                resultado["numero_pedido"]
                if resultado["numero_pedido"]
                else "-",
                estilo_normal
            )
        ],
        [
            Paragraph("<b>Produto / Projeto</b>", estilo_normal),
            Paragraph(
                resultado["produto"]
                if resultado["produto"]
                else "-",
                estilo_normal
            ),
            Paragraph("<b>Quantidade</b>", estilo_normal),
            Paragraph(
                f"{resultado['quantidade_pedido']} peças",
                estilo_normal
            )
        ]
    ]

    tabela_pedido = Table(
        dados_pedido,
        colWidths=[85, 190, 85, 190]
    )

    tabela_pedido.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#D1D5DB")
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#F3F4F6")
            ),
            (
                "BACKGROUND",
                (2, 0),
                (2, -1),
                colors.HexColor("#F3F4F6")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            )
        ])
    )

    elementos.append(tabela_pedido)


    # =====================================================
    # RESUMO DA PRODUÇÃO
    # =====================================================

    elementos.append(
        Paragraph(
            "RESUMO DA PRODUÇÃO",
            estilo_secao
        )
    )

    resumo = [
        [
            "Impressoras",
            str(resultado["numero_impressoras"]),
            "Peças por impressora",
            str(resultado["pecas_por_impressora"])
        ],
        [
            "Capacidade por rodada",
            f"{resultado['pecas_por_rodada']} peças",
            "Rodadas necessárias",
            str(resultado["quantidade_rodadas"])
        ],
        [
            "Tempo por rodada",
            formatar_tempo(
                resultado["tempo_por_rodada"]
            ),
            "Conclusão prevista",
            (
                f"Dia {resultado['dia_conclusao']} - "
                f"{resultado['hora_conclusao']}"
            )
        ]
    ]

    tabela_resumo = Table(
        resumo,
        colWidths=[125, 145, 135, 145]
    )

    tabela_resumo.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#D1D5DB")
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#F3F4F6")
            ),
            (
                "BACKGROUND",
                (2, 0),
                (2, -1),
                colors.HexColor("#F3F4F6")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTNAME",
                (2, 0),
                (2, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3.5
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3.5
            )
        ])
    )

    elementos.append(tabela_resumo)


    # =====================================================
    # MATERIAL
    # =====================================================

    elementos.append(
        Paragraph(
            "MATERIAL",
            estilo_secao
        )
    )

    material = [
        [
            "Peso por peça",
            f"{resultado['peso_por_peca']:.0f} g",
            "Filamento total",
            f"{resultado['filamento_total_kg']:.2f} kg"
        ],
        [
            "Peso do rolo",
            f"{resultado['peso_rolo']:.0f} g",
            "Rolos necessários",
            str(resultado["rolos_necessarios"])
        ]
    ]

    tabela_material = Table(
        material,
        colWidths=[125, 145, 135, 145]
    )

    tabela_material.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#D1D5DB")
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#F3F4F6")
            ),
            (
                "BACKGROUND",
                (2, 0),
                (2, -1),
                colors.HexColor("#F3F4F6")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTNAME",
                (2, 0),
                (2, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3.5
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3.5
            )
        ])
    )

    elementos.append(tabela_material)


    # =====================================================
    # CRONOGRAMA
    # =====================================================

    elementos.append(
        Paragraph(
            "CRONOGRAMA DE PRODUÇÃO",
            estilo_secao
        )
    )

    dados_cronograma = [
        [
            "[ ]",
            "Rodada",
            "Dia",
            "Início",
            "Fim",
            "Peças"
        ]
    ]

    for _, linha in resultado["tabela"].iterrows():

        dados_cronograma.append(
            [
                "[ ]",
                str(linha["Rodada"]),
                str(linha["Dia"]),
                str(linha["Início"]),
                str(linha["Fim"]),
                str(linha["Peças"])
            ]
        )


    # Quanto mais rodadas, mais compacto
    quantidade_linhas = len(resultado["tabela"])

    if quantidade_linhas <= 10:
        fonte_cronograma = 7
        padding_cronograma = 3.2

    elif quantidade_linhas <= 15:
        fonte_cronograma = 6.5
        padding_cronograma = 2.4

    else:
        fonte_cronograma = 6
        padding_cronograma = 1.8


    tabela_cronograma = Table(
        dados_cronograma,
        colWidths=[
            35,
            65,
            95,
            100,
            100,
            70
        ],
        repeatRows=1
    )

    tabela_cronograma.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#E5E7EB")
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#D1D5DB")
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                fonte_cronograma
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                padding_cronograma
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                padding_cronograma
            )
        ])
    )

    elementos.append(tabela_cronograma)


    # =====================================================
    # CONTROLE DE PRODUÇÃO
    # =====================================================

    elementos.append(
        Paragraph(
            "CONTROLE DE PRODUÇÃO",
            estilo_secao
        )
    )

    controle = [
        [
            Paragraph(
                "<b>Perdas</b>",
                estilo_normal
            ),
            "________ peças",
            Paragraph(
                "<b>Retrabalho</b>",
                estilo_normal
            ),
            "________ peças"
        ],
        [
            Paragraph(
                "<b>Motivo das perdas</b>",
                estilo_normal
            ),
            (
                "_____________________________________"
                "_____________________"
            ),
            "",
            ""
        ],
        [
            Paragraph(
                "<b>Observações</b>",
                estilo_normal
            ),
            (
                "_____________________________________"
                "_____________________"
            ),
            "",
            ""
        ],
        [
            "",
            (
                "_____________________________________"
                "_____________________"
            ),
            "",
            ""
        ]
    ]

    tabela_controle = Table(
        controle,
        colWidths=[
            95,
            220,
            90,
            145
        ]
    )

    tabela_controle.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#D1D5DB")
            ),
            (
                "SPAN",
                (1, 1),
                (3, 1)
            ),
            (
                "SPAN",
                (1, 2),
                (3, 2)
            ),
            (
                "SPAN",
                (1, 3),
                (3, 3)
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            )
        ])
    )

    elementos.append(tabela_controle)

    elementos.append(
        Spacer(1, 6)
    )


    # =====================================================
    # RESPONSÁVEL / FINALIZAÇÃO
    # =====================================================

    finalizacao = [
        [
            "Responsável:",
            "____________________________",
            "Data:",
            "____ / ____ / ______"
        ],
        [
            "[ ] PRODUÇÃO FINALIZADA",
            "",
            "",
            ""
        ]
    ]

    tabela_finalizacao = Table(
        finalizacao,
        colWidths=[
            75,
            245,
            40,
            190
        ]
    )

    tabela_finalizacao.setStyle(
        TableStyle([
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica"
            ),
            (
                "FONTNAME",
                (0, 1),
                (0, 1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "SPAN",
                (0, 1),
                (-1, 1)
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            )
        ])
    )

    elementos.append(
        tabela_finalizacao
    )


    # =====================================================
    # GERAR ARQUIVO
    # =====================================================

    documento.build(elementos)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# MEMÓRIA DO SISTEMA
# =========================================================

if "resultado_producao" not in st.session_state:
    st.session_state.resultado_producao = None


# =========================================================
# ESTILO DO SISTEMA
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .subtitulo {
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 24px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 700;
    }

    div.stButton > button {
        width: 100%;
        min-height: 52px;
        border-radius: 10px;
        font-size: 17px;
        font-weight: 700;
    }

    .bloco-titulo {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 2px;
    }

    .bloco-subtitulo {
        color: #6b7280;
        margin-bottom: 18px;
    }

    .info-box {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 14px;
        color: #475569;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🧊 ATENTO 3D"
    )

    st.caption(
        "Soluções em produção"
    )

    st.divider()

    st.markdown(
        "### 🧮 Calculadora"
    )

    st.write("📅 Cronograma")
    st.write("💰 Custos")
    st.write("📄 Orçamento")

    st.divider()

    st.write("🧱 Modelos 3D")
    st.write("🖨️ Impressoras")
    st.write("🧵 Materiais")
    st.write("📊 Relatórios")

    st.divider()

    st.caption(
        "Sistema interno de produção 3D"
    )


# =========================================================
# CABEÇALHO
# =========================================================

st.title(
    "Calculadora de Produção 3D"
)

st.markdown(
    """
    <div class="subtitulo">
    Planejamento de capacidade, material, custo e prazo
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DADOS DO PEDIDO
# =========================================================

st.markdown(
    "## 📋 Dados do pedido"
)

pedido1, pedido2, pedido3 = st.columns(3)

with pedido1:

    cliente = st.text_input(
        "Cliente"
    )

with pedido2:

    numero_pedido = st.text_input(
        "Número do pedido / OS"
    )

with pedido3:

    produto = st.text_input(
        "Produto / Projeto"
    )


# =========================================================
# PRODUÇÃO / MATERIAL
# =========================================================

coluna_producao, coluna_material = st.columns(
    2,
    gap="large"
)


with coluna_producao:

    st.markdown(
        """
        <div class="bloco-titulo">
        ⚙️ Produção
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="bloco-subtitulo">
        Configure a capacidade de produção do pedido.
        </div>
        """,
        unsafe_allow_html=True
    )

    quantidade_pedido = st.number_input(
        "Quantidade do pedido",
        min_value=1,
        value=50
    )

    numero_impressoras = st.number_input(
        "Número de impressoras",
        min_value=1,
        value=6
    )

    pecas_por_impressora = st.number_input(
        "Peças por impressora em cada rodada",
        min_value=1,
        value=1
    )

    tempo_por_rodada = st.number_input(
        "Tempo de cada rodada em horas",
        min_value=0.5,
        value=3.0,
        step=0.5
    )


with coluna_material:

    st.markdown(
        """
        <div class="bloco-titulo">
        🧵 Material
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="bloco-subtitulo">
        Informe os dados do filamento utilizado.
        </div>
        """,
        unsafe_allow_html=True
    )

    peso_por_peca = st.number_input(
        "Peso de filamento por peça (g)",
        min_value=1.0,
        value=70.0,
        step=1.0
    )

    custo_filamento_kg = st.number_input(
        "Custo do filamento por kg (R$)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    peso_rolo = st.number_input(
        "Peso do rolo (g)",
        min_value=1.0,
        value=1000.0,
        step=100.0
    )

    st.markdown(
        """
        <div class="info-box">
        O sistema calcula consumo total,
        custo de filamento e planejamento
        das rodadas de produção.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BOTÃO CALCULAR
# =========================================================

calcular = st.button(
    "🧮 Calcular produção",
    type="primary"
)


# =========================================================
# EXECUTAR CÁLCULO
# =========================================================

if calcular:

    # -----------------------------------------------------
    # CAPACIDADE
    # -----------------------------------------------------

    pecas_por_rodada = (
        numero_impressoras
        * pecas_por_impressora
    )

    quantidade_rodadas = math.ceil(
        quantidade_pedido
        / pecas_por_rodada
    )


    # -----------------------------------------------------
    # MATERIAL
    # -----------------------------------------------------

    filamento_total_g = (
        quantidade_pedido
        * peso_por_peca
    )

    filamento_total_kg = (
        filamento_total_g
        / 1000
    )

    rolos_necessarios = math.ceil(
        filamento_total_g
        / peso_rolo
    )

    custo_filamento_por_peca = (
        peso_por_peca
        / 1000
    ) * custo_filamento_kg

    custo_filamento_total = (
        filamento_total_kg
        * custo_filamento_kg
    )


    # -----------------------------------------------------
    # CRONOGRAMA
    # -----------------------------------------------------

    dia = 1
    hora_atual = 8

    cronograma = []

    pecas_restantes = quantidade_pedido


    for rodada in range(
        1,
        quantidade_rodadas + 1
    ):

        hora_inicio = hora_atual

        hora_fim = (
            hora_inicio
            + tempo_por_rodada
        )

        pecas_nesta_rodada = min(
            pecas_por_rodada,
            pecas_restantes
        )

        filamento_rodada_kg = (
            pecas_nesta_rodada
            * peso_por_peca
            / 1000
        )

        custo_rodada = (
            filamento_rodada_kg
            * custo_filamento_kg
        )


        cronograma.append(
            {
                "Rodada":
                    rodada,

                "Dia":
                    f"Dia {dia}",

                "Início":
                    formatar_hora(
                        hora_inicio
                    ),

                "Fim":
                    formatar_hora(
                        hora_fim
                    ),

                "Peças":
                    pecas_nesta_rodada,

                "Filamento (kg)":
                    round(
                        filamento_rodada_kg,
                        2
                    ),

                "Custo":
                    moeda(
                        custo_rodada
                    )
            }
        )


        pecas_restantes -= (
            pecas_nesta_rodada
        )

        hora_atual = hora_fim


        # Uma rodada pode começar exatamente às 18:00.
        # Se ela terminar depois das 18:00,
        # a próxima começa às 08:00 do dia seguinte.

        if (
            hora_atual > 18
            and rodada < quantidade_rodadas
        ):

            dia += 1
            hora_atual = 8


    tabela = pd.DataFrame(
        cronograma
    )


    # -----------------------------------------------------
    # SALVAR RESULTADO
    # -----------------------------------------------------

    st.session_state.resultado_producao = {

        "cliente":
            cliente,

        "numero_pedido":
            numero_pedido,

        "produto":
            produto,

        "quantidade_pedido":
            quantidade_pedido,

        "numero_impressoras":
            numero_impressoras,

        "pecas_por_impressora":
            pecas_por_impressora,

        "tempo_por_rodada":
            tempo_por_rodada,

        "peso_por_peca":
            peso_por_peca,

        "custo_filamento_kg":
            custo_filamento_kg,

        "peso_rolo":
            peso_rolo,

        "pecas_por_rodada":
            pecas_por_rodada,

        "quantidade_rodadas":
            quantidade_rodadas,

        "filamento_total_g":
            filamento_total_g,

        "filamento_total_kg":
            filamento_total_kg,

        "rolos_necessarios":
            rolos_necessarios,

        "custo_filamento_por_peca":
            custo_filamento_por_peca,

        "custo_filamento_total":
            custo_filamento_total,

        "dia_conclusao":
            dia,

        "hora_conclusao":
            formatar_hora(
                hora_fim
            ),

        "tabela":
            tabela
    }


# =========================================================
# RESULTADO
# =========================================================

if (
    st.session_state.resultado_producao
    is not None
):

    resultado = (
        st.session_state
        .resultado_producao
    )

    st.divider()

    st.markdown(
        "## 📊 Resumo"
    )


    # -----------------------------------------------------
    # CARDS PRINCIPAIS
    # -----------------------------------------------------

    card1, card2, card3, card4 = st.columns(4)

    card1.metric(
        "📦 Pedido",
        f"{resultado['quantidade_pedido']} peças"
    )

    card2.metric(
        "🧵 Filamento total",
        f"{resultado['filamento_total_kg']:.2f} kg"
    )

    card3.metric(
        "💰 Custo total",
        moeda(
            resultado[
                "custo_filamento_total"
            ]
        )
    )

    card4.metric(
        "⏱️ Conclusão",
        (
            f"Dia "
            f"{resultado['dia_conclusao']}"
            f" - "
            f"{resultado['hora_conclusao']}"
        )
    )


    # -----------------------------------------------------
    # CARDS SECUNDÁRIOS
    # -----------------------------------------------------

    detalhe1, detalhe2, detalhe3, detalhe4 = st.columns(4)

    detalhe1.metric(
        "Capacidade por rodada",
        (
            f"{resultado['pecas_por_rodada']} "
            "peças"
        )
    )

    detalhe2.metric(
        "Rodadas necessárias",
        resultado[
            "quantidade_rodadas"
        ]
    )

    detalhe3.metric(
        "Rolos necessários",
        (
            f"{resultado['rolos_necessarios']} "
            "rolos"
        )
    )

    detalhe4.metric(
        "Custo por peça",
        moeda(
            resultado[
                "custo_filamento_por_peca"
            ]
        )
    )


    # -----------------------------------------------------
    # IDENTIFICAÇÃO
    # -----------------------------------------------------

    st.markdown(
        "### Identificação"
    )

    info1, info2, info3 = st.columns(3)

    info1.write(
        "**Cliente:** "
        + (
            resultado["cliente"]
            if resultado["cliente"]
            else "-"
        )
    )

    info2.write(
        "**Pedido / OS:** "
        + (
            resultado["numero_pedido"]
            if resultado["numero_pedido"]
            else "-"
        )
    )

    info3.write(
        "**Produto:** "
        + (
            resultado["produto"]
            if resultado["produto"]
            else "-"
        )
    )


    # -----------------------------------------------------
    # CRONOGRAMA
    # -----------------------------------------------------

    st.markdown(
        "## 📅 Cronograma de produção"
    )

    st.caption(
        "Planejamento das rodadas de impressão."
    )

    st.dataframe(
        resultado["tabela"],
        width="stretch",
        hide_index=True
    )


    # -----------------------------------------------------
    # FICHA PDF
    # -----------------------------------------------------

    st.markdown(
        "## 🖨️ Ficha de produção"
    )

    st.caption(
        "A ficha para a produção não exibe valores financeiros."
    )

    pdf = gerar_pdf_producao(
        resultado
    )


    nome_arquivo = "ficha_producao"

    if resultado["numero_pedido"]:

        nome_arquivo += (
            "_"
            + str(
                resultado[
                    "numero_pedido"
                ]
            )
        )

    nome_arquivo += ".pdf"


    st.download_button(
        label="🖨️ Gerar ficha de produção em PDF",
        data=pdf,
        file_name=nome_arquivo,
        mime="application/pdf",
        type="primary",
        width="stretch"
    )
