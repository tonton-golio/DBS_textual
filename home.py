import streamlit as st


# Sidebar
st.title('Semantic analysis of digital business strategy')
st.sidebar.write("[github](https://github.com/tonton-golio)")

with st.expander('TODO', expanded=True):
    st.markdown(r"""
        ## TODO
        - [] Add progress bars to long runs
        """)

st.write('''For this project, we have pulled quarterly 
    shareholder presentations/letter for each of the 
    currently listed Nasdaq 100 companies since 2017.
    We are looking for a list of keyword related to each
    [scope, scale, speed, source] and our suggested factor
    *digital business strategy*. We want to guage the
    digital nature of these companies, and as such; we
    assess the relatedness of the keywords in each category 
    to the keywords describing *digital business strategy*. ''')


