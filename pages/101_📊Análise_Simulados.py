import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pdfkit


st.set_page_config(layout="wide",page_title="Resultados Simulados", page_icon="🎛")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("# Resultados Simulados")

def clear_submit():
    st.session_state["submit"] = False


@st.cache_data
def carregar_dados():
    # tabela = pd.concat(map(pd.read_excel, glob.glob('Resultado_9ano.xlsx')))
    # tabela['ano'] = tabela['ano'].apply(lambda _: str(_))
    tabela = pd.read_excel('conjunto1_3serie2023.xlsx')
    return tabela

def _draw_as_table(df, pagesize):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                        rowLabels=df.index,
                        colLabels=df.columns,
                        rowColours=['lightblue']*len(df),
                        colColours=['lightblue']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center')
    return fig
  

def dataframe_to_pdf(df, filename, numpages=(1, 1), pagesize=(11, 8.5)):
  with PdfPages(filename) as pdf:
    nh, nv = numpages
    rows_per_page = len(df) // nh
    cols_per_page = len(df.columns) // nv
    for i in range(0, nh):
        for j in range(0, nv):
            page = df.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df)),
                           (j*cols_per_page):min((j+1)*cols_per_page, len(df.columns))]
            fig = _draw_as_table(page, pagesize)
            if nh > 1 or nv > 1:
                # Add a part/page number at bottom-center of page
                fig.text(0.5, 0.5/pagesize[0],
                         "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                         ha='center', fontsize=12)
            pdf.savefig(fig, bbox_inches='tight')
            
            plt.close()





uploaded_file = st.file_uploader("Faça o upload do Arquivo Desejado", type='xlsx')
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.xlsx', '')
    nome_arquivo = nome_arquivo.replace('_', ' - ')
    nome_arquivo = nome_arquivo.replace('serie', 'ª Série')
    nome_arquivo = nome_arquivo.replace('conjunto', 'Conjunto ')


#dados = carregar_dados()
    dados = data
    disciplina = st.sidebar.selectbox("Disciplina", dados["Disciplina"].unique())

    #dados = dados[dados["Disciplina"]==disciplina]

    dados["Percentual de acerto escola"] = dados["Percentual de acerto escola"].replace('%', '', regex=True)
    dados["Percentual de acerto escola"] = dados["Percentual de acerto escola"].replace(',', '.', regex=True)
    dados["Percentual de acerto escola"] = dados["Percentual de acerto escola"].astype(float)
    dados["Percentual de acerto geral"] = dados["Percentual de acerto geral"].replace('%', '', regex=True)
    dados["Percentual de acerto geral"] = dados["Percentual de acerto geral"].replace(',', '.', regex=True)
    dados["Percentual de acerto geral"] = dados["Percentual de acerto geral"].astype(float)
    dados["Diferença"] = dados["Diferença"].replace('%', '', regex=True)
    dados["Diferença"] = dados["Diferença"].replace(',', '.', regex=True)
    dados["Diferença"] = dados["Diferença"].astype(float)


    lista = []
    for i in dados["Disciplina"].unique():
        dados1 = dados[dados["Disciplina"]==i]
        media_geral =  dados1["Percentual de acerto geral"].mean().round(1)
        media_escola = dados1["Percentual de acerto escola"].mean().round(1)
        delta = media_escola - media_geral
        lista.append([i, media_geral, media_escola, delta])

    df = pd.DataFrame(lista, columns=['Disciplina', 'Média Geral', 'Média Escola', 'Diferença (Escola - Geral)'])
    #df
    df_ordenado = df.sort_values(by='Diferença (Escola - Geral)')

    newnames={'Média Geral': 'Média Escolas Bernoulli',
            'Média Escola': 'Média Turma Jayme',
            'Diferença (Escola - Geral)': 'Diferença (Jayme - Bernoulli)'}

    fig = px.bar(df_ordenado, x='Disciplina', y = ['Média Geral', 'Média Escola', 'Diferença (Escola - Geral)'],
                                barmode='group', title=f'Média Por Disciplina: {nome_arquivo}',
                                labels = {'value': 'Média'},
                                            height=800, width=1280, text_auto = True,)
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig


    dados = dados[dados["Disciplina"]==disciplina]
    
    
    fig_disciplina = px.bar(dados, x='Numeração', y = ['Percentual de acerto geral', 'Percentual de acerto escola'],
                                 barmode='group', title=f'Percentual de Acerto por Questão - {disciplina} - {nome_arquivo}',
                                labels = {'Numeração': 'Questão do Simulado',
                                          'value': 'Média'},
                                            height=800, width=1280, text_auto = True,)

    fig_disciplina.update_layout(
            xaxis=dict(
                tickvals = dados['Numeração']
            )
        )
    #fig_disciplina.update_layout(yaxis = {"categoryorder":"total ascending"})
    fig_disciplina

    print = dados.sort_values(by='Diferença')
    print = print.rename(columns={'Numeração': 'Questão'})
    #print
    df_pdf = print.drop(['Área', 'Habilidade', 'Competência', 'Gabarito'], axis=1)
    #df_pdf
    st.table(df_pdf.assign(hack='').set_index('hack'))
    #dataframe_to_pdf(df_pdf, 'test_1.pdf')

    # if st.button('Gerar PDF'):
    #     f = open('exp.html','w')
    #     a = df_pdf.to_html()
    #     f.write(a)
    #     f.close()

     
    #     options = {
    #     'page-size': 'Letter',
    #     'margin-top': '0.75in',
    #     'margin-right': '0.75in',
    #     'margin-bottom': '0.75in',
    #     'margin-left': '0.75in',
    #     'encoding': "UTF-8",
    #     'custom-header': [
    #         ('Accept-Encoding', 'gzip')
    #     ],
    #     'no-outline': None
    #     }
        

    #     pdfkit.from_file('exp.html', disciplina, options=options)

    # # nome_pdf = f'{disciplina}'
    # # with open(nome_pdf, "rb") as pdf_file:
    # #     PDFbyte = pdf_file.read()

    # st.download_button(label="Download PDF",
    #                 data=PDFbyte,
    #                 file_name=f'{disciplina}.pdf',
    #                 mime='application/octet-stream')

    df2 = df[df['Disciplina']==disciplina]
    #df2
    st.table(df2.assign(hack='').set_index('hack'))

