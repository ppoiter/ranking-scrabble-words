def scrabble_word_leaderboard(max_length = 7):
    """
    Returns a leaderboard of the top scoring words of a user-defined maximum length from the scrabble dictionary.
    :param max_length: maximum length of words to be returned in the leaderboard
    :return:
    """
    import pandas as pd

    # build dictionary for letter values
    letterval_df = pd.read_csv('letterValues.txt', sep = ':', names = ['letter', 'value'])
    letterval_df['letter'] = letterval_df['letter'].str.lower()
    VALUES_DICT = dict(zip(letterval_df.letter, letterval_df.value))
    
    # generate words variable from sowpod.txt
    with open('sowpods.txt', "r") as sowpods:
        words = sowpods.read().split("\n")
        
    allowed_words = []
    for word in words:
        if len(word) <= max_length:
            allowed_words.append(word)

    
    # generate list of scores for each word
    score_lst = []
    for word in allowed_words:
        score = sum([VALUES_DICT[c] for c in word])
        score_lst.append(score)

    # generate and return rankings

    ranking_df = pd.DataFrame(
    {'word': allowed_words,
     'score': score_lst
    })

    ranking_df = ranking_df.sort_values(['score','word'], ascending=[False,True])
    ranking_df = ranking_df[0:100]
    ranking_df.reset_index(inplace = True, drop = True)
    ranking_df.insert(0,'rank',list(range(1,101)))

    return ranking_df 