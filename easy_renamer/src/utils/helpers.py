def count_fullwidth_chars(text):
    """全角文字を1、半角文字を0.5としてカウント"""
    count = 0
    for char in text:
        if ord(char) > 127:  # 全角文字
            count += 1
        else:
            count += 0.5
    return count
