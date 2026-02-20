import streamlit as st
import math

# Configuration de la page
st.set_page_config(page_title="Calculateur Chute de Tension - FC ELEC", layout="centered")

# --- AFFICHAGE DU LOGO ET TITRE ---
# Note : Assurez-vous que le fichier 'logo FC ELEC.png' est dans le même dossier
try:
    st.image("logo FC ELEC.png", width=200)
except:
    st.warning("⚠️ Logo 'logo FC ELEC.png' non trouvé. Placez l'image dans le répertoire du script.")

st.title("⚡ Calcul de Chute de Tension (NF C 15-100)")
st.markdown("---")

# --- ENTRÉES UTILISATEUR (Sidebar) ---
st.sidebar.header("Paramètres de l'installation")

type_phase = st.sidebar.selectbox("Type de circuit", ["Monophasé (230V)", "Triphasé (400V)"])
nature_cable = st.sidebar.selectbox("Nature du conducteur", ["Cuivre", "Aluminium"])
section = st.sidebar.number_input("Section du conducteur (mm²)", min_value=1.5, value=2.5, step=0.5)
longueur = st.sidebar.number_input("Longueur du câble (m)", min_value=1.0, value=20.0, step=1.0)
intensite = st.sidebar.number_input("Intensité du courant (A)", min_value=1.0, value=16.0, step=1.0)
cos_phi = st.sidebar.slider("Facteur de puissance (cos φ)", 0.0, 1.0, 0.8)

# --- LOGIQUE DE CALCUL ---

# 1. Constantes selon NF C 15-100
rho = 0.0225 if nature_cable == "Cuivre" else 0.036  # Résistivité à 100°C (en ohm.mm²/m)
x = 0.00008  # Réactance linéique par défaut (en ohm/m)
b = 2 if type_phase == "Monophasé (230V)" else 1    # Coefficient de phase
tension_nominale = 230 if type_phase == "Monophasé (230V)" else 400

# 2. Calcul du Sin φ
sin_phi = math.sqrt(1 - cos_phi**2)

# 3. Formule de la chute de tension (Delta U)
# Delta U = b * (rho/S * L * cos_phi + x * L * sin_phi) * Ib
delta_u = b * ((rho / section) * longueur * cos_phi + (x * longueur * sin_phi)) * intensite
delta_u_pourcent = (delta_u / tension_nominale) * 100

# --- AFFICHAGE DES RÉSULTATS ---

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Chute de Tension (V)", value=f"{delta_u:.2f} V")
with col2:
    st.metric(label="Chute de Tension (%)", value=f"{delta_u_pourcent:.2f} %")

# --- VÉRIFICATION DES LIMITES ---
st.markdown("### Diagnostic de conformité")

# Seuils NF C 15-100 (Cas général)
# Éclairage : 3% | Autres usages : 5%
if delta_u_pourcent <= 3:
    st.success("✅ Installation conforme pour tous usages (Eclairage et Force).")
elif delta_u_pourcent <= 5:
    st.warning("⚠️ Conforme pour 'Autres usages' uniquement. Non conforme pour l'éclairage (>3%).")
else:
    st.error(f"❌ Non conforme (>5%). Augmentez la section du câble ou réduisez la longueur.")

# Détails techniques en expander
with st.expander("Voir le détail des paramètres de calcul"):
    st.write(f"**Résistivité (ρ) utilisée :** {rho} $\Omega \cdot mm^2/m$")
    st.write(f"**Réactance (x) :** {x} $\Omega/m$")
    st.write(f"**Coefficient de phase (b) :** {b}")