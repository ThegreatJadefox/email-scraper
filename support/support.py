import streamlit as st

def support_me():
    st.header("Thanks in advance for your support!")
    st.write("Your support would motivate me to add more features to this project. 😊")
    col1, col2, col3, col4 = st.columns(4, gap = "small", vertical_alignment = "center")
    with col1:
        st.subheader("Opay")
        st.write("7019567938\n\nAkintola Oladapo Julius\n")
    with col2:
        st.subheader("Access Bank")
        st.write("1510983546\n\nAkintola Oladapo Julius\n")
    with col3:
        st.subheader("Crypto Transfer")
        st.write("BTC wallet address\n1Dcpo8oWa6QwA5wVYER4UbWZh4zKWE3C85")
    with col4:
        st.subheader("USDT")
        st.write("USDT\n TRC20\nTSgoS6vPmfbtTzL7VAxSmr5ZShYHS3Rveq")

    st.write("Email verification features coming soon ...")
