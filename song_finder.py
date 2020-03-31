import jellyfish


def find_song(df, input_phrase):
    test_string = input_phrase
    test_met = jellyfish.metaphone(test_string).split(' ')

    min_dist = 10000
    min_dist_idx = None
    phrase = ''
    idx = 0

    def find_min_dist(lyrics):
        nonlocal min_dist
        nonlocal min_dist_idx
        nonlocal phrase
        nonlocal idx

        # Find best match phrase in lyrics
        min_dist_this_lyrics = 10000
        min_dist_start_idx = 0
        min_dist_end_idx = 0
        lyrics_met = jellyfish.metaphone(lyrics).split(' ')
        for i in range(0, len(lyrics_met) - len(test_met)):
            this_lyrics_met = lyrics_met[i:i + len(test_met)]
            if this_lyrics_met[0] == test_met[0]:
                dist = jellyfish.levenshtein_distance(''.join(test_met), ''.join(this_lyrics_met))
                if dist < min_dist_this_lyrics:
                    min_dist_this_lyrics = dist
                    min_dist_start_idx = i
                    min_dist_end_idx = i + len(test_met)

        # Check against global min
        if min_dist_this_lyrics < min_dist:
            min_dist = min_dist_this_lyrics
            min_dist_idx = idx
            phrase = ' '.join(lyrics.split(' ')[min_dist_start_idx:min_dist_end_idx])

        # Increment global idx
        idx += 1

    # Find song and actual phrase
    print('Starting search, given_phrase={}'.format(input_phrase))
    df['LYRICS'].apply(find_min_dist)
    name = df.iloc[min_dist_idx]['SONG_NAME']
    print('Results: name={}, phrase={}'.format(name, phrase))

    # Return
    return name, phrase
