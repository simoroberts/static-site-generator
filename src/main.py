from textnode import TextNode, TextType

def main():
    node = TextNode("Anchor Text", TextType.LINK, "https://127.0.0.1")
    print(node)

if __name__ == "__main__":
    main()
