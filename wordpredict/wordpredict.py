from wordpredict.utils import (
    build_trie,
    get_autocomplete_candidates,
    update_valid_nodes,
)


class WordPredict:
    def __init__(self, corpus_words, corpus_freq, alpha=0.62):
        self.root = build_trie(corpus_words, corpus_freq)
        self.alpha = alpha
        self.valid_nodes_for_undo = []  # 2次元配列

    def update(self, new_char_list, max_candidates=6):
        if new_char_list:
            self.valid_nodes_for_undo.append(
                update_valid_nodes(
                    (
                        self.valid_nodes_for_undo[-1]
                        if len(self.valid_nodes_for_undo) >= 1
                        else []
                    ),
                    new_char_list,
                    self.root,
                )
            )

        return get_autocomplete_candidates(
            self.valid_nodes_for_undo[-1], max_candidates, self.alpha
        )

    def next_word(self):
        self.valid_nodes_for_undo.append([])

    def reset(self):
        self.valid_nodes_for_undo = []

    def get_current_candidates(self, max_candidates=6):
        return get_autocomplete_candidates(
            self.valid_nodes_for_undo[-1], max_candidates, self.alpha
        )

    def undo(self, max_candidates=6):
        if len(self.valid_nodes_for_undo) == 0:
            return []

        elif len(self.valid_nodes_for_undo) == 1:
            self.valid_nodes_for_undo = []
            return []

        else:
            self.valid_nodes_for_undo.pop()
            prev_valid_nodes = self.valid_nodes_for_undo[-1]

            return get_autocomplete_candidates(
                prev_valid_nodes, max_candidates, self.alpha
            )
