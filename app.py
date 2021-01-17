import os
import av
import cv2
import PIL
import time
import numpy as np
import streamlit as st
from pathlib import Path
from aiortc.contrib.media import MediaPlayer
from retinaface.pulse_retina import PulseMonitor

from streamlit_webrtc import ClientSettings, VideoTransformerBase, WebRtcMode, webrtc_streamer

HERE = Path(__file__).parent

def main():
    st.set_page_config(page_title="Pulse", page_icon="assets/favicon.png", initial_sidebar_state="collapsed")
    st.image("assets/favicon.png")
    st.markdown("<style> .reportview-container .main footer {visibility: hidden;}    #MainMenu {visibility: hidden;}</style>", unsafe_allow_html=True)
    get_pulsemonitor_frames()


def app_loopback():
    """ Simple video loopback """
    webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDRECV,
        client_settings=WEBRTC_CLIENT_SETTINGS,
        video_transformer_factory=None,  # NoOp
    )


def get_pulsemonitor_frames():

    class NNVideoTransformer(VideoTransformerBase):

        def __init__(self) -> None:
            self.processor = PulseMonitor()

        def transform(self, frame: av.VideoFrame) -> np.ndarray:
            image = frame.to_ndarray(format="bgr24")
            annotated_image, _ = self.processor.process_frame(image)
            return annotated_image

    webrtc_ctx = webrtc_streamer(key="loopback", mode=WebRtcMode.SENDRECV, client_settings=WEBRTC_CLIENT_SETTINGS, video_transformer_factory=NNVideoTransformer, async_transform=True,)


WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
)

if __name__ == "__main__":
    main()