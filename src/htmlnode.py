from __future__ import annotations

class HTMLNode:
    def __init__(self, tag:str|None=None, value:str|None=None, children:list[HTMLNode]|None=None, props:dict[str, str]|None=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        prop_strings = []
        for prop in self.props:
            prop_strings.append(f" {prop}=\"{self.props[prop]}\"")
        return "".join(prop_strings)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
