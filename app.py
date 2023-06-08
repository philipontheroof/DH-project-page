import matplotlib
import streamlit as st
from collections import Counter
import pickle
import koreanize_matplotlib
import pandas as pd
import plotly.graph_objects as go

START = 1920
END = 1999


@st.cache_resource
def load_pickle():

    import os
    import zipfile

    def join_split_files(split_files, output_file):
        with open(output_file, "wb") as output:
            for file in split_files:
                with open(file, "rb") as file_input:
                    output.write(file_input.read())

    def extract_zipfile(file_path, output_dir):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

    split_files = ['data.zip.001', 'data.zip.002', 'data.zip.003', 'data.zip.004', 'data.zip.005', 'data.zip.006', 'data.zip.007', 'data.zip.008', 'data.zip.009',
                   'data.zip.010', 'data.zip.011', 'data.zip.012', 'data.zip.013', 'data.zip.014', 'data.zip.015', 'data.zip.016', 'data.zip.017', 'data.zip.018', 'data.zip.019',
                   'data.zip.020', 'data.zip.021', 'data.zip.022', 'data.zip.023', 'data.zip.024', 'data.zip.025', 'data.zip.026', 'data.zip.027', 'data.zip.028', 'data.zip.029',
                   'data.zip.030', 'data.zip.031', 'data.zip.032', 'data.zip.033', 'data.zip.034', 'data.zip.035', 'data.zip.036', 'data.zip.037', 'data.zip.038', 'data.zip.039',
                   'data.zip.040']  # Add your filenames here

    output_file = './data/data.zip'
    output_dir = 'data'

    # Join the split zip files
    join_split_files(split_files, output_file)

    # Extract the single .zip file
    extract_zipfile(output_file, output_dir)

    counteds = {}
    for year in range(1920, 1999+1):
        counteds[year] = {}
        with open(f'./data/komoran_counter_{year}_chosun.pickle', 'rb') as f:
            counteds[year]['chosun'] = pickle.load(f)
        with open(f'./data/komoran_counter_{year}_donga.pickle', 'rb') as f:
            counteds[year]['donga'] = pickle.load(f)
    return counteds


def words_to_df(dict_data, papers, scope, words):
    x = list(range(scope[0], scope[1]+1))
    ys = {}

    for word in words:
        for paper in papers:
            if word not in ys.keys():
                ys[word] = {}
            if paper not in ys[word].keys():
                ys[word][paper] = []
            for year in range(scope[0], scope[1]+1):
                s = sum(dict_data[year][paper].values())
                if word in dict_data[year][paper].keys():
                    ys[word][paper].append(dict_data[year][paper][word]/s)
                else:
                    ys[word][paper].append(None)

    r = {'x': x}
    for word, v in ys.items():
        for paper, y in v.items():
            r[f'{word} {paper}'] = y

    df = pd.DataFrame(r)
    return df


# Read and cache the files
counteds = load_pickle()

# Streamlit application
st.title(f'Plot frequency of words ({START}-{END})')


# Get user input using text_input
user_input = st.text_input('Please enter words separated by ","')
if user_input == '':
    user_input = []
else:
    user_input = user_input.split(',')

user_input = [x.strip(' ') for x in user_input]

print(user_input)

if len(user_input) > 0:
    fig = go.Figure()

    df = words_to_df(counteds, ['chosun', 'donga'], [START, END], user_input)

    colors = ['#636EFA',
              '#EF553B',
              '#00CC96',
              '#AB63FA',
              '#FFA15A',
              '#19D3F3',
              '#FF6692',
              '#B6E880',
              '#FF97FF',
              '#FECB52'] * 10  # Repeated colors for sequential pairs of rows

    for i, column in enumerate(df.columns[1:]):
        if i % 2 == 0:
            fig.add_trace(go.Scatter(
                x=df['x'], y=df[column], mode='lines', name=column, line=dict(color=colors[i//2])))
        else:
            fig.add_trace(go.Scatter(x=df['x'], y=df[column], mode='lines', name=column, line=dict(
                color=colors[i//2], dash='dot')))

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
