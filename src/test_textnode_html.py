import unittest

from textnode import text_node_to_html_node, TextType, LeafNode

class DummyTextNode:
    def __init__(self, text_type, text, url=None):
        self.text_type = text_type
        self.text = text
        self.url = url

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_text(self):
        node = DummyTextNode(TextType.TEXT, "hello")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "hello")

    def test_text_type_bold(self):
        node = DummyTextNode(TextType.BOLD, "bold text")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_text_type_italic(self):
        node = DummyTextNode(TextType.ITALIC, "italic text")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_text_type_code(self):
        node = DummyTextNode(TextType.CODE, "code snippet")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code snippet")

    def test_text_type_link(self):
        node = DummyTextNode(TextType.LINK, "Google", "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_text_type_image(self):
        node = DummyTextNode(TextType.IMAGE, "Alt text", "https://image.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://image.url", "alt": "Alt text"})

    def test_invalid_text_type(self):
        class FakeTextType:
            pass
        node = DummyTextNode(FakeTextType, "Invalid")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Invalid text type.")

if __name__ == '__main__':
    unittest.main()
