
import streamlit as st
import gpxpy
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import imageio
from PIL import Image
import os

st.title("Generador de vídeo de ruta GPX con icono de moto -2")

gpx_file = st.file_uploader("Sube tu archivo GPX", type=["gpx"])
moto_file = st.file_uploader("Sube una imagen PNG para la moto", type=["png"])
fps = st.slider("Fotogramas por segundo", min_value=1, max_value=30, value=10)

if gpx_file and moto_file:
    gpx = gpxpy.parse(gpx_file)

    coords = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coords.append((point.longitude, point.latitude))

    if not coords:
        st.error("No se encontraron puntos en el archivo GPX.")
    else:
        st.success(f"{len(coords)} puntos cargados correctamente.")

        icon_img = Image.open(moto_file)
        frames = []

        st.info("Generando vídeo, por favor espera...")

        for i in range(2, len(coords)+1):
            fig, ax = plt.subplots(figsize=(6, 6))
            xs, ys = zip(*coords[:i])
            ax.plot(xs, ys, color="red", linewidth=2)
            ax.set_xlim(min(xs)-0.01, max(xs)+0.01)
            ax.set_ylim(min(ys)-0.01, max(ys)+0.01)
            ax.set_xticks([]), ax.set_yticks([])
            ax.set_title("Motovolta - Ruta GPX")

            imagebox = OffsetImage(icon_img, zoom=0.05)
            ab = AnnotationBbox(imagebox, (xs[-1], ys[-1]), frameon=False)
            ax.add_artist(ab)

            frame_path = f"_frame_{i}.png"
            plt.savefig(frame_path, bbox_inches="tight")
            frames.append(imageio.v2.imread(frame_path))
            plt.close()
            os.remove(frame_path)

        output_file = "video_gpx_moto.mp4"
        imageio.mimsave(output_file, frames, fps=fps)

        st.success("Vídeo generado correctamente.")
        st.video(output_file)
        with open(output_file, "rb") as f:
            st.download_button("Descargar vídeo", f, file_name=output_file, mime="video/mp4")
