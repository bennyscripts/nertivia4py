class Embed:
    """
    Nertivia HTMLEmbed
    
    Attributes:
    - title (str): The title of the embed.
    - description (str): The description of the embed.
    - colour (str): The colour of the embed.
    - color (str): The color of the embed.
    """

    def __init__(self, title, description="", colour="#ffffff", color="#ffffff"):
        if colour == "":
            colour = color
        self.images = 0
        self.videos = 0
        self.footers = 0
        self.json = {
            "tag": "div",
            "styles": {
                "backgroundColor": f"rgb(0 0 0 / 15%)",
                "borderRadius": "4px",
                "display": "flex"
            },
            "content": [
                {
                    "tag": "div",
                    "styles": {
                        "backgroundColor": colour,
                        "flex": "left",
                        "width": "4px",
                        "borderRadius": "4px",
                        "flexShrink": 0
                    }
                },
                {
                    "tag": "div",
                    "styles": {
                        "backgroundColor": "inherit",
                        "flex": "right",
                        "width": "auto",
                        "padding": "10px",
                        "borderRadius": "4px"
                    },
                    "content": [
                        {
                            "tag": "strong", 
                            "styles": {
                                "fontSize": "16px"
                            },
                            "content": title
                        },
                        {
                            "tag": "div", 
                            "styles": {
                                "fontSize": "14px"
                            },
                            "content": description
                        }
                    ]
                }
            ]
        }

    def set_image(self, url):
        """
        Set the image of the embed.

        Args:
        - url (str): The url of the image.
        """

        self.images += 1

        if self.images <= 1:
            self.json["content"][1]["content"][1]["content"] += "\n** **"
            
            self.json["content"][1]["content"].append({
                "tag": "img",
                "styles": {
                    "width": "100%",
                    "overflow": "hidden",
                    "borderRadius": "4px"
                },
                "attributes": {
                    "src": url
                }
            })

    def set_footer(self, text, icon_url=""):
        """
        Set the footer of the embed.
            
        Args:
        - text (str): The text of the footer.
        - icon_url (str): The url of the icon.
        """

        self.footers += 1
        if self.footers <= 1:
            if icon_url != "":
                self.json["content"][1]["content"].append({
                    "tag": "div",
                    "styles": {
                        "display": "flex",
                        "flexDirection": "row"
                    },
                    "content": [
                        {
                            "tag": "img",
                            "styles": {
                                "width": "20px",
                                "height": "20px",
                                "borderRadius": "4px",
                                "marginRight": "5px",
                                "marginTop": "5px"
                            },
                            "attributes": {
                                "src": icon_url
                            }
                        },
                        {
                            "tag": "span",
                            "styles": {
                                "fontSize": "12px",
                                "paddingTop": "10px"
                            },
                            "content": text
                        }
                    ]
                })
            else:
                self.json["content"][1]["content"].append({
                    "tag": "div",
                    "styles": {
                        "display": "flex",
                        "flexDirection": "row"
                    },
                    "content": [
                        {
                            "tag": "span",
                            "styles": {
                                "fontSize": "12px",
                                "paddingTop": "10px"
                            },
                            "content": text
                        }
                    ]
                })