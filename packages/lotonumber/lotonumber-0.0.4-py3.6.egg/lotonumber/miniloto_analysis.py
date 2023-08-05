from analysis_basic import AnalysisBasic

class MinilotoAnalysis(AnalysisBasic):
    def __init__(self, miniloto_data):
        super().__init__(miniloto_data, 5)

    def __str__(self):
        return 'ミニロトの当選番号を予想します。'


if __name__ == '__main__':
    pass
