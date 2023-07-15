# pylint: disable=E0401
import js
import sys

sys.path.append("vdom")

import json
import operator
from collections import OrderedDict
from vdom import App, p, VDom, State, Actions


PRIMARY_COLOR = "#FEFEFE"
SECONDARY_COLOR = "#8894AD"

GMAIL = "harehare1110@gmail.com"
GITHUB = "harehare"
SKILLS = OrderedDict(
    {
        "Frontend": [
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-elm-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Elm",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-typescript-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "TypeScript",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-react-original colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "React",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-flutter-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Flutter",
                ],
            ),
        ],
        "Backend": [
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-go-original-wordmark colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Golang",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-python-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Python",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-ruby-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Ruby",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-scala-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Scala",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-rust-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Rust",
                ],
            ),
        ],
        "Other": [
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-amazonwebservices-original colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "AWS",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-googlecloud-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "GCP",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-firebase-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "Firebase",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    p(
                        "i",
                        {
                            "class": "devicon-mysql-plain colored",
                            "style": "margin-right: 4px;",
                        },
                        [],
                    ),
                    "MySQL",
                ],
            ),
            p(
                "div",
                {"style": "display: flex; align-items: center;"},
                [
                    "Solr, Elasticsearch",
                ],
            ),
        ],
    }
)
REPO_IMAGE: dict[str, str] = {
    "textusm": "https://raw.githubusercontent.com/harehare/textusm/master/frontend/src/public/images/logo.svg",
    "portable-kanban": "https://raw.githubusercontent.com/harehare/portable-kanban/master/assets/icon.png",
    "gitype": "https://raw.githubusercontent.com/harehare/gitype/master/demo.gif",
    "rbgrep": "https://raw.githubusercontent.com/harehare/rbgrep/master/assets/rbgrep.png",
    "blazeman": "https://raw.githubusercontent.com/harehare/blazeman/master/.github/icon.svg",
    "chick": "https://raw.githubusercontent.com/harehare/chick/master/img/logo.png",
}


# model
state: State = {
    "tab_index": 0,
    "github": None,
}


def tab_changed(s: State, v: int):
    s["tab_index"] = v
    if v != 2 or s["github"]:
        return

    req = js.XMLHttpRequest.new()
    req.open(
        "GET",
        "https://api.github.com/users/harehare/repos?sort=stars&order=desc&per_page=100",
        False,
    )
    req.send()
    s["github"] = [
        {
            "name": repo["name"],
            "description": repo["description"] if repo["description"] else "",
            "html_url": repo["html_url"],
            "language": repo["language"],
            "image_url": REPO_IMAGE.get(repo["name"]),
        }
        for repo in filter(
            lambda x: not x.get("forked") and not x.get("private"),
            sorted(
                json.loads(str(req.response)),
                key=operator.itemgetter("stargazers_count"),
                reverse=True,
            ),
        )
    ]


# update
actions = {"tab_changed": tab_changed}


# view
def view(s: State, a: Actions) -> VDom:
    return p(
        "div",
        {},
        [tabs_view(s, a), main_view(s, a), footer_view()],
    )


def home_view() -> VDom:
    return p(
        "div",
        {
            "style": "display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 8rem;"
        },
        [
            p(
                "div",
                {},
                [
                    # message
                    p(
                        "div",
                        {
                            "class": "p-heading--1",
                            "style": "padding-top: 24px; margin-bottom: 0;",
                        },
                        ["Hello, I'm Takahiro Sato"],
                    ),
                    # description
                    p(
                        "div",
                        {"class": "p-heading--6", "style": f"color: {SECONDARY_COLOR}"},
                        ["Web developer living in Saitama, Japan."],
                    ),
                    # icon
                    p(
                        "div",
                        {
                            "style": "display: flex; align-items: center; justify-content: center;"
                        },
                        [
                            p(
                                "img",
                                {
                                    "src": "https://avatars3.githubusercontent.com/u/533078?s=460&v=4",
                                    "style": "border-radius: 100%; width: 192px;",
                                },
                                [],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def skills_view() -> VDom:
    return p(
        "div",
        {
            "style": "display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 16px;"
        },
        [
            p(
                "div",
                {},
                [
                    p(
                        "dl",
                        {},
                        [p("dt", {}, [eng])]
                        + [p("dd", {}, [skill]) for skill in skills],
                    )
                    for eng, skills in SKILLS.items()
                ],
            )
        ],
    )


def works_view(s: State) -> VDom:
    return p(
        "div",
        {},
        [
            p(
                "ul",
                {
                    "class": "p-matrix",
                },
                [
                    p(
                        "li",
                        {"class": "p-matrix__item"},
                        [
                            p(
                                "img",
                                {
                                    "src": item["image_url"],
                                    "alt": f"{item['name']}-image",
                                    "class": "p-matrix__img",
                                },
                                [],
                            )
                            if item["image_url"]
                            else p("div", {}, []),
                            p(
                                "div",
                                {
                                    "class": "p-matrix__content",
                                    "style": "padding-left: 8px;",
                                },
                                [
                                    p(
                                        "h3",
                                        {},
                                        [
                                            p(
                                                "a",
                                                {
                                                    "class": "p-matrix__link",
                                                    "href": item["html_url"],
                                                    "target": "_blank",
                                                    "rel": "noopener noreferrer",
                                                },
                                                [item["name"]],
                                            ),
                                            p(
                                                "div",
                                                {"class": "p-matrix__desc"},
                                                [p("p", {}, [item["description"]])],
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ],
                    )
                    for item in s["github"]
                ]
                if isinstance(s["github"], list)
                else [p("div", {}, [])],
            )
            if s["github"]
            else p(
                "div",
                {
                    "style": "font-size: 2.8rem; font-weight: 700; padding: 56px 16px 16px 16px;"
                },
                ["Loading..."],
            ),
        ],
    )


def main_view(s: State, a: Actions) -> VDom:
    _view = home_view()

    if state["tab_index"] == 1:
        _view = skills_view()
    elif state["tab_index"] == 2:
        _view = works_view(s)

    return p("div", {"style": "height: calc(100vh - 90px)"}, [_view])


def tab_view(s: State, tab_index: int, icon: str, text: str, action) -> VDom:
    selected = s["tab_index"] == tab_index
    return p(
        "li",
        {
            "class": "p-tabs__item",
            "style": "cursor: pointer; display: flex; align-items: center; justify-content: center; padding-right: 16px;",
            "onClick": action,
        },
        [
            p(
                "span",
                {
                    "class": "material-icons p-tabs__link",
                    "style": (
                        f"background-color: #262626; color: {PRIMARY_COLOR}"
                        if selected
                        else "background-color: #262626; color: #3d4047"
                    )
                    + "; margin: 0; padding: 12px 8px 0 0;",
                    "aria-selected": "true" if selected else "false",
                },
                [icon],
            ),
            p(
                "span",
                {
                    "style": f"background-color: #262626; color: {PRIMARY_COLOR}"
                    if selected
                    else "background-color: #262626; color: #3d4047"
                },
                [text],
            ),
        ],
    )


def link_view(link: str, icon: VDom) -> VDom:
    return p(
        "li",
        {
            "class": "p-tabs__item",
            "style": "cursor: pointer; display: flex; align-items: center; justify-content: center;",
        },
        [
            p(
                "span",
                {
                    "class": "material-icons p-tabs__link",
                    "style": "background-color: #262626;",
                },
                [
                    p(
                        "a",
                        {
                            "href": link,
                            "style": f"color: {PRIMARY_COLOR};",
                            "target": "_blank",
                            "rel": "noopener noreferrer",
                        },
                        [icon],
                    )
                ],
            )
        ],
    )


def tabs_view(s: State, a: Actions) -> VDom:
    return p(
        "nav",
        {"class": "p-tabs", "style": "height: 51px;"},
        [
            p(
                "ul",
                {
                    "class": "p-tabs__list",
                    "style": "width: 100vw; justify-content: center;",
                },
                [
                    tab_view(s, 0, "home", "Home", lambda _e: a["tab_changed"](s, 0)),
                    tab_view(s, 1, "code", "Skills", lambda _e: a["tab_changed"](s, 1)),
                    tab_view(
                        s,
                        2,
                        "work",
                        "Personal Works",
                        lambda _e: a["tab_changed"](s, 2),
                    ),
                    link_view(
                        f"https://github.com/{GITHUB}",
                        p("i", {"class": "devicon-github-original"}, []),
                    ),
                    link_view(
                        f"mailto:{GMAIL}",
                        p("span", {"class": "material-icons"}, ["mail"]),
                    ),
                ],
            )
        ],
    )


def footer_view() -> VDom:
    return p(
        "div",
        {"class": "p-text--x-small", "style": "margin-left: 8px;"},
        [
            "This page was build with ",
            p(
                "a",
                {
                    "href": "https://github.com/harehare/python-wasm-vdom",
                    "rel": "noopener noreferrer",
                },
                ["python-wasm-vdom"],
            ),
        ],
    )


App(
    selector="#app",
    state=state,
    view=view,
    actions=actions,
)
