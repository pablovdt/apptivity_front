import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_page_config(
    page_title="Apptivity - Web -",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)

st.image("images/APPTIVITY_cutted.png", use_column_width=True)
# st.title("🌍 Bienvenido a Apptivity")
st.subheader("Conéctate con lo mejor de La Rioja")

st.markdown("""
### ¿Qué hace Apptivity?

Apptivity es la aplicación definitiva para fomentar el **turismo en La Rioja**. Diseñada tanto para usuarios como 
para organizadores de actividades, ofrece una plataforma sencilla y poderosa para descubrir, gestionar y participar
en actividades turísticas locales. 

- **Para los usuarios:** Apptivity te mantiene al tanto de todas las actividades que más te interesan en La Rioja.
 Desde degustaciones, rutas, conciertos, festivales de vino, actividades al aire libre.
 Personaliza tus notificaciones para recibir alertas según tus preferencias, como la distancia y el tipo de actividad.

- **Para los organizadores:** Si eres responsable de actividades turísticas o eventos en La Rioja, Apptivity es tu
 mejor aliado. Podrás gestionar tus actividades, promocionarlas a un público local, acceder a estadísticas detalladas
  sobre el interés en tus eventos y mucho más.

---

### ¿Cómo funciona Apptivity?

- 📍 **Descubre actividades cercanas:** Apptivity utiliza la geolocalización para mostrarte eventos y actividades 
    cerca de tu ubicación. Tú decides la distancia a la que quieres recibir las notificaciones.
- 🕵️‍♂️ **Filtra por tus intereses:** Ya sea que te guste el vino, la gastronomía, el senderismo o los festivales, 
    puedes elegir qué tipo de actividades te interesan para recibir alertas personalizadas.
- 🔔 **Notificaciones personalizadas:** Recibe actividades de los lugares que más te interesan. Personaliza el radio
        de distancia para estar al tanto de lo que sucede cerca de ti.

---

### ¿Eres usuario? :

- **Actividades sobre tus intereses** 
- **Norificaciones sobre cambios en actividades** 
- **Actividades más demandadas**
- **¿Quieres algo nuevo? Más actividades**
- **Promociones y ofertas exclusivas** 


---

### ¿Eres organizador?:

- **Crea actividades de forma sencilla** 
- **LLega a un gran número de personas** 
- **Gestióna las actividades comodamente**
- **Estadísticas detalladas:** 
- **Consulta de donde procede tu turismo** 

---

""")
st.title("Difunde tu actividad en toda La Rioja")
latitudes = [
    42.5663460958579, 42.4362228354874, 41.9536806059926, 0.0, 42.3652087121677,
    42.4000988625693, 42.4042978479629, 42.2291365184681, 42.4239310584127, 42.4076250619403,
    42.159620809149, 42.2261819365028, 42.5754139174408, 42.2509713543766, 42.3808925396522,
    42.374238544551, 42.2153974306128, 42.2214660084789, 42.4285206632771, 42.3524652340104,
    42.2082301769762, 42.4385845190338, 42.3618856739874, 42.4736206831463, 42.3430593665927,
    42.5136609827223, 42.3291482093304, 42.2660101845995, 42.2506801404284, 42.3658189369826,
    42.3183673907055, 42.1793991149214, 42.6039860769164, 42.5240684236217, 42.1864583823243,
    42.307869084608, 42.3557343859451, 42.1818161333813, 42.3975611299978, 42.3949124722046,
    42.3745623270071, 42.5473655679105, 42.5132277804401, 42.3287926947192, 42.6237349419408,
    42.4793401851368, 42.0313213115163, 42.4850778032649, 42.5787454428988, 42.4244987501371,
    42.3501521107654, 42.3883897225054, 42.3540815888504, 42.0664425892735, 42.4217034099617,
    42.5507366690794, 42.3585033026039, 42.139771238006, 42.3957954781069, 42.3207194262645,
    42.2632528627069, 42.6119695530579, 42.589710205357, 42.4748305758632, 42.6208995345344,
    42.3634408919726, 42.1747862789859, 42.5535057324179, 42.5070606590734, 0.0, 42.5665431693139,
    42.2297004411065, 42.5029436390292, 42.4501602843016, 42.4540010101185, 42.4637573560773,
    42.212465838362, 42.3973352780627, 42.4320364267258, 42.0528316309918, 42.2135462397888,
    42.1639712318572, 42.3268777644748, 42.4140906991708, 42.3185040396705, 42.508890719051,
    42.3361972838805, 42.4671213247137, 0.0, 42.3916280148364, 42.1119435586792, 42.3819635256435,
    42.2928877233593, 42.3899570168005, 42.1981754173837, 42.4074310816256, 42.1292692853894,
    42.2208698946984, 42.4244023325867, 42.3323129233651, 41.9683867883856, 42.4281220151845
]

longitudes = [
    -2.7034943374, -2.2788383532, -1.9926018698, 0.0, -2.4705590378, -2.4096007466,
    -2.1517406543, -1.9095509798, -2.8187652436, -2.6706871818, -1.82434230161,
    -2.5905467066, -2.9063688464, -2.7983743493, -2.7176400739, -2.68634985729,
    -2.2361404735, -2.0928397047, -2.2526572875, -2.135227057, -1.9710936698,
    -2.7978709938, -2.802085684, -2.8883326121, -2.7564729255, -2.9491648931,
    -2.8695445041, -2.1530620079, -2.1650826072, -2.6692798714, -2.7567546253,
    -2.7926186067, -2.8318039238, -2.7859777951, -2.5179706471, -1.95261811526,
    -2.7186478806, -3.0824681337, -2.8319112761, -2.8530221082, -2.7664815967,
    -2.905370377, -2.9214958059, -2.6556475534, -3.001187041, -2.6450279797,
    -1.9660351248, -2.8558342852, -2.9210575006, -2.8776634292, -2.4284464099,
    -2.8085357294, -2.2145637018, -2.1027286414, -3.0062943017, -2.9665987939,
    -2.5930698423, -2.24938132387, -2.5151438685, -2.8441499088, -3.023839979,
    -3.0422377156, -3.00067125681, -2.5842047984, -2.9572233569, -2.2309856978,
    -2.6119312518, -2.8955422108, -2.8999689315, 0.0, -2.8690706501, -2.1708500468,
    -3.0130398755, -2.855648421, -2.7783462571, -2.7294201043, -2.40323291675,
    -2.5789128875, -2.6675309918, -2.0263592501, -2.4926787549, -2.540238188,
    -2.345139903, -2.4720644516, -2.7042727116, -3.04404257768, -2.4081349444,
    -2.4454133612, 0.0, -2.6618651429, -2.9063983997, -2.9047043149, -2.7931509702,
    -2.558175328, -2.3258655889, -2.3083786887, -2.1229521868, -2.5385617796,
    -2.7339858072, -2.4880427984, -2.0831289392, -2.5638104829
]

# Crear un DataFrame con las coordenadas
tourism_data = pd.DataFrame({
    "lat": latitudes,
    "lon": longitudes
})

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",  # Estilo del mapa
        initial_view_state=pdk.ViewState(
            latitude=42.4671213247137,
            longitude=-2.4454133612,
            zoom=8,
            pitch=90,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=tourism_data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=tourism_data,
                get_position="[lon, lat]",
                get_color="[130, 178, 154, 160]",  # 82b29a
                get_radius=200,
            ),
        ],
    )
)

st.markdown("---")
st.write("### 📬 Contáctanos")
st.write("¿Tienes dudas o preguntas sobre cómo usar la app? ¡Estamos para ayudarte!")
st.write("Puedes enviarnos un mensaje a través del siguiente formulario.")
with st.form("contact_form"):
    name = st.text_input("Tu nombre")
    email = st.text_input("Tu correo electrónico")
    message = st.text_area("Tu mensaje")
    submitted = st.form_submit_button("Enviar")
    if submitted:
        st.success(f"Gracias por contactarnos, {name}. Nos pondremos en contacto contigo pronto.")

st.markdown("""
    <style>
        .btn-custom {
            background-color: #82b29a;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 10px;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s, transform 0.2s;
        }
        .btn-custom:hover {
            background-color: #6d9e7f;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# Título atractivo
st.title("Bienvenido a Apptivity")

# Texto explicativo para el usuario
st.write("Haz clic en el botón para comenzar tu experiencia.")

# Botón atractivo con estilo
if st.button("Quiero usar Apptivity", key="use_app", help="Haz clic para empezar a usar Apptivity",
             use_container_width=True):
    st.switch_page("app.py")
