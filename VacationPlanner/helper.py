SINGLE_TAB_LEVEL = 4

def print_in_box(text, title="", cols=120, tab_level=0):
    import textwrap

    text = str(text)

    # Make a box using extended ASCII characters
    if cols < 4 + tab_level * SINGLE_TAB_LEVEL:
        cols = 4 + tab_level * SINGLE_TAB_LEVEL

    tabs = " " * tab_level * SINGLE_TAB_LEVEL

    top = (
        tabs
        + "\u2554"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u2557"
    )
    if tab_level == 0:
        print()  # Print a newline before any box at level 0

    if title:
        # replace the middle of the top with the title
        title = "[ " + title + " ]"
        top = top[: (cols - len(title)) // 2] + title + top[(cols + len(title)) // 2 :]
    print(top)

    for line in text.split("\n"):
        for wrapped_line in textwrap.wrap(
            line, cols - 4 - tab_level * SINGLE_TAB_LEVEL
        ):
            print(
                f"{tabs}\u2551 {wrapped_line:<{cols - 4 - tab_level * SINGLE_TAB_LEVEL}} \u2551"
            )

    print(
        f"{tabs}\u255a"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u255d"
    )

def do_chat_completion(messages: list[dict[str, str]], model=None, client=None, **kwargs):

    if "response_format" not in kwargs:
        response = client.chat.completions.create(  # type: ignore
            model=model,
            messages=messages,  # type: ignore
            **kwargs,  # type: ignore
        )
    else:
        response = client.beta.chat.completions.parse(  # type: ignore
            model=model,
            messages=messages,  # type: ignore
            **kwargs,  # type: ignore
        )

    if hasattr(response, "error"):
        raise RuntimeError(
            f"OpenAI API returned an error: {str(response.error)}"
        )

    return response.choices[0].message.content