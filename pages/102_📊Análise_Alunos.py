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
def carregar_dados_sisu():
    # tabela = pd.concat(map(pd.read_excel, glob.glob('Resultado_9ano.xlsx')))
    # tabela['ano'] = tabela['ano'].apply(lambda _: str(_))
    tabela = pd.read_excel('sisu2024.xlsx', sheet_name=1)
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
    nome_arquivo = nome_arquivo.replace('- alunos', '')
    nome_arquivo = nome_arquivo.replace('conjunto', 'Conjunto ')


#dados = carregar_dados()
    dados = data

    lista2 = []
    for i in dados['Nome'].unique():
        lista2.append([i, dados['Média com RD'][dados['Nome']==i].values])
    df2 = pd.DataFrame(lista2, columns=['Aluno', 'Média com RD'])
    df2['Média com RD'] = df2['Média com RD'].astype(float)
    
    
    fig2 = px.bar(df2, x = 'Aluno',  y = 'Média com RD',
                                barmode='group', title=f'Média com Redação dos Alunos - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig2

    lista_LC = []
    for i in dados['Nome'].unique():
        lista_LC.append([i, dados['Nota LC'][dados['Nome']==i].values])
    df_LC = pd.DataFrame(lista_LC, columns=['Aluno', 'Nota LC'])
    df_LC['Nota LC'] = df_LC['Nota LC'].astype(float)

    fig_LC = px.bar(df_LC, x = 'Aluno',  y = 'Nota LC',
                                barmode='group', title=f'Notas Linguagens - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig_LC

    lista_CH = []
    for i in dados['Nome'].unique():
        lista_CH.append([i, dados['Nota CH'][dados['Nome']==i].values])
    df_CH = pd.DataFrame(lista_CH, columns=['Aluno', 'Nota CH'])
    df_CH['Nota CH'] = df_CH['Nota CH'].astype(float)

    fig_CH = px.bar(df_CH, x = 'Aluno',  y = 'Nota CH',
                                barmode='group', title=f'Notas Ciências Humanas - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig_CH

    lista_CN = []
    for i in dados['Nome'].unique():
        lista_CN.append([i, dados['Nota CN'][dados['Nome']==i].values])
    df_CN = pd.DataFrame(lista_CN, columns=['Aluno', 'Nota CN'])
    df_CN['Nota CN'] = df_CN['Nota CN'].astype(float)

    fig_CN = px.bar(df_CN, x = 'Aluno',  y = 'Nota CN',
                                barmode='group', title=f'Notas Ciências Natureza - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig_CN

    lista_MT = []
    for i in dados['Nome'].unique():
        lista_MT.append([i, dados['Nota MT'][dados['Nome']==i].values])
    df_MT = pd.DataFrame(lista_MT, columns=['Aluno', 'Nota MT'])
    df_MT['Nota MT'] = df_MT['Nota MT'].astype(float)

    fig_MT = px.bar(df_MT, x = 'Aluno',  y = 'Nota MT',
                                barmode='group', title=f'Notas Matemática - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig_MT

    lista_RD = []
    for i in dados['Nome'].unique():
        lista_RD.append([i, dados['Nota RD'][dados['Nome']==i].values])
    df_RD = pd.DataFrame(lista_RD, columns=['Aluno', 'Nota RD'])
    df_RD['Nota RD'] = df_RD['Nota RD'].astype(float)

    fig_RD = px.bar(df_RD, x = 'Aluno',  y = 'Nota RD',
                                barmode='group', title=f'Notas Redação - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig_RD


    Aluno = st.sidebar.selectbox("Selecione um Aluno", dados["Nome"].sort_values().unique())

    dados = dados[dados["Nome"]==Aluno]

    dados["Porcentagem CH"] = dados["Porcentagem CH"].replace('%', '', regex=True)
    dados["Porcentagem CH"] = dados["Porcentagem CH"].replace(',', '.', regex=True)
    dados["Porcentagem CH"] = dados["Porcentagem CH"].astype(float)
    dados["Porcentagem CN"] = dados["Porcentagem CN"].replace('%', '', regex=True)
    dados["Porcentagem CN"] = dados["Porcentagem CN"].replace(',', '.', regex=True)
    dados["Porcentagem CN"] = dados["Porcentagem CN"].astype(float)
    dados["Porcentagem LC"] = dados["Porcentagem LC"].replace('%', '', regex=True)
    dados["Porcentagem LC"] = dados["Porcentagem LC"].replace(',', '.', regex=True)
    dados["Porcentagem LC"] = dados["Porcentagem LC"].astype(float)
    dados["Porcentagem MT"] = dados["Porcentagem MT"].replace('%', '', regex=True)
    dados["Porcentagem MT"] = dados["Porcentagem MT"].replace(',', '.', regex=True)
    dados["Porcentagem MT"] = dados["Porcentagem MT"].astype(float)
    dados['Média sem RD'] = dados["Média sem RD"].replace(',', '.', regex=True)
    dados["Média sem RD"] = dados["Média sem RD"].astype(float)
    dados['Média com RD'] = dados["Média com RD"].replace(',', '.', regex=True)
    dados["Média com RD"] = dados["Média com RD"].astype(float)

    lista = []
    for i in ['Porcentagem CH', 'Porcentagem LC', 'Porcentagem CN', 'Porcentagem MT']:
        lista.append([i, dados[i].values])
    df = pd.DataFrame(lista, columns=['Área', 'Nota'])
    df['Nota'] = df['Nota'].astype(float)
    

    fig = px.bar(df, x = 'Área',  y = 'Nota',
                                barmode='group', title=f'Porcentagem de Acertos por Área: {Aluno} - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig
    #df

    lista1 = []
    for j in ['Nota CH', 'Nota LC', 'Nota CN', 'Nota MT', 'Nota RD']:
        lista1.append([j, dados[j].values])
    df1 = pd.DataFrame(lista1, columns=['Área', 'Nota'])
    df1['Nota'] = df1['Nota'].astype(float)
    
    fig_tri = px.bar(df1, x = 'Área',  y = 'Nota',
                                barmode='group', title=f'Nota TRI por Área: {Aluno}  - {nome_arquivo}',
                                labels = {'value': '',
                                          'index': ''},
                                            height=800, width=1280, text_auto = True,).update_xaxes(categoryorder="total descending")
    #fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    y = dados.iat[0, 22]
    fig_tri.add_shape( # add a horizontal "target" line
    label_textposition='end', label_font_size=22, label_text=f'Média Geral do Aluno = {y}',     
    type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y")
    
    fig_tri

    sisu = carregar_dados_sisu()

    sisu = sisu.rename(columns={"SG_IES": "Univ.", 
                         "NO_CAMPUS": "Campus",
                         "NO_MUNICIPIO_CAMPUS": "Cidade",
                         "NO_CURSO": "Curso",
                         "DS_GRAU": "Grau",
                         "DS_TURNO": "Turno",
                         "NU_NOTACORTE": "Nota de Corte"})
    
    universidade = st.selectbox("Selecione uma universidade", sisu['NO_IES'].sort_values().unique(), index=None)
    #sisu
    sisu = sisu[sisu['TIPO_CONCORRENCIA']=="AC"]
    #st.table(sisu[sisu['NO_CURSO']=='MEDICINA'])

    sisu_filtrado = sisu[sisu['NO_IES']==universidade]
    
    sisu_filtrado = sisu_filtrado[sisu_filtrado['Nota de Corte']<=y]
    # sisu = sisu.rename(columns={"SG_IES": "Univ.", 
    #                      "NO_CAMPUS": "Campus",
    #                      "NO_MUNICIPIO_CAMPUS": "Cidade",
    #                      "NO_CURSO": "Curso",
    #                      "DS_GRAU": "Grau",
    #                      "DS_TURNO": "Turno",
    #                      "NU_NOTACORTE": "Nota de Corte"})
   
    
    aprovado = sisu_filtrado.drop(['EDICAO', 'CO_IES', 'DS_ORGANIZACAO_ACADEMICA', 'SG_UF_CAMPUS', 'DS_REGIAO_CAMPUS', 
                          'CO_IES_CURSO', 'TP_MOD_CONCORRENCIA', 'DS_MOD_CONCORRENCIA', 'NU_PERCENTUAL_BONUS', 
                          'QT_INSCRICAO', 'NO_IES', 'DS_CATEGORIA_ADM', 'QT_VAGAS_OFERTADAS', 'TIPO_CONCORRENCIA'], axis=1)
    
    aprovado = aprovado.sort_values(by='Nota de Corte')
    st.markdown("Cursos Aprovados na 1ª Chamada 2024 na universidade selecionada, com base no resultado do simulado. Ampla Concorrência!")
    #st.table(aprovado)
    st.table(aprovado.assign(hack='').set_index('hack'))

    curso_pretendido = st.selectbox("Selecione o Curso Pretendido", sisu['Curso'].sort_values().unique(), index=None)

    df_curso = sisu[sisu['Curso']==curso_pretendido]

    univ_curso = df_curso.drop(['EDICAO', 'CO_IES', 'DS_ORGANIZACAO_ACADEMICA', 'SG_UF_CAMPUS', 'DS_REGIAO_CAMPUS', 
                          'CO_IES_CURSO', 'TP_MOD_CONCORRENCIA', 'DS_MOD_CONCORRENCIA', 'NU_PERCENTUAL_BONUS', 
                          'QT_INSCRICAO', 'NO_IES', 'DS_CATEGORIA_ADM', 'QT_VAGAS_OFERTADAS', 'TIPO_CONCORRENCIA'], axis=1)
    
    univ_curso = univ_curso.sort_values(by='Nota de Corte')
    # st.markdown("Cursos Aprovados na 1ª Chamada 2024 na universidade selecionada, com base no resultado do simulado. Ampla Concorrência!")
    # #st.table(aprovado)
    # st.table(univ_curso.assign(hack='').set_index('hack'))

    # teste = univ_curso.style.apply(axis=1, func=apply_style)
    # univ_curso
    df = univ_curso
    df = df.style.applymap(lambda x: f"background-color: {'green' if x<y else 'red'}", subset='Nota de Corte')
    # st.table(df.assign(hack='').set_index('hack'))
    # df = st.dataframe(df)
    st.markdown(f'Nota Média {Aluno} = {y}')
    st.table(df)
    # st.dataframe(df)

    # ['background-color: green']*len(curso) if curso['Nota de Corte']<600 else ['background-color: red']*len(curso)
    # print(univ_curso['Nota de Corte'])
    # if (univ_curso[univ_curso['Nota de Corte']]<y):
    #     cor = ['background-color: red']*len(curso)
    # else:
    #     cor = ['background-color: green']*len(curso)

    # st.dataframe(univ_curso.style.apply(cor, axis=1))
    
    # if (univ_curso['Nota de Corte'].values <= y):
    #     # return ['background-color: green'] * len(linha)
    #     teste = univ_curso.style.apply(['background-color: green'] * len(linha))
    # else:
    #     # return ['background-color: red'] * len(linha)
    #     teste = univ_curso.style.apply(['background-color: red'] * len(linha))
    # st.table(teste)

    
    