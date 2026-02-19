import streamlit as st
import math

# Configuration de l'affichage
st.set_page_config(page_title="Calculateur NF C 15-100", page_icon="⚡")

def calcul_chute_tension():
    st.title("⚡ Calcul de chute de tension (NF C 15-100)")
    st.markdown("""
    Cette application calcule la chute de tension $\Delta U$ en fonction de la norme française **NF C 15-100**.
    """)

    # --- Saisie des données ---
    st.sidebar.header("Configuration")
    
    phase = st.sidebar.selectbox("Phase", ["Monophasé 230V", "Triphasé 400V"])
    nature = st.sidebar.selectbox("Nature du câble", ["Cuivre", "Aluminium"])
    section = st.sidebar.selectbox("Section du conducteur (mm²)", 
                                   [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95])
    
    longueur = st.sidebar.number_input("Longueur du câble (m)", min_value=1, value=25)
    intensite = st.sidebar.number_input("Intensité du courant (A)", min_value=1, value=16)
    cos_phi = st.sidebar.number_input("Facteur de puissance (cos φ)", min_value=0.1, max_value=1.0, value=0.8, step=0.05)
    
    usage = st.sidebar.radio("Usage du circuit", ["Éclairage (Limite 3%)", "Autres usages (Limite 5%)"])

    # --- Paramètres de calcul ---
    # rho1 : Résistivité à 20°C x 1.25 (pour prendre en compte la température de service de 70°C)
    rho = 0.0225 if nature == "Cuivre" else 0.036
    
    # Réactance linéique (X) négligeable pour sections < 50mm², mais fixée à 0.08 mΩ/m par défaut
    X = 0.00008 
    sin_phi = math.sqrt(1 - cos_phi**2)
    
    b = 2 if phase == "Monophasé 230V" else 1
    tension_nominale = 230 if phase == "Monophasé 230V" else 400

    # --- Formule de calcul ---
    # DU = b * (rho * (L/S) * cos_phi + X * L * sin_phi) * Ib
    delta_u = b * ((rho * (longueur / section) * cos_phi) + (X * longueur * sin_phi)) * intensite
    pourcentage = (delta_u / tension_nominale) * 100

    # --- Affichage des résultats ---
    st.subheader("Résultats du calcul")
    
    col1, col2 = st.columns(2)
    col1.metric("Chute de tension (V)", f"{delta_u:.2f} V")
    col2.metric("Chute de tension (%)", f"{pourcentage:.2f} %")

    # --- Diagnostic de conformité ---
    limite = 3.0 if usage == "Éclairage (Limite 3%)" else 5.0
    
    if pourcentage <= limite:
        st.success(f"✅ CONFORME : La chute est inférieure à {limite}%")
    else:
        st.error(f"❌ NON CONFORME : La chute dépasse la limite de {limite}%")
        st.info("💡 Suggestion : Augmentez la section du câble ou réduisez la longueur.")

    # --- Rappel technique ---
    with st.expander("Détails techniques (Norme)"):
        st.write(f"- **Coefficient de phase (b) :** {b}")
        st.write(f"- **Résistivité utilisée (ρ) :** {rho} Ω.mm²/m")
        st.write(f"- **Tension de référence :** {tension_nominale} V")

if __name__ == "__main__":
    calcul_chute_tension()