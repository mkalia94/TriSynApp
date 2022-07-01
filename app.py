from tps import *
import streamlit as st

st.title("Simulating the tripartite synapse")

st.text("A short overview of the model with iamage of the model")

st.sidebar.header("Simulation set up")

paramdict["tfinal"] = st.sidebar.number_input("Final time of the simulation (in min.)")
alphae0 = st.sidebar.slider("Extracellular volume fraction (in %)")
paramdict["alphae0"] = alphae0/100
nogates = st.sidebar.radio("Gates at infinity? (Skips fast-timescale simulation)",("Yes","No"))
if nogates == 'Yes':
    paramdict["nogates"] = True
else:
    paramdict["nogates"] = False

st.sidebar.markdown("""---""")

st.sidebar.text("Short description of what options you have")


# ----------------------- ED --------------------------------
st.sidebar.subheader("Energy deprivation")

ed = st.sidebar.radio("Simulate energy deprivation (ED)?",("Yes","No"))

if ed == 'Yes':
    perc = st.sidebar.slider("How much energy is available (in %)")
    paramdict["perc"] = perc/100
    paramdict["tstart"] = st.sidebar.number_input("Start time ED (in min.)")
    paramdict["tend"] = st.sidebar.number_input("End time ED (in min.)")

else:
    paramdict["perc"] = 1
    paramdict["tstart"] = 0
    paramdict["tend"] = 0
st.sidebar.markdown("""---""")

#---------------------------Stimulation-----------------------
st.sidebar.subheader("Stimulating the neuronal membrane")

st.sidebar.text("The neuron is electrically stimulated with a square wave current multiple times, based on the parameters below")
stim = st.sidebar.radio("Simulate electrical stimulation?",("Yes","No"))

if stim == 'Yes':
    stim_start = st.sidebar.number_input("Start time stimulation (in min.)")
    stim_end = st.sidebar.number_input("End time stimulation (in min.)")
    stim_strength = st.sidebar.slider("Stimulation current (in pA)",0.0,30.0)
    stim_length = st.sidebar.number_input("Stimulation duration (in seconds)")
    stim_frequency = st.sidebar.slider("Active or passive stimulation? Low is less frequent, high is more frequent", 0.0,0.99)
    paramdict["excite"] = [stim_start, stim_end, stim_strength, stim_length, stim_frequency]

st.sidebar.markdown("""---""")

#------------------------- Channel blockers ------------------------
st.sidebar.subheader("Channel blockers")

block_switch = st.sidebar.radio("Block specific channels?",("Yes","No"))

channel = {}
channel["INa (neuron)"] = "INaG"
channel["IK (neuron)"] = "IKG"
channel["KCl cotransporter (neuron)"] = "JKCl"

if block_switch == 'Yes':
    block = st.sidebar.multiselect("Select channels to block",("INa (neuron)","IK (neuron)","KCl cotransporter (neuron)"))
    block_dict = {}
    for key in block:
        st.sidebar.write("Blocking ",key)
        block_dict[channel[key]] = [st.sidebar.number_input("Start time block {} (in min.)".format(key)), st.sidebar.number_input("End time block {} (in min.)".format(key))]

    paramdict["block"] = block_dict

st.sidebar.markdown("""---""")

# Empty parameters
paramdict["nosynapse"] = False
paramdict["s"] = False
paramdict["m"] = False
paramdict["b"] = False
paramdict["solve"] = False
paramdict["savenumpy"] = False
paramdict["savematlab"] = False
paramdict["plotall"] = False
paramdict["nochargecons"] = False
paramdict["geteigs"] = False
paramdict["savematlabpar"] = False

#----------------------------- Set up simulation ------------------------

if st.sidebar.button("Set up simulation"):
    fm = fmclass(paramdict)
    st.sidebar.success("Ready to simulate!")
    fm.solve = True
    fm.plotall = True
    with st.spinner("Simulating.."):
        t,y = exec_solve(fm)
        st.sidebar.success("Done!")
        fig = plt.gcf()
        st.pyplot(fig)


    
    


# ED
# Stimulation
# Channel blockers
# Ion Current injection
# Bath coupling
# Nogates
# Astrocyte block


