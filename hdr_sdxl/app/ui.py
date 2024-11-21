# SPDX-License-Identifier: Apache-2.0
import io
import logging
import streamlit as st
from PIL import Image
from app.logger import log
import app.pipeline


args = None
st_log = None


def init(_args):
    class STLogHandler(logging.StreamHandler):
        def emit(self, record: logging.LogRecord):
            if st_log is not None:
                st_log.text(f'{record.asctime} {record.levelname} {record.msg}')

    st.set_page_config(page_title="SDXL HDR", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")
    global args  # pylint: disable=global-statement
    args = _args
    st_log_handler = STLogHandler()
    log.addHandler(st_log_handler)


def start(_args):
    def change_model():
        args.model = st.session_state.model
        app.pipeline.load(args)

    def run():
        args.prompt = st.session_state.prompt
        args.negative = st.session_state.negative
        args.width = st.session_state.width
        args.height = st.session_state.height
        args.exp = st.session_state.exp
        args.gamma = st.session_state.gamma
        args.timestep = st.session_state.timestep
        args.steps = st.session_state.steps
        args.seed = st.session_state.seed
        args.cfg = st.session_state.cfg
        args.sampler = st.session_state.sampler
        args.strength = st.session_state.strength
        args.output = st.session_state.output
        args.format = st.session_state.format
        args.save = st.session_state.save
        args.ldr = st.session_state.ldr
        args.json = st.session_state.json
        args.image = Image.open(io.BytesIO(st.session_state.image.getvalue())) if st.session_state.image is not None else None
        log.info(f'UI Run: {args} prompt="{args.prompt}" negative="{args.negative}" image={args.image}')
        i = 0
        for img in app.pipeline.run(args, args.prompt, args.negative, args.image):  # run-as-generator
            caption = f'{st.session_state.prompt}' if i == 3 else f'exposure: {i * args.exp - args.exp}'
            images[i].image(img, channels='BGR', caption=caption)
            i += 1

    if args is None:
        init(_args)
    with st.sidebar:
        st.button('generate', on_click=run, use_container_width=True)
        st.text_input('model', args.model, key='model', on_change=change_model)
        st.text_area('prompt', args.prompt, key='prompt')
        st.text_area('negative prompt', args.negative, key='negative')
        st.slider('width', key='width', min_value=256, max_value=4096, value=args.width, step=8)
        st.slider('height', key='height', min_value=256, max_value=4096, value=args.height, step=8)
        with st.expander('hdr options'):
            st.slider('exposure compensation', key='exp', min_value=0.0, max_value=3.0, value=args.exp, step=0.1)
            st.slider('gamma adjust', key='gamma', min_value=0.1, max_value=5.0, value=args.gamma, step=0.1)
            st.number_input('timestep', key='timestep', value=args.timestep)
        with st.expander('generate options'):
            st.slider('steps', key='steps', min_value=1, max_value=99, value=args.steps, step=1)
            st.number_input('seed', key='seed', value=args.seed)
            st.slider('cfg', min_value=0.0, key='cfg', max_value=14.0, value=args.cfg, step=0.1)
            st.text_input('sampler', key='sampler', value=args.sampler)
        with st.expander('init image'):
            st.file_uploader('image', key='image', type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'hdr', 'webp'])
            st.slider('denoise strength', key="strength", min_value=0.01, max_value=0.99, value=args.strength, step=0.01)
        with st.expander('save options'):
            st.text_input('output folder', key='output', value=args.output)
            st.text_input('image format', key='format', value=args.format)
            st.checkbox('save interim images', key='save', value=args.save)
            st.checkbox('create 8bpc hdr png image', key='ldr', value=args.ldr)
            st.checkbox('save params to json', key='json', value=args.json)
    images = 4 * [None]
    with st.container():
        images[3] = st.empty()
    with st.container():
        col = st.columns(3)
        with col[0]:
            images[0] = st.empty()
        with col[1]:
            images[1] = st.empty()
        with col[2]:
            images[2] = st.empty()
    global st_log  # pylint: disable=global-statement
    st_log = st.container()
    st_log.header('log')
