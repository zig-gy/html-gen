class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        html_props = ""
        for k,v in self.props.items():
            html_props += f' {k}="{v}"'
        return html_props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


