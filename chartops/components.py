from ipywidgets import (
    Button, 
    Layout,
    VBox,
    HTML
)
from IPython.display import display

def double_border_box(content) -> VBox:
    style="""
        <style>                
            .box {
                background-color: #202020;
            }
        </style>
    """
    display(HTML(style))
    inner = VBox(
        [content],
        layout=Layout(
            border=f'1px solid #FCFCFC',
        )
    )
    outer = VBox(
        [inner],
        layout=Layout(
            padding='0.3rem',
            border=f'1px solid #FCFCFC',
        )
    )
    outer.add_class('box')
    inner.add_class('box')
    return outer
