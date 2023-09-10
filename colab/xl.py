a="stable"
b="Stable"
c="sd"

%cd /content
%env TF_CPP_MIN_LOG_LEVEL=1

!apt -y update -qq
!wget https://github.com/camenduru/gperftools/releases/download/v1.0/libtcmalloc_minimal.so.4 -O /content/libtcmalloc_minimal.so.4
%env LD_PRELOAD=/content/libtcmalloc_minimal.so.4

!apt -y install -qq aria2
!pip install -q xformers==0.0.20 triton==2.0.0 -U

!git clone -b v2.5 https://github.com/camenduru/ui
# !git clone https://huggingface.co/embed/negative /content/ui/embeddings/negative
# !git clone https://huggingface.co/embed/lora /content/ui/models/Lora/positive
# !aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/embed/upscale/resolve/main/4x-UltraSharp.pth -d /content/ui/models/ESRGAN -o 4x-UltraSharp.pth
!git clone https://github.com/camenduru/{c}-civitai-browser /content/ui/extensions/{c}-civitai-browser
# !git clone https://github.com/camenduru/control /content/ui/extensions/control
# !git clone https://github.com/fkunn1326/openpose-editor /content/ui/extensions/openpose-editor
!git clone https://github.com/camenduru/tunnels /content/ui/extensions/tunnels
!git clone https://github.com/etherealxx/batchlinks-webui /content/ui/extensions/batchlinks-webui
%cd /content/ui
!git reset --hard
!git -C /content/ui/repositories/{a}-diffusion-stability-ai reset --hard

#!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/ckpt/{c}_xl_base_1.0/resolve/main/{c}_xl_base_1.0.safetensors -d /content/ui/models/{b}-diffusion -o {c}_xl_base_1.0.safetensors
#!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/ckpt/{c}_xl_refiner_1.0/resolve/main/{c}_xl_refiner_1.0.safetensors -d /content/ui/models/{b}-diffusion -o {c}_xl_refiner_1.0.safetensors
#!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/ckpt/{c}xl_vae/resolve/main/{c}xl_vae.safetensors -d /content/ui/models/VAE -o {c}xl_vae.vae.safetensors

!sed -i -e '''/from modules import launch_utils/a\import os''' /content/ui/launch.py
!sed -i -e '''/        prepare_environment()/a\        os.system\(f\"""sed -i -e ''\"s/dict()))/dict())).cuda()/g\"'' /content/ui/repositories/{a}-diffusion-stability-ai/ldm/util.py""")''' /content/ui/launch.py
!sed -i -e 's/\["{c}_model_checkpoint"\]/\["{c}_model_checkpoint","{c}_vae","CLIP_stop_at_last_layers"\]/g' /content/ui/modules/shared.py

!python launch.py --listen --xformers --enable-insecure-extension-access --theme dark --gradio-queue --multiple