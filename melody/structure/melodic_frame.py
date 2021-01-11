

class MelodicFrame(object):

    def __init__(self, lite_score):
        self.__score = lite_score

        self.__motifs = list()

    @property
    def score(self):
        return self.__score

    @property
    def motifs(self):
        return self.__motifs

    def add_motif(self, motif):
        self.__motifs.append(motif)
        self.__motifs.sort(key=lambda x: x.position)

    def remove_motif(self, motif):
        if motif in self.motifs:
            self.__motifs.remove(motif)
            self.__motifs.sort(key=lambda x: x.position)

    def __str__(self):
        return str(self.score)