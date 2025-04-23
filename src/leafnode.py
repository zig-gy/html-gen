from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,value , tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("wrong value")
        tag = ""
        closing_tag = ""
        props = ""
        if self.props != None:
            props = self.props_to_html()
        if self.tag != None:
            tag = f"<{self.tag}{props}>"
            closing_tag = f"</{self.tag}>"
        return tag + self.value + closing_tag
