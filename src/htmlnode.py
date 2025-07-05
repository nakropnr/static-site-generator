class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        # Case 1: If there's no tag, this is a text node
        if self.tag is None:
            return self.value
        
        # Case 2: Build the opening tag
        opening_tag = f"<{self.tag}"
        
        # Add attributes if they exist
        if self.props:
            for key, value in self.props.items():
                opening_tag += f' {key}="{value}"'
        
        opening_tag += ">"
        
        # Case 3: Handle self-closing tags (like <img>, <br>)
        if self.tag in ["img", "br", "hr", "input", "meta", "link"]:
            return opening_tag[:-1] + " />"  # Replace > with />
        
        # Case 4: Build the content
        content = ""
        if self.children:
            # If there are children, convert each child to HTML
            for child in self.children:
                content += child.to_html()
        elif self.value:
            # If there's a value but no children, use the value
            content = self.value
        
        # Case 5: Build the closing tag and return
        closing_tag = f"</{self.tag}>"
        return opening_tag + content + closing_tag
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return (f"tag:{self.tag} value:{self.value} children:{self.children} props:{self.props}")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf node must have value.")
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None,):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent node must have tag.")
        elif self.children == None:
            raise ValueError("All parent node must have children.")
        else:
            child_html = ''
            for child in self.children:
                child_html += child.to_html()
            return f"<{self.tag}>{child_html}</{self.tag}>"