import matplotlib.pyplot as plt
import streamlit as st
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import pandas as pd
import numpy as np
import altair as alt
import io

"""
This is a simple application to explore GC fractions of all sequences in a FASTA file.
Author: Niveditha M.S.
"""
def parse_data(uploaded_file):
    fasta_sequences = SeqIO.parse(io.TextIOWrapper(uploaded_file), "fasta")
    seqs = []
    gc_fractions = []
    for record in fasta_sequences:
        gc = "{:.4f}".format(gc_fraction(record.seq))
        gc_fractions.append(gc)
        seqs.append(record.id)
    df = pd.DataFrame({"Seq ID": seqs, "GC Fraction": np.array(gc_fractions,dtype=np.float64)})
    return df


st.title("GC Viewer")
st.markdown("GC Viewer is a simple application to explore GC fractions of all sequences in a FASTA file.")
st.markdown("Select a FASTA file to get started.")
st.markdown("## Select a FASTA file")
uploaded_file = st.file_uploader("Select Fasta file", type=["fa", "fasta", "faa"])
if uploaded_file is not None: 
    df = parse_data(uploaded_file)
    st.markdown("## GC Fraction as Table")
    st.write(df.set_index("Seq ID"))
    st.markdown("## GC Fraction as Chart")
    chart = alt.Chart(df).mark_bar().encode(
        x='Seq ID',
        y='GC Fraction',
        tooltip=['Seq ID', 'GC Fraction']).properties()
    st.altair_chart(chart, use_container_width=True)
