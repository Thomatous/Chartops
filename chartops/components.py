from ipywidgets import (
    Button, 
    Layout,
    VBox,
    ToggleButton,
    Layout,
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

def icon_toggle_button(value: bool, tooltip: str = '', icon: str = '', layout: Layout = Layout(), disabled: bool = False) -> ToggleButton:
    style = """
    <style>
    .toggle {
        background-color: #7E451D;
    }

    .toggle:hover {
        background-color: #A35829;
    }

    .toggle:active {
        background-color: #331E0B;
    }

    .toggle:focus {
        outline: 2px solid #FFA057;
    }

    .toggle:disabled {
        background-color: #17120E;
        color: #666;
        opacity: 0.5;
    }

    .toggle.mod-active {
        background-color: #F76B15;
    }
    </style>
    """
    display(HTML(style))
    toggle = ToggleButton(
        value=value,
        tooltip=tooltip,
        icon=icon,
        description='',
        layout=layout,
        disabled=disabled,
        style=dict(
            description_width='0',
            text_color='#FCFCFC'
        )
    )
    toggle.add_class('toggle')
    return toggle