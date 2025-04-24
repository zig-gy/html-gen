from htmlnode import  HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None:
            raise ValueError("no children")
        
        props = ""
        if self.props != None:
            props = self.props_to_html()
        tag = f"<{self.tag}{props}>"
        closing_tag = f"</{self.tag}>"
            
        output = ""
        for child in self.children:
            output += child.to_html()
            
        return tag + output + closing_tag