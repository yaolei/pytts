def judge_language(sentence):
    chinese_count = sum(1 for char in sentence if '\u4e00' <= char <= '\u9fff')
    english_count = sum(1 for char in sentence if '\u0041' <= char <= '\u005a' or '\u0061' <= char <= '\u007a')
    if chinese_count > english_count:
        return "CN"
    elif english_count > chinese_count:
        return "EN"
    else:
        return "EN"