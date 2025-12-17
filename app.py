import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

st.set_page_config(
    page_title="Hidden Text App",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para design moderno
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: transparent;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #e0e7ff;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
    }
    .success-msg {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
    }
    .info-box {
        background: #3b82f6;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título e subtítulo
st.markdown("<h1>🔍 Hidden Text App</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Escreva mensagens secretas em suas imagens</p>", unsafe_allow_html=True)

# Info box
st.markdown("""
<div class='info-box'>
    ℹ️ <strong>Como funciona:</strong> Este app escreve texto microscópico em sua imagem. 
    O texto será invisível a olho nu, mas aparecerá quando você der zoom!
</div>
""", unsafe_allow_html=True)

# Layout em colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📤 Upload da Imagem")
    uploaded_file = st.file_uploader("Escolha uma imagem", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Imagem Original", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Configurações")

    text_input = st.text_area("Digite o texto secreto:", height=100, placeholder="Escreva sua mensagem secreta aqui...")

    col_a, col_b = st.columns(2)
    with col_a:
        text_size = st.slider("Tamanho do texto (pixels)", 1, 10, 2, help="Quanto menor, mais escondido!")
    with col_b:
        text_opacity = st.slider("Opacidade", 1, 50, 15, help="Quanto menor, mais invisível!")

    text_color = st.color_picker("Cor do texto", "#000000")

    position = st.selectbox("Posição do texto", 
                           ["Centro", "Canto Superior Esquerdo", "Canto Superior Direito", 
                            "Canto Inferior Esquerdo", "Canto Inferior Direito"])

    st.markdown("</div>", unsafe_allow_html=True)

# Botão de processar
if uploaded_file and text_input:
    if st.button("🎨 Criar Imagem com Texto Oculto", use_container_width=True):
        with st.spinner("Processando sua imagem..."):
            # Processar imagem
            img_copy = image.copy()
            draw = ImageDraw.Draw(img_copy, 'RGBA')

            # Tentar carregar fonte, se não funcionar usa default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", text_size)
            except:
                font = ImageFont.load_default()

            # Calcular posição
            width, height = img_copy.size

            # Dividir texto em linhas se necessário
            lines = text_input.split('\n')

            # Calcular altura total do texto
            line_heights = []
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_heights.append(bbox[3] - bbox[1])

            total_height = sum(line_heights) + (len(lines) - 1) * 2  # 2 pixels entre linhas

            if position == "Centro":
                x = width // 2
                y = height // 2 - total_height // 2
                anchor = "mt"
            elif position == "Canto Superior Esquerdo":
                x, y = 10, 10
                anchor = "lt"
            elif position == "Canto Superior Direito":
                x, y = width - 10, 10
                anchor = "rt"
            elif position == "Canto Inferior Esquerdo":
                x, y = 10, height - 10 - total_height
                anchor = "lt"
            else:  # Canto Inferior Direito
                x, y = width - 10, height - 10 - total_height
                anchor = "rt"

            # Converter cor hex para RGB
            rgb_color = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))
            color_with_opacity = rgb_color + (text_opacity,)

            # Desenhar cada linha
            current_y = y
            for line in lines:
                draw.text((x, current_y), line, fill=color_with_opacity, font=font, anchor=anchor)
                bbox = draw.textbbox((0, 0), line, font=font)
                current_y += (bbox[3] - bbox[1]) + 2

            # Converter para bytes
            buf = io.BytesIO()
            img_copy.save(buf, format='PNG')
            byte_im = buf.getvalue()

            st.markdown("<div class='success-msg'>✅ Imagem criada com sucesso!</div>", unsafe_allow_html=True)

            # Mostrar resultado
            col_res1, col_res2 = st.columns(2)

            with col_res1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("🖼️ Resultado (100%)")
                st.image(img_copy, use_container_width=True, caption="Zoom para ver o texto!")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_res2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("💾 Download")
                st.download_button(
                    label="📥 Baixar Imagem",
                    data=byte_im,
                    file_name="imagem_texto_oculto.png",
                    mime="image/png",
                    use_container_width=True
                )

                st.info("💡 **Dica:** Abra a imagem em um visualizador e dê zoom para revelar o texto secreto!")
                st.markdown("</div>", unsafe_allow_html=True)

elif uploaded_file and not text_input:
    st.warning("⚠️ Por favor, digite um texto para esconder na imagem!")
elif not uploaded_file and text_input:
    st.warning("⚠️ Por favor, faça upload de uma imagem!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: white; opacity: 0.8;'>Desenvolvido com ❤️ usando Streamlit</p>", unsafe_allow_html=True)
