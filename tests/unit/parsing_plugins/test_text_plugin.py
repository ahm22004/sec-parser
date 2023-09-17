import pytest
from sec_parser import TextElement
from tests.unit.parsing_plugins._utils import (
    get_elements_from_html,
    DummyElement,
    SpecialElement,
    assert_elements,
)
from sec_parser.parsing_plugins import TextPlugin
from sec_parser.semantic_elements.semantic_elements import TextElement


@pytest.mark.parametrize(
    "html_str, expected_elements",
    [
        (
            """
               <special>0</special>
               <p>1</p>
               <div>
                   <i>2</i>
                   <p></p>
               </div>
               <span>3</span>
            """,
            [
                {"type": SpecialElement, "tag": "special"},
                {"type": TextElement, "tag": "p"},
                {
                    "type": TextElement,
                    "tag": "div",
                    "children": [
                        {"type": TextElement, "tag": "i"},
                        {"type": DummyElement, "tag": "p"},
                    ],
                },
                {"type": TextElement, "tag": "span"},
            ],
        )
    ],
)
def test_text_plugin(html_str, expected_elements):
    # Arrange
    elements = get_elements_from_html(html_str)
    plugin = TextPlugin(dont_convert_from={SpecialElement})

    # Act
    processed_elements = plugin.transform(elements)

    # Assert
    assert_elements(processed_elements, expected_elements)