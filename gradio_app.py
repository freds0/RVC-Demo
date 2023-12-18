from infer_web import *
import gradio as gr

spk_map = {
    "M1": 3,
    "M2": 41,
    "H1": 60,
    "H2": 70,
    "M3": 499,
    "H3": 500,
}


print(names)


def upload_audio(file):
    return file.name, file.name


# Your existing code for UI creation
with gr.Blocks(title="Ceia - Voice Conversion") as app:
    gr.Markdown("## Ceia - Voice Conversion")
    gr.Markdown(
        value="Abaixo, selecione a voz de destino e faça upload de um ou mais arquivos a serem convertidos."
    )
    with gr.Tabs():
        with gr.TabItem("Converter Voz"):
            with gr.Row():
                sid0 = gr.Dropdown(label="Modelo", choices=names)

                spk_item = gr.Dropdown(label="Voz de destino", choices=spk_map.keys())

            with gr.Group():
                with gr.Row():
                    with gr.Column():
                        vc_transform0 = gr.Number(
                            label="Transposição(número de semitons, ex: aumentar em uma oitava: 12, reduzir em uma oitava: -12)",
                            value=0,
                        )
                        input_audio0 = gr.File()
                        input_audio_filename = gr.Textbox(visible=False)
                        upload_button = gr.UploadButton(file_types=["wav"])
                        upload_button.upload(
                            upload_audio,
                            upload_button,
                            outputs=[input_audio0, input_audio_filename],
                        )

                        # input_audio0 = gr.File(
                        #     label="Arquivo de entrada", file_types=[".wav"]
                        # )

                        # Add event handling for file upload
                        # input_audio0.change(upload_audio)

            with gr.Group():
                with gr.Column():
                    but0 = gr.Button(i18n("Converter"), variant="primary")
                    with gr.Row():
                        vc_output1 = gr.Textbox(label=i18n("Informações de saída:"))
                        vc_output2 = gr.Audio(
                            label=i18n(
                                "Exportar áudio(Clique nos três pontos para baixar)"
                            )
                        )

                    protect0 = gr.Number(value=0.33, visible=False)
                    file_index = gr.Textbox(value="", visible=False)

                    but0.click(
                        vc.vc_single,
                        [
                            spk_item,
                            input_audio_filename,
                            vc_transform0,
                            gr.Textbox(value="", visible=False),
                            gr.Textbox(value="rmvpe", visible=False),
                            file_index,
                            file_index,
                            # file_big_npy1,
                            gr.Number(value=0.75, visible=False),
                            gr.Number(value=3, visible=False),
                            gr.Number(value=0, visible=False),
                            gr.Number(value=0.25, visible=False),
                            protect0,
                        ],
                        [vc_output1, vc_output2],
                        api_name="infer_convert",
                    )

                sid0.change(
                    fn=vc.get_vc,
                    inputs=[sid0, protect0, protect0],
                    outputs=[protect0, protect0, file_index, file_index],
                    api_name="infer_change_voice",
                )

    if config.iscolab:
        app.queue(concurrency_count=511, max_size=1022).launch(share=True)
    else:
        app.queue(concurrency_count=511, max_size=1022).launch(
            server_name="0.0.0.0",
            inbrowser=not config.noautoopen,
            server_port=config.listen_port,
            quiet=True,
            share=False,
        )
