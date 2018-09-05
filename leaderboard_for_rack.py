def build_leaderboard_for_rack(rack_string, min_length = 3, max_length = 7):
    """
    Build a leaderboard of the top scoring words that can be built using only the letters contained in 
    a given rack. Words are ordered in the leaderboard by their score (with the highest score first) and then 
    alphabetically for words which have the same score.
    :param rack_string: a random string of letters from which to build words that are valid against the contents 
    of the scrabble dictionary file (sowpods.txt)
    :param min_length: minimum length of words to be returned in the leaderboard
    :param max_length: maximum length of words to be returned in the leaderboard
    :return:
    """
    from collections import Counter
    
    
    # build dictionary for letter values
    letterval_df = pd.read_csv('letterValues.txt', sep = ':', names = ['letter', 'value'])
    letterval_df['letter'] = letterval_df['letter'].str.lower()
    VALUES_DICT = dict(zip(letterval_df.letter, letterval_df.value))

    # generate words variable from sowpod.txt
    with open('sowpods.txt', "r") as sowpods:
        words = sowpods.read().split("\n")
        
    allowed_words = []
    for word in words:
        if min_length <= len(word) <= max_length:
            allowed_words.append(word)

    # define function to check if word can be spelled from rack
    def can_spell(word, rack_string):
        if not Counter(word) - Counter(rack_string):
            return word
    
    # generate list of spellable words from rack string
    
    spellable_words = []
    for word in allowed_words:
        if can_spell(word, rack_string):
            spellable_words.append(word)
        
    # generate score list for spellable words
    
    score_lst = []
    for word in spellable_words:
        score = sum([VALUES_DICT[c] for c in word])
        score_lst.append(score)
    
    # generate ranking dataframe
    ranking_df = pd.DataFrame(
        {'word': spellable_words,
         'score': score_lst
        })

    ranking_df = ranking_df.sort_values(['score','word'], ascending=[False,True])
    ranking_df = ranking_df[0:100]
    ranking_df.reset_index(inplace = True, drop = True)
    ranking_df.insert(0,'rank',list(range(1,len(spellable_words)+1)))

    return(ranking_df)
            
        