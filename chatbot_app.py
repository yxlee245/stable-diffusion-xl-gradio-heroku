import os
from typing import Iterable, List, Tuple

import gradio as gr
from PIL import Image

from src.inference import generate_image_from_text


def return_output_image(
    huggingface_token: str, message: str, chat_history: List[Iterable[str]]
) -> Image.Image:
    """Event function to accept prompts from user and return generated image

    Args:
        huggingface_token (str): Huggingface Access Token needed to access SDXL models on Huggingface Hub
        message (str): New message from user
        chat_history (List[Iterable[str]]): Past messages from user and chatbot, in the form
            [[user_msg_1, bot_msg_1], [user_msg_2, bot_msg_2], ...]

    Raises:
        gr.Error: Huggingface Access Token not provided by user

    Returns:
        Image.Image: Generated image from the SDXL models
    """
    if huggingface_token == "":
        raise gr.Error("Please enter a Huggingface token")
    messages_for_prompt = [past_user_msg for past_user_msg, _ in chat_history] + [
        message
    ]
    full_prompt = "\n\n".join(messages_for_prompt)
    pil_image = generate_image_from_text(huggingface_token, full_prompt)
    return pil_image


def return_chatbot_message(
    message: str, chat_history: List[Iterable[str]]
) -> Tuple[str, List[Iterable[str]]]:
    """Event function to return messages in chatbot windowm

    Args:
        message (str): New message from user
        chat_history (List[Iterable[str]]): Past messages from user and chatbot, in the form
            [[user_msg_1, bot_msg_1], [user_msg_2, bot_msg_2], ...]

    Returns:
        Tuple[str, List[Iterable[str]]]: Tuple containing
            1. Empty string to be rendered in chat textbox
            2. Updated chat history to be rendered in conversation window
    """
    bot_message = "Generating image based on past message(s)..."
    chat_history.append((message, bot_message))
    return "", chat_history


def undo_chatbot_history(chat_history: List[Iterable[str]]) -> List[Iterable[str]]:
    """Event function to undo the last pair of messages in the conversation window

    Args:
        chat_history (List[Iterable[str]]): Past messages from user and chatbot, in the form
            [[user_msg_1, bot_msg_1], [user_msg_2, bot_msg_2], ...]

    Returns:
        List[Iterable[str]]: Updated chat history with the last pair of messages removed
    """
    if len(chat_history) > 0:
        chat_history.pop()
    return chat_history


with gr.Blocks() as app:
    gr.Markdown("# Text-to-image chatbot")
    gr.Markdown(
        "Generate image using Stable Diffusion XL 1.0 "
        "[base](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) and "
        "[refiner](https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0) models"
    )

    with gr.Row():
        with gr.Column():
            huggingface_token = gr.Textbox(
                type="password", placeholder="Enter Huggingface token", show_label=False
            )
            chatbot = gr.Chatbot()
            input_msg = gr.Textbox(
                placeholder="Enter message to generate some image", show_label=False
            )
            with gr.Row():
                undo_button = gr.Button(value="↩️ Undo")
                retry_button = gr.Button(value="🔄 Retry")
                clear_button = gr.ClearButton([input_msg, chatbot], value="🗑️ Clear")
        output_image = gr.Image(format="png", type="pil", interactive=False)

    input_msg.submit(
        fn=return_chatbot_message,
        inputs=[input_msg, chatbot],
        outputs=[input_msg, chatbot],
    )
    input_msg.submit(
        fn=return_output_image,
        inputs=[huggingface_token, input_msg, chatbot],
        outputs=[output_image],
    )
    undo_button.click(fn=undo_chatbot_history, inputs=[chatbot], outputs=[chatbot])
    retry_button.click(
        fn=return_output_image,
        inputs=[huggingface_token, input_msg, chatbot],
        outputs=[output_image],
    )

app.launch(server_port=int(os.getenv("PORT", "7860")))
